%global debug_package %{nil}

Name:           ublue-recipes
Version:        0.1.1
Release:        1%{?dist}
Summary:        Shared Ujust recipes

License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

Recommends:     glow
Recommends:     gum
Requires:       ublue-os-just

%description
Shared ujust recipes for Universal Blue systems

%prep
{{{ git_dir_setup_macro }}}

%build
for file in src/recipes/*.just ; do
	cat <<EOF >> recipes.just

########################
### $(basename $file)
########################

EOF
	cat $file >> recipes.just
done

%install
install -Dm0644 -t %{buildroot}/%{_datadir}/ublue-os/recipes recipes.just

# Breaks the build on te CentOS default chroot on COPR, we need to enable EPEL
# %check
# just --unstable --fmt --check -f recipes.just

%files
%{_datadir}/ublue-os/recipes/recipes.just

%changelog
%autochangelog
