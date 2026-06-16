#!/usr/bin/env python3
"""patch-npm.py — Apply Nginx Proxy Manager patches for HAOS addon build.

Replaces the 48 sed/find/echo commands in the Dockerfile RUN block with
a single Python script. Each patch self-validates immediately and a final
validation suite runs after all patches.

Usage:
    python3 proxy-manager/scripts/patch-npm.py v2.15.1      # standalone
    python3 /tmp/patch-npm.py --dir /app                    # inside Docker

Exit code: 0 = all OK, 1 = any error.
"""

import os
import re
import sys
import shutil
import tempfile
import urllib.request
import tarfile

NPM_REPO = "https://github.com/NginxProxyManager/nginx-proxy-manager"
NPM_ARCHIVE_URL = f"{NPM_REPO}/archive/{{version}}.tar.gz"


# Helpers
def info(msg: str) -> None:
    print(f"  \u2022 {msg}")

def ok(msg: str) -> None:
    print(f"  \u2713 {msg}")

def fail(msg: str) -> None:
    print(f"  \u2717 {msg}", file=sys.stderr)

def die(msg: str) -> None:
    fail(msg)
    sys.exit(1)

def _read(path: str) -> str:
    with open(path) as f:
        return f.read()

def _write(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


# Patcher
class Patcher:
    """Downloads upstream NPM source and applies all patches."""

    def __init__(self, version: str) -> None:
        self.version = version
        self.workdir = tempfile.mkdtemp(prefix="patch-npm-")
        self.srcdir = os.path.join(self.workdir, "src")

    def cleanup(self) -> None:
        if hasattr(self, "workdir") and os.path.isdir(self.workdir):
            shutil.rmtree(self.workdir, ignore_errors=True)

    def _path(self, *parts: str) -> str:
        return os.path.join(self.srcdir, *parts)

    # Download & Extract
    def download_and_extract(self) -> None:
        url = NPM_ARCHIVE_URL.format(version=self.version)
        info(f"Downloading {url} ...")
        archive = os.path.join(self.workdir, "npm.tar.gz")
        try:
            urllib.request.urlretrieve(url, archive)
        except Exception as e:
            die(f"Failed to download {url}: {e}")
        info("Extracting ...")
        os.makedirs(self.srcdir, exist_ok=True)
        with tarfile.open(archive, "r:gz") as tf:
            members = tf.getmembers()
            for m in members:
                parts = m.name.split("/", 1)
                m.name = parts[1] if len(parts) > 1 else ""
            tf.extractall(self.srcdir)
        ok(f"Extracted to {self.srcdir}")

    # Patch 1: /data/ → /config/
    def patch_01_data_to_config(self) -> None:
        info("Patch 1: /data/ → /config/")
        js_files = [
            ("backend/internal/access-list.js", "/data/access/", "/config/access/"),
            ("backend/internal/certificate.js", "/data/custom_ssl/", "/config/custom_ssl/"),
            ("backend/internal/certificate.js", "/data/letsencrypt-acme-challenge/", "/config/letsencrypt-acme-challenge/"),
            ("backend/internal/nginx.js", "/data/nginx/", "/config/nginx/"),
            ("backend/internal/setting.js", "/data/nginx/default_www/", "/config/nginx/default_www/"),
            ("backend/lib/config.js", "/data/keys.json", "/config/keys.json"),
            ("backend/lib/config.js", "/data/database.sqlite", "/config/database.sqlite"),
        ]
        for relpath, old, new in js_files:
            fpath = self._path(relpath)
            if os.path.exists(fpath):
                content = _read(fpath)
                if old in content:
                    _write(fpath, content.replace(old, new))
        tdir = self._path("backend", "templates")
        if os.path.isdir(tdir):
            for fn in os.listdir(tdir):
                if fn.endswith(".conf"):
                    fpath = os.path.join(tdir, fn)
                    c = _read(fpath)
                    if "/data/" in c:
                        _write(fpath, c.replace("/data/", "/config/"))
        rdir = self._path("docker", "rootfs", "etc", "nginx")
        if os.path.isdir(rdir):
            for root, _dirs, files in os.walk(rdir):
                for fn in files:
                    if not fn.endswith(".conf"):
                        continue
                    fpath = os.path.join(root, fn)
                    c = _read(fpath)
                    if "/data/" in c:
                        _write(fpath, c.replace("/data/", "/config/"))
        nginx_conf = self._path("docker", "rootfs", "etc", "nginx", "nginx.conf")
        if os.path.exists(nginx_conf):
            c = _read(nginx_conf)
            c = c.replace("/var/lib/nginx/cache/", "/tmp/nginx/cache/")
            if not c.startswith("load_module"):
                c = "load_module /usr/lib/nginx/modules/ngx_stream_module.so;\n" + c
            _write(nginx_conf, c)
        dns = self._path("backend", "certbot", "dns-plugins.json")
        if os.path.exists(dns):
            c = _read(dns)
            _write(dns, c.replace("/data/acme-registration.json", "/config/acme-registration.json"))
        _js_pat = re.compile(r"/data/(access|custom_ssl|letsencrypt|nginx|keys\.json|database\.sqlite|acme-registration)")
        for relpath, _old, _new in js_files:
            fpath = self._path(relpath)
            if os.path.exists(fpath) and _js_pat.search(_read(fpath)):
                die(f"Patch 1: {relpath} still contains /data/")
        for fn in os.listdir(self._path("backend", "templates")):
            if fn.endswith(".conf") and "/data/" in _read(self._path("backend", "templates", fn)):
                die(f"Patch 1: templates/{fn} still contains /data/")
        if os.path.isdir(rdir):
            for root, _dirs, files in os.walk(rdir):
                for fn in files:
                    if fn.endswith(".conf") and "/data/" in _read(os.path.join(root, fn)):
                        die(f"Patch 1: rootfs/{fn} still contains /data/")
        ok("Patch 1 applied")

    # Patch 2: access_log/error_log → /proc/1/fd/1
    def patch_02_logs_to_stdout(self) -> None:
        info("Patch 2: logs → stdout")
        changed = 0
        for root, dirs, files in os.walk(self.srcdir):
            dirs[:] = [d for d in dirs if d != "node_modules"]
            for fn in files:
                if not fn.endswith(".conf"):
                    continue
                fpath = os.path.join(root, fn)
                c = _read(fpath)
                old = c
                # Preserve optional format name (required by nginx stream context)
                c = re.sub(
                    r'access_log\s+/config/logs/[^;]+?(\s+\w+)?;',
                    lambda m: 'access_log /proc/1/fd/1' + (m.group(1) or '') + ';',
                    c)
                c = re.sub(
                    r'error_log\s+/config/logs/[^;]+?(\s+\w+)?;',
                    lambda m: 'error_log /proc/1/fd/1' + (m.group(1) or '') + ';',
                    c)
                if c != old:
                    _write(fpath, c)
                    changed += 1
        tdir = self._path("backend", "templates")
        if os.path.isdir(tdir):
            for fn in sorted(os.listdir(tdir)):
                if not fn.endswith(".conf"):
                    continue
                c = _read(os.path.join(tdir, fn))
                if "access_log" in c and "access_log /proc/1/fd/1" not in c:
                    die(f"Patch 2: templates/{fn}: access_log not redirected")
        ok(f"Patch 2 applied: {changed} files changed")

    # Patch 3: certbot pip without venv
    def patch_03_certbot_pip(self) -> None:
        info("Patch 3: certbot pip without venv")
        fp = self._path("backend", "lib", "certbot.js")
        if not os.path.exists(fp):
            return ok("Patch 3: certbot.js not found, skipping")
        c = _read(fp)
        old = c
        c = c.replace('. /opt/certbot/bin/activate && pip install ', 'pip install ').replace(' && deactivate', '')
        c = c.replace('. /opt/certbot/bin/activate && pip3 install ', 'pip3 install ').replace(' && deactivate', '')
        if c == old:
            return ok("Patch 3: no venv pattern found, skipping")
        _write(fp, c)
        ok("Patch 3 applied")

    # Patch 4: cloudflare without version pin
    def patch_04_cloudflare(self) -> None:
        info("Patch 4: cloudflare without version pin")
        fp = self._path("backend", "certbot", "dns-plugins.json")
        if not os.path.exists(fp):
            return ok("Patch 4: dns-plugins.json not found, skipping")
        c = _read(fp)
        old = c
        c = re.sub(r'"cloudflare==4\.0\.\*"', '"cloudflare"', c)
        c = re.sub(r'"cloudflare==\d+\.\d+\.\*"', '"cloudflare"', c)
        if c == old:
            return ok("Patch 4: no version pin found, skipping")
        _write(fp, c)
        ok("Patch 4 applied")
        if re.search(r'"cloudflare==\d+\.\d+\.\*"', _read(fp)):
            die("Patch 4: cloudflare version pin still present")

    # Patch 5: locale symlink for frontend build
    def patch_05_locale_symlink(self) -> None:
        info("Patch 5: locale lang symlink")
        src = self._path("frontend", "src", "locale", "src")
        dst = self._path("frontend", "src", "locale", "lang")
        if not os.path.exists(src):
            return ok("Patch 5: locale src not found, skipping")
        if os.path.exists(dst) and not os.path.islink(dst):
            os.remove(dst)
        if not os.path.exists(dst):
            os.symlink("src", dst)
        ok("Patch 5 applied")

    # Patch 6: vite build without tsc
    def patch_06_vite_no_tsc(self) -> None:
        info("Patch 6: vite build without tsc")
        pkg = self._path("frontend", "package.json")
        vcfg = self._path("frontend", "vite.config.ts")
        if os.path.exists(pkg):
            c = _read(pkg)
            n = c.replace('"build": "tsc && vite build"', '"build": "vite build"')
            if n != c:
                _write(pkg, n)
        if os.path.exists(vcfg):
            c = _read(vcfg)
            n = c.replace("typescript: true", "typescript: false")
            if n != c:
                _write(vcfg, n)
        ok("Patch 6 applied")

    # Patch 7: version string
    def patch_07_version(self) -> None:
        info("Patch 7: version string")
        ver = self.version.lstrip("v")
        for p in [self._path("frontend", "package.json"), self._path("backend", "package.json")]:
            if not os.path.exists(p):
                continue
            c = _read(p)
            n = re.sub(r'"version":\s*"2\.0\.0"', f'"version": "{ver}"', c)
            if n != c:
                _write(p, n)
        ok("Patch 7 applied")

    # Patch 8: user root, production paths
    def patch_08_user_root(self) -> None:
        info("Patch 8: user root, root path fixes")
        nginx_conf = self._path("docker", "rootfs", "etc", "nginx", "nginx.conf")
        if os.path.exists(nginx_conf):
            c = _read(nginx_conf)
            c = re.sub(r'^user\s+(?:nginx|npm)\s+(?:nginx|npm)', 'user root root', c, flags=re.MULTILINE)
            c = re.sub(r'^user\s+(?:nginx|npm)', 'user root', c, flags=re.MULTILINE)
            _write(nginx_conf, c)
        prod_conf = self._path("docker", "rootfs", "etc", "nginx", "conf.d", "production.conf")
        if os.path.exists(prod_conf):
            c = _read(prod_conf)
            c = c.replace("root /app/frontend", "root /opt/nginx-proxy-manager/frontend")
            c = c.replace("/app/frontend", "/opt/nginx-proxy-manager/frontend")
            _write(prod_conf, c)
        ok("Patch 8 applied")


    # Patch 9: post-build fixes (migration + logrotate)
    def patch_09_post_build(self) -> None:
        info("Patch 9: post-build fixes")
        # Migration: table.string('id') -> table.string('id', 32)
        mig = self._path("backend", "migrations", "20190227065017_settings.js")
        if os.path.exists(mig):
            c = _read(mig)
            n = c.replace(
                "table.string('id').notNull().primary();",
                "table.string('id', 32).notNull().primary();"
            )
            if n != c:
                _write(mig, n)
        # Logrotate: su npm npm -> su root root
        lr = self._path("docker", "rootfs", "etc", "logrotate.d", "nginx-proxy-manager")
        if os.path.exists(lr):
            c = _read(lr)
            n = c.replace("su npm npm", "su root root")
            if n != c:
                _write(lr, n)
        ok("Patch 9 applied")

    # Final validation
    def _find_data_refs(self) -> list:
        found = []
        js_pat = re.compile(r"/data/(access|custom_ssl|letsencrypt|nginx|keys\.json|database\.sqlite|acme-registration)")
        bdir = self._path("backend")
        if os.path.isdir(bdir):
            for root, dirs, files in os.walk(bdir):
                dirs[:] = [d for d in dirs if d != "node_modules"]
                for fn in files:
                    if not (fn.endswith(".js") or fn.endswith(".json")):
                        continue
                    try:
                        with open(os.path.join(root, fn)) as f:
                            m = js_pat.search(f.read())
                        if m:
                            found.append((os.path.relpath(os.path.join(root, fn), self.srcdir), m.group()[:80]))
                    except Exception:
                        continue
        for sub in ["backend/templates", "docker/rootfs/etc/nginx"]:
            sd = self._path(sub)
            if not os.path.isdir(sd):
                continue
            for root, _dirs, files in os.walk(sd):
                for fn in files:
                    if not fn.endswith(".conf"):
                        continue
                    try:
                        with open(os.path.join(root, fn)) as f:
                            c = f.read()
                        if "/data/" in c:
                            rel = os.path.relpath(os.path.join(root, fn), self.srcdir)
                            for line in c.split("\n"):
                                if "/data/" in line and not line.strip().startswith("#"):
                                    found.append((rel, line.strip()[:80]))
                                    break
                    except Exception:
                        continue
        return found

    def final_validation(self) -> None:
        info("Final validation")
        errors = []
        data_refs = self._find_data_refs()
        if data_refs:
            for r, l in data_refs[:5]:
                errors.append(f"  {r}: {l}")
            errors.insert(0, f"  {len(data_refs)} files still reference /data/ paths")
        tdir = self._path("backend", "templates")
        if os.path.isdir(tdir):
            for fn in sorted(os.listdir(tdir)):
                if not fn.endswith(".conf"):
                    continue
                c = _read(os.path.join(tdir, fn))
                if "access_log" in c and "access_log /proc/1/fd/1" not in c:
                    errors.append(f"  templates/{fn}: access_log not redirected")
                if re.search(r"\{\{.*\}\}\.(log|access|error)", c):
                    errors.append(f"  templates/{fn}: {{ }} still in log path")
        fp = self._path("backend", "certbot", "dns-plugins.json")
        if os.path.exists(fp) and re.search(r'"cloudflare==\d+\.\d+\.\*"', _read(fp)):
            errors.append("  cloudflare version pin still present")
        for pk in ["frontend", "backend"]:
            p = self._path(pk, "package.json")
            if os.path.exists(p) and '"version": "2.0.0"' in _read(p):
                errors.append(f"  {pk}/package.json: version still 2.0.0")
        nc = self._path("docker", "rootfs", "etc", "nginx", "nginx.conf")
        if os.path.exists(nc) and re.search(r"^user\s+nginx", _read(nc), re.MULTILINE):
            errors.append("  nginx.conf: user still nginx (should be root)")
        if errors:
            for e in errors:
                fail(e)
            die(f"  Final validation: {len(errors)} error(s)")
        ok("All checks passed")

    # Run
    def run(self) -> int:
        print(f"\n{'=' * 60}")
        print(f"  NPM Patcher v{self.version}")
        print(f"  Source: {self.srcdir}")
        print(f"{'=' * 60}\n")
        if not os.path.isdir(os.path.join(self.srcdir, "backend")):
            self.download_and_extract()
        else:
            info("Source directory already has content, skipping download")
        patches = [
            ("Patch 1/9: /data/ → /config/", self.patch_01_data_to_config),
            ("Patch 2/9: logs → stdout", self.patch_02_logs_to_stdout),
            ("Patch 3/9: certbot pip", self.patch_03_certbot_pip),
            ("Patch 4/9: cloudflare", self.patch_04_cloudflare),
            ("Patch 5/9: locale symlink", self.patch_05_locale_symlink),
            ("Patch 6/9: vite no tsc", self.patch_06_vite_no_tsc),
            ("Patch 7/9: version", self.patch_07_version),
            ("Patch 8/9: user root", self.patch_08_user_root),
            ("Patch 9/9: post-build fixes", self.patch_09_post_build),
        ]
        for name, fn in patches:
            print(f"\n--- {name} ---")
            fn()
        print(f"\n{'=' * 60}")
        print("  FINAL VALIDATION")
        print(f"{'=' * 60}")
        self.final_validation()
        print(f"\n{'=' * 60}")
        print("  ALL PATCHES APPLIED SUCCESSFULLY")
        print(f"{'=' * 60}")
        return 0


# Entry point
def main() -> int:
    version = "v2.15.1"
    existing_dir = None
    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg.startswith("v"):
            version = arg
        elif arg == "--dir" and i + 1 < len(args):
            existing_dir = args[i + 1]
    patcher = Patcher(version)
    if existing_dir:
        patcher.srcdir = existing_dir
        if not os.path.isdir(patcher.srcdir):
            die(f"Directory not found: {patcher.srcdir}")
    try:
        return patcher.run()
    except SystemExit as e:
        return e.code
    except Exception as e:
        fail(f"Unhandled exception: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        patcher.cleanup()


if __name__ == "__main__":
    sys.exit(main())
