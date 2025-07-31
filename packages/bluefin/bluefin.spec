%global debug_package %{nil}
%global vendor bluefin

Name:           bluefin
Version:        0.3.19
Release:        1%{?dist}
Summary:        Bluefin branding

License:        CC-BY-CA
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch

%description
Branding for Bluefin-related projects

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/bluefin-logos/sixels/ cli-logos/sixels/*
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/bluefin-logos/symbols/ cli-logos/symbols/*
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/bluefin-logos/ cli-logos/logos/*
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/dconf/db/distro.d/ schemas%{_sysconfdir}/dconf/db/distro.d/*-*
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/dconf/db/distro.d/locks/ schemas%{_sysconfdir}/dconf/db/distro.d/locks/*
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ logos/*
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-background-properties/ wallpapers/gnome-background-properties/*.xml
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/ wallpapers/images/*.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/ wallpapers/images/*.xml
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/faces/bluefin/ faces/*
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/ fastfetch/fastfetch.jsonc
install -Dpm0644 -t %{buildroot}%{_datadir}/plymouth/themes/spinner/ plymouth/themes/spinner/*.png
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/skel/.config/toolbox/ schemas%{_sysconfdir}/skel/.config/toolbox/*
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/xdg schemas%{_sysconfdir}/xdg/*
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/profile.d/ schemas%{_sysconfdir}/profile.d/*.sh
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/skel/.local/share/flatpak/overrides/ schemas%{_sysconfdir}/skel/.local/share/flatpak/overrides/*
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/skel/.local/share/org.gnome.Ptyxis/palettes/ schemas%{_sysconfdir}/skel/.local/share/org.gnome.Ptyxis/palettes/*
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/skel/.var/app/io.github.dvlv.boxbuddyrs/config/glib-2.0/settings/ schemas%{_sysconfdir}/skel/.var/app/io.github.dvlv.boxbuddyrs/config/glib-2.0/settings/keyfile
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/geoclue/conf.d/ schemas%{_sysconfdir}/geoclue/conf.d/99-beacondb.conf
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/homebrew/ schemas%{_datadir}/ublue-os/homebrew/*.Brewfile
install -Dpm0644 -t %{buildroot}%{_datadir}/glib-2.0/schemas/ schemas%{_datadir}/glib-2.0/schemas/zz0-bluefin-modifications.gschema.override
install -Dpm0644 -t %{buildroot}%{_datadir}/applications/ schemas%{_datadir}/applications/*.desktop
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/gnome-initial-setup/ schemas%{_sysconfdir}/gnome-initial-setup/vendor.conf
%if ((0%{?fedora} && 0%{?fedora} < 43) || 0%{?rhel})
install -Dpm0644 -t %{buildroot}%{_datadir}/pipewire/pipewire.conf.d/ schemas%{_datadir}/pipewire/pipewire.conf.d/raop.conf
%endif

%check

%package logos
Summary:        Logos for GNOME
Version:        0.2.2
License:        CC-BY-CA
Provides: fedora-logos
Provides: centos-logos
Provides: system-logos
Conflicts: aurora-logos
Conflicts: centos-logos
Conflicts: system-logos
Conflicts: fedora-logos

%description logos
Replacement logos for GNOME


%files logos
%{_datadir}/pixmaps/fedora*
%{_datadir}/pixmaps/system-*
%{_datadir}/pixmaps/ublue-*


%package cli-logos
Version:        0.2.1
Summary:        Logos for CLI
License:        CC-BY-CA

%description cli-logos
Logos for CLI applications like Fastfetch

%files cli-logos
%{_datadir}/ublue-os/bluefin-logos/*


%package fastfetch
Summary:        Fastfetch configuration for Bluefin
Version:        0.2.3
License:        CC-BY-CA

%description fastfetch
Fastfetch configuration for Bluefin

%files fastfetch
%{_datadir}/ublue-os/fastfetch.jsonc


%package plymouth
Summary:        Plymouth customization for Bluefin
Version:        0.2.1
License:        CC-BY-CA

%description plymouth
Plymouth logo customization for Bluefin

%files plymouth
%{_datadir}/plymouth


%package schemas
Version:        0.2.11
Summary:        GNOME Schemas for Bluefin

%description schemas
Contains all of the DConf settings that Bluefin ships by default

%files schemas
%{_sysconfdir}/dconf/db
%{_sysconfdir}/profile.d
%{_sysconfdir}/gnome-initial-setup
%{_sysconfdir}/geoclue
%{_sysconfdir}/skel
%{_sysconfdir}/xdg
%{_datadir}/glib-2.0
%{_datadir}/applications
%{_datadir}/ublue-os/homebrew/*.Brewfile
%if ((0%{?fedora} && 0%{?fedora} < 43) || 0%{?rhel})
%{_datadir}/pipewire/pipewire.conf.d/raop.conf
%endif


%package backgrounds
Summary:        Bluefin wallpapers
Version:        0.2.6
License:        CC-BY-CA

%description backgrounds
Wallpapers included on Bluefin by default

%files backgrounds
%{_datadir}/backgrounds/%{vendor}/*
%{_datadir}/gnome-background-properties/*.xml


%package faces
Summary:      Bluefin GNOME Faces
Version:      0.2.1
License:      CC-BY-CA

%description faces
GNOME profile pictures for Bluefin

%files faces
%{_datadir}/pixmaps/faces/bluefin/*


%changelog
%autochangelog
