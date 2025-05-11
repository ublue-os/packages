%global debug_package %{nil}
%global vendor bluefin

Name:           fedora-logos
Version:        0.1.0
Release:        1%{?dist}
Summary:        Bluefin branding

License:        CC-BY-CA
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Provides: fedora-logos
Provides: redhat-logos
Provides: gnome-logos
Provides: system-logos
BuildArch:      noarch

%description
Branding for Bluefin's anaconda

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ src/logos/*
install -Dpm0644 -t %{buildroot}%{_datadir}/anaconda/pixmaps/ src/anaconda/*

%files
%{_datadir}/pixmaps/
%{_datadir}/anaconda/pixmaps/

%changelog
%autochangelog
