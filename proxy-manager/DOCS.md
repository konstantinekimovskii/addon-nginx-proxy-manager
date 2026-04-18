# Nginx Proxy Manager — Home Assistant Add-on

This add-on enables you to easily forward incoming connections to anywhere,
including free SSL, without having to know too much about Nginx
or Let’s Encrypt.

Forward your domain to your Home Assistant, add-ons, or websites running
at home or anywhere else, straight from a simple, powerful interface.

Want to protect the website with a username/password? Well, it can do that too!
Enable authentication and create a list of usernames/password that can access
that specific application.

For the power users, you can customize the behavior of each host in the
Nginx proxy manager by providing additional Nginx directives.

## Installation

The installation of this add-on is pretty straightforward and not different in
comparison to installing any other Home Assistant add-on.

1. In Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories**
2. Add: `https://github.com/konstantinekimovskii/addon-nginx-proxy-manager`
3. Install **Nginx Proxy Manager**
4. Start the add‑on and check logs for any issues.
5. Open Web UI (port 81) and login with:
   `admin@example.com` / `changeme`
6. Forward ports `80` and `443` from your router to your Home Assistant machine.
7. Enjoy the add‑on!

## Configuration

This add‑on does not provide any configuration.

## Changelog & Releases

See [CHANGELOG.md](../CHANGELOG.md) for detailed release notes.

Releases are based on [Semantic Versioning][semver], and use the format
`MAJOR.MINOR.PATCH`. In a nutshell:

- `MAJOR`: Incompatible or major changes.
- `MINOR`: Backwards‑compatible new features and enhancements.
- `PATCH`: Backwards‑compatible bugfixes and package updates.

## Support

Got questions?

- Open an [issue on GitHub][issue].
- Check the [Home Assistant Community Forum][forum] (original add‑on thread).

## Authors & contributors

Original add‑on by [Franck Nijhof][frenck].

Fork maintained by [Konstantin Ekimovskii][konstantinekimovskii].

## License

MIT License

Copyright (c) 2019‑2025 Franck Nijhof (original work)
Copyright (c) 2026 Konstantin Ekimovskii (fork modifications)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[addon-badge]: https://my.home-assistant.io/badges/supervisor_addon.svg
[addon]: https://my.home-assistant.io/redirect/supervisor_addon/?addon=a0d7b954_nginxproxymanager&repository_url=https%3A%2F%2Fgithub.com%2Fkonstantinekimovskii%2Faddon-nginx-proxy-manager
[forum]: https://community.home-assistant.io/t/home-assistant-community-add-on-nginx-proxy-manager/111830?u=frenck
[frenck]: https://github.com/frenck
[issue]: https://github.com/konstantinekimovskii/addon-nginx-proxy-manager/issues
[konstantinekimovskii]: https://github.com/konstantinekimovskii
[semver]: https://semver.org/spec/v2.0.0.html
