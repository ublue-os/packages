Summary:        tauOS Icon Theme
Name:           hydrogen-icon-theme
Version:        1.0.16
Release:        2%?dist
License:        GPL-3.0
URL:            https://github.com/tau-OS/tau-hydrogen
Source0:        https://github.com/tau-OS/tau-hydrogen/archive/refs/tags/%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  librsvg2-tools
BuildRequires:  xcursorgen
BuildRequires:  fdupes
Provides: tau-hydrogen = %{version}-%{release}
Obsoletes: tau-hydrogen < 1.0.16-2

%description
Hydrogen is the default icon theme in tauOS

%prep
%autosetup -n tau-hydrogen-%{version}

%build
%meson
%meson_build

%install
# Install licenses
mkdir -p licenses
%meson_install
%fdupes %buildroot%_datadir

%files
%license LICENSE
%doc README.md
%{_datadir}/icons/Hydrogen/*
%{_datadir}/gimp/2.0/palettes/Helium.gpl
%{_datadir}/inkscape/palettes/Helium.gpl

%changelog
* Sun Nov 20 2022 Lleyton Gray <lleyton@fyralabs.com> - 1.0.1
- Terra Release
