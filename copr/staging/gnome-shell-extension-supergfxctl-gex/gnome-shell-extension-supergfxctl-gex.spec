%global extdir %{_datadir}/gnome-shell/extensions/supergfxctl-gex@asus-linux.org

Name:           gnome-shell-extension-supergfxctl-gex
Version:        33
Release:        2%{?dist}
Summary:        Extension for visualizing supergfxctl settings and status.

License:        MIT
URL:            https://extensions.gnome.org/extension/5344/supergfxctl-gex
Source0:        https://extensions.gnome.org/extension-data/supergfxctl-gexasus-linux.org.v%{version}.shell-extension.zip
BuildArch:      noarch

Requires:       gnome-shell-extension-common
Requires:       dconf-editor
Requires:       dconf
Requires:       supergfxctl

%description
Extension for visualizing supergfxctl settings and status.

%install
mkdir -p %{buildroot}%{extdir}
unzip %{SOURCE0} -d %{buildroot}%{extdir}

%files
%{extdir}

%changelog
