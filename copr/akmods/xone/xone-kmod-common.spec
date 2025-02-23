%global real_name xone

Name:           %{real_name}-kmod-common
Version:        1000.{{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Linux kernel driver for Xbox One and Xbox Series X|S accessories common files
License:        GPLv2
URL:            https://github.com/KyleGospo/xonedo
BuildArch:      noarch

Source:         %{url}/archive/refs/heads/master.tar.gz

# Windows driver and firmware file:
Source1:        1cd6a87c-623f-4407-a52d-c31be49e925c_e19f60808bdcbfbd3c3df6be3e71ffc52e43261e.cab

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
cabextract -F FW_ACC_00U.bin %{SOURCE1}

%install
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_prefix}/lib/modprobe.d/

# Blacklist:
install -p -m 0644 install/modprobe.conf %{buildroot}%{_prefix}/lib/modprobe.d/xone.conf

# Firmware:
install -p -m 0644 -D FW_ACC_00U.bin %{buildroot}%{_prefix}/lib/firmware/xow_dongle.bin

%files
%license LICENSE
%doc README.md
%{_prefix}/lib/modprobe.d/%{real_name}.conf
%{_prefix}/lib/firmware/xow_dongle.bin

%changelog
{{{ git_dir_changelog }}}
