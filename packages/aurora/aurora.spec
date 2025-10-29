%global debug_package %{nil}
%global vendor aurora

Name:           aurora
Version:        0.1.39
Release:        1%{?dist}
Summary:        Aurora branding

License:        CC-BY-SA
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch

%description
Branding for Aurora-related projects

%prep
{{{ git_dir_setup_macro }}}

%build

%install
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/{apps,places}/
mkdir -p %{buildroot}%{_datadir}/pixmaps/
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/scalable/ logos/distributor-logo.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/scalable/places/ logos/auroralogo-white.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/scalable/places/ logos/distributor-logo-symbolic.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/scalable/places/ logos/auroralogo-circle-symbolic.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/scalable/places/ logos/auroralogo-pride.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/icons/hicolor/scalable/places/ logos/auroralogo-pride-trans.svg
install -Dpm0644 -t %{buildroot}%{_datadir}/pixmaps/ logos/fedora-logo.svg
magick -background none logos/fedora-logo.svg -quality 90 -resize $((400-10*2))x100 -gravity center -extent 400x100 %{buildroot}%{_datadir}/pixmaps/fedora-logo.png
magick -background none logos/fedora-logo.svg -quality 90 -resize $((128-3*2))x32 -gravity center -extent 128x32 %{buildroot}%{_datadir}/pixmaps/fedora-logo-small.png
magick -background none logos/fedora-logo.svg -quality 90 -resize $((200-5*2))x50 -gravity center -extent 200x100 %{buildroot}%{_datadir}/pixmaps/fedora_logo_med.png
magick -background none logos/distributor-logo.svg -quality 90 -resize 256x256! %{buildroot}%{_datadir}/pixmaps/system-logo.png
magick -background none logos/distributor-logo.svg -quality 90 -resize 128x128! %{buildroot}%{_datadir}/pixmaps/fedora-logo-sprite.png
magick -background none logos/distributor-logo.svg -quality 90 -resize 256x256! %{buildroot}%{_datadir}/pixmaps/system-logo-white.png
ln -sr %{buildroot}%{_datadir}/pixmaps/fedora-logo.svg %{buildroot}%{_datadir}/pixmaps/fedora_whitelogo.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/distributor-logo.svg %{buildroot}%{_datadir}/pixmaps/fedora-logo-sprite.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/distributor-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/places/distributor-logo.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/distributor-logo.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/places/auroralogo-gradient.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/places/distributor-logo-symbolic.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/places/auroralogo-symbolic.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/places/distributor-logo-symbolic.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/places/distributor-logo-white.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/places/distributor-logo-symbolic.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/places/start-here.svg
ln -sr %{buildroot}%{_datadir}/icons/hicolor/scalable/places/distributor-logo-symbolic.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/start-here.svg

mkdir -p %{buildroot}/%{_datadir}/plymouth/themes/spinner/

magick -background none logos/fedora-logo.svg -quality 90 -resize $((128-3*2))x32 -gravity center -extent 128x32 %{buildroot}%{_datadir}/plymouth/themes/spinner/watermark.png
magick -background none logos/fedora-logo.svg -quality 90 -resize $((128-3*2))x32 -gravity center -extent 128x32 %{buildroot}%{_datadir}/plymouth/themes/spinner/kinoite-watermark.png

mkdir -p %{buildroot}%{_datadir}/{backgrounds,wallpapers}/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-2/contents/images/ wallpapers/images/aurora-wallpaper-2/contents/images/3840x2160.png
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-2/ wallpapers/images/aurora-wallpaper-2/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-2/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-3/contents/images/ wallpapers/images/aurora-wallpaper-3/contents/images/3840x2160.png
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-3/ wallpapers/images/aurora-wallpaper-3/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-3/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-4/contents/images/ wallpapers/images/aurora-wallpaper-4/contents/images/3840x2160.png
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-4/ wallpapers/images/aurora-wallpaper-4/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-4/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-5/contents/images/ wallpapers/images/aurora-wallpaper-5/contents/images/3840x2160.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-5/ wallpapers/images/aurora-wallpaper-5/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-5/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-6/contents/images/ wallpapers/images/aurora-wallpaper-6/contents/images/3840x2160.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-6/ wallpapers/images/aurora-wallpaper-6/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-6/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-7/contents/images/ wallpapers/images/aurora-wallpaper-7/contents/images/3840x2160.jxl
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-7/ wallpapers/images/aurora-wallpaper-7/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-7/ %{buildroot}%{_datadir}/wallpapers/

# Replace the old wallpaper with the new one
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-6/ %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-1
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/aurora-wallpaper-1/ %{buildroot}%{_datadir}/wallpapers/

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

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/looking_towards_the_future/contents/images/ wallpapers/images/looking_towards_the_future/contents/images/1920x1080.png
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/looking_towards_the_future/contents/images_dark/ wallpapers/images/looking_towards_the_future/contents/images_dark/1920x1080.png
install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/looking_towards_the_future/ wallpapers/images/looking_towards_the_future/metadata.json
ln -sr %{buildroot}%{_datadir}/backgrounds/%{vendor}/looking_towards_the_future/ %{buildroot}%{_datadir}/wallpapers/

install -Dpm0644 -t %{buildroot}%{_datadir}/backgrounds/%{vendor}/ kde-config/aurora.xml
install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/ kde-config/dev.getaurora.aurora.desktop/metadata.{desktop,json}
install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/ kde-config/dev.getaurora.aurora.desktop/contents/defaults
install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/plasmoidsetupscripts/ kde-config/dev.getaurora.aurora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.{folder,kickoff,systemtray}.js

mkdir -p %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/icons/
ln -sr %{buildroot}/icons/hicolor/scalable/distributor-logo.svg %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/icons/aurora-logo.svg

mkdir -p %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/splash/images/
install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/splash/ kde-config/dev.getaurora.aurora.desktop/contents/splash/Splash.qml

gzip -c logos/distributor-logo.svg > %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/splash/images/aurora_logo.svgz

install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/previews/ kde-config/dev.getaurora.aurora.desktop/contents/previews/fullscreenpreview.jpg
install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/previews/ kde-config/dev.getaurora.aurora.desktop/contents/previews/preview.png
install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/previews/ kde-config/dev.getaurora.aurora.desktop/contents/previews/splash.png

install -Dpm0644 -t %{buildroot}/%{_kf6_datadir}/discover/ kde-config/discover/featuredurlrc
install -Dpm0644 -t %{buildroot}/%{_datadir}/ublue-os/discover/ kde-config/discover/featured.json

mkdir -p %{buildroot}/%{_datadir}/sddm/themes/01-breeze-aurora/faces
install -Dpm0644 -t %{buildroot}/%{_datadir}/sddm/themes/01-breeze-aurora/ kde-config/sddm/01-breeze-aurora/*.qml kde-config/sddm/01-breeze-aurora/*.desktop kde-config/sddm/01-breeze-aurora/*.png kde-config/sddm/01-breeze-aurora/*.conf

install -Dpm0644 -t %{buildroot}/%{_datadir}/sddm/themes/01-breeze-aurora/faces/ kde-config/sddm/01-breeze-aurora/faces/.face.icon
ln -sr %{buildroot}/icons/hicolor/scalable/distributor-logo.svg %{buildroot}/%{_datadir}/sddm/themes/01-breeze-aurora/default-logo.svg


%check

%package logos
Summary:        Logos for KDE
Version:        0.2.1
License:        CC-BY-SA
BuildRequires: ImageMagick
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
%{_datadir}/pixmaps/fedora_logo_med.png
%{_datadir}/pixmaps/fedora_whitelogo.svg
%{_datadir}/pixmaps/fedora-logo.{png,svg}
%{_datadir}/pixmaps/fedora-logo-small.png
%{_datadir}/pixmaps/fedora-logo-sprite.{png,svg}
%{_datadir}/pixmaps/system-logo{,-white}.png
%{_datadir}/icons/hicolor/scalable/distributor-logo.svg
%{_datadir}/icons/hicolor/scalable/places/distributor-logo-symbolic.svg
%{_datadir}/icons/hicolor/scalable/places/distributor-logo.svg
%{_datadir}/icons/hicolor/scalable/places/distributor-logo-white.svg
%{_datadir}/icons/hicolor/scalable/places/auroralogo-white.svg
%{_datadir}/icons/hicolor/scalable/{apps,places}/start-here.svg
%{_datadir}/icons/hicolor/scalable/places/auroralogo-circle-symbolic.svg
%{_datadir}/icons/hicolor/scalable/places/auroralogo-pride.svg
%{_datadir}/icons/hicolor/scalable/places/auroralogo-pride-trans.svg
%{_datadir}/icons/hicolor/scalable/places/auroralogo-symbolic.svg
%{_datadir}/icons/hicolor/scalable/places/auroralogo-gradient.svg

%package plymouth
Summary:        Plymouth customization for Aurora
Version:        0.1.6
License:        CC-BY-SA

%description plymouth
Plymouth logo customization for Aurora

%files plymouth
%{_datadir}/plymouth/themes/spinner/watermark.png
%{_datadir}/plymouth/themes/spinner/kinoite-watermark.png

%package backgrounds
Version:        0.1.8
Summary:        Aurora wallpapers
License:        CC-BY-SA

%description backgrounds
Wallpapers included on Aurora by default

%files backgrounds
# NOTE: KDE wants those wallpapers on /usr/share/wallpapers so badly :(
%{_datadir}/backgrounds/%{vendor}
%{_datadir}/wallpapers/aurora-wallpaper-1
%{_datadir}/wallpapers/aurora-wallpaper-2
%{_datadir}/wallpapers/aurora-wallpaper-3
%{_datadir}/wallpapers/aurora-wallpaper-4
%{_datadir}/wallpapers/aurora-wallpaper-5
%{_datadir}/wallpapers/aurora-wallpaper-6
%{_datadir}/wallpapers/aurora-wallpaper-7
%{_datadir}/wallpapers/greg-rakozy-aurora
%{_datadir}/wallpapers/jonatan-pie-aurora
%{_datadir}/wallpapers/xe_clouds
%{_datadir}/wallpapers/xe_foothills
%{_datadir}/wallpapers/xe_space_needle
%{_datadir}/wallpapers/xe_sunset
%{_datadir}/wallpapers/looking_towards_the_future


%package kde-config
Version:        0.1.4
Summary:        Aurora KDE Plasma configuration
License:        Apache-2.0 AND GPL-2.0-or-later
Requires:       aurora-logos
# Needed when we want to use kf6_datadir macro
BuildRequires:  kf6-rpm-macros

%description kde-config
This sets the Aurora defaults for Logos, Wallpapers, Theme and Editor's choice in Discover.

%files kde-config
%{_datadir}/backgrounds/aurora/aurora.xml
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/metadata.{desktop,json}
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/defaults
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/plasmoidsetupscripts/org.kde.plasma.{folder,kickoff,systemtray}.js
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/icons/aurora-logo.svg
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/splash/Splash.qml
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/splash/images/aurora_logo.svgz
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/previews/fullscreenpreview.jpg
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/previews/preview.png
%{_kf6_datadir}/plasma/look-and-feel/dev.getaurora.aurora.desktop/contents/previews/splash.png
%{_kf6_datadir}/discover/featuredurlrc
%{_datadir}/ublue-os/discover/featured.json
%{_datadir}/sddm/themes/01-breeze-aurora/{Background,KeyboardButton,Login,Main,SessionButton}.qml
%{_datadir}/sddm/themes/01-breeze-aurora/default-logo.svg
%{_datadir}/sddm/themes/01-breeze-aurora/metadata.desktop
%{_datadir}/sddm/themes/01-breeze-aurora/preview.png
%{_datadir}/sddm/themes/01-breeze-aurora/theme.conf
%{_datadir}/sddm/themes/01-breeze-aurora/faces/.face.icon


%changelog
%autochangelog
