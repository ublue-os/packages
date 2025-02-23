Name:           nautilus-open-any-terminal
Version:        0.4.0
Release:        1%{?dist}
Summary:        Context-menu entry for opening other terminal in nautilus
License:        GPLv3
URL:            https://github.com/Stunkymonkey/nautilus-open-any-terminal

Source:         %{url}/archive/refs/tags/%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  gettext

Requires:       nautilus-python
Requires:       glib2

%description
An extension for nautilus, which adds an context-entry for opening other terminal emulators than gnome-terminal.

%prep
%autosetup -n %{name}-%{version}

%build
%{python3} setup.py build

%install
%{python3} setup.py install --root="%{buildroot}" --optimize=1

%post
glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null || :

%files
%license LICENSE
%doc README.md
%{python3_sitelib}/nautilus_open_any_terminal*
%{_datadir}/glib-2.0/schemas/com.github.stunkymonkey.%{name}.gschema.xml
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_datadir}/nautilus-python/extensions/open_any_terminal_extension.py
