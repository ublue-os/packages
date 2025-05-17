%global debug_package %{nil}

Name:           ublue-setup-services
Version:        0.1.8
Release:        1%{?dist}
Summary:        Universal Blue setup services

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildRequires:  systemd-rpm-macros
BuildArch:      noarch

%description
Universal Blue setup scripts

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 -t %{buildroot}%{_libexecdir}/ ./src/scripts/*
install -Dm0755 -t %{buildroot}%{_bindir}/ ./src/bin/*
install -Dm0644 -t %{buildroot}%{_unitdir}/ ./src/services/*.service
install -Dm0644 -t %{buildroot}%{_prefix}/lib/systemd/user/ ./src/user-services/*.service
install -Dm0644 -t %{buildroot}%{_sysconfdir}/polkit-1/rules.d/ ./src/polkit/*.rules 
install -Dm0644 -t %{buildroot}%{_sysconfdir}/polkit-1/actions/ ./src/polkit/*.policy
install -Dm0755 -t %{buildroot}%{_sysconfdir}/profile.d/ ./src/profile/*.sh
install -Dm0644 -t %{buildroot}%{_exec_prefix}/lib/ublue/setup-services/ ./src/lib/libsetup.sh
install -Dm0644 -t %{buildroot}%{_sysconfdir}/skel/.config/autostart/ src/skel/.config/autostart/*.desktop

%post
%systemd_post ublue-user-setup.service
%systemd_post ublue-system-setup.service

%preun
%systemd_preun ublue-user-setup.service
%systemd_preun ublue-system-setup.service

%files
%{_bindir}/sb*
%{_exec_prefix}/lib/ublue/setup-services/lib*.sh
%{_libexecdir}/ublue-*
%{_libexecdir}/check-*
%{_sysconfdir}/polkit-1/rules.d/*
%{_sysconfdir}/polkit-1/actions/*
%{_sysconfdir}/profile.d/*
%{_sysconfdir}/skel/.config/autostart/*.desktop
%{_unitdir}/*.service
%{_prefix}/lib/systemd/user/*.service

%changelog
%autochangelog
