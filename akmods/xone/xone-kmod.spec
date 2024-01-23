%global commit0 af5e344fb0203738c5892e295aa4f7138889393d
%global date 20240116
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod

%global debug_package %{nil}

Name:           xone-kmod
Version:        0.3
Release:        4%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Linux kernel driver for Xbox One and Xbox Series X|S accessories
License:        GPLv2
URL:            https://github.com/medusalix/xone

%if 0%{?tag:1}
Source0:        %{url}/archive/v%{version}.tar.gz#/xone-%{version}.tar.gz
%else
Source0:        %{url}/archive/%{commit0}.tar.gz#/xone-%{shortcommit0}.tar.gz
%endif

# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Linux kernel driver for Xbox One and Xbox Series X|S accessories.

%prep
# Error out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%if 0%{?tag:1}
%autosetup -p1 -n xone-%{version}
%else
%autosetup -p1 -n xone-%{commit0}
%endif

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr bus driver transport Kbuild _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        %make_build -C "${kernel_version##*___}" M=$(pwd) VERSION="v%{version}" modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Wed Jan 17 2024 Simone Caronni <negativo17@gmail.com> - 0.3-4.20240116gitaf5e344
- Update to latest snapshot.

* Wed Nov 15 2023 Simone Caronni <negativo17@gmail.com> - 0.3-3.20230517gitbbf0dcc
- Drop custom signing and compressing in favour of kmodtool.

* Sun Jun 04 2023 Simone Caronni <negativo17@gmail.com> - 0.3-2.20230517gitbbf0dcc
- Update to latest commits.

* Tue Aug 9 2022 Simone Caronni <negativo17@gmail.com> - 0.3-1
- First build.
