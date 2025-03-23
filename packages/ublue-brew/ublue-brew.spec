%global debug_package %{nil}
# renovate: datasource=github-releases depName=ublue-os/packages
%define homebrew_release homebrew-2025-02-16-23-20-49

Name:           ublue-brew
Version:        0.1.3
Release:        1%{?dist}
Summary:        Homebrew integration for Universal Blue systems

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}
Source1:        https://github.com/ublue-os/packages/releases/download/%{homebrew_release}/homebrew-x86_64.tar.zst
ExclusiveArch:  x86_64

BuildRequires:  systemd-rpm-macros

%description
Homebrew integration for Universal Blue systems

%prep
{{{ git_dir_setup_macro }}}

%install
mkdir -p %{buildroot}{%{_unitdir},%{_prefix}/lib/systemd/system-preset,%{_sysconfdir}}
install -Dpm0644 %{SOURCE1} %{buildroot}/%{_datadir}/homebrew.tar.zst
install -Dpm0644 src/systemd/*.service %{buildroot}%{_unitdir}
install -Dpm0644 src/systemd/*.preset %{buildroot}%{_prefix}/lib/systemd/system-preset
install -Dm0644 ./src/vendor.fish %{buildroot}%{_datadir}/fish/vendor_conf.d/%{name}.fish
cp -rp src/security %{buildroot}%{_sysconfdir}
cp -rp src/profile.d %{buildroot}%{_sysconfdir}
cp -rp src/tmpfiles.d %{buildroot}%{_prefix}/lib

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
