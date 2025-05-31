%global debug_package %{nil}

Name:       ublue-branding
Version:    0.1.0
Release:    1%{?dist}
Summary:    ublue-branding

License:    CC-BY-SA
URL:        https://github.com/ublue-os/packages
VCS:        {{{ git_dir_vcs }}}
Source:     {{{ git_dir_pack }}}

BuildArch:  noarch

%description
Branding for Universal Blue projects

%prep
{{{ git_dir_setup_macro }}}

%build

%install
%doc LICENSE
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ublue-discourse.svg src/ublue-discourse.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ublue-docs.svg src/ublue-docs.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ublue-update.svg src/ublue-update.svg

%files
%{_datadir}/pixmaps/ublue-discourse.svg
%{_datadir}/pixmaps/ublue-docs.svg
%{_datadir}/pixmaps/ublue-update.svg

%changelog
%autochangelog
