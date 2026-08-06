%global debug_package %{nil}
# See: https://src.fedoraproject.org/rpms/yad/blob/rawhide/f/yad.spec

Name:           yad
# renovate: datasource=github-releases depName=v1cont/yad
Version:        14.1
Release:        1%{?dist}
Summary:        Display graphical dialogs from shell scripts or command line

License:        GPL-3.0-or-later
URL:            https://github.com/v1cont/%{name}
Source0:        https://github.com/v1cont/%{name}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  make
BuildRequires:  automake
BuildRequires:  intltool
BuildRequires:  gtk3-devel >= 3.22.0
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  desktop-file-utils
BuildRequires:  perl(XML::Parser)
BuildRequires:  intltool >= 0.40.0
BuildRequires:  pkgconfig
BuildRequires:  gettext
BuildRequires:  gtksourceview3-devel
BuildRequires:  gspell-devel

BuildRequires:  gcc


%description
Yad (yet another dialog) is a fork of zenity with many improvements, such as
custom buttons, additional dialogs, pop-up menu in notification icon and more.


%prep
%setup -q


%build
autoreconf -ivf && intltoolize

%configure --enable-standalone

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}

rm -f %{buildroot}%{_bindir}/pfd

%find_lang %{name}

# Encoding key in group "Desktop Entry" is deprecated.
# Place the menu entry for yad-icon-browser under "Utilities".
desktop-file-install --remove-key Encoding     \
    --remove-category Development              \
    --add-category    Utility                  \
    --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/%{name}-icon-browser.desktop


%post
update-desktop-database %{_datadir}/applications &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
update-desktop-database %{_datadir}/applications &>/dev/null || :
if [ $1 -eq 0 ] ; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc README.md AUTHORS NEWS THANKS TODO
%license COPYING
%{_bindir}/*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/*.desktop
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/*/*


%changelog
%autochangelog
