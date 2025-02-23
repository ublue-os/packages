Name:           ublue-os-luks
Vendor:         ublue-os
Version:        0.4
Release:        1%{?dist}
Summary:        ublue-os scripts for simplified LUKS usage
License:        MIT
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch

%description
Adds scripts and dracut config to simplify LUKS autounlock

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm755 -t %{buildroot}%{_libexecdir}/ src/luks-disable-tpm2-autounlock
install -Dm755 -t %{buildroot}%{_libexecdir}/ src/luks-enable-tpm2-autounlock
install -Dm644 -t %{buildroot}%{_exec_prefix}/lib/dracut/dracut.conf.d src/90-ublue-luks.conf

%check

%files
%{_libexecdir}/luks-disable-tpm2-autounlock
%{_libexecdir}/luks-enable-tpm2-autounlock
%{_exec_prefix}/lib/dracut/dracut.conf.d/90-ublue-luks.conf

%changelog
* Sun Feb 23 2025 Tulip Blossom <tulilirockz@outlook.com> - 0.4
- Satisfy rpmlint and use rpkg macros for sources

* Thu Jul 04 2024 m2Giles <69128853+m2Giles@users.noreply.github.com> - 0.3
- Rewrite enable script to fail out if disk is not found
- LUKs disk is determined from kernel commandline instead of /etc/crypttab

* Sat Jun 29 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.2
- Add tpm, fido2, pkcs11 to dracut config enabling initramfs LUKS unlock options

* Tue Apr 30 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.1
- Add tpm2 autounlock enable/disable scripts
- Original source: https://github.com/bsherman/ublue-custom/
