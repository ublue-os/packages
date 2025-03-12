%global debug_package %{nil}
%global vendor bluefin

Name:           bluefin
Version:        0.1.9
Release:        1%{?dist}
Summary:        Bluefin branding

License:        CC-BY-CA
URL:            https://github.com/ublue-os/packages
VCS:           {{{ git_dir_vcs }}}
Source:        {{{ git_dir_pack }}}

%description
Branding for Bluefin-related projects

%prep
{{{ git_dir_setup_macro }}}

%install
mkdir -p -m0755 \
    %{buildroot}%{_datadir}/backgrounds/%{vendor} \
    %{buildroot}%{_datadir}/gnome-background-properties \
    %{buildroot}%{_datadir}/pixmaps/faces \
    %{buildroot}%{_datadir}/ublue-os/homebrew \
    %{buildroot}%{_sysconfdir}

mv wallpapers/gnome-background-properties/*.xml %{buildroot}%{_datadir}/gnome-background-properties
rm -rf wallpaper/gnome-background-properties
mv wallpapers/*.xml %{buildroot}%{_datadir}/backgrounds/%{vendor}
mv wallpapers/* %{buildroot}%{_datadir}/backgrounds/%{vendor}
mv faces %{buildroot}%{_datadir}/pixmaps/faces/bluefin
mv logos/* %{buildroot}%{_datadir}/pixmaps
mv cli-logos %{buildroot}%{_datadir}/ublue-os/bluefin-logos
mv fastfetch/fastfetch.jsonc %{buildroot}%{_datadir}/ublue-os/fastfetch.jsonc
mv schemas/dconf %{buildroot}%{_sysconfdir}
mv schemas/skel %{buildroot}%{_sysconfdir}
mv schemas/profile.d %{buildroot}%{_sysconfdir}
mv schemas/distrobox %{buildroot}%{_sysconfdir}
mv schemas/geoclue %{buildroot}%{_sysconfdir}
mv schemas/glib-2.0 %{buildroot}%{_datadir}
mv schemas/homebrew/* %{buildroot}%{_datadir}/ublue-os/homebrew
mv schemas/applications %{buildroot}%{_datadir}
mv plymouth %{buildroot}%{_datadir}

%package logos
Summary:        Logos for GNOME
License:        CC-BY-CA
Provides: fedora-logos
Provides: centos-logos
Provides: system-logos
Obsoletes: fedora-logos
Obsoletes: centos-logos
Obsoletes: system-logos

%description logos
Replacement logos for GNOME

%files logos
%attr(0755,root,root) %{_datadir}/pixmaps/fedora*
%attr(0755,root,root) %{_datadir}/pixmaps/system-*
%attr(0755,root,root) %{_datadir}/pixmaps/ublue-*

%package cli-logos
Summary:        Logos for CLI
License:        CC-BY-CA

%description cli-logos
Logos for CLI applications like Fastfetch

%files cli-logos
%attr(0755,root,root) %{_datadir}/ublue-os/bluefin-logos/*

%package fastfetch
Summary:        Fastfetch configuration for Bluefin
License:        CC-BY-CA

%description fastfetch
Fastfetch configuration for Bluefin

%files fastfetch
%attr(0755,root,root) %{_datadir}/ublue-os/fastfetch.jsonc

%package plymouth
Summary:        Plymouth customization for Bluefin
License:        CC-BY-CA

%description plymouth
Plymouth logo customization for Bluefin

%files plymouth
%attr(0755,root,root) %{_datadir}/plymouth

%package schemas
Summary:        GNOME Schemas for Bluefin

%description schemas
Contains all of the DConf settings that Bluefin ships by default

%files schemas
%attr(0755,root,root) %{_sysconfdir}/dconf/db
%attr(0755,root,root) %{_sysconfdir}/profile.d
%attr(0755,root,root) %{_sysconfdir}/geoclue
%attr(0755,root,root) %{_sysconfdir}/distrobox
%attr(0755,root,root) %{_sysconfdir}/skel
%attr(0755,root,root) %{_datadir}/glib-2.0
%attr(0755,root,root) %{_datadir}/applications
%attr(0755,root,root) %{_datadir}/ublue-os/homebrew/kubernetes.Brewfile
%attr(0755,root,root) %{_datadir}/ublue-os/homebrew/bluefin-cli.Brewfile

%package backgrounds
Summary:        Bluefin wallpapers
License:        CC-BY-CA

%description backgrounds
Wallpapers included on Bluefin by default

%files backgrounds
%attr(0755,root,root) %{_datadir}/backgrounds/%{vendor}/*
%attr(0755,root,root) %{_datadir}/gnome-background-properties/*.xml

%package faces
Summary:      Bluefin GNOME Faces
License:      CC-BY-CA

%description faces
GNOME profile pictures for Bluefin

%pre faces
rm -rf %{_datadir}/pixmaps/faces/*

%files faces
%attr(0755,root,root) %{_datadir}/pixmaps/faces/bluefin/*

%changelog
%autochangelog
