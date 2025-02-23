%global modname rtl8814au

%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     %{modname}
Version:  5.8.5.1.git
Release:  3%{?dist}
Summary:  Realtek RTL8814AU Driver
License:  GPLv2
URL:      https://github.com/morrownr/8814au
Source0:  https://raw.githubusercontent.com/morrownr/8814au/main/LICENSE?name=LICENSE.%{modname}

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Realtek RTL8814AU Driver

%build
cp %{SOURCE0} LICENSE

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_datarootdir}/licenses/%{modname}/LICENSE

%files
%license LICENSE

%changelog
