Name:           ublue-polkit-rules
Version:        0.1.0
Release:        1%{?dist}
Summary:        Polkit rules for Universal Blue projects

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}

BuildArch:      noarch

%description
Polkit Rules for Universal Blue

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dm0644 -t %{buildroot}%{_sysconfdir}/polkit-1/rules.d/ src/*.rules

%check

%files
%{_sysconfdir}/polkit-1/rules.d/*.rules

%changelog
%autochangelog
