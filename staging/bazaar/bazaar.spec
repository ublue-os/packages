# renovate: datasource=git-refs depName=https://github.com/kolunmi/bazaar.git versioning=loose currentValue=master
%global commit 8642831f7743c35b9b7a010ac6ce4251d8fb19ad
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global appid io.github.kolunmi.bazaar

Name:           bazaar
Version:        {{{ git_dir_version }}}.%{shortcommit}
Release:        2%{?dist}
Summary:        A new app store idea for GNOME. 

License:        GPL-3.0-only
URL:            https://github.com/kolunmi/bazaar
Source0:        %{url}/archive/%{commit}.tar.gz

BuildRequires:  meson
BuildRequires:  libadwaita-devel
BuildRequires:  libxmlb-devel
BuildRequires:  flatpak-devel
BuildRequires:  glycin-devel
BuildRequires:  glycin-gtk4-devel
BuildRequires:  libdex-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libyaml-devel
BuildRequires:  libsoup3-devel
BuildRequires:  json-glib
Requires:       glycin-libs
Requires:       libadwaita
Requires:       libsoup3
Requires:       json-glib

%description
%summary

%prep
%autosetup -n bazaar-%{commit}

%build
%meson -Dhardcoded_content_config_path=/usr/share/ublue-os/bazaar/config.yaml -Dhardcoded_blocklist_path=/usr/share/ublue-os/bazaar/blocklist.txt
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_datadir}/applications/%{appid}.desktop
%{_bindir}/%{name}
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{appid}-symbolic.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/gnome-shell/search-providers/%{appid}.search-provider.ini

%changelog
* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
