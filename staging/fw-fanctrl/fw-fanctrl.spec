%global jobid 899
%global debug_package %{nil}

%global reponame    fw-fanctrl
%global commit      b040da6686f694504b8dc22918be5cb655e75bf5
%global commit_date 20260606
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-fanctrl
Version:        0.0.0
Release:        11%{gitrel}%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/%{name}
Source0:        https://github.com/TamtamHero/%{name}/archive/%{commit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3-build
Requires:       python3
Requires:       fw-ectool

Source1:        99-fw-fanctrl.rules

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
    --no-post-install \
    -p %{buildroot}/usr \
    --sysconf-dir %{buildroot}/etc
# Strip the temporary buildroot path out of the generated systemd service files
sed -i 's|%{buildroot}||g' %{buildroot}%{_unitdir}/fw-fanctrl.service
sed -i 's|%{buildroot}||g' %{buildroot}%{_unitdir}/fw-fanctrl-suspend.service
%pyproject_install

install -D -m 0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/99-fw-fanctrl.rules
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
%{_udevrulesdir}/99-fw-fanctrl.rules

%changelog
%autochangelog
