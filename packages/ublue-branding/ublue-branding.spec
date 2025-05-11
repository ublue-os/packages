%global debug_package %{nil}
%global vendor ublue
Name:           ublue-branding
Version:        0.0.0
Release:        1%{?dist}
Summary:        Universal Blue branding

License:        CC-BY-SA
URL:            https://github.com/ublue-os/packages
VCS:           {{{ git_dir_vcs }}}
Source:        {{{ git_dir_pack }}}

BuildArch:     noarch

%description
Branding for Universal Blue related projects

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps logos/ublue-discourse.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps logos/ublue-docs.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps logos/ublue-update.svg

%check

%package logos
Summary:        Logos for Universal Blue
Version:        0.0.0
License:        CC-BY-SA
%description logos


%files logos
%{_datadir}/pixmaps/ublue-discourse.svg
%{_datadir}/pixmaps/ublue-docs.svg
%{_datadir}/pixmaps/ublue-update.svg

%changelog
%autochangelog
