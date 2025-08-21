Name:           ublue-os-flatpak
Version:        1000
Release:        1%{?dist}
Summary:        Prevents issues caused by removing the misconfigured Fedora flatpak remote on Fedora systems.
License:        GPLv3
URL:            https://github.com/ublue-os/
BuildArch:      noarch

Source0:        LICENSE

Provides:       fedora-third-party = %{version}
Obsoletes:      fedora-third-party < %{version}

%description
Prevents issues caused by removing the misconfigured Fedora flatpak remote on Fedora systems.

# Disable debug packages
%define debug_package %{nil}

%install
mkdir -p %{buildroot}%{_defaultlicensedir}/%{name}
install -D -m 0644 %{SOURCE0} %{buildroot}%{_defaultlicensedir}/%{name}/LICENSE

%files
%license LICENSE
