%global debug_package %{nil}

Name:           glorpfetch
Version:        0.1.0
Release:        0%{?dist}
Summary:        Glorper Fetcher

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}

Requires:       fastfetch

%description
Glorps the Fetch


%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0755 -t %{buildroot}%{_bindir} ./src/glorpfetch
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/glorpfetch ./src/glorpfetch.jsonc
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/glorpfetch ./src/glorp.txt


%files
%{_bindir}/%{name}
%{_datadir}/ublue-os/%{name}


%changelog
* Thu Apr 17 2025 Tulip Blossom <tulilirockz@proton.me>
- Initialize the glorpfetch
