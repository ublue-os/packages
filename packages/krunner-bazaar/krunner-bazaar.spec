%global majmin_ver 1.0.5

Name:           krunner-bazaar
Version:        %{majmin_ver}
Release:        1%{?dist}
Summary:        KDE KRunner plugin for searching Flatpak applications via Bazaar

License:        Apache-2.0
URL:            https://github.com/ublue-os/krunner-bazaar
Source:         %{url}/archive/refs/tags/v%{majmin_ver}.zip

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules
BuildRequires:  kf6-krunner-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  kf6-rpm-macros

Requires:       kf6-krunner
Requires:       qt6-qtbase
Requires:       flatpak
Requires:       bazaar

%description
A KDE KRunner plugin that integrates with Bazaar, a GTK application for browsing
and installing Flatpak applications. This plugin allows users to search for
Flatpak applications directly from KRunner and launch them via Bazaar for
installation.

%package        tools
Summary:        CLI tools for %{name}
Requires:       %{name} = %{version}-%{release}

%description    tools
Command-line tools for testing and debugging the krunner-bazaar plugin,
including a standalone tool for testing Bazaar D-Bus interactions.

%prep
%autosetup

%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=%{_prefix}
%cmake_build

%install
%cmake_install

%check
# Basic smoke test - check if the plugin file was created
test -f %{buildroot}%{_kf6_plugindir}/krunner/bazaarrunner.so

%files
%license LICENSE
%doc README.md
%{_kf6_plugindir}/krunner/bazaarrunner.so

%files tools
%{_bindir}/bazaar-dbus-tool

%changelog
* Tue Jun 24 2025 Adam Fidel <adam@fidel.cloud> - 1.0.0-1
- Initial RPM package
