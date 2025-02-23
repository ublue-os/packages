Name:           ublue-os-signing
Vendor:         ublue-os
Version:        0.4
Release:        1%{?dist}
Summary:        Signing files and keys for Universal Blue
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds files and keys for signing Universal Blue images

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm0644 -t %{buildroot}%{_exec_prefix}/etc/containers/ src/%{_exec_prefix}/etc/containers/policy.json
install -Dm0644 -t %{buildroot}%{_sysconfdir}/containers/registries.d/ src/%{_sysconfdir}/containers/registries.d/*.yaml
install -Dm0644 -t %{buildroot}%{_sysconfdir}/pki/containers/ src/%{_sysconfdir}/pki/containers/*.pub
install -Dm0644 -t %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/etc/containers/ src/%{_exec_prefix}/etc/containers/policy.json
install -Dm0644 -t %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/containers/registries.d/ src/%{_sysconfdir}/containers/registries.d/*.yaml
install -Dm0644 -t %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/pki/containers/ src/%{_sysconfdir}/pki/containers/*.pub

%check

%files
%{_datadir}/%{VENDOR}/%{sub_name}/%{_exec_prefix}/etc/containers/policy.json
%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/containers/registries.d/ublue-os.yaml
%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/containers/registries.d/quay.io-toolbx-images.yaml
%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/pki/containers/quay.io-toolbx-images.pub
%{_datadir}/%{VENDOR}/%{sub_name}/%{_sysconfdir}/pki/containers/ublue-os.pub
%{_exec_prefix}/etc/containers/policy.json
%{_sysconfdir}/containers/registries.d/ublue-os.yaml
%{_sysconfdir}/containers/registries.d/quay.io-toolbx-images.yaml
%{_sysconfdir}/pki/containers/quay.io-toolbx-images.pub
%{_sysconfdir}/pki/containers/ublue-os.pub

%changelog
* Thu Aug 08 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.4
- Moved policy.json back to /usr/etc/ temporarily

* Wed Aug 07 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.3
- Moved files from /usr/etc/ to /etc/

* Sat May 18 2024 qoijjj <129108030+qoijjj@users.noreply.github.com> - 0.2
- Add signature verification for toolbx images

* Mon Jul 17 2023 RJ Trujillo <eyecantcu@pm.me> - 0.1
- Add package for signing files and keys
