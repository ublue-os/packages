Name:           ghostty
Version:        1.0.0
Release:        1%{?dist}
Summary:        👻 Ghostty is a fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration. 

License:        MIT
URL:            https://github.com/%{name}-org/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
ExclusiveArch:  x86_64

BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: glib2-devel
BuildRequires: gtk4-devel
BuildRequires: harfbuzz-devel
BuildRequires: libadwaita-devel
BuildRequires: libpng-devel
BuildRequires: oniguruma-devel
BuildRequires: pandoc-cli
BuildRequires: pixman-devel
BuildRequires: pkg-config
BuildRequires: zig
BuildRequires: zlib-ng-devel

Requires: fontconfig
Requires: freetype
Requires: glib2
Requires: gtk4
Requires: harfbuzz
Requires: libadwaita
Requires: libpng
Requires: oniguruma
Requires: pixman
Requires: zlib-ng

%description
%{summary}

%prep
%global debug_package %{nil}
%setup -q -n %{name}-%{version}

%build
ZIG_GLOBAL_CACHE_DIR=/tmp/offline-cache ./nix/build-support/fetch-zig-cache.sh

%define _zig_release_mode fast
%define _zig_cache_dir /tmp/offline-cache/p

%zig_build \
	-Doptimize=ReleaseFast \
	-Dpie=true \
	-Demit-docs

%install
%zig_install \
	-p %{buildroot} \
	-Doptimize=ReleaseFast \
	-Dpie=true \
	-Demit-docs
mv %{buildroot}/%{buildroot}/share %{buildroot}/usr/
mv %{buildroot}/share/g %{buildroot}/usr/share/terminfo/g
mv %{buildroot}/share/x %{buildroot}/usr/share/terminfo/x
rm -rf %{buildroot}/{home,share}

%check
%zig_test

%files
# Binary
%{_bindir}/%{name}
%license LICENSE
# Data
%dir %{_datadir}/%{name}
%doc %{_datadir}/%{name}/doc/%{name}*
# Shell Integrations
%{_datadir}/%{name}/shell-integration/bash/bash-preexec.sh
%{_datadir}/%{name}/shell-integration/bash/%{name}*
%{_datadir}/%{name}/shell-integration/elvish/lib/%{name}-integration.elv
%{_datadir}/%{name}/shell-integration/fish/vendor_conf.d/%{name}-shell-integration.fish
%{_datadir}/%{name}/shell-integration/zsh/%{name}-integration
%{_datadir}/%{name}/shell-integration/zsh/.zshenv
%dir %{_datadir}/%{name}/themes/
%{_datadir}/%{name}/themes/*
# Terminfo
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/%{name}.*
%{_datadir}/terminfo/x/xterm-%{name}
# Icons
%{_datadir}/icons/hicolor/128x128/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/128x128@2/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/16x16@2/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/256x256/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/256x256@2/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/32x32@2/apps/com.mitchellh.%{name}.png
%{_datadir}/icons/hicolor/512x512/apps/com.mitchellh.%{name}.png
# Desktop Entry
%{_datadir}/applications/com.mitchellh.%{name}.desktop
%{_datadir}/kio/servicemenus/com.mitchellh.%{name}.desktop
# Application Integrations
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
%{_datadir}/nvim/site/ftdetect/%{name}.vim
%{_datadir}/nvim/site/ftplugin/%{name}.vim
%{_datadir}/nvim/site/syntax/%{name}.vim
%{_datadir}/vim/vimfiles/ftdetect/%{name}.vim
%{_datadir}/vim/vimfiles/ftplugin/%{name}.vim
%{_datadir}/vim/vimfiles/syntax/%{name}.vim
# Shell Completions
%{bash_completions_dir}/%{name}*
%{fish_completions_dir}/%{name}*
%{zsh_completions_dir}/_%{name}
# Man Pages
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man5/%{name}.5.*

%changelog
* Sat Dec 28 2024 - m2Giles <69128853+m2Giles@users.noreply.github.com>
  - Initial Package
