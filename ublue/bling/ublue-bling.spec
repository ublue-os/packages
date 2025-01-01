%global debug_package %{nil}

Name:           ublue-bling
Version:        0.1.0
Release:        1%{?dist}
Summary:        Universal Blue Bling CLI setup scripts

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

# Requires: ublue-os-just but we cant add it here because it is sourced from ublue-os/config now.
# It would be interesting to move it here but we need some discussion
Requires:       gum

%description
Universal Blue Bling CLI setup scripts

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 ./src/%{name} %{buildroot}%{_libexecdir}/ublue-motd
# Intented to either be symlinked into the correct directories or be used directly
install -Dm0755 ./src/bling.sh %{buildroot}%{_datadir}/ublue-os/bling/bling.sh
install -Dm0755 ./src/bling.fish %{buildroot}%{_datadir}/ublue-os/bling/bling.fish

%files
%{_libexecdir}/ublue-motd
%{_datadir}/ublue-os/bling/bling.*sh

%changelog
%autochangelog
