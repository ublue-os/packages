%global srccommit 866a9100c7b3f6508b81b31a22cae19dcacdacb9
%global modname rtl8814au
%global srcname 8814au

%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

# name should have a -kmod suffix
Name:           %{modname}-kmod
# Version comes from include/rtw_version.h
Version:        5.8.5.1.git
Release:        1%{?dist}
Summary:        Realtek RTL8814AU Driver
Group:          System Environment/Kernel
License:        GPLv2
URL:            https://github.com/morrownr/8814au
Source0:        %{url}/archive/%{srccommit}.zip

BuildRequires: kmodtool

%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Realtek RTL8814AU Driver

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c %{modname}

for kernel_version  in %{?kernel_versions} ; do
  mkdir -p _kmod_build_${kernel_version%%___*}
  cp -a %{srcname}-%{srccommit} _kmod_build_${kernel_version%%___*}/
done

%build
for kernel_version  in %{?kernel_versions} ; do
  pushd _kmod_build_${kernel_version%%___*}/
  cd %{srcname}-%{srccommit}
  make clean
  make
  # Rename the module to have rtl prefix for Realtek
  mv %{srcname}.ko %{modname}.ko
  popd
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/%{srcname}-%{srccommit}/%{modname}.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{modname}.ko
done
%{?akmod_install}

%clean
rm -rf "%{buildroot}"

%changelog
