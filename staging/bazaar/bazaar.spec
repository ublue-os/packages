%global appid io.github.kolunmi.Bazaar

Name:           bazaar
# renovate: datasource=gitlab-releases depName=bazaar-org/bazaar
Version:        0.9.4
Release:        4%{?dist}
Summary:        Flatpak-centric software center and app store

License:        GPL-3.0-only
URL:            https://usebazaar.org/
Source:         https://gitlab.gnome.org/World/bazaar/-/archive/v%{version}/bazaar-v%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  blueprint-compiler >= 0.20.0
BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/xmllint
BuildRequires:  python3-babel
BuildRequires:  python3-gobject-base
BuildRequires:  pkgconfig(gtk4) >= 4.22.1
BuildRequires:  pkgconfig(gtksourceview-5) >= 5.17
BuildRequires:  pkgconfig(libadwaita-1) >= 1.8
BuildRequires:  pkgconfig(appstream) >= 1.0
BuildRequires:  pkgconfig(xmlb) >= 0.3.4
BuildRequires:  pkgconfig(flatpak) >= 1.9
BuildRequires:  pkgconfig(libdex-1) >= 1.0.0
BuildRequires:  pkgconfig(yaml-0.1) >= 0.2.5
BuildRequires:  pkgconfig(libsoup-3.0) >= 3.6.0
BuildRequires:  pkgconfig(json-glib-1.0) >= 1.10.0
BuildRequires:  pkgconfig(glycin-2) >= 2.0
BuildRequires:  pkgconfig(glycin-gtk4-2) >= 2.0
BuildRequires:  pkgconfig(webkitgtk-6.0) >= 2.50.2
BuildRequires:  pkgconfig(libsecret-1) >= 0.20
BuildRequires:  pkgconfig(md4c) >= 0.5.1
BuildRequires:  pkgconfig(libproxy-1.0) >= 0.5
BuildRequires:  pkgconfig(malcontent-0) >= 0.12.0
BuildRequires:  pkgconfig(libsystemd) >= 245

%description
A new app store with a focus on discovering and installing
applications and add-ons from Flatpak remotes, particularly Flathub.
It emphasizes supporting the developers who make the Linux desktop possible.

%prep
%autosetup -n bazaar-%{version}

%conf
%meson \
  -Dhardcoded_main_config_path=/usr/share/ublue-os/bazaar/main.yaml \
  -Dhardcoded_content_config_path=/usr/share/ublue-os/bazaar/content.yaml

%build
%meson_build

%install
%meson_install
%find_lang %{name}
rm %{buildroot}%{_bindir}/bge-demo
rm %{buildroot}%{_libdir}/pkgconfig/bge.pc
rm %{buildroot}%{_libdir}/libbge.so
rm -rf %{buildroot}%{_includedir}/bge/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop

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
%{_bindir}/%{name}-daemon
%{_bindir}/%{name}-dl-worker
%{_userunitdir}/%{appid}.service
%{_datadir}/dbus-1/services/%{appid}.SearchProvider.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{appid}-symbolic.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/gnome-shell/search-providers/%{appid}.search-provider.ini
%{_libdir}/libbge.so.0*

%changelog
* Wed Aug 5 2026 Kyle Gospodnetich <me@kylegospodneti.ch>
- Fix file list for 0.9.2: bazaar-refresh-worker is now a bazaar subcommand,
  add bazaar-daemon, rename D-Bus service to *.SearchProvider.service
- Add appstream, libsystemd, xmllint and PyGObject build dependencies
- Pin minimum versions for all upstream-declared dependencies

* Wed Apr 1 2026 Jill Fiore <contact@lumaeris.com>
- Update to version v0.7.13 and enforce GTK4 version

* Tue Dec 30 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.7.0

* Sun Aug 17 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.3.1

* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
