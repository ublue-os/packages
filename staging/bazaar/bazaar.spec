# renovate: datasource=git-refs depName=https://github.com/kolunmi/bazaar.git
%global commit fcc10da362760123041e35e59de8097733883d0e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global appid org.gnome.Example

Name:           bazaar
Version:        %{shortcommit}
Release:        1%{?dist}
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
BuildRequires:  desktop-file-utils
Requires:       glycin-libs
Requires:       libadwaita

%description
%summary

%prep
%autosetup -n bazaar-%{commit}

%build
%meson
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

%changelog
* Sat May 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Init package
