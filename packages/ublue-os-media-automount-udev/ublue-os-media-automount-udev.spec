Name:           ublue-os-media-automount-udev
Vendor:         ublue-os
Version:        0.5
Release:        1%{?dist}
Summary:        udev rules to mount non-removable disk partitions

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages

VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}

BuildArch:      noarch
Supplements:    systemd-udev

%description
%{summary}

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -p -Dm0644 ./99-media-automount.rules %{buildroot}%{_exec_prefix}/lib/udev/rules.d/99-media-automount.rules
install -p -Dm0755 ./is_in_fstab.sh %{buildroot}%{_libexecdir}/is_in_fstab.sh

%check

%files
%{_exec_prefix}/lib/udev/rules.d/99-media-automount.rules
%{_libexecdir}/is_in_fstab.sh

%changelog
* Wed Mar 12 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.5
- Only mount labeled partitions

* Wed Mar 12 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.4
- Load rule the latest and fetch UUID with lsblk

* Wed Mar 12 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.3
- Dont error out in is_in_fstab.sh

* Mon Mar 10 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.2
- Add missing permissions and use 'exit' instead of 'return' in is_in_fstab.sh

* Wed Mar 05 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.1
- Initial release