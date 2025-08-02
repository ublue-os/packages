# NOTICE: staright up a spec that i got from https://github.com/xanderlent/intel-npu-driver-rpm

Name:		intel-npu-level-zero
# renovate: datasource=github-releases depName=intel/linux-npu-driver
Version:	1.19.0
Release:	1%{?dist}
Summary:	Intel Neural Processing Unit Driver for Linux

# MIT license for linux-npu-driver (except firmware and Linux uapi headers)
# MIT license for level-zero-npu-extensions
# Apache 2.0 license for npu_plugin_elf
License:	MIT AND Apache-2.0
URL:		https://github.com/intel/linux-npu-driver
Source:		%{url}/archive/refs/tags/v%{version}.tar.gz
# TODO: Long-term it would be nice to untangle these vendored dependencies
%define lz_npu_exts_version a63155ae4e64feaaa6931f4696c2e2e699063875
# v1.10.1 vendors commit a63155ae4e64feaaa6931f4696c2e2e699063875 which does not correspond to any tag or release in the secondary repo, sigh.
Source:		https://github.com/intel/level-zero-npu-extensions/archive/%{lz_npu_exts_version}.tar.gz
%define npu_elf_version 98f6fc4e93c0aca2c7620a32bd5c684b515f8532
# v1.10.1 vendors commit 98f6fc4e93c0aca2c7620a32bd5c684b515f8532 which should be tagged npu_ud_2024_44_rc1, but it seems like they forgot to push the tag to the secondary repo, sigh.
Source:		https://github.com/openvinotoolkit/npu_plugin_elf/archive/%{npu_elf_version}.tar.gz
Patch:		0001-Disable-third-party-googletest-and-yaml-cpp.patch
Patch:		0002-Make-firmware-install-respect-CMAKE_INSTALL_PATH.patch
# Some extra patches are needed when building against OneAPI Level Zero >= 1.8.4.
# NOTE: These MUST be specified unconditionally or copr won't import them into dist-git.
Patch:		0003-Uprev-level-zero-npu-extensions-to-build-against-hea.patch
Patch:		0004-Fix-usage-of-upstreamed-extension.patch
Patch:		0001-Remove-structure-and-enum-that-are-introduced-in-ze-.patch


# TODO: Can this build on non-x86?
# TODO: Can this even build 32-bit? I haven't tested!
ExclusiveArch:	x86_64

# NOTE: This project vendors the drm/ivpu_accel.h header and the DMA-BUF headers
# TODO: Compare vendored headers and switch to using kernel-headers as needed, since the kernel side is upstream.
BuildRequires:	cmake >= 3.22
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	glibc-devel
BuildRequires:	gmock-devel >= 1.14.0
BuildRequires:	gtest-devel >= 1.14.0
BuildRequires:	libudev-devel
# NOTE: If building against level zero 1.18 or newer headers, we need to patch the extension headers
%if 0%{?fedora} >= 41
# is Fedora 41 or Fedora 42 (rawhide)
BuildRequires:	oneapi-level-zero-devel >= 1.18.4
%else
# is Fedora 40, since we don't support anything lower
BuildRequires:	oneapi-level-zero-devel >= 1.17.44
%endif
# TODO: maybe higher requirement, but definitely 3.0+
BuildRequires:	openssl-devel >= 3.0.0
# Upstream is using 0.8.0 as of v1.5.1, but with no meaningful updates to upstream code
BuildRequires:	yaml-cpp-devel >= 0.7.0
# v1.10.0 recommends kernel v6.8.12 or later
# TODO: Requires at runtime? Recommends?
#Recommends:	intel-npu-firmware = #{version}
#Requires:	oneapi-level-zero >= 1.16.1
# Need to Provides: bundled(level-zero-npu-exts) = some_version
# Need to Provides: bundled(vpux_elf) = some_version

# Tweaked from the upstream README.md.
%description
This is the user space driver for the Intel NPU device. It allows the use
of the Intel NPU via the Level Zero API.

The Intel NPU device is an AI inference accelerator integrated with Intel
client CPUs, starting from the Intel Core Ultra generation of CPUs (CPUs
formerly known as Meteor Lake). It enables energy-efficient execution of
artificial neural network tasks.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).

%package -n intel-npu-firmware
License:	Redistributable, no modification permitted
Summary:	Intel Neural Processing Unit Firmware
BuildArch:	noarch
# NOTE: Keep the description of the firmware in sync with the main package
# TODO: Do what the upstream package does and auto-reload the NPU kernel module on firmware install?
# TODO: Trigger regeneration of initramfs since firmware needs to be included there?
%description -n intel-npu-firmware
This is the firmware for the Intel NPU device.

The Intel NPU device is an AI inference accelerator integrated with Intel
client CPUs, starting from the Intel Core Ultra generation of CPUs (CPUs
formerly known as Meteor Lake). It enables energy-efficient execution of
artificial neural network tasks.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).


%package tests
License:	MIT AND Apache-2.0
Summary:	Tests for the Intel Neural Processing Unit Driver for Linux
# TODO: Do the tests actually require any of the other parts? Or any deps?
%description tests
Tests for the Intel NPU Driver for Linux.

These programs exercise the kernel-mode (kmd) and user-mode (umd) parts of
the driver.

Note that while this device is officially called the Neural Processing Unit,
the Linux kernel driver uses the previous name of Versatile Processing Unit
(VPU).

%prep
%setup -q -n linux-npu-driver-%{version}
%setup -q -n linux-npu-driver-%{version} -T -D -a 1
# Patch out the vendored googletest and yaml-cpp directories
# (these are git submodules and so are empty in the tarball)
# TODO: Work with upstream to handle detecting these libraries in CMake
%patch -P 0 -p1
# Fix firmware install path to be relative
# TODO: Propose this patch to upstream
%patch -P 1 -p1
# Now, stitch the two vendored projects that we need into the source tree
rmdir third_party/level-zero-npu-extensions/
mv level-zero-npu-extensions-%{lz_npu_exts_version} third_party/level-zero-npu-extensions/
# When building on Fedroa 41+, patch the extension headers and main code
%if 0%{?fedora} >= 41
cd third_party/level-zero-npu-extensions/
# Note that we never actually apply patch #2! It just uprevs a git submodule in the source tree.
# It exists only so you can build from the modified source tree on Fedora 41+.
# This patch (to the extensions repo) uprevs lz_npu_exts_version to 110f48ee8eda22d8b40daeeecdbbed0fc3b08f8b
%patch -P 4 -p1
cd ../..
# Also patch the driver to work with the new headers
%patch -P 3 -p1
%endif
cp third_party/level-zero-npu-extensions/LICENSE.txt LICENSE-level-zero-npu-extensions.txt
cp validation/umd-test/configs/README.md README-umd-test-configs.md
%setup -q -n linux-npu-driver-%{version} -T -D -a 2
rmdir third_party/vpux_elf/
mv npu_plugin_elf-%{npu_elf_version} third_party/vpux_elf
cp third_party/vpux_elf/LICENSE LICENSE-vpux_elf

%build
%cmake
%cmake_build

%install
%cmake_install

%files
%license LICENSE.md third-party-programs.txt LICENSE-level-zero-npu-extensions.txt LICENSE-vpux_elf
# TODO: Also include the RPM repo readme?
%doc README.md docs/overview.md security.md README-umd-test-configs.md validation/umd-test/configs/basic.yaml
# TODO: Does the unversioned library belong in a -devel package?
%{_libdir}/libze_intel_vpu.so
%{_libdir}/libze_intel_vpu.so.1
%{_libdir}/libze_intel_vpu.so.%{version}

%files tests
%{_bindir}/npu-kmd-test
%{_bindir}/npu-umd-test

%files -n intel-npu-firmware
%license firmware/bin/COPYRIGHT
/usr/lib/firmware/updates/intel

%check
%ctest


%changelog
* Wed Jan 1 2025 Alexander F. Lent <lx@xanderlent.com> - 1.10.1-1
- Uprev to latest upstream version.
- Upstream moved firmware file from LFS into repo, so that eliminates some workarounds.
* Sat Nov 9 2024 Alexander F. Lent <lx@xanderlent.com> - 1.10.0-3
- Fix copr import (build should be fine) by unconditionally specifying patchfiles.
* Fri Nov 8 2024 Alexander F. Lent <lx@xanderlent.com> - 1.10.0-2
- Whoops, need to patch the extension headers if building against OneAPI Level Zero >= 1.8
- Apparently they have not tested this since GCC correctly errors out with a type mismatch
  because of the change, so patch the driver to fix the bug.
* Fri Nov 8 2024 Alexander F. Lent <lx@xanderlent.com> - 1.10.0-1
- Update package to the latest released version.
- Allows us to drop a substantial number of patches, including one downstream, yay!
- Requires us to uprev bundled packages and some dependencies.
* Wed Sep 25 2024 Alexander F. Lent <lx@xanderlent.com> - 1.8.0-2
- Update the package to the latest upstream patch, not yet in any release.
- It is just a fix to a documented option we aren't using, but still.
* Wed Sep 18 2024 Alexander F. Lent <lx@xanderlent.com> - 1.8.0-1
- Add some additional documentation files to the package.
- Update the package to the latest upstream release & patch.
* Wed Aug 14 2024 Alexander F. Lent <lx@xanderlent.com> - 1.6.0-2
- Whoops, sources file has special semantics.
* Wed Aug 14 2024 Alexander F. Lent <lx@xanderlent.com> - 1.6.0-1
- Update package to latest upstream release.
- Bump minimum dependency versions where upstream's preferred version is now in Fedora.
* Tue Jul 9 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.1-1
- Update to latest upstream release.
* Thu Jul 4 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-5
- Revert firmware location change, it seems like a deeper bug
- Attempt to also own the other directories that we install like /lib/firmware/updates/intel (etc)
* Thu Jul 4 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-4
- Fix dracut not picking up the NPU/VPU firmware
- Fix a typo in the firmware patch name
* Mon Jul 1 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-3
- Fix vpu_37xx_v0.0.bin being a Git LFS pointer, replace it with the real blob
* Mon Jul 1 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-2
- Fix build broken by incorrect paths in various last-minute additions
* Sun Jun 30 2024 Alexander F. Lent <lx@xanderlent.com> - 1.5.0-1
- Intial Release
