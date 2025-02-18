%global debug_package %{nil}

Name:           ublue-rebase-helper
Version:        0.1.0
Release:        1%{?dist}
Summary:        Rebase helper for Universal Blue images

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}

%description
Rebase helper script and develoepr edition script for Universal Blue images

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 -t %{buildroot}%{_libexecdir} ./src/ublue-*-helper

%files
%{_libexecdir}/ublue-*-helper

%changelog
%autochangelog
