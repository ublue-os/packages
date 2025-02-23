%global real_name framework-laptop

Name:           %{real_name}-kmod-common
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Kernel module to expose more Framework Laptop stuff
License:        GPLv2
URL:            https://github.com/KyleGospo/framework-laptop-kmod
BuildArch:      noarch

Source:         %{url}/archive/refs/heads/main.tar.gz

Requires:       %{real_name}-kmod = %{?epoch:%{epoch}:}%{version}
Provides:       %{real_name}-kmod-common = %{?epoch:%{epoch}:}%{version}

%description
A kernel module that exposes the Framework Laptop (13, 16)'s battery charge limit and LEDs to userspace.
 
%prep
%autosetup -p1 -n %{real_name}-kmod-main

%files
%license LICENSE
%doc README.md

%changelog
{{{ git_dir_changelog }}}
