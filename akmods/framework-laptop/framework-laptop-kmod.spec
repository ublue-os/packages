# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod
%global real_name framework-laptop
%global modname   framework_laptop

%global debug_package %{nil}

Name:           %{real_name}-kmod
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Kernel module to expose more Framework Laptop stuff
License:        GPLv2
URL:            https://github.com/KyleGospo/framework-laptop-kmod

Source:         %{url}/archive/refs/heads/main.tar.gz

# Get the needed BuildRequires (in parts depending on what we build for):
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
A kernel module that exposes the Framework Laptop (13, 16)'s battery charge limit and LEDs to userspace.

%prep
# Error out if there was something wrong with kmodtool:
%{?kmodtool_check}
# Print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n %{real_name}-kmod-master

for kernel_version  in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a %{modname}.c %{modname}.h Makefile _kmod_build_${kernel_version%%___*}/
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/%{modname}.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{modname}.ko
done
%{?akmod_install}

%changelog
{{{ git_dir_changelog }}}
