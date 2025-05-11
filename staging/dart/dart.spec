%define debug_package %{nil}

Name: dart
# renovate: datasource=dart-version
Version: 3.7.3
Release: 2%?dist
Summary: The Dart Language
License: BSD-3-Clause
URL: https://dart.dev/

%ifarch x86_64
%define arch x64
%elifarch aarch64
%define arch arm64
%endif

Source0: https://storage.googleapis.com/dart-archive/channels/stable/release/%{version}/sdk/dartsdk-linux-x64-release.zip
Source1: https://storage.googleapis.com/dart-archive/channels/stable/release/%{version}/sdk/dartsdk-linux-arm64-release.zip
BuildRequires: fdupes

%description
Dart is a client-optimized language for fast apps on any platform.
This package contains the SDK used to develop and compile Dart applications.

%prep
# This is nasty and terrible but I havent found any way to build the dart-sdk from source given a stable release archive
if [ "$(arch)" == "x86_64" ]; then
	unzip %{SOURCE0}
else
	unzip %{SOURCE1}
fi

%build

%install
# install the folders inside
install -vd %{buildroot}%{_bindir}
install -vd %{buildroot}%{_libdir}/dart

cp -rv ./dart-sdk %{buildroot}%{_libdir}/

ln -sf %{_libdir}/dart-sdk/bin/dart %{buildroot}%{_bindir}/dart
ln -sf %{_libdir}/dart-sdk/bin/dartaotruntime %{buildroot}%{_bindir}/dartaotruntime

%fdupes %buildroot%_libdir/dart/bin/

%files
%{_libdir}/dart-sdk/
%{_bindir}/dart
%{_bindir}/dartaotruntime


%changelog
* Thu Nov 17 2022 windowsboy111 <windowsboy111@fyralabs.com> - 2.18.4-1
- Bump

* Tue Oct 11 2022 Cappy Ishihara <cappy@cappuchino.xyz> - 2.18.2-1
- Repackaged dart for Terra
