# renovate: datasource=git-refs depName=https://github.com/fyralabs/readymade versioning=loose currentValue=main
%global commit fbb329b160154a444998d5c6a669ca38db8ff908
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           readymade-nightly
Version:        %shortcommit
Release:        1%?dist
Summary:        Install ready-made distribution images!
License:        GPL-3.0-or-later
URL:            https://github.com/FyraLabs/readymade
Source0:        %url/archive/%commit.tar.gz
BuildRequires:  rust-packaging mold
BuildRequires:  pkgconfig(libhelium-1)
BuildRequires:  pkgconfig(gnome-desktop-4)
BuildRequires:  clang-devel
BuildRequires:  cmake
Conflicts:      readymade

Requires:  efibootmgr

%description
Readymade is a simple Linux Distribution installer.

It is created as a replacement to Red Hat's Anaconda installer.


%package config-ultramarine
Summary:        Readymade Configuration for Ultramarine Linux
Requires:       readymade-nightly
Provides:       readymade-nightly-config
Conflicts:      readymade-config-ultramarine

%description config-ultramarine
This package contains the configuration files for Readymade to install Ultramarine Linux.


%prep
%autosetup -n readymade-%commit
cargo vendor -v vendor

%build

%install
cargo build --release
install -Dm0755 -t %{buildroot}/%{_bindir} ./target/release/readymade
./install.sh %buildroot
ln -sf %{_datadir}/applications/com.fyralabs.Readymade.desktop %{buildroot}%{_datadir}/applications/liveinst.desktop


%files config-ultramarine
%_sysconfdir/readymade.toml


%files
%license LICENSE
%_bindir/readymade
%_datadir/polkit-1/actions/com.fyralabs.pkexec.readymade.policy
%_datadir/applications/com.fyralabs.Readymade.desktop
%_datadir/applications/liveinst.desktop
%ghost %_datadir/readymade
%_datadir/icons/hicolor/scalable/apps/com.fyralabs.Readymade.svg


