%global uuid search-light@icedman.github.com

# renovate: datasource=github-releases depName=icedman/search-light
%global commit      e7a351121706343abe7a164b625a55e245c16ab5
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .git%{shortcommit}

Name:        gnome-shell-extension-search-light
Version:     0.0.0
Release:     3%{gitrel}%{?dist}
Summary:     Take the apps search out of overview

Group:       User Interface/Desktops
License:     GPLv3
URL:         https://github.com/icedman/search-light
Source0:     %{url}/archive/%{commit}.tar.gz
BuildArch:   noarch

# Patch Upstream https://github.com/icedman/search-light/pull/116
Patch0:      7193320dde849a06c3cee04f42450efb3c192874.patch

BuildRequires:  pkgconfig(glib-2.0)
Requires:    gnome-shell >= 3.12
Requires:    glib2

BuildRequires: make

%description
This is a Gnome Shell extension that takes the apps search widget out of Overview. Like the macOS spotlight, or Alfred.

%prep
%autosetup -n search-light-%{commit} -N

%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10
%patch -P 0 -p1
%endif


%build
make build

%install
make publish
mkdir -p %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}
unzip -q %{uuid}.zip -d %{buildroot}%{_datadir}/gnome-shell/extensions/%{uuid}/

%files
%doc README.md
%license LICENSE
%{_datadir}/gnome-shell/extensions/%{uuid}/

%changelog
%autochangelog
