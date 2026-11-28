# SPDX-License-Identifier: GPL-2.0-only

%global buildforkernels akmod
%global debug_package %{nil}

%global kmod_name gc570d
%global upstream_name OpenGC570D

Name:           %{kmod_name}-kmod
# renovate: datasource=github-releases depName=neoyagami/OpenGC570D
Version:        1.0.5
Release:        1%{?dist}
Summary:        Linux kernel module for the AVerMedia Live Gamer DUO GC570D
License:        GPL-2.0-only
URL:            https://github.com/neoyagami/OpenGC570D
Source0:        %{url}/archive/refs/tags/v%{version}/%{upstream_name}-%{version}.tar.gz

ExclusiveArch:  x86_64
BuildRequires:  kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{kmod_name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Experimental Linux driver for the AVerMedia Live Gamer DUO GC570D PCIe
capture card (PCI 1461:0054, subsystem 1461:5700).

This package contains the %{kmod_name} kernel module.

%prep
%{?kmodtool_check}

%autosetup -c %{name}-%{version}

for kernel_version in %{?kernel_versions}; do
    cp -a %{upstream_name}-%{version} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    make V=1 %{?_smp_mflags} \
        GC570D_DEVELOPER_DEBUGFS=0 \
        -C ${kernel_version##*___} \
        M=${PWD}/_kmod_build_${kernel_version%%___*} \
        modules
done

%check
test -f %{upstream_name}-%{version}/Makefile
test -f %{upstream_name}-%{version}/src/gc570d-main.c
test -f %{upstream_name}-%{version}/data/gc570d_no_signal_640x360.inc

%install
for kernel_version in %{?kernel_versions}; do
    install -D -m 0755 \
        _kmod_build_${kernel_version%%___*}/%{kmod_name}.ko \
        %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{kmod_name}.ko
done

%{?akmod_install}

%changelog
* Sat Oct 24 2026 neoyagami <neoyagami@gmail.com> - 1.0.5-1
- Add the initial Universal Blue AKMOD package
- Disable the development debugfs interface in distribution builds
