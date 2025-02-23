Name:           ublue-os-update-services
Vendor:         ublue-os
Version:        0.91
Release:        1%{?dist}
Summary:        Automatic updates for rpm-ostree and flatpak
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Supplements:    rpm-ostree flatpak

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds systemd units and configuration files for enabling automatic updates in rpm-ostree and flatpak

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm0644 -t %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/ src/%{_sysconfdir}/rpm-ostreed.conf
install -Dm0644 -t %{buildroot}%{_presetdir}/ src/%{_presetdir}/10-flatpak-system-update.preset
install -Dm0644 -t %{buildroot}%{_unitdir}/ src/%{_unitdir}/flatpak-system-update.service
install -Dm0644 -t %{buildroot}%{_unitdir}/ src/%{_unitdir}/flatpak-system-update.timer
install -Dm0644 -t %{buildroot}%{_userpresetdir}/ src/%{_userpresetdir}/10-flatpak-user-update.preset
install -Dm0644 -t %{buildroot}%{_userunitdir}/ src/%{_userunitdir}/flatpak-user-update.service
install -Dm0644 -t %{buildroot}%{_userunitdir}/ src/%{_userunitdir}/flatpak-user-update.timer
install -Dm0644 -t %{buildroot}%{_unitdir}/rpm-ostreed-automatic.timer.d/ src/%{_unitdir}/rpm-ostreed-automatic.timer.d/override.conf
install -Dm0644 -t %{buildroot}%{_unitdir}/rpm-ostreed-automatic.service.d/ src/%{_unitdir}/rpm-ostreed-automatic.service.d/override.conf

%check

%post
%systemd_post flatpak-system-update.timer
%systemd_user_post flatpak-user-update.timer

%preun
%systemd_preun flatpak-system-update.timer
%systemd_user_preun flatpak-user-update.timer

%files
%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/rpm-ostreed.conf
%{_presetdir}/10-flatpak-system-update.preset
%{_unitdir}/flatpak-system-update.service
%{_unitdir}/flatpak-system-update.timer
%{_userpresetdir}/10-flatpak-user-update.preset
%{_userunitdir}/flatpak-user-update.service
%{_userunitdir}/flatpak-user-update.timer
%{_unitdir}/rpm-ostreed-automatic.timer.d/override.conf
%{_unitdir}/rpm-ostreed-automatic.service.d/override.conf

%changelog
* Sun Feb 23 2025 Tulip Blossom <tulilirockz@outlook.com> - 0.91
- Explicitly only put rpm-ostreed configuration in different path instead of having a copy of everything on /usr/share/ublue-os

* Wed Aug 7 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.9
- Use etc over usr etc folder

* Mon Oct 2 2023 ArtikusHG <24320212+ArtikusHG@users.noreply.github.com> - 0.8
- Add metered connection check to system and flatpak update services

* Sat Aug 12 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.7
- Add randmized delay to update timers, and always run flatpak updates on boot

* Sat Aug 12 2023 Fifty Dinar <srbaizoki4@tuta.io> - 0.6
- Switch to drop-in overrides for rpm-ostreed-automatic modifications

* Sat Jul 22 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.5
- Set flatpak and rpm-ostree upgrade timers to run daily at 4am local time

* Fri Jun 30 2023 gerblesh <101901964+gerblesh@users.noreply.github.com> - 0.4
- Add BuildRequires for rpm-systemd-macros to fix enabling systemd services and uninstalling the RPM

* Fri May 12 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.4
- Refactor directory structure

* Fri Mar 03 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.3
- Enable timers for flatpak update services

* Fri Mar 03 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.2
- Add presets for flatpak update services

* Fri Mar 03 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.1
- Add flatpak update service and rpm-ostree config file
