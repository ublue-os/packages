Name:           prompt
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Prompt is a terminal for GNOME with first-class support for containers.

License:        GPLv3
URL:            https://gitlab.gnome.org/chergert/prompt
Source:         %{url}/-/archive/main/prompt-main.tar.gz

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(vte-2.91-gtk4)
BuildRequires:  pkgconfig(libportal-gtk4)
BuildRequires:  pkgconfig(json-glib-1.0)

%description
Prompt is a terminal for GNOME with first-class support for containers.

%prep
%autosetup -n prompt-main

%build
%meson \
	-Ddebug=false
%meson_build

%install
%meson_install

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/%{name}-agent
%{_datadir}/applications/org.gnome.Prompt.desktop
%{_datadir}/dbus-1/services/org.gnome.Prompt.service
%{_datadir}/glib-2.0/schemas/org.gnome.Prompt.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Prompt*.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Prompt*.svg
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_datadir}/metainfo/org.gnome.Prompt.metainfo.xml