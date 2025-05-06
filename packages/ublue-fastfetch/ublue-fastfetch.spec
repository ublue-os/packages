%global debug_package %{nil}

Name:           ublue-fastfetch
Version:        0.1.4
Release:        1%{?dist}
Summary:        Fastfetch configuration for Universal Blue systems

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Requires:       fastfetch
BuildArch:      noarch

%description
Fastfetch configuration for Universal Blue systems

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 -t %{buildroot}%{_libexecdir}/ ./src/%{name}
install -Dm0755 -t %{buildroot}%{_libexecdir}/ ./src/ublue-bling-fastfetch
install -Dm0755 ./src/vendor.sh %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh
install -Dm0755 ./src/vendor.fish %{buildroot}%{_datadir}/fish/vendor_conf.d/%{name}.fish

%files
%{_libexecdir}/%{name}
%{_libexecdir}/ublue-bling-fastfetch
%{_sysconfdir}/profile.d/%{name}.sh
%{_datadir}/fish/vendor_conf.d/%{name}.fish

%changelog
%autochangelog
