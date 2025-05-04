%global debug_package %{nil}
# renovate: datasource=github-releases depName=ublue-os/packages
%define homebrew_release homebrew-2025-05-04-04-03-02

Name:           ublue-brew
Version:        0.1.4
Release:        1%{?dist}
Summary:        Homebrew integration for Universal Blue systems

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}
Source1:        https://github.com/ublue-os/packages/releases/download/%{homebrew_release}/homebrew-%{_arch}.tar.zst

BuildRequires:  systemd-rpm-macros

%description
Homebrew integration for Universal Blue systems

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dpm0644 %{SOURCE1} %{buildroot}/%{_datadir}/homebrew.tar.zst
install -Dpm0644 -t %{buildroot}%{_unitdir}/ src/systemd/*.service 
install -Dpm0644 -t %{buildroot}%{_unitdir}/ src/systemd/*.timer 
install -Dpm0644 -t %{buildroot}%{_prefix}/lib/systemd/system-preset/ src/systemd/*.preset 
install -Dpm0644 ./src/vendor.fish %{buildroot}%{_datadir}/fish/vendor_conf.d/%{name}.fish
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/security/limits.d/ ./src%{_sysconfdir}/security/limits.d/*.conf
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/profile.d/ ./src%{_sysconfdir}/profile.d/*.sh
install -Dpm0644 %{buildroot}%{_prefix}/lib ./src%{_prefix}/tmpfiles.d/*.conf 

%post
%systemd_post brew-setup.service

%preun
%systemd_preun brew-setup.service

%files
%ghost %{_sysconfdir}/profile.d/brew.sh
%{_datadir}/homebrew.tar.zst
%{_sysconfdir}/profile.d/brew-bash-completion.sh
%{_datadir}/fish/vendor_conf.d/%{name}.fish
%{_sysconfdir}/security/limits.d/*brew*.conf
%{_unitdir}/brew-setup.service
%{_unitdir}/brew-update.timer
%{_unitdir}/brew-update.service
%{_unitdir}/brew-upgrade.timer
%{_unitdir}/brew-upgrade.service
%{_prefix}/lib/systemd/system-preset/01-homebrew.preset
%{_prefix}/lib/tmpfiles.d/*brew.conf

%changelog
%autochangelog
