%global debug_package %{nil}
%global vendor bluefin

Name:           bluefin-readymade-config
Version:        0.1.0
Release:        1%{?dist}
Summary:        Bluefin branding for Readymade

License:        CC-BY-CA
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source0:        {{{ git_dir_pack }}}
Source1:        https://github.com/FyraLabs/readymade/archive/refs/tags/v0.12.2.tar.gz

BuildArch: noarch

%description
Branding for Bluefin's Readymade config

%prep
{{{ git_dir_setup_macro }}}
mkdir -p readymade
tar xzvf ./%{SOURCE1}

%build
install -Dpm0644 src/bento/middle-left.jxl ./readymade-0.12.2/data/viewports-light.webp
install -Dpm0644 src/bento/middle-left-dark.jxl ./readymade-0.12.2/data/viewports-dark.webp
install -Dpm0644 src/bento/top-right.jxl ./readymade-0.12.2/data/umbrella-light.webp
install -Dpm0644 src/bento/top-right-dark.jxl ./readymade-0.12.2/data/umbrella-dark.webp
install -Dpm0644 src/bento/bottom-right.jxl ./readymade-0.12.2/data/blueprint.webp
install -Dpm0644 src/bento/bottom-right-dark.jxl ./readymade-0.12.2/data/blueprint-dark.webp

pushd ./readymade-0.12.2/data

# FIXME: remove once https://github.com/FyraLabs/readymade/pull/92 is merged
sed -i '/<file>blueprint.webp<\/file>/a \        <file>blueprint-dark.webp</file>' ./resources.gresource.xml
tee -a ./style-dark.css <<EOF
.installation-bento-card.contribute-card {
    background-position: bottom;
    background-image: url("blueprint-dark.webp");
}
EOF
glib-compile-resources resources.gresource.xml
mv *.gresource ../..
popd

pushd ./readymade-0.12.2/po/en-US
sed -i \
    -e 's@page-installation-help-desc.*@page-installation-help-desc = Ask questions on our forums!@' \
    -e 's@page-installation-contrib = .*@page-installation-contrib = Read the Documentation@' \
    -e 's@page-installation-contrib-desc.*@page-installation-contrib-desc = Set yourself up for success by reading the docs@' \
    ./readymade.ftl
popd

%install
install -Dpm0644 ./*.gresource %{buildroot}%{_datadir}/readymade/resources/bluefin.gresource
install -Dpm0644 -t %{buildroot}%{_datadir}/readymade/repart-cfgs/bootcwholedisk/ src/repart/*.conf
for f in readymade-0.12.2/po/*; do
    install -Dpm644 $f/readymade.ftl %{buildroot}%{_datadir}/readymade/bento/po/$(basename $f)/readymade.ftl
done

%check

%files
%{_datadir}/readymade/

%changelog
%autochangelog
