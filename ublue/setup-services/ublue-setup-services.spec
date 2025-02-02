%global debug_package %{nil}

Name:           ublue-setup-services
Version:        0.1.2
Release:        1%{?dist}
Summary:        Universal Blue setup services

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildRequires:  systemd-rpm-macros

%description
Universal Blue setup scripts

%prep
{{{ git_dir_setup_macro }}}

%install
mkdir -p %{buildroot}{%{_bindir},%{_libexecdir},%{_unitdir},%{_prefix}/lib/systemd/user,%{_sysconfdir}/{polkit-1/{rules.d,actions},profile.d}}
install -Dm0755 ./src/scripts/* %{buildroot}%{_libexecdir}
install -Dm0755 ./src/bin/* %{buildroot}%{_bindir}
install -Dpm0644 ./src/services/* %{buildroot}%{_unitdir}
install -Dpm0644 ./src/user-services/* %{buildroot}%{_prefix}/lib/systemd/user/
install -Dpm0644 ./src/polkit/*.rules %{buildroot}%{_sysconfdir}/polkit-1/rules.d
install -Dpm0644 ./src/polkit/*.policy %{buildroot}%{_sysconfdir}/polkit-1/actions
install -Dpm0755 ./src/profile/* %{buildroot}%{_sysconfdir}/profile.d
cp -rp ./src/skel %{buildroot}%{_sysconfdir}

%post
%systemd_post ublue-user-setup.service
%systemd_post ublue-system-setup.service

%preun
%systemd_preun ublue-user-setup.service
%systemd_preun ublue-system-setup.service

%files
%{_bindir}/sb*
%{_libexecdir}/ublue-*
%{_libexecdir}/check-*
%config(noreplace) %{_sysconfdir}/polkit-1/rules.d/*
%config(noreplace) %{_sysconfdir}/polkit-1/actions/*
%config(noreplace) %{_sysconfdir}/profile.d/*
%config(noreplace) %{_sysconfdir}/skel/.config/autostart/*
%{_unitdir}/*.service
%{_prefix}/lib/systemd/user/*.service

%changelog
%autochangelog
