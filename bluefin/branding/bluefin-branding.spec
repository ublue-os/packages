%global debug_package %{nil}
%global vendor bluefin

Name:           bluefin
Version:        0.1.0
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
    %{buildroot}%{_datadir}/pixmaps \
    %{buildroot}%{_datadir}/ublue-os \
    %{buildroot}%{_sysconfdir}

mv wallpapers/*.xml %{buildroot}%{_datadir}/gnome-background-properties
mv wallpapers/* %{buildroot}%{_datadir}/backgrounds/%{vendor}
mv faces %{buildroot}%{_datadir}/pixmaps
mv logos/* %{buildroot}%{_datadir}/pixmaps
mv cli-logos %{buildroot}%{_datadir}/ublue-os/bluefin-logos
mv schemas/dconf %{buildroot}%{_sysconfdir}
mv schemas/glib-2.0 %{buildroot}%{_datadir}

%package logos
Summary:        Logos for GNOME
License:        CC-BY-CA

%description logos
Replacement logos for GNOME

%files logos
%attr(0755,root,root) %{_datadir}/pixmaps/fedora*
%attr(0755,root,root) %{_datadir}/pixmaps/system-*

%package cli-logos
Summary:        Logos for CLI
License:        CC-BY-CA

%description cli-logos
Logos for CLI applications like Fastfetch

%files cli-logos
%attr(0755,root,root) %{_datadir}/ublue-os/bluefin-logos/*

%package schemas
Summary:        GNOME Schemas for Bluefin

%description schemas
Contains all of the DConf settings that Bluefin ships by default

%files schemas
%attr(0755,root,root) %{_sysconfdir}/dconf/db
%attr(0755,root,root) %{_datadir}/glib-2.0

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
License:        CC-BY-CA

%description faces
GNOME profile pictures for Bluefin

%files faces
%attr(0755,root,root) %{_datadir}/pixmaps/faces/*

%changelog
%autochangelog
