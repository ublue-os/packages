Name:           power-profiles-daemon
Version:        0.13
Release:        6%{?dist}.ublue
Summary:        Makes power profiles handling available over D-Bus

License:        GPL-3.0-or-later
URL:            https://gitlab.freedesktop.org/hadess/power-profiles-daemon
Source0:        https://gitlab.freedesktop.org/hadess/power-profiles-daemon/uploads/1f2ea40547b2af8d255875d7085211e5/power-profiles-daemon-0.13.tar.xz
Patch1:         0001-tests-Split-immutable-control-into-a-test-helper.patch
Patch2:         0002-Allow-both-CPU-and-platform-drivers-to-be-simultaneo.patch
Patch3:         0003-Update-integration-test-to-be-compatible-with-pm-pro.patch
Patch4:         0004-Disable-loading-amd-pstate-when-the-PM-profile-is-a-.patch
Patch5:         0005-Don-t-change-governor-for-amd-pstate-at-probe.patch


BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  gtk-doc
BuildRequires:  pkgconfig(udev)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(polkit-gobject-1)
BuildRequires:  systemd
BuildRequires:  umockdev
BuildRequires:  python3-dbusmock
BuildRequires:  systemd-rpm-macros

%description
%{summary}.

%package docs
Summary:        Documentation for %{name}
BuildArch:      noarch

%description docs
This package contains the documentation for %{name}.

%prep
%autosetup -N
%autopatch -p1

%build
%meson -Dgtk_doc=true
%meson_build

%install
%meson_install
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/power-profiles-daemon

%check
%meson_test

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%triggerpostun -- power-profiles-daemon < 0.10.1-2
if [ $1 -gt 1 ] && [ -x /usr/bin/systemctl ] ; then
    # Apply power-profiles-daemon.service preset on upgrades to F35 and F36 as
    # the preset was changed to enabled in F35.
    /usr/bin/systemctl --no-reload preset power-profiles-daemon.service || :
fi

%files
%license COPYING
%doc README.md
%{_bindir}/powerprofilesctl
%{_libexecdir}/%{name}
%{_unitdir}/%{name}.service
%{_datadir}/dbus-1/system.d/net.hadess.PowerProfiles.conf
%{_datadir}/dbus-1/system-services/net.hadess.PowerProfiles.service
%{_datadir}/polkit-1/actions/net.hadess.PowerProfiles.policy
%{_localstatedir}/lib/power-profiles-daemon

%files docs
%dir %{_datadir}/gtk-doc/
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/%{name}/

%changelog
%autochangelog
