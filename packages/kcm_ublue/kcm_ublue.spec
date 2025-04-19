%global majmin_ver_kcm 0.5.8

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

BuildRequires:  cmake(GTest)
BuildRequires:  cmake(KF6Auth)
BuildRequires:  cmake(KF6Codecs)
BuildRequires:  cmake(KF6ColorScheme)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6Service)
BuildRequires:  cmake(KF6WidgetsAddons)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6Tools)

%description
KDE Configuration Module (KCM) for Aurora.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake
%cmake_build

%install
%cmake_install
install -Dm0755 system/usr/share/polkit-1/actions/org.ublue.rebase.policy %{buildroot}%{_datadir}/polkit-1/actions/org.ublue.rebase.policy
install -Dm0755 system/usr/share/polkit-1/rules.d/21-ublue-rebase.rules %{buildroot}%{_datadir}/polkit-1/rules.d/21-ublue-rebase.rules
install -Dm0755 system/usr/share/polkit-1/rules.d/22-ublue-rebase-systemd.rules %{buildroot}%{_datadir}/polkit-1/rules.d/22-ublue-rebase-systemd.rules
install -Dm0755 system/usr/lib/systemd/system/ublue-rebase@.service %{buildroot}%{_prefix}/lib/systemd/system/ublue-rebase@.service
install -Dm0755 system/usr/libexec/ublue-rebase %{buildroot}%{_libexecdir}/ublue-rebase

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
