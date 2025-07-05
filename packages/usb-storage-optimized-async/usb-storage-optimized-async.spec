Name:           usb-storage-optimized-async
Version:        1.0
Release:        1%{?dist}
Summary:        Optimize async for USB storage devices minimizing the potential for data corruption

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Requires:       bash
Requires:       gawk
Requires:       grep
Requires:       coreutils
Requires:       findutils
Requires:       bc
Requires:       usbutils
Requires:       systemd
Requires:       systemd-udev

%description
Optimize async for USB storage devices minimizing the potential for data corruption

%prep
{{{ git_dir_setup_macro }}}

%install
install -Dm0755 ./src/%{name}-udev -t %{buildroot}%{_bindir}/%{name}-udev
install -Dm0644 ./src/zz1-%{name}-udev.rules -t %{buildroot}%{_udevrulesdir}/zz1-%{name}-udev.rules
install -Dm0755 ./src/%{name}-service -t %{buildroot}%{_bindir}/%{name}-service
install -Dm0644 ./src/%{name}-service.service -t %{buildroot}%{_unitdir}/%{name}-service.service
install -Dm0644 ./src/01-%{name}-service.preset -t %{buildroot}%{_presetdir}/01-%{name}-service.preset

%post
%systemd_post %{name}-service.service

%preun
%systemd_preun %{name}-service.service

%files
%{_bindir}/%{name}-udev
%{_udevrulesdir}/zz1-%{name}-udev.rules
%{_bindir}/%{name}-service
%{_unitdir}/%{name}-service.service
%{_presetdir}/01-%{name}-service.preset

%changelog
* Fri Jul 04 2025 Fifty Dinar <srbaizoki4@tuta.io> - 1.0-1
- Initial release
