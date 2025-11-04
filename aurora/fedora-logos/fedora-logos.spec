%global debug_package %{nil}
%global vendor aurora

Name:           fedora-logos
Version:        100.0.0
Release:        8%{?dist}
Summary:        Aurora branding

License:        CC-BY-SA
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Provides: fedora-logos
Provides: redhat-logos
Provides: gnome-logos
Provides: system-logos
Conflicts: fedora-logos
BuildArch:      noarch

%description
Branding for Aurora's anaconda

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ src/logos/*
install -Dpm0644 -t %{buildroot}%{_datadir}/anaconda/pixmaps/ src/anaconda/*
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ src/misc/*

%check

%files
%{_datadir}/pixmaps/
%{_datadir}/anaconda/pixmaps/

%changelog
%autochangelog
