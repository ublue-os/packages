%global buildforkernels akmod
%global debug_package %{nil}

Name:           new-lg4ff
Version:        0.4.0
Release:        1%{?dist}
Summary:        Experimental Logitech force feedback module for Linux 
License:        GPL-2.0-only

URL:            https://github.com/berarma/new-lg4ff
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

Provides:       %{name}-kmod-common = %{version}-%{release}
Requires:       %{name}-kmod >= %{version}

%description
Improved Linux module driver for Logitech driving wheels.

%prep
%autosetup

for kernel_version  in %{?kernel_versions} ; do
  cp -a %{name}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
# Nothing to build

%install
# Nothing to install

%files
%doc README.md 
%license LICENSE

%changelog
