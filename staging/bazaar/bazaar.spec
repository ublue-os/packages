%global appid io.github.kolunmi.Bazaar

Name:           bazaar
# renovate: datasource=github-releases depName=bazaar-org/bazaar
Version:        0.7.13
Release:        1%{?dist}
Summary:        Flatpak-centric software center and app store

License:        GPL-3.0-only
URL:            https://usebazaar.org/
Source:         %{url}/archive/v%{version}/bazaar-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros
BuildRequires:  blueprint-compiler >= 0.20.0
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gtk4) >= 4.22.1
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(xmlb)
BuildRequires:  pkgconfig(flatpak)
BuildRequires:  pkgconfig(libdex-1) >= 1.0.0
BuildRequires:  pkgconfig(yaml-0.1)
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(glycin-2)
BuildRequires:  pkgconfig(glycin-gtk4-2)
BuildRequires:  pkgconfig(webkitgtk-6.0)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(md4c)
BuildRequires:  pkgconfig(libproxy-1.0)
BuildRequires:  pkgconfig(malcontent-0)

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
rm %{buildroot}%{_libdir}/pkgconfig/bge-0.1.pc
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
%{_bindir}/%{name}-dl-worker
%{_userunitdir}/%{appid}.service
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{appid}-symbolic.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/gnome-shell/search-providers/%{appid}.search-provider.ini
%{_libdir}/libbge-0.1.so

%changelog
* Wed Apr 1 2026 Jill Fiore <contact@lumaeris.com>
- Update to version v0.7.13 and enforce GTK4 version

* Tue Dec 30 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.7.0

* Sun Aug 17 2025 Kyle Gospodnetich <me@kylegospodneti.ch>
- Update to version v0.3.1

* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
