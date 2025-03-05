Name:           ublue-os-media-automount-udev
Vendor:         ublue-os
Version:        0.1
Release:        %{autorelease}
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
install -p -Dm0644 ./60-media-automount.rules %{buildroot}%{_exec_prefix}/lib/udev/rules.d/60-media-automount.rules
install -p -Dm0644 ./is_in_fstab.sh %{buildroot}%{_libexecdir}/is_in_fstab.sh

%check

%files
%{_exec_prefix}/lib/udev/rules.d/60-media-automount.rules
%{_libexecdir}/is_in_fstab.sh

%changelog
* Wed Mar 05 2025 Zeglius <33781398+Zeglius@users.noreply.github.com> - 0.1
- Initial release