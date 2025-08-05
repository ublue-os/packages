# renovate: datasource=git-refs depName=https://github.com/kolunmi/bazaar.git versioning=loose currentValue=master
%global commit aa6b4eaf3ee50ef405a68a99001bf36d25826618
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global appid io.github.kolunmi.Bazaar

Name:           bazaar
Version:        {{{ git_dir_version }}}.%{shortcommit}
Release:        4%{?dist}
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
BuildRequires:  systemd-rpm-macros
BuildRequires:  blueprint-compiler
BuildRequires:  glycin-devel
# Needed until libdex is fixed
BuildRequires:  wget
BuildRequires:  sed

Requires:       glycin-libs
Requires:       libadwaita
Requires:       libsoup3
Requires:       json-glib
Requires:       libdex = 0.9.1

%description
%summary

%prep
%autosetup -n bazaar-%{commit}
# Needed until libdex is fixed
cd subprojects
wget https://gitlab.gnome.org/GNOME/libdex/-/archive/0.9.1/libdex-0.9.1.tar.gz
tar xf libdex-0.9.1.tar.gz
mv libdex-0.9.1 libdex
sed -i '/add_global_arguments/d' libdex/meson.build

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
%{_userunitdir}/%{appid}.service
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{appid}-symbolic.svg
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/gnome-shell/search-providers/%{appid}.search-provider.ini

%changelog
* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
