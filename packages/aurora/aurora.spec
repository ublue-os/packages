%global debug_package %{nil}
%global vendor aurora

Name:           aurora
Version:        0.1.7
Release:        2%{?dist}
Summary:        Aurora branding

License:        CC-BY-SA
URL:            https://github.com/ublue-os/packages
VCS:           {{{ git_dir_vcs }}}
Source:        {{{ git_dir_pack }}}

%description
Branding for Aurora-related projects

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/aurora-logos/symbols/ cli-logos/symbols/*
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ logos/*
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/ fastfetch/fastfetch.jsonc
install -Dpm0644 -t %{buildroot}%{_datadir}/plymouth/themes/spinner/ plymouth/themes/spinner/*.png
install -Dpm0644 -t %{buildroot}%{_sysconfdir}/geoclue/conf.d/ schemas%{_sysconfdir}/geoclue/conf.d/99-beacondb.conf
install -Dpm0644 -t %{buildroot}%{_datadir}/ublue-os/homebrew/ schemas%{_datadir}/ublue-os/homebrew/*.Brewfile

mkdir -p %{buildroot}%{_datadir}/{backgrounds,wallpapers}/
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-1/contents/images/ wallpapers/images/aurora-wallpaper-1/contents/images/15392x8616.jpg
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-1/ wallpapers/images/aurora-wallpaper-1/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-1/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-2/contents/images/ wallpapers/images/aurora-wallpaper-2/contents/images/3840x2160.png
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-2/ wallpapers/images/aurora-wallpaper-2/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-2/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/greg-rakozy-aurora/contents/images/ wallpapers/images/greg-rakozy-aurora/contents/images/5616x3744.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/greg-rakozy-aurora/ wallpapers/images/greg-rakozy-aurora/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/greg-rakozy-aurora/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/jonatan-pie-aurora/contents/images/ wallpapers/images/jonatan-pie-aurora/contents/images/3944x2770.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/jonatan-pie-aurora/ wallpapers/images/jonatan-pie-aurora/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/jonatan-pie-aurora/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_clouds/contents/images/ wallpapers/images/xe_clouds/contents/images/6000x4000.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_clouds/ wallpapers/images/xe_clouds/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_clouds/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_foothills/contents/images/ wallpapers/images/xe_foothills/contents/images/4032x3024.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_foothills/ wallpapers/images/xe_foothills/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_foothills/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_space_needle/contents/images/ wallpapers/images/xe_space_needle/contents/images/6000x4000.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_space_needle/ wallpapers/images/xe_space_needle/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_space_needle/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_sunset/contents/images/ wallpapers/images/xe_sunset/contents/images/6000x4000.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_sunset/ wallpapers/images/xe_sunset/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/xe_sunset/ %{buildroot}%{_datadir}/wallpapers/


%check

%package logos
Summary:        Logos for KDE
Version:        0.1.3
License:        CC-BY-SA
Provides: fedora-logos
Provides: centos-logos
Provides: system-logos
Conflicts: bluefin-logos
Conflicts: fedora-logos
Conflicts: centos-logos
Conflicts: system-logos

%description logos
Replacement logos for KDE

%files logos
%{_datadir}/pixmaps/fedora*
%{_datadir}/pixmaps/system-*
%{_datadir}/pixmaps/ublue-*


%package cli-logos
Version:        0.1.3
Summary:        Logos for CLI
License:        CC-BY-SA

%description cli-logos
Logos for CLI applications like Fastfetch

%files cli-logos
%{_datadir}/ublue-os/aurora-logos/*


%package fastfetch
Summary:        Fastfetch configuration for Aurora
Version:        0.1.3
License:        CC-BY-SA

%description fastfetch
Fastfetch configuration for Aurora

%files fastfetch
%{_datadir}/ublue-os/fastfetch.jsonc


%package plymouth
Summary:        Plymouth customization for Aurora
Version:        0.1.3
License:        CC-BY-SA

%description plymouth
Plymouth logo customization for Aurora

%files plymouth
%{_datadir}/plymouth


%package schemas
Version:        0.1.4
Summary:        KDE Schemas for Aurora

%description schemas
Default schemas for Aurora

%files schemas
%{_sysconfdir}/geoclue
%{_datadir}/ublue-os/homebrew/*.Brewfile


%package backgrounds
Version:        0.1.3
Summary:        Aurora wallpapers
License:        CC-BY-SA

%description backgrounds
Wallpapers included on Aurora by default

%files backgrounds
# NOTE: KDE wants those wallpapers on /usr/share/wallpapers so badly :(
%{_datadir}/backgrounds/%{vendor}
%{_datadir}/wallpapers/aurora-wallpaper-1
%{_datadir}/wallpapers/aurora-wallpaper-2
%{_datadir}/wallpapers/greg-rakozy-aurora
%{_datadir}/wallpapers/jonatan-pie-aurora
%{_datadir}/wallpapers/xe_clouds
%{_datadir}/wallpapers/xe_foothills
%{_datadir}/wallpapers/xe_space_needle
%{_datadir}/wallpapers/xe_sunset


%changelog
%autochangelog
