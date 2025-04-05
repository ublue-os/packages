%global debug_package %{nil}
%global vendor aurora

Name:           aurora
Version:        0.1.0
Release:        1%{?dist}
Summary:        Aurora branding

License:        CC-BY-CA
URL:            https://github.com/ublue-os/packages
VCS:           {{{ git_dir_vcs }}}
Source:        {{{ git_dir_pack }}}

%description
Branding for Aurora-related projects

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/aurora-logos/symbols/ cli-logos/symbols/*
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/ fastfetch/fastfetch.jsonc

%check

%package cli-logos
Version:        0.2.0
Summary:        Logos for CLI
License:        CC-BY-CA

%description cli-logos
Logos for CLI applications like Fastfetch

%files cli-logos
%{_datadir}/ublue-os/aurora-logos/*


%package fastfetch
Summary:        Fastfetch configuration for Aurora
Version:        0.2.0
License:        CC-BY-CA

%description fastfetch
Fastfetch configuration for Aurora

%files fastfetch
%{_datadir}/ublue-os/fastfetch.jsonc

%changelog
%autochangelog
