Name:           ublue-os-selinux-workarounds
Vendor:         ublue-os
Version:        0.1
Release:        1%{?dist}
Summary:        SELinux policy workarounds for ublue-os images
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch
BuildRequires:  checkpolicy
BuildRequires:  policycoreutils
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%global policy_module ublue_os_composefs_execmem

%description
Installs targeted SELinux policy workarounds for ublue-os images.

This currently contains a narrow temporary mitigation for Linux 7.0
composefs/overlay backing-file mmap checks causing legitimate userspace
execmem mappings to be evaluated as kernel_t.

%prep
{{{ git_dir_setup_macro }}}

%build
checkmodule -M -m -o %{policy_module}.mod src/selinux/%{policy_module}.te
semodule_package -o %{policy_module}.pp -m %{policy_module}.mod

%install
install -Dm0644 %{policy_module}.pp %{buildroot}%{_datadir}/selinux/packages/%{policy_module}.pp

%check

%post
%selinux_modules_install %{_datadir}/selinux/packages/%{policy_module}.pp

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall %{_datadir}/selinux/packages/%{policy_module}.pp
fi

%files
%{_datadir}/selinux/packages/%{policy_module}.pp

%changelog
%autochangelog
