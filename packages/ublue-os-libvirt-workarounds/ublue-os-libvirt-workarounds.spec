Name:           ublue-os-libvirt-workarounds
Vendor:         ublue-os
Version:        1.0
Release:        1%{?dist}
Summary:        Services to workaround issues in -dx images
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Supplements:    libvirt

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds systemd units and configuration files for workarounds with -dx images

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm0644 -t %{buildroot}%{_presetdir}/ src/%{_presetdir}/54-ublue-os-libvirt-workarounds.preset
install -Dm0644 -t %{buildroot}%{_unitdir}/ src/%{_unitdir}/libvirt-workaround.service
install -Dm0644 -t %{buildroot}%{_prefix}/lib/tmpfiles.d src/%{_prefix}/lib/tmpfiles.d/libvirt-workaround.conf

%check

%post
%systemd_post libvirt-workaround.service

%preun
%systemd_preun libvirt-workaround.service

%files
%{_presetdir}/54-ublue-os-libvirt-workarounds.preset
%{_unitdir}/libvirt-workaround.service
%{_prefix}/lib/tmpfiles.d/libvirt-workaround.conf

%changelog
* Thu Apr 17 2025 Adam Fidel <adam@fidel.cloud> - 1.0
- Port from ublue-os/aurora
