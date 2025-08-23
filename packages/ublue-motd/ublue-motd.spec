%global debug_package %{nil}

Name:           ublue-motd
Version:        0.2.6
Release:        1%{?dist}
Summary:        MOTD scripts for Universal Blue images

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Requires:       glow
Requires:       jq
Requires:       curl

BuildArch:      noarch

%description
MOTD and changelogs script for Universal Blue

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0644 -t %{buildroot}%{_datadir}/ublue-os/motd/themes/ ./src/themes/*.json
install -Dm0755 -t %{buildroot}%{_libexecdir}/ ./src/%{name}
install -Dm0755 -t %{buildroot}%{_libexecdir}/ ./src/ublue-changelog
install -Dm0755 ./src/vendor.sh %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
install -Dm0755 ./src/vendor.fish %{buildroot}%{_datadir}/fish/vendor_conf.d/%{name}.fish

%files
%{_libexecdir}/%{name}
%{_libexecdir}/ublue-changelog
%{_datadir}/ublue-os/motd/themes/*
%{_sysconfdir}/profile.d/%{name}.sh
%{_datadir}/fish/vendor_conf.d/%{name}.fish

%changelog
%autochangelog
