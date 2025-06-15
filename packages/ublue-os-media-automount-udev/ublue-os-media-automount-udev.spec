Name:           ublue-os-media-automount-udev
Vendor:         ublue-os
Version:        0.16
Release:        1%{?dist}
Summary:        udev rules to mount non-removable disk partitions

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages

VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}

BuildArch:      noarch
Supplements:    systemd-udev
BuildRequires:  systemd-rpm-macros

%description
%{summary}

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -p -Dm0755 ./ublue-os-media-automount.py %{buildroot}%{_libexecdir}/ublue-os-media-automount.py
install -p -Dm0644 ./ublue-os-media-automount.service %{buildroot}%{_prefix}/lib/systemd/system/ublue-os-media-automount.service
install -p -Dm0644 ./ublue-os-media-automount.conf %{buildroot}%{_tmpfilesdir}/ublue-os-media-automount.conf

%check

%files
%{_libexecdir}/ublue-os-media-automount.py
%{_prefix}/lib/systemd/system/ublue-os-media-automount.service
%{_tmpfilesdir}/ublue-os-media-automount.conf

%changelog
* Mon Jun 09 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.16
- feat: log reason for mounting skip

* Thu May 22 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.15
- fix: ignore nonexisting entries in fstab

* Wed May 21 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.14
- fix: Start mounting before graphical session

* Tue May 20 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.13
- fix: use getuid to check root

* Sat May 17 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.12
- fix: Use service instead of udev

* Mon May 12 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.11
- fix: Preload database

* Sat May 10 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.10
- fix: Better prevention of ntfs mounting

* Tue May 06 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.9
- fix: Typo in udev attr

* Sat May 03 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.8
- Simpler exclusion and handle windows partitions

* Wed Mar 12 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.7
- Add /run/media/media-automount symlink for compatibility

* Wed Mar 12 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.6
- Add missing mount options to btrfs partitions

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
