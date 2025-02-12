%global majmin_ver_kcm 0.5.6

Name:           kcm_ublue
Version:        %{majmin_ver_kcm}
Release:        1%{?dist}
Summary:        KCM for KDE-based Universal Blue images

URL:            https://github.com/ledif/kcm_ublue
Source:         https://github.com/ledif/kcm_ublue/archive/refs/tags/v%{majmin_ver_kcm}.zip
License:        Apache-2.0

BuildRequires:  cmake
BuildRequires:  gcc-g++
BuildRequires:  extra-cmake-modules
BuildRequires:  kf6-kauth-devel
BuildRequires:  kf6-kcmutils-devel
BuildRequires:  kf6-kcodecs-devel
BuildRequires:  kf6-kcolorscheme-devel
BuildRequires:  kf6-kconfig-devel
BuildRequires:  kf6-kconfigwidgets-devel
BuildRequires:  kf6-kcoreaddons-devel
BuildRequires:  kf6-ki18n-devel
BuildRequires:  kf6-kservice-devel
BuildRequires:  kf6-kwidgetsaddons-devel
BuildRequires:  qt6-doc-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  gtest-devel

%description
KDE Configuration Module (KCM) for Aurora.

%prep
%autosetup -n %{name}-%{version}

%build
mkdir build
cmake -B build
cmake --build build

%install
install -Dm0755 ./build/bin/plasma/kcms/systemsettings/kcm_ublue.so %{buildroot}%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_ublue.so
install -Dm0755 ./system/usr/share/applications/kcm_ublue.desktop %{buildroot}%{_datadir}/applications/kcm_ublue.desktop
install -Dm0755 ./system/usr/share/polkit-1/actions/org.ublue.rebase.policy %{buildroot}%{_datadir}/polkit-1/actions/org.ublue.rebase.policy
install -Dm0755 ./system/usr/share/polkit-1/rules.d/21-ublue-rebase.rules %{buildroot}%{_datadir}/polkit-1/rules.d/21-ublue-rebase.rules
install -Dm0755 ./system/usr/share/polkit-1/rules.d/22-ublue-rebase-systemd.rules %{buildroot}%{_datadir}/polkit-1/rules.d/22-ublue-rebase-systemd.rules
install -Dm0755 ./system/usr/lib/systemd/system/ublue-rebase@.service %{buildroot}%{_prefix}/lib/systemd/system/ublue-rebase@.service
install -Dm0755 ./system/usr/libexec/ublue-rebase %{buildroot}%{_libexecdir}/ublue-rebase

%files
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_ublue.so
%{_datadir}/applications/kcm_ublue.desktop
%{_datadir}/polkit-1/actions/org.ublue.rebase.policy
%{_datadir}/polkit-1/rules.d/21-ublue-rebase.rules
%{_datadir}/polkit-1/rules.d/22-ublue-rebase-systemd.rules
%{_prefix}/lib/systemd/system/ublue-rebase@.service
%{_libexecdir}/ublue-rebase

%changelog
%autochangelog
