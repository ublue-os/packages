%global glib2_version 2.58
%global colord_version 1.4.5
%global geocode_glib_version 3.26.3
%global gnome_desktop_version 3.37.1
%global gsettings_desktop_schemas_version 46~beta
%global gtk3_version 3.15.3
%global geoclue_version 2.3.1

%ifnarch s390 s390x
%global wacom_unit org.gnome.SettingsDaemon.Wacom.service
%else
%global wacom_unit %{nil}
%endif
%global systemd_units org.gnome.SettingsDaemon.A11ySettings.service org.gnome.SettingsDaemon.Color.service org.gnome.SettingsDaemon.Datetime.service org.gnome.SettingsDaemon.Housekeeping.service org.gnome.SettingsDaemon.Keyboard.service org.gnome.SettingsDaemon.MediaKeys.service org.gnome.SettingsDaemon.Power.service org.gnome.SettingsDaemon.PrintNotifications.service org.gnome.SettingsDaemon.Rfkill.service org.gnome.SettingsDaemon.ScreensaverProxy.service org.gnome.SettingsDaemon.Sharing.service org.gnome.SettingsDaemon.Smartcard.service org.gnome.SettingsDaemon.Sound.service org.gnome.SettingsDaemon.UsbProtection.service org.gnome.SettingsDaemon.Wwan.service org.gnome.SettingsDaemon.XSettings.service %%{wacom_unit}

%global gnome_major_version 46
%global gnome_version %{gnome_major_version}.0

%global tarball_version %%(echo %{gnome_version} | tr '~' '.')
%global major_version %%(echo %{gnome_version} | cut -f 1 -d '~' | cut -f 1 -d '.')

Name:           gnome-settings-daemon
Version:        %{gnome_version}
Release:        %autorelease.xscaling.{{{ git_dir_version }}}
Summary:        The daemon sharing settings from GNOME to GTK+/KDE applications

License:        GPL-2.0-or-later AND LGPL-2.1-or-later
URL:            https://gitlab.gnome.org/GNOME/gnome-settings-daemon
Source0:        https://download.gnome.org/sources/%{name}/%{gnome_major_version}/%{name}-%{tarball_version}.tar.xz

# https://gitlab.gnome.org/GNOME/gnome-settings-daemon/-/merge_requests/353
Patch0:         353.patch

BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson >= 0.49.0
BuildRequires:  perl-interpreter
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(colord) >= %{colord_version}
BuildRequires:  pkgconfig(cups)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gck-2)
BuildRequires:  pkgconfig(gcr-4)
BuildRequires:  pkgconfig(geoclue-2.0) >= %{geoclue_version}
BuildRequires:  pkgconfig(geocode-glib-2.0) >= %{geocode_glib_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-desktop-3.0) >= %{gnome_desktop_version}
BuildRequires:  pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(gweather4)
BuildRequires:  pkgconfig(lcms2) >= 2.2
BuildRequires:  pkgconfig(libcanberra-gtk3)
BuildRequires:  pkgconfig(libgeoclue-2.0)
BuildRequires:  pkgconfig(libnm)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-mainloop-glib)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(mm-glib)
BuildRequires:  pkgconfig(nss)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(wayland-client)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(libwacom) >= 0.7
%endif

Requires: colord >= %{colord_version}
Requires: iio-sensor-proxy
Requires: geoclue2 >= %{geoclue_version}
Requires: geocode-glib2%{?_isa} >= %{geocode_glib_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gnome-desktop3%{?_isa} >= %{gnome_desktop_version}
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: libgweather4%{?_isa}

%description
A daemon to share settings from GNOME to other applications. It also
handles global keybindings, as well as a number of desktop-wide settings.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}

%build
%meson
%meson_build

%install
%meson_install

%find_lang %{name} --with-gnome

%post
%systemd_user_post %{systemd_units}

%preun
%systemd_user_preun %{systemd_units}

%files -f %{name}.lang
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README

# list daemons explicitly, so we notice if one goes missing
# some of these don't have a separate gschema
%{_libexecdir}/gsd-datetime
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Datetime.desktop

%{_libexecdir}/gsd-housekeeping
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Housekeeping.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.housekeeping.gschema.xml

%{_libexecdir}/gsd-keyboard
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Keyboard.desktop

%{_libexecdir}/gsd-media-keys
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.MediaKeys.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.media-keys.gschema.xml

%{_libexecdir}/gsd-backlight-helper
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.power.policy
%{_libexecdir}/gsd-power
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Power.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.power.gschema.xml

%{_libexecdir}/gsd-print-notifications
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.PrintNotifications.desktop
%{_libexecdir}/gsd-printer

%{_libexecdir}/gsd-rfkill
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Rfkill.desktop

%{_libexecdir}/gsd-screensaver-proxy
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.ScreensaverProxy.desktop

%{_libexecdir}/gsd-smartcard
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Smartcard.desktop

%{_libexecdir}/gsd-sound
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Sound.desktop

%{_libexecdir}/gsd-usb-protection
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.UsbProtection.desktop

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.peripherals.wacom.gschema.xml
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Wacom.desktop

%ifnarch s390 s390x
%{_libexecdir}/gsd-wacom
%{_libexecdir}/gsd-wacom-oled-helper
%{_datadir}/polkit-1/actions/org.gnome.settings-daemon.plugins.wacom.policy
%endif

%{_libexecdir}/gsd-xsettings
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.XSettings.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.xsettings.gschema.xml

%{_libexecdir}/gsd-a11y-settings
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.A11ySettings.desktop

%{_libexecdir}/gsd-color
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Color.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.color.gschema.xml

%{_libexecdir}/gsd-sharing
%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Sharing.desktop
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.sharing.gschema.xml

%{_sysconfdir}/xdg/autostart/org.gnome.SettingsDaemon.Wwan.desktop
%{_libexecdir}/gsd-wwan
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.wwan.gschema.xml

%dir %{_libdir}/gnome-settings-daemon-%{gnome_major_version}
%{_libdir}/gnome-settings-daemon-%{gnome_major_version}/libgsd.so

%{_sysconfdir}/xdg/Xwayland-session.d/00-xrdb
%{_userunitdir}/gnome-session-x11-services-ready.target.wants/
%{_userunitdir}/gnome-session-x11-services.target.wants/
%{lua: for service in string.gmatch(rpm.expand('%{systemd_units}'), "[^%s]+") do print(rpm.expand('%{_userunitdir}/')..service..'\n') end}
%{_userunitdir}/*.target
%{_udevrulesdir}/61-gnome-settings-daemon-rfkill.rules
%{_datadir}/gnome-settings-daemon/
%{_datadir}/GConf/gsettings/gnome-settings-daemon.convert

%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.settings-daemon.plugins.gschema.xml

%files devel
%{_includedir}/gnome-settings-daemon-%{gnome_major_version}
%{_libdir}/pkgconfig/gnome-settings-daemon.pc

%changelog
%autochangelog
