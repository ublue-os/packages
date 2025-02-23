%global debug_package %{nil}
%global _appid de.haeckerfelix.Souk
%define _git_ref 02eb39da6f7199f880a1a8c24f34d254715d95c9

Name:           souk
Version:        0.0.0
Release:        1%{?dist}
Summary:        Independent Flatpak App Store

License:        GPL-3.0-only
URL:            https://github.com/ublue-os/souk
Source0:        https://github.com/ublue-os/souk/archive/%{_git_ref}.tar.gz

BuildRequires:  flatpak-devel
BuildRequires:  sqlite-devel
BuildRequires:  dbus-devel
BuildRequires:  libadwaita-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libxmlb-devel
BuildRequires:  cargo
BuildRequires:  meson
BuildRequires:  git

%description
Independent Flatpak App Store
This package is just for iteration and testing purposes and requires a network connection to build

%prep
%autosetup -n %{name}-%{_git_ref}

%build
%meson
%meson_build

%install
%meson_install

%files
%{_bindir}/%{name}
%{_bindir}/%{name}-worker
%{_datadir}/applications/%{_appid}.desktop
%{_datadir}/dbus-1/services/%{_appid}.Worker.service
%{_datadir}/dbus-1/services/%{_appid}.service
%{_datadir}/glib-2.0/schemas/%{_appid}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{_appid}.svg
%{_datadir}/icons/hicolor/symbolic/apps/%{_appid}-symbolic.svg
%{_datadir}/metainfo/%{_appid}.metainfo.xml
%{_datadir}/souk/%{_appid}.gresource

%changelog
%autochangelog
