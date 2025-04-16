%global extdir		caffeine@patapon.info
%global gschemadir	%{_datadir}/glib-2.0/schemas

Name:		gnome-shell-extension-caffeine
# renovate: datasource=github-releases depName=eonpatapon/gnome-shell-extension-caffeine versioning=semver-major
Version:	56
Release:	%autorelease
Summary:	Disable the screen saver and auto suspend in gnome shell

# Automatically converted from old format: GPLv2 - review is highly recommended.
License:	GPL-2.0-only
URL:		https://github.com/eonpatapon/gnome-shell-extension-caffeine
%if 0%{?shortcommit:1}
Source0:	https://github.com/eonpatapon/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
%else
Source0:	https://github.com/eonpatapon/%{name}/archive/v%{version}.tar.gz#/%{name}-v%{version}.tar.gz
%endif

BuildArch:	noarch

BuildRequires:	gettext
BuildRequires:	%{_bindir}/glib-compile-schemas

Requires:	gnome-shell-extension-common

%description
This extension allows the user to easily disable the screen saver and auto
suspend in gnome shell via an icon in the top bar. By default, this function
is also enabled if a full screen application is running, and can be configured
to disable gnome shell's night light as well.

%prep
%autosetup %{?commit:-n %{name}-%{commit}}

%build
./update-locale.sh
glib-compile-schemas --strict --targetdir=%{extdir}/schemas/ %{extdir}/schemas

%install
mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions
cp -ar %{extdir} %{buildroot}%{_datadir}/gnome-shell/extensions/%{extdir}

# Fedora and EPEL 8 handles post scripts via triggers
%if 0%{?rhel} && 0%{?rhel} <= 7
%postun
if [ $1 -eq 0 ] ; then
	%{_bindir}/glib-compile-schemas %{gschemadir} &> /dev/null || :
fi

%posttrans
%{_bindir}/glib-compile-schemas %{gschemadir} &> /dev/null || :
%endif

%files
%license COPYING
%{_datadir}/gnome-shell/extensions/%{extdir}

%changelog
%autochangelog
