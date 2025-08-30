Name:           ublue-os-update-reminder
Vendor:         ublue-os
Version:        1.0
Release:        1%{?dist}
Summary:        Reboot reminder notifications for long-running systems
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Requires:       python3-dbus-next
Requires:       libnotify
Supplements:    rpm-ostree

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Provides systemd units and scripts for reminding users to reboot systems that have been running for an extended period (28+ days), helping ensure system updates are applied.

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm0644 -t %{buildroot}%{_userpresetdir}/ src/%{_userpresetdir}/99-ublue-reboot-notifier.preset
# Install systemd user units
install -Dm0644 -t %{buildroot}%{_userunitdir}/ src/%{_userunitdir}/ublue-reboot-notifier.service
install -Dm0644 -t %{buildroot}%{_userunitdir}/ src/%{_userunitdir}/ublue-uptime-checker-boot.service
install -Dm0644 -t %{buildroot}%{_userunitdir}/ src/%{_userunitdir}/ublue-uptime-checker.service
install -Dm0644 -t %{buildroot}%{_userunitdir}/ src/%{_userunitdir}/ublue-uptime-checker.timer

# Install executable scripts
install -Dm0755 -t %{buildroot}%{_libexecdir}/ src/%{_libexecdir}/ublue-reboot-notifier-watcher.py
install -Dm0755 -t %{buildroot}%{_libexecdir}/ src/%{_libexecdir}/ublue-uptime-checker.sh

# scripts
install -Dm0755 -t %{buildroot}%{_libexecdir}/ src/%{_libexecdir}/ublue-reboot-notifier-show.sh
install -Dm0755 -t %{buildroot}%{_libexecdir}/ src/%{_libexecdir}/ublue-reboot-notifier-watcher.py
install -Dm0755 -t %{buildroot}%{_libexecdir}/ src/%{_libexecdir}/ublue-uptime-checker.sh

%check

%post
%systemd_user_post ublue-uptime-checker.timer
%systemd_user_post ublue-uptime-checker-boot.service

%preun
%systemd_user_preun ublue-uptime-checker.timer
%systemd_user_preun ublue-uptime-checker-boot.service

%files
%{_userpresetdir}/99-ublue-reboot-notifier.preset
%{_userunitdir}/ublue-reboot-notifier.service
%{_userunitdir}/ublue-uptime-checker-boot.service
%{_userunitdir}/ublue-uptime-checker.service
%{_userunitdir}/ublue-uptime-checker.timer
%{_libexecdir}/ublue-reboot-notifier-watcher.py
%{_libexecdir}/ublue-uptime-checker.sh

%changelog
* Fri Aug 30 2025 Adam Fidel <adam@fidel.cloud> - 1.0
- Initial release

