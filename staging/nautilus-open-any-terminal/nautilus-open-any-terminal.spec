Name:           nautilus-open-any-terminal
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Context-menu entry for opening other terminal in nautilus
License:        GPLv3
URL:            https://github.com/KyleGospo/nautilus-open-any-terminal

VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  gettext

Requires:       nautilus-python
Requires:       glib2

%description
An extension for nautilus, which adds an context-entry for opening other terminal emulators than gnome-terminal.

%prep
{{{ git_dir_setup_macro }}}

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

%changelog
{{{ git_dir_changelog }}}
