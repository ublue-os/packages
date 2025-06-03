%global uuid logomenu@aryan_k

# renovate: datasource=git-refs depName=https://github.com/Aryan20/Logomenu versioning=loose currentValue=main
%global commit bbbc77836d1bb853f4bbaf683674c3bbae19cf66
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:          gnome-shell-extension-logo-menu
Version:       0.0.0
Release:       5%{gitrel}%{?dist}
Summary:       Quick access menu for the GNOME panel

Group:         User Interface/Desktops
License:       GPLv2
URL:           https://github.com/Aryan20/Logomenu

Source0:       %{url}/archive/%{commit}.tar.gz
Source1:       org.gnome.shell.extensions.logo-menu.gschema.xml
Source2:       ampere-logo-symbolic.svg
Source3:       framework-logo-symbolic.svg

BuildArch:     noarch

Patch0:        extension-boxbuddy.patch
Patch1:        logos-entries.patch

BuildRequires:  pkgconfig(glib-2.0)
Requires:    gnome-shell >= 3.12
Requires:    glib2

%description
Quick access menu for the GNOME panel with options that help ease the workflow for newcomers and power users alike. 

%prep
%autosetup -n Logomenu-%{commit}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/ *.js
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/ *.json
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/ *.css
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/schemas/ schemas/*.xml
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/schemas/ %{SOURCE1}
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/po/ po/*.po
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/Resources/ Resources/*.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/Resources %{SOURCE2}
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/Resources %{SOURCE3}
install -Dpm0644 -t %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/PrefsLib/ PrefsLib/*.js
glib-compile-schemas %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/schemas/

%files
%license LICENSE
%doc README.md
%{_datadir}/gnome-shell/extensions/%{uuid}/

%changelog
%autochangelog
