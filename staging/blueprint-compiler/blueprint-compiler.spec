%global         forgeurl https://gitlab.gnome.org/jwestman/blueprint-compiler

Name:           blueprint-compiler
Version:        0.18.0
Release:        %autorelease
Summary:        A markup language for GTK user interfaces

%global         tag v%{version}
%forgemeta

License:        LGPL-3.0-or-later
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildArch:      noarch

BuildRequires:  meson
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  python3-devel
BuildRequires:  python3-gobject-devel

Requires:       python3-gobject-devel

%description
GtkBuilder XML format is quite verbose, and many app developers don't like
using WYSIWYG editors for creating UIs. Blueprint files are intended to be a
concise, easy-to-read format that makes it easier to create and edit GTK UIs.
Internally, it compiles to GtkBuilder XML as part of an app's build system. It
adds no new features, just makes the features that exist more accessible.
Another goal is to have excellent developer tooling--including a language
server--so that less knowledge of the format is required. Hopefully this will
increase adoption of cool advanced features like GtkExpression.


%prep
%forgeautosetup


%build
%meson
%meson_build


%install
%meson_install


# Tests fail in mock, but pass otherwise. For some reason, no log is available
# to debug the issue when it fails.
#check
#meson_test


%files
%license COPYING
%doc README.md docs/*.rst
%{_bindir}/%{name}
%{python3_sitelib}/blueprintcompiler
%{_datadir}/pkgconfig/%{name}.pc


%changelog
%autochangelog

