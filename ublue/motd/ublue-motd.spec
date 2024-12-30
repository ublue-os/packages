%global debug_package %{nil}

Name:           ublue-motd
Version:        0.1.0
Release:        1%{?dist}
Summary:        MOTD scripts for Universal Blue images

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Requires:       glow

%description
MOTD script for Universal Blue

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 ./src/ublue-motd %{buildroot}%{_libexecdir}/ublue-motd
install -dm 0755 %{buildroot}%{_datadir}/ublue-os/motd/themes
cp -rp ./src/themes/* %{buildroot}%{_datadir}/ublue-os/motd/themes
install -Dm0755 ./src/vendor.sh %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
install -Dm0755 ./src/vendor.fish %{buildroot}%{_datadir}/fish/vendor_conf.d/%{name}.fish

%files
%{_libexecdir}/ublue-motd
%{_datadir}/ublue-os/motd/themes/*
%{_sysconfdir}/profile.d/%{name}.sh
%{_datadir}/fish/vendor_conf.d/%{name}.fish

%changelog
%autochangelog
