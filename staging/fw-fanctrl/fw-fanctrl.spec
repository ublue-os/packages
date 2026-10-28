%global jobid 899
%global debug_package %{nil}

Name:           fw-fanctrl
# renovate: datasource=github-releases depName=TamtamHero/fw-fanctrl
Version:        1.1.0
Release:        1%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/%{name}
Source0:        https://github.com/TamtamHero/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3-build
Requires:       python3
Requires:       fw-ectool

%description
Framework Fan control script

%prep
%autosetup -n %{name}-%{version}

%build
%pyproject_wheel

%install
./install.sh --no-sudo \
    --no-ectool \
    --no-pip-install \
    --no-post-install \
    -p %{buildroot}/usr \
    --sysconf-dir %{buildroot}/etc
# Strip the temporary buildroot path out of the generated systemd service files
sed -i 's|%{buildroot}||g' %{buildroot}%{_unitdir}/fw-fanctrl.service
sed -i 's|%{buildroot}||g' %{buildroot}%{_unitdir}/fw-fanctrl-suspend.service
%pyproject_install

# framework_tool already included in framework-system package
rm -f %{buildroot}%{_bindir}/framework_tool

%post
%systemd_post %{name}.service
%udev_rules_update

%preun
%systemd_preun %{name}.service
%udev_rules_update

%postun
%systemd_postun %{name}.service
%udev_rules_update

%files
%license LICENSE
%{_bindir}/%{name}
%{python3_sitelib}/fw_fanctrl*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-suspend.service
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_sysconfdir}/%{name}/config.schema.json

%changelog
%autochangelog
