Name:           gnome-rounded-blur
# renovate: datasource=github-tags depName=kancko/gnome-rounded-blur
Version:        1.0.1 
Release:        1%{?dist}
Summary:        Library providing Blur.Blur Effect with corner radius support

License:        GPL-3.0-or-later
URL:            https://github.com/kancko/gnome-rounded-blur 
Source0:        %{url}/archive/v%{version}.tar.gz
#This patch allows building on fedora 45/rawhide
#https://github.com/kancko/gnome-rounded-blur/pull/4
Patch0:         relax-dependency.patch

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  mutter-devel
Requires:       mutter >= 50
Recommends:     gnome-shell-extension-blur-my-shell

%description
A standalone library providing Blur.Blur Effect with corner radius support
for GNOME Shell extensions. It's basically just copy of ShellBlur Effect with
a corner mask and a different namespace (Blur).


%package devel
Summary:  Libraries and header files for file development
Requires: gnome-rounded-blur%{?_isa} = %{version}-%{release}

%description devel
The gnome-rounded-blur-devel package contains the
header files necessary for developing programs 
using gnome-rounded-blur-devel.

# Upstream hard-coded the build process on libmutter-18 (Gnome 50). As such, I have confirmed it works on Gnome 51, and am modifying the dependency check to allow libmutter-51
%prep
%autosetup
%conf
%meson

%build
%meson_build

%install
%meson_install


%files
%{_libdir}/girepository-1.0/Blur-1.0.typelib
%{_libdir}/libblur-effect-1.0.so.1
%{_libdir}/libblur-effect-1.0.so.1.0.0
%license LICENSE
%doc README.md

%files devel
%{_includedir}/blur-effect-1.0/rounded-blur-effect.h
%dir %{_includedir}/blur-effect-1.0
%{_libdir}/libblur-effect-1.0.so
%{_libdir}/pkgconfig/blur-effect-1.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Blur-1.0.gir
%doc README.md

%changelog
%autochangelog
