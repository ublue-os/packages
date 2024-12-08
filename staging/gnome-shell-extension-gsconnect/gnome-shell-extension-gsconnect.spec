# Firefox doesn't provide arch-independent web extension directory, although
# GSConnect web extension is arch-independent
%global debug_package %{nil}

%global app_id org.gnome.Shell.Extensions.GSConnect

Name:           gnome-shell-extension-gsconnect
# renovate: datasource=github-releases depName=GSConnect/gnome-shell-extension-gsconnect
Version:        58
Release:        1%{?dist}
Summary:        KDE Connect implementation for GNOME Shell

License:        GPL-2.0-or-later
URL:            https://github.com/GSConnect/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        nautilus-gsconnect.metainfo.xml
Source2:        nemo-gsconnect.metainfo.xml
# Fix Firewalld path
Patch0:         %{name}-42-firewalld.patch

BuildRequires:  desktop-file-utils
BuildRequires:  firewalld-filesystem
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gtk4
BuildRequires:  libappstream-glib
BuildRequires:  meson
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(glib-2.0)
Requires:       firewalld-filesystem
Requires:       gnome-shell
# Needed for ssh-keygen
Requires:       openssh
# Needed for ssh-add
Requires:       openssh-clients
Requires:       openssl
Requires:       /usr/bin/ffmpeg
Requires(post): firewalld-filesystem
Recommends:     evolution-data-server
Recommends:     gsound
Recommends:     libcanberra-gtk3
Suggests:       (nautilus-gsconnect = %{version}-%{release} if nautilus)
Suggests:       (nemo-gsconnect = %{version}-%{release} if nemo)
Suggests:       webextension-gsconnect = %{version}-%{release}

%description
The KDE Connect project allows devices to securely share content such as
notifications and files as well as interactive features such as SMS messaging
and remote input. The KDE Connect team maintains cross-desktop, Android and
Sailfish applications as well as an interface for KDE Plasma.

GSConnect is a complete implementation of KDE Connect especially for GNOME Shell
with Nautilus, Chrome and Firefox integration. It is does not rely on the KDE
Connect desktop application and will not work with it installed.


%package -n nautilus-gsconnect
Summary:        Nautilus extension for GSConnect
Requires:       gobject-introspection
Requires:       nautilus-extensions
Requires:       nautilus-python
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description -n nautilus-gsconnect
The nautilus-gsconnect package provides a Nautilus context menu for sending
files to devices that are online, paired and have the "Share and receive" plugin
enabled.


%package -n nemo-gsconnect
Summary:        Nemo extension for GSConnect
Requires:       gobject-introspection
Requires:       nemo-extensions
Requires:       nemo-python
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description -n nemo-gsconnect
The nemo-gsconnect package provides a Nemo context menu for sending files to
devices that are online, paired and have the "Share and receive" plugin enabled.


%package -n webextension-gsconnect
Summary:        Web browser integration for GSConnect
Requires:       mozilla-filesystem
Requires:       %{name} = %{version}-%{release}

%description -n webextension-gsconnect
The webextension-gsconnect package allows Google Chrome/Chromium, Firefox,
Vivaldi, Opera (and other Browser Extension, Chrome Extension or WebExtensions
capable browsers) to interact with GSConnect, using the Share plugin to open
links in device browsers and the Telephony plugin to share links with contacts
by SMS.


%prep
%autosetup -p0


%build
%meson \
    -Dfirewalld=true \
    -Dinstalled_tests=false \
    -Dnemo=true
%meson_build


%install
%meson_install

# Install AppData files
install -Dpm 0644 %{SOURCE1} %{SOURCE2} -t $RPM_BUILD_ROOT%{_metainfodir}/

%find_lang %{app_id}


%check
desktop-file-validate \
    $RPM_BUILD_ROOT%{_datadir}/applications/%{app_id}.desktop \
    $RPM_BUILD_ROOT%{_datadir}/applications/%{app_id}.Preferences.desktop
appstream-util validate-relax --nonet \
    $RPM_BUILD_ROOT%{_metainfodir}/nautilus-gsconnect.metainfo.xml \
    $RPM_BUILD_ROOT%{_metainfodir}/nemo-gsconnect.metainfo.xml \
    $RPM_BUILD_ROOT%{_metainfodir}/%{app_id}.metainfo.xml


%post
%firewalld_reload


%files -f %{app_id}.lang
%doc CONTRIBUTING.md README.md
%license LICENSES/GPL-2.0-or-later.txt
%{_datadir}/gnome-shell/extensions/gsconnect@andyholmes.github.io/
%{_datadir}/applications/%{app_id}.desktop
%{_datadir}/applications/%{app_id}.Preferences.desktop
%{_datadir}/dbus-1/services/%{app_id}.service
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_prefix}/lib/firewalld/services/*.xml
%{_metainfodir}/%{app_id}.metainfo.xml


%files -n nautilus-gsconnect
%{_datadir}/nautilus-python/extensions/nautilus-gsconnect.py
%{_metainfodir}/nautilus-gsconnect.metainfo.xml


%files -n nemo-gsconnect
%{_datadir}/nemo-python/extensions/nemo-gsconnect.py
%{_metainfodir}/nemo-gsconnect.metainfo.xml


%files -n webextension-gsconnect
%{_libdir}/mozilla/native-messaging-hosts/
%{_sysconfdir}/chromium/
%{_sysconfdir}/opt/chrome/


%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 57-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Apr 19 2024 Mohamed El Morabity <melmorabity@fedoraproject.org> - 57-1
- Update to 57

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 56-1
- Update to 56

* Thu Oct 19 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 55^20231004git018c7fe-1
- Update to latest snapshot for GNOME 45 support

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 27 2023 Mohamed El Morabity <melmorabity@fedoraproject.org> - 55-1
- Update to 55

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 19 2022 Mohamed El Morabity <melmorabity@fedoraproject.org> - 54-1
- Update to 54

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Mar 20 2022 Mohamed El Morabity <melmorabity@fedoraproject.org> - 50-1
- Update to 50

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 48-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 03 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 48-1
- Update to 48

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 47-1
- Update to 47

* Mon Mar 29 2021 Mohamed El Morabity <melmorabity@fedoraproject.org> - 46-1
- Update to 46

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 44-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov  2 10:36:48 CET 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 44-1
- Update to 44

* Tue Sep 22 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 43-1
- Update to 43

* Sun Sep 20 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 42-1
- Update to 42

* Wed Aug 19 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 41-1
- Update to 41

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 39-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 39-1
- Update to 39

* Fri May 15 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 38-1
- Update to 38

* Fri Apr 17 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 37-1
- Update to 37

* Sat Mar 28 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 36-1
- Update to 36

* Tue Mar 24 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 35-1
- Update to 35

* Wed Mar 11 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 34-1
- Update to 34

* Wed Mar 04 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 33-1
- Update to 33

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 31-1
- Update to 31

* Mon Dec 02 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 30-1
- Update to 30

* Wed Oct 16 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 27-1
- Update to 27

* Tue Sep 10 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 26-1
- Update to 26

* Tue Sep 10 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 25-1
- Update to 25

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 24-1
- Update to 24

* Thu May 02 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 23-1
- Update to 23

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 21-2
- Rebuild with Meson fix for #1699099

* Mon Mar 18 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 21-1
- Update to 21

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 20-1
- Update to 20

* Tue Nov 27 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 16-1
- Initial RPM release
