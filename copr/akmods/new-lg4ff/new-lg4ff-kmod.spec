%global buildforkernels akmod
%global debug_package %{nil}

%global prjname new-lg4ff

Name:           %{prjname}-kmod
Summary:        Improved Linux module driver for Logitech driving wheels.
Version:        0.4.0
Release:        1%{?dist}
License:        GPL-2.0-only

URL:            https://github.com/berarma/new-lg4ff
Source0:        %{url}/archive/%{version}/%{prjname}-%{version}.tar.gz

BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Improved Linux module driver for Logitech driving wheels.

This package contains the kmod module for %{prjname}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{prjname} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c %{name}-%{version}

for kernel_version  in %{?kernel_versions} ; do
    cp -a %{prjname}-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -D -m 755 _kmod_build_${kernel_version%%___*}/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
