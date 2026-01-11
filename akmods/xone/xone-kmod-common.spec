%global real_name xone

Name:           %{real_name}-kmod-common
Version:        1000.{{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Linux kernel driver for Xbox One and Xbox Series X|S accessories common files
License:        GPLv2
URL:            https://github.com/ublue-os/xonedo
BuildArch:      noarch

Source:         %{url}/archive/refs/heads/master.tar.gz

# Windows driver and firmware file:
Source1:        1cd6a87c-623f-4407-a52d-c31be49e925c_e19f60808bdcbfbd3c3df6be3e71ffc52e43261e.cab
Source2:        20810869_8ce2975a7fbaa06bcfb0d8762a6275a1cf7c1dd3.cab

BuildRequires:  cabextract
# UDev rule location (_udevrulesdir) and systemd macros:
BuildRequires:  systemd-rpm-macros

Requires:       wireless-regdb
Requires:       %{real_name}-kmod = %{?epoch:%{epoch}:}%{version}
Provides:       %{real_name}-kmod-common = %{?epoch:%{epoch}:}%{version}

%description
Linux kernel driver for Xbox One and Xbox Series X|S accessories common files.
 
%prep
%autosetup -p1 -n xonedo-master

# Firmware:
cabextract -F FW_ACC_00U.bin %{SOURCE2}
mv FW_ACC_00U.bin FW_ACC_00U-2.bin
cabextract -F FW_ACC_00U.bin %{SOURCE1}

%install
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_prefix}/lib/modprobe.d/

# Blacklist:
install -p -m 0644 install/modprobe.conf %{buildroot}%{_prefix}/lib/modprobe.d/xone.conf

# Firmware:
install -p -m 0644 -D FW_ACC_00U.bin %{buildroot}%{_prefix}/lib/firmware/xow_dongle.bin
install -p -m 0644 -D FW_ACC_00U-2.bin %{buildroot}%{_prefix}/lib/firmware/xow_dongle_045e_02e6.bin

%files
%license LICENSE
%doc README.md
%{_prefix}/lib/modprobe.d/%{real_name}.conf
%{_prefix}/lib/firmware/xow_dongle.bin
%{_prefix}/lib/firmware/xow_dongle_045e_02e6.bin

%changelog
{{{ git_dir_changelog }}}
