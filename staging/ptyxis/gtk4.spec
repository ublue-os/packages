%if 0%{?fedora}
%global with_broadway 1
%endif

%global glib2_version 2.76.0
%global pango_version 1.50.0
%global cairo_version 1.14.0
%global gdk_pixbuf_version 2.30.0
%global wayland_protocols_version 1.31
%global wayland_version 1.21.0
%global epoxy_version 1.4

%global bin_version 4.0.0

# Filter provides for private modules
%global __provides_exclude_from ^%{_libdir}/gtk-4.0

# FTBFS on i686 with GCC 14 -Werror=int-conversion
# https://gitlab.gnome.org/GNOME/gtk/-/issues/6033
%if 0%{?fedora} >= 40 || 0%{?rhel} >= 10
%ifarch %{ix86}
%global build_type_safety_c 1
%endif
%endif

Name:           gtk4
Version:        4.14.1
Release:        %autorelease
Summary:        GTK graphical user interface library

License:        LGPL-2.0-or-later
URL:            https://www.gtk.org
Source0:        https://download.gnome.org/sources/gtk/4.14/gtk-%{version}.tar.xz

BuildRequires:  cups-devel
BuildRequires:  desktop-file-utils
BuildRequires:  docbook-style-xsl
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  glslc
BuildRequires:  meson
BuildRequires:  python3-gobject
BuildRequires:  pkgconfig(avahi-gobject)
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
BuildRequires:  pkgconfig(cairo-gobject) >= %{cairo_version}
BuildRequires:  pkgconfig(colord)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= %{gdk_pixbuf_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(graphene-gobject-1.0)
BuildRequires:  pkgconfig(gstreamer-player-1.0)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(pango) >= %{pango_version}
BuildRequires:  pkgconfig(sysprof-capture-4)
BuildRequires:  pkgconfig(tracker-sparql-3.0)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-client) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-cursor) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-egl) >= %{wayland_version}
BuildRequires:  pkgconfig(wayland-protocols) >= %{wayland_protocols_version}
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/rst2man

# standard icons
Requires: adwaita-icon-theme
# required for icon theme apis to work
Requires: hicolor-icon-theme
# split out in a subpackage
Requires: gtk-update-icon-cache

Requires: cairo%{?_isa} >= %{cairo_version}
Requires: cairo-gobject%{?_isa} >= %{cairo_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: libepoxy%{?_isa} >= %{epoxy_version}
Requires: libwayland-client%{?_isa} >= %{wayland_version}
Requires: libwayland-cursor%{?_isa} >= %{wayland_version}
Requires: pango%{?_isa} >= %{pango_version}

# required to support all the different image formats
Requires: gdk-pixbuf2-modules%{?_isa}

# make sure we have a reasonable gsettings backend
Recommends: dconf%{?_isa}

%description
GTK is a multi-platform toolkit for creating graphical user
interfaces. Offering a complete set of widgets, GTK is suitable for
projects ranging from small one-off tools to complete application
suites.

This package contains version 4 of GTK.

%package devel
Summary: Development files for GTK
Requires: gtk4%{?_isa} = %{version}-%{release}

%description devel
This package contains the libraries and header files that are needed
for writing applications with version 4 of the GTK widget toolkit.

%package devel-docs
Summary: Developer documentation for GTK
BuildArch: noarch
Requires: gtk4 = %{version}-%{release}
# Because web fonts from upstream are not bundled in the gi-docgen package,
# packages containing documentation generated with gi-docgen should depend on
# this metapackage to ensure the proper system fonts are present.
Recommends: gi-docgen-fonts

%description devel-docs
This package contains developer documentation for version 4 of the GTK
widget toolkit.

%package devel-tools
Summary: Developer tools for GTK
Requires: gtk4%{?_isa} = %{version}-%{release}

%description devel-tools
This package contains helpful applications for developers using GTK.

%prep
%autosetup -p1 -n gtk-%{version}

%build
export CFLAGS='-fno-strict-aliasing -DG_DISABLE_CAST_CHECKS -DG_DISABLE_ASSERT %optflags'
%meson \
%if 0%{?with_broadway}
        -Dbroadway-backend=true \
%endif
        -Dsysprof=enabled \
        -Dtracker=enabled \
        -Dcolord=enabled \
        -Dgtk_doc=true \
        -Dman-pages=true

%meson_build

%install
%meson_install

%find_lang gtk40

%if !0%{?with_broadway}
rm $RPM_BUILD_ROOT%{_mandir}/man1/gtk4-broadwayd.1*
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/gtk-4.0
mkdir -p $RPM_BUILD_ROOT%{_libdir}/gtk-4.0/modules

%check
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_metainfodir}/*.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

%files -f gtk40.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/gtk4-launch
%{_bindir}/gtk4-update-icon-cache
%{_libdir}/libgtk-4.so.1*
%dir %{_libdir}/gtk-4.0
%dir %{_libdir}/gtk-4.0/%{bin_version}
%{_libdir}/gtk-4.0/%{bin_version}/media/
%{_libdir}/gtk-4.0/%{bin_version}/printbackends/
%{_libdir}/gtk-4.0/modules
%{_libdir}/girepository-1.0/
%{_mandir}/man1/gtk4-launch.1*
%{_mandir}/man1/gtk4-update-icon-cache.1*
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.ColorChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.Debug.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.EmojiChooser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gtk.gtk4.Settings.FileChooser.gschema.xml
%dir %{_datadir}/gtk-4.0
%{_datadir}/gtk-4.0/emoji/
%if 0%{?with_broadway}
%{_bindir}/gtk4-broadwayd
%{_mandir}/man1/gtk4-broadwayd.1*
%endif

%files devel
%{_libdir}/libgtk-4.so
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_bindir}/gtk4-builder-tool
%{_bindir}/gtk4-encode-symbolic-svg
%{_bindir}/gtk4-path-tool
%{_bindir}/gtk4-query-settings
%{_datadir}/gettext/
%{_datadir}/gir-1.0/
%{_datadir}/gtk-4.0/gtk4builder.rng
%{_datadir}/gtk-4.0/valgrind/
%{_mandir}/man1/gtk4-builder-tool.1*
%{_mandir}/man1/gtk4-encode-symbolic-svg.1*
%{_mandir}/man1/gtk4-path-tool.1*
%{_mandir}/man1/gtk4-query-settings.1*

%files devel-docs
%{_datadir}/doc/gdk4/
%{_datadir}/doc/gdk4-wayland/
%{_datadir}/doc/gdk4-x11/
%{_datadir}/doc/gsk4/
%{_datadir}/doc/gtk4/

%files devel-tools
%{_bindir}/gtk4-demo
%{_bindir}/gtk4-demo-application
%{_bindir}/gtk4-icon-browser
%{_bindir}/gtk4-node-editor
%{_bindir}/gtk4-print-editor
%{_bindir}/gtk4-rendernode-tool
%{_bindir}/gtk4-widget-factory
%{_datadir}/applications/org.gtk.gtk4.NodeEditor.desktop
%{_datadir}/applications/org.gtk.Demo4.desktop
%{_datadir}/applications/org.gtk.IconBrowser4.desktop
%{_datadir}/applications/org.gtk.PrintEditor4.desktop
%{_datadir}/applications/org.gtk.WidgetFactory4.desktop
%{_datadir}/icons/hicolor/*/apps/org.gtk.gtk4.NodeEditor*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.Demo4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.IconBrowser4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.PrintEditor4*.svg
%{_datadir}/icons/hicolor/*/apps/org.gtk.WidgetFactory4*.svg
%{_datadir}/glib-2.0/schemas/org.gtk.Demo4.gschema.xml
%{_metainfodir}/org.gtk.gtk4.NodeEditor.appdata.xml
%{_metainfodir}/org.gtk.Demo4.appdata.xml
%{_metainfodir}/org.gtk.IconBrowser4.appdata.xml
%{_metainfodir}/org.gtk.PrintEditor4.appdata.xml
%{_metainfodir}/org.gtk.WidgetFactory4.appdata.xml
%{_mandir}/man1/gtk4-demo.1*
%{_mandir}/man1/gtk4-demo-application.1*
%{_mandir}/man1/gtk4-icon-browser.1*
%{_mandir}/man1/gtk4-node-editor.1*
%{_mandir}/man1/gtk4-rendernode-tool.1*
%{_mandir}/man1/gtk4-widget-factory.1*

%changelog
%autochangelog
