Name:           ublue-os-udev-rules
Vendor:         ublue-os
Version:        0.9
Release:        1%{?dist}
Summary:        Additional udev files for device support

License:        MIT
URL:            https://github.com/ublue-os/packages

BuildArch:      noarch
Supplements:    systemd-udev

VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}
Source1:        https://codeberg.org/fabiscafe/game-devices-udev/archive/main.tar.gz
Source2:        https://raw.githubusercontent.com/LizardByte/Sunshine/refs/heads/master/src_assets/linux/misc/60-sunshine.rules
Source3:        https://raw.githubusercontent.com/FrameworkComputer/inputmodule-rs/main/release/50-framework-inputmodule.rules

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds various udev rules for improving device support

%prep
{{{ git_dir_setup_macro }}}

%build

%install
mkdir -p -m0755 %{buildroot}%{_datadir}/%{VENDOR}/{%{sub_name},game-devices-udev}

# add repo local udev rules
install -pm0644 ./src/udev-rules.d/* %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}

# add contents of remote-sourced game-devices-udev rules archive
tar xzf %{SOURCE1} -C %{buildroot}%{_datadir}/%{VENDOR}/game-devices-udev --strip-components=1

# add other remote-sourced rules
install -m0644 %{SOURCE2} %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/60-sunshine-ublue.rules
install -m0644 %{SOURCE3} %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/50-framework-inputmodule.rules

mkdir -p -m0755 %{buildroot}%{_exec_prefix}/lib/udev/rules.d
cp -a %{buildroot}%{_datadir}/%{VENDOR}/{%{sub_name},game-devices-udev}/*.rules %{buildroot}%{_exec_prefix}/lib/udev/rules.d/

%files
%{_datadir}/%{VENDOR}/%{sub_name}/*.rules
%{_datadir}/%{VENDOR}/game-devices-udev/*.rules
%{_datadir}/%{VENDOR}/game-devices-udev/README.md
%{_datadir}/%{VENDOR}/game-devices-udev/LICENSE
%{_datadir}/%{VENDOR}/game-devices-udev/game-controller-udev.svg
%{_datadir}/%{VENDOR}/game-devices-udev/8BitDo.md
%{_exec_prefix}/lib/udev/rules.d/*.rules


%changelog
* Tue Jun 25 2024 Fifty Dinar <srbaizoki4@tuta.io> - 0.10
- Add Apple SuperDrive udev rule

* Sun Jun 02 2024 Fifty Dinar <srbaizoki4@tuta.io> - 0.9
- Add Neutron HiFi DAC V1 udev rule

* Fri Apr 26 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.8
- Add Framework Computer udev rules

* Mon Oct 23 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.7
- Rename Sunshine and OpenTabletDriver rules files to prevent filename collisions

* Fri Oct 20 2023 ArtikusHG <24320212+ArtikusHG@users.noreply.github.com> - 0.6
- Add Sunshine udev rules

* Thu Sep 28 2023 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.5
- Add OpenTabletDriver udev rules

* Sat May 13 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.4
- Add usb-realtek-net rules

* Fri May 12 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.3
- Refactor directory structure
- Adjust RPM description

* Fri Mar 03 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.2
- Add game-devices-udev rules

* Sat Feb 25 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.1
- Add game-devices-udev rules
