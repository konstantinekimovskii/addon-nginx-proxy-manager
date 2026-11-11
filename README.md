# Nginx Proxy Manager — Home Assistant Add-on

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE.md)
[![GitHub Actions][github-actions-shield]][github-actions]

> [!WARNING]
> **This fork is no longer maintained as of November 11, 2026.** The last
> release is `2.15.1-r1`. It will receive no further updates, including
> security fixes. Please migrate to the actively maintained
> [Home Assistant Community Apps project][upstream].

Manage Nginx proxy hosts with a simple, powerful interface.

## About

This repository was an independent fork created to keep up with Nginx Proxy
Manager releases and HAOS versions while the original project was inactive.

Development has since resumed in the original project, now located at
[hassio-addons/app-nginx-proxy-manager][upstream]. New installations should use
that project instead of this fork. Existing releases and container images are
kept here for reference and recovery of legacy installations.

The final fork release supports `aarch64` (including Raspberry Pi 5) and
`amd64`.

## Maintained alternative

Use the [maintained project][upstream] and follow its
[installation documentation][upstream-docs]. Its Home Assistant Community Apps
repository is available at:

```text
https://github.com/hassio-addons/repository
```

## Migration to the maintained project

A direct, in-place migration between these repositories has **not been tested**.
Both projects use the `nginxproxymanager` slug, so do not assume that they can
be installed side by side or that one can safely be installed over the other.

Before changing an existing installation:

1. Create a full Home Assistant backup that includes the Nginx Proxy Manager
   add-on and download a copy outside Home Assistant.
2. Record your proxy hosts, access lists, DNS-provider settings and custom Nginx
   directives. Plan a maintenance window for the proxy downtime.
3. Follow the [maintained project's documentation][upstream-docs] for
   installation and recovery guidance.
4. Do not uninstall this fork until you have a restorable backup and understand
   how you will restore or recreate the configuration. Uninstalling an add-on
   can delete its local data.
5. After migration, verify login and 2FA, proxy hosts, custom certificates,
   Let's Encrypt issuance and renewal, and every DNS provider you use.

The legacy documentation remains available in
[`proxy-manager/DOCS.md`](proxy-manager/DOCS.md).

## Support and contributing

This fork no longer accepts support requests or contributions. Please use the
[maintained project's support channels][upstream-support] and contribute there.

## License

MIT — see [LICENSE.md](LICENSE.md)

[releases-shield]: https://img.shields.io/github/release/konstantinekimovskii/addon-nginx-proxy-manager.svg
[releases]: https://github.com/konstantinekimovskii/addon-nginx-proxy-manager/releases
[license-shield]: https://img.shields.io/github/license/konstantinekimovskii/addon-nginx-proxy-manager.svg
[github-actions-shield]: https://github.com/konstantinekimovskii/addon-nginx-proxy-manager/workflows/CI/badge.svg
[github-actions]: https://github.com/konstantinekimovskii/addon-nginx-proxy-manager/actions
[upstream]: https://github.com/hassio-addons/app-nginx-proxy-manager
[upstream-docs]: https://github.com/hassio-addons/app-nginx-proxy-manager/blob/main/proxy-manager/DOCS.md
[upstream-support]: https://github.com/hassio-addons/app-nginx-proxy-manager#support
