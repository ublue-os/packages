%global appid io.github.kolunmi.Bazaar

Name:           bazaar
# renovate: datasource=github-releases depName=kolunmi/bazaar
Version:        0.4.4
Release:        1%{?dist}
Summary:        A flatpak centered app store

License:        GPL-3.0-only
URL:            https://github.com/kolunmi/bazaar
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  blueprint-compiler
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(xmlb)
BuildRequires:  pkgconfig(flatpak)
BuildRequires:  pkgconfig(libdex-1)
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(glycin-1)
BuildRequires:  pkgconfig(glycin-gtk4-1)

Requires:       glycin-libs
Requires:       libadwaita
Requires:       libsoup3
Requires:       json-glib

%description
A new app store for GNOME with a focus on discovering and installing applications and add-ons from Flatpak remotes, particularly Flathub.
It emphasizes supporting the developers who make the Linux desktop possible.
Bazaar features a "curated" tab that can be configured by distributors to allow for a more locallized experience.

%prep
%autosetup -n bazaar-%{version}

%build
%meson \
  -Dhardcoded_content_config_path=/usr/share/ublue-os/bazaar/config.yaml \
  -Dhardcoded_blocklist_path=/usr/share/ublue-os/bazaar/blocklist.txt
%meson_build

%install
%meson_install
%find_lang %{name}

%post
%systemd_user_post %{appid}.service

%preun
%systemd_user_preun %{appid}.service

%postun
%systemd_user_postun_with_restart %{appid}.service

%files -f %{name}.lang
%license COPYING
%doc README.md
%{_datadir}/applications/%{appid}.desktop
%{_bindir}/%{name}
%{_bindir}/%{name}-dl-worker
%{_userunitdir}/%{appid}.service
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{appid}-symbolic.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/gnome-shell/search-providers/%{appid}.search-provider.ini

%changelog
* Sun Aug 17 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.3.1

* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
