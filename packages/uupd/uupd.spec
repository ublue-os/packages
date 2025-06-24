Name:           uupd
# renovate: datasource=github-releases depName=ublue-os/uupd
Version:        1.2.4
Release:        1%{?dist}
Summary:       Centralized update service/checker made for Universal Blue
Vendor:        ublue-os
URL:           https://github.com/%{vendor}/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
License:        Apache-2.0

BuildRequires:  golang
BuildRequires:  systemd-rpm-macros
BuildRequires:  git
Recommends:     bootc
Recommends:     distrobox
Recommends:     flatpak
Requires:       libnotify
Requires:       systemd
Provides:       %{name} = %{version}

%description
A simple updater for Universal Blue systems

%global debug_package %{nil}

%prep
%autosetup

%build
go build -v -o %{name}

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dpm 644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -Dpm 644 %{name}.timer %{buildroot}%{_unitdir}/%{name}.timer
install -Dpm 644 %{name}.rules %{buildroot}%{_sysconfdir}/polkit-1/rules.d/%{name}.rules

%check
go test -v ./...

%post
%systemd_post %{name}.timer

%preun
%systemd_preun %{name}.timer

%files
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer
%config(noreplace) %{_sysconfdir}/polkit-1/rules.d/%{name}.rules

%changelog
%autochangelog

