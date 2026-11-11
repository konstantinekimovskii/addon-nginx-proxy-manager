# Nginx Proxy Manager — Home Assistant Add-on

> [!WARNING]
> **This fork is no longer maintained as of November 11, 2026.** Version
> `2.15.1-r1` is the final release. No further updates or security fixes will
> be provided. Use the actively maintained
> [Home Assistant Community Apps project][upstream] for new installations.

This document describes the final legacy release of the fork.

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

## Migrating to the maintained project

Development has resumed in the original project:
[hassio-addons/app-nginx-proxy-manager][upstream]. Follow its
[installation and usage documentation][upstream-docs]. The Home Assistant
Community Apps repository is `https://github.com/hassio-addons/repository`.

A direct, in-place migration from this fork has **not been tested**. Both
projects use the `nginxproxymanager` slug, so do not assume that they can be
installed side by side or that installing the maintained version will safely
replace this fork.

1. Create a full Home Assistant backup that includes this add-on and download a
   copy outside Home Assistant.
2. Record your proxy hosts, access lists, DNS-provider settings and custom Nginx
   directives. Plan a maintenance window for proxy downtime.
3. Use the [maintained project's documentation][upstream-docs] for installation
   and recovery guidance.
4. Do not uninstall this fork until you have a restorable backup and understand
   how you will restore or recreate the configuration. Uninstalling an add-on
   can delete its local data.
5. After migration, verify login and 2FA, proxy hosts, custom certificates,
   Let's Encrypt issuance and renewal, and every DNS provider you use.

## Legacy configuration

This add-on does not provide any configuration options.

The legacy add-on serves its admin interface on port `81` and uses ports `80`
and `443` for HTTP and HTTPS traffic. Do not expose the admin interface on port
`81` directly to the internet.

## Changelog & Releases

See [CHANGELOG.md](CHANGELOG.md) for detailed legacy release notes. For current
releases, see the [maintained project's releases][upstream-releases].

## Support

This fork no longer provides support. For the maintained version, use the
[original project's support channels][upstream-support] or the
[Home Assistant Community Forum][forum].

## Authors & contributors

Original add-on by [Franck Nijhof][frenck].

This fork was maintained by [Konstantin Ekimovskii][konstantinekimovskii].

## License

MIT License

Copyright (c) 2019–2025 Franck Nijhof (original work)

Copyright (c) 2026 Konstantin Ekimovskii (fork modifications)

[forum]: https://community.home-assistant.io/t/home-assistant-community-add-on-nginx-proxy-manager/111830?u=frenck
[frenck]: https://github.com/frenck
[konstantinekimovskii]: https://github.com/konstantinekimovskii
[upstream]: https://github.com/hassio-addons/app-nginx-proxy-manager
[upstream-docs]: https://github.com/hassio-addons/app-nginx-proxy-manager/blob/main/proxy-manager/DOCS.md
[upstream-releases]: https://github.com/hassio-addons/app-nginx-proxy-manager/releases
[upstream-support]: https://github.com/hassio-addons/app-nginx-proxy-manager#support
