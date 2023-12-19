Name:           devpod
Version:        v0.4.2
Release:        1%{?dist}
Summary:        Codespaces but open-source, client-only and unopinionated.

License:        MPL-2.0
URL:            https://github.com/loft-sh/%{name}
Source0:        %{url}/releases/download/%{version}/DevPod_linux_x86_64.tar.gz
BuildArch:      x86_64

Requires:       cairo
Requires:       cairo-gobject
Requires:       dbus-libs
Requires:       gdk-pixbuf2
Requires:       glib2
Requires:       glibc
Requires:       gtk3
Requires:       gtk3-immodules
Requires:       javascriptcoregtk4.0
Requires:       libXdmcp
Requires:       libappindicator-gtk3
Requires:       libbsd
Requires:       libdeflate
Requires:       libgcc
Requires:       libwmf
Requires:       openssl1.1
Requires:       pango
Requires:       webkit2gtk4.0

%description
Codespaces but open-source, client-only and unopinionated: Works with any IDE and lets you use any cloud, kubernetes or just localhost docker.

%prep
%autosetup -c

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/
rm -rf usr/bin/xdg-open
rm -rf usr/share/glib-2.0
cp -rf usr/bin/* %{buildroot}%{_bindir}/
cp -rf usr/share/* %{buildroot}%{_datadir}/
rm -rf usr

%files
%{_bindir}/devpod-cli
%{_bindir}/dev-pod
%{_datadir}/icons/hicolor/256x256@2/apps/dev-pod.png
%{_datadir}/icons/hicolor/128x128/apps/dev-pod.png
%{_datadir}/icons/hicolor/32x32/apps/dev-pod.png
%{_datadir}/applications/dev-pod.desktop

%changelog
