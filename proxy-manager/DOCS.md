# Nginx Proxy Manager — Home Assistant Add-on

This add-on enables you to easily forward incoming connections to anywhere,
including free SSL, without having to know too much about Nginx
or Let's Encrypt.

Forward your domain to your Home Assistant, add-ons, or websites running
at home or anywhere else, straight from a simple, powerful interface.

Want to protect the website with a username/password? Well, it can do that too!
Enable authentication and create a list of usernames/passwords that can access
that specific application.

For the power users, you can customize the behavior of each host in the
Nginx proxy manager by providing additional Nginx directives.

## Installation

1. In Home Assistant: **Settings → Add-ons → Add-on Store → ⋮ → Repositories**
2. Add: `https://github.com/konstantinekimovskii/addon-nginx-proxy-manager`
3. Install **Nginx Proxy Manager**
4. Start the add-on and check logs for any issues.
5. Open Web UI (port 81) and log in
6. Forward ports `80` and `443` from your router to your Home Assistant machine.
7. Enjoy the add-on!

## Configuration

This add-on does not provide any configuration options.

## Changelog & Releases

See [CHANGELOG.md](../../CHANGELOG.md) for detailed release notes.

## Support

Got questions?

- Open an [issue on GitHub][issue].
- Check the [Home Assistant Community Forum][forum] (original add-on thread).

## Authors & contributors

Original add-on by [Franck Nijhof][frenck].

Fork maintained by [Konstantin Ekimovskii][konstantinekimovskii].

## License

MIT License

Copyright (c) 2019–2025 Franck Nijhof (original work)
Copyright (c) 2026 Konstantin Ekimovskii (fork modifications)

[forum]: https://community.home-assistant.io/t/home-assistant-community-add-on-nginx-proxy-manager/111830?u=frenck
[frenck]: https://github.com/frenck
[issue]: https://github.com/konstantinekimovskii/addon-nginx-proxy-manager/issues
[konstantinekimovskii]: https://github.com/konstantinekimovskii
