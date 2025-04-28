%global jobid 899
%global debug_package %{nil}

%global reponame    fw-fanctrl
%global commit      80ecc5d273b46f715d924c49234b6867fe3daf33
%global commit_date 20250302
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-fanctrl
Version:        0.0.0
Release:        10%{gitrel}%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/%{name}
Source0:        https://github.com/TamtamHero/%{name}/archive/%{commit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)
Requires:       python3
Requires:       fw-ectool

Patch0:         138-no-build.patch

Source1:        fw-fanctrl-auto-setup
Source2:        fw-fanctrl-auto-setup.service

%description
Framework Fan control script

%prep
%autosetup -n %{name}-%{commit}

%build
%pyproject_wheel

%install
./install.sh --no-sudo \
    --no-ectool \
    --no-pip-install \
    --no-pip-build \
    --no-post-install \
    --no-override-python-installation-path \
    -p %{buildroot}/usr \
    --sysconf-dir %{buildroot}/etc
%pyproject_install

install -D -m 0755 %{SOURCE1} %{buildroot}/usr/libexec/fw-fanctrl-auto-setup
install -D -m 0644 %{SOURCE2} %{buildroot}/usr/lib/systemd/system/fw-fanctrl-auto-setup.service

%post
%systemd_post %{name}.service
%systemd_post fw-fanctrl-auto-setup.service

%preun
%systemd_preun %{name}.service
%systemd_preun fw-fanctrl-auto-setup.service

%postun
%systemd_postun %{name}.service
%systemd_postun fw-fanctrl-auto-setup.service

%files
%license LICENSE
%{_bindir}/%{name}
%{python3_sitelib}/fw_fanctrl*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_sysconfdir}/%{name}/config.schema.json
%{_prefix}/lib/systemd/system-sleep/%{name}-suspend
%{_libexecdir}/fw-fanctrl-auto-setup
%{_unitdir}/fw-fanctrl-auto-setup.service

%changelog
%autochangelog
