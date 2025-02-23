%global modname 88XXau
%global srcversion 5.6.4.2
%global srcname rtl8812au
%global pkgname rtl88xxau

%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

# name should have a -kmod suffix
Name:          %{pkgname}-kmod
Version:       %{srcversion}.git
Release:       2%{?dist}
Summary:       Realtek RTL8812AU/21AU and RTL8814AU driver
License:       GPLv2
URL:           https://github.com/aircrack-ng/rtl8812au
Source0:       %{url}/archive/refs/heads/v%{srcversion}.zip

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Realtek RTL8812AU/21AU and RTL8814AU driver with monitor mode and frame injection

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c %{pkgname}
for kernel_version  in %{?kernel_versions} ; do
  cp -a %{srcname}-%{srcversion} _kmod_build_${kernel_version%%___*}/
done

%build
for kernel_version  in %{?kernel_versions} ; do
  pushd _kmod_build_${kernel_version%%___*}/
  make clean
  make KVER=${kernel_version%%___*}
  popd
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/%{modname}.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{modname}.ko
done
%{?akmod_install}

%changelog
