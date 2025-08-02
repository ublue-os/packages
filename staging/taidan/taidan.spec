# renovate: datasource=git-refs depName=https://github.com/Ultramarine-Linux/taidan versioning=loose currentValue=master
%global commit b951808e55f0935fab774e33563ca1e37805b80b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           taidan
Version:        %shortcommit
Release:        1%?dist
Summary:        Out-Of-Box-Experience (OOBE) and Welcome App
SourceLicense:  GPL-3.0-or-later AND GPL-2.0-or-later
License:        (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND MIT AND (MIT OR Apache-2.0) AND (MIT OR Zlib OR Apache-2.0) AND Unicode-3.0 AND (Unlicense OR MIT) AND Zlib AND GPL-3.0-or-later AND GPL-2.0-or-later
URL:            https://github.com/Ultramarine-Linux/taidan
Source0:        %url/archive/%commit.tar.gz
Requires:       (glib2 or (/usr/bin/plasma-apply-colorscheme and kf6-kconfig))
Requires:       shadow-utils
Requires:       systemd-udev
Requires:       bash
Requires:       (dnf5 and dnf5-command(copr))
Requires:       flatpak
Requires:       libwebp
Requires:       webp-pixbuf-loader
Requires:       xhost
# Requires:       labwc
Requires:       cage
# Requires:       swaybg
Requires:       nm-connection-editor
BuildRequires:  mold cargo rust-packaging perl systemd-rpm-macros
BuildRequires:  pkgconfig(libhelium-1)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  clang-libs
BuildRequires:  clang-devel
BuildRequires:  libicu-devel
BuildRequires:  pkgconfig(libacl)
BuildRequires:  pkgconfig(libattr)

%description
Taidan is a GUI Out-Of-Box-Experience (OOBE) and Welcome App for Ultramarine
Linux, written in Rust and the Helium toolkit.

%prep
%autosetup -n taidan-%commit
cargo vendor -v vendor

%build
cargo build --release

%install
install -Dm0755 -t %{buildroot}/%{_bindir} ./target/release/taidan
DESTDIR=%buildroot ./scripts/install.sh

%files
%doc README.md
%license LICENSE.md
%_bindir/taidan
%_libexecdir/start-taidan
%_datadir/polkit-1/rules.d/100-taidan.rules
%_presetdir/95-taidan.preset
%_sysconfdir/com.fyralabs.Taidan/
%_sysconfdir/pam.d/taidan
%_sysusersdir/taidan.conf
%_unitdir/taidan-initial-setup.service
%_unitdir/taidan-initial-setup-reconfiguration.service
%dir %_prefix/lib/taidan/
%_prefix/lib/taidan/labwc/*
