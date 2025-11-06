%global debug_package %{nil}

Name:           ublue-bling
Version:        0.1.12
Release:        1%{?dist}
Summary:        Universal Blue Bling CLI setup scripts

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Requires:       gum
BuildArch:      noarch
# FIXME: make ublue-builder be able to handle stuff like this
# Requires:       ublue-os-just

%description
Universal Blue Bling CLI setup scripts

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 ./src/%{name} %{buildroot}%{_libexecdir}/%{name}
# Intented to either be symlinked into the correct directories or be used directly
install -Dm0755 ./src/bling.sh %{buildroot}%{_datadir}/ublue-os/bling/bling.sh
install -Dm0755 ./src/bling.fish %{buildroot}%{_datadir}/ublue-os/bling/bling.fish

%files
%{_libexecdir}/%{name}
%{_datadir}/ublue-os/bling/bling.*sh

%changelog
%autochangelog
