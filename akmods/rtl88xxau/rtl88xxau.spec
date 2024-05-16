%global modname 88XXau
%global srcversion 5.6.4.2
%global srcname rtl8812au
%global pkgname rtl88xxau

%if 0%{?fedora}
%global debug_package %{nil}
%endif

Name:     %{pkgname}
Version:  %{srcversion}.git
Release:  2%{?dist}
Summary:  Realtek RTL8812AU/21AU and RTL8814AU driver
License:  GPLv2
URL:      https://github.com/aircrack-ng/rtl8812au
Source0:  https://raw.githubusercontent.com/aircrack-ng/rtl8812au/v%{srcversion}/LICENSE?name=LICENSE.%{pkgname}

Provides: %{name}-kmod-common = %{version}
Requires: %{name}-kmod >= %{version}

BuildRequires: systemd-rpm-macros

%description
Realtek RTL8812AU/21AU and RTL8814AU driver with monitor mode and frame injection

%build
cp %{SOURCE0} LICENSE

%install
install -D -m 0644 %{SOURCE0} %{buildroot}%{_datarootdir}/licenses/%{pkgname}/LICENSE

%files
%license LICENSE

%changelog
