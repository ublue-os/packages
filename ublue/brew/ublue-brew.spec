%global debug_package %{nil}

Name:           ublue-brew
Version:        0.1.0
Release:        1%{?dist}
Summary:        Homebrew integration for Universal Blue systems

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildRequires:  systemd-rpm-macros

%description
Homebrew integration for Universal Blue systems

%prep
{{{ git_dir_setup_macro }}}

%install
mkdir -p %{buildroot}{%{_unitdir},%{_prefix}/lib/systemd/system-preset,%{_sysconfdir}}
install -Dpm0755 src/systemd/*.service %{buildroot}%{_unitdir}
install -Dpm0755 src/systemd/*.preset %{buildroot}%{_prefix}/lib/systemd/system-preset
cp -rp src/security %{buildroot}%{_sysconfdir}
cp -rp src/profile.d %{buildroot}%{_sysconfdir}
cp -rp src/tmpfiles.d %{buildroot}%{_prefix}/lib

%post
%systemd_post brew-setup.service

%preun
%systemd_preun brew-setup.service

%files
%{_sysconfdir}/profile.d/brew*
%{_sysconfdir}/security/limits.d/*brew*.conf
%{_unitdir}/brew-setup.service
%{_prefix}/lib/systemd/system-preset/01-homebrew.preset
%{_prefix}/lib/tmpfiles.d/*brew.conf

%changelog
%autochangelog
