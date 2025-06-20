Name:           ublue-os-libvirt-workarounds
Vendor:         ublue-os
Version:        1.1
Release:        1%{?dist}
Summary:        Services to workaround libvirt issues
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Supplements:    libvirt

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds systemd service and configuration for workarounds with libvirt on images

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm0644 -t %{buildroot}%{_presetdir}/ src/%{_presetdir}/54-ublue-os-libvirt-workarounds.preset
install -Dm0644 -t %{buildroot}%{_unitdir}/ src/%{_unitdir}/ublue-os-libvirt-workarounds.service
install -Dm0644 -t %{buildroot}%{_prefix}/lib/sysusers.d src/%{_prefix}/lib/sysusers.d/ublue-os-libvirt-workarounds.conf
install -Dm0644 -t %{buildroot}%{_prefix}/lib/tmpfiles.d src/%{_prefix}/lib/tmpfiles.d/ublue-os-libvirt-workarounds.conf

%check

%post
%systemd_post libvirt-workarounds.service

%preun
%systemd_preun libvirt-workarounds.service

%files
%{_presetdir}/54-ublue-os-libvirt-workarounds.preset
%{_unitdir}/ublue-os-libvirt-workarounds.service
%{_prefix}/lib/sysusers.d/ublue-os-libvirt-workarounds.conf
%{_prefix}/lib/tmpfiles.d/ublue-os-libvirt-workarounds.conf

%changelog
* Fri Jun 20 2025 Benjamin Sherman <benjamin@holyarmy.org> - 1.1
- Add sysusers config for libvirt and libvirtdbus
- Rename all files for consistency

* Thu Apr 17 2025 Adam Fidel <adam@fidel.cloud> - 1.0
- Port from ublue-os/aurora
