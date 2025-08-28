Name:           ublue-os-just
Vendor:         ublue-os
Version:        0.50
Release:        1%{?dist}
Summary:        ublue-os just integration
License:        Apache-2.0
URL:            https://github.com/ublue-os/packages
VCS:            {{{ git_dir_vcs }}}
Source:         {{{ git_dir_pack }}}

BuildArch:      noarch

# Needed for generating shell completions
BuildRequires: just

Requires:       just
Requires:       ublue-os-luks
Recommends:     powerstat

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^ublue%-os%-", ""); print(t)}

%description
Adds ublue-os just integration for easier setup

%prep
{{{ git_dir_setup_macro }}}

%build

%install
install -d -m0755 %{buildroot}%{_sysconfdir}/profile.d
install -Dpm0755 ./src/etc-profile.d/* %{buildroot}%{_sysconfdir}/profile.d/

install -d -m0755 %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}
install -Dpm0644 ./src/recipes/*  %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/

install -d -m0755 %{buildroot}%{_datadir}/%{VENDOR}/motd/tips
install -Dpm0644 ./src/ublue-tips/* %{buildroot}%{_datadir}/%{VENDOR}/motd/tips/

# Create justfile which contains all .just files included in this package
# Apply header first due to default not working in included justfiles
install -Dpm0644 ./src/header.just "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
for justfile in %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/*.just; do
    echo "import \"%{_datadir}/%{VENDOR}/%{sub_name}/$(basename ${justfile})\"" >> "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
done
echo "import? \"%{_datadir}/%{VENDOR}/%{sub_name}/60-custom.just\"" >> "%{buildroot}%{_datadir}/%{VENDOR}/justfile"

# Add global "ujust" script to run just with --unstable
install -Dpm0755 ./src/ujust %{buildroot}%{_bindir}/ujust
install -Dpm0755 ./src/ugum %{buildroot}%{_bindir}/ugum

# Add bash library for use in just
install -d -m0755 %{buildroot}/%{_exec_prefix}/lib/ujust/
install -Dpm0644 ./src/lib-ujust/* %{buildroot}/%{_exec_prefix}/lib/ujust/

# Add default manifest files for distrobox
install -d -m0755 %{buildroot}/%{_sysconfdir}/distrobox
install -Dpm0644 ./src/etc-distrobox/* %{buildroot}/%{_sysconfdir}/distrobox/

# Add default manifest file for toolbox
install -d -m0755 %{buildroot}/%{_sysconfdir}/toolbox
install -Dpm0644 ./src/etc-toolbox/* %{buildroot}/%{_sysconfdir}/toolbox/


mkdir -p %{buildroot}%{bash_completions_dir} %{buildroot}%{zsh_completions_dir} %{buildroot}%{fish_completions_dir}

# Generate ujust bash completion
just --completions bash | sed -E 's/([\(_" ])just/\1ujust/g' > %{buildroot}%{bash_completions_dir}/ujust

# Generate ujust zsh completion
just --completions zsh | sed -E 's/([\(_" ])just/\1ujust/g' > %{buildroot}%{zsh_completions_dir}/_ujust

# Generate ujust fish completion
just --completions fish | sed -E 's/([\(_" ])just/\1ujust/g' > %{buildroot}%{fish_completions_dir}/ujust.fish

%check
find %{buildroot}/%{_datadir}/%{VENDOR}/%{sub_name}/ -type f -name "*.just" | while read -r file; do
  just --unstable --fmt --check -f $file
done

%files
%{_sysconfdir}/profile.d/user-motd.sh
%{_datadir}/%{VENDOR}/%{sub_name}/*.just
%{_datadir}/%{VENDOR}/justfile
%{_datadir}/%{VENDOR}/motd/tips/*.md
%{_bindir}/ujust
%{_bindir}/ugum
%{_exec_prefix}/lib/ujust/ujust.sh
%{_exec_prefix}/lib/ujust/lib*.sh
%{_sysconfdir}/distrobox/*.ini
%{_sysconfdir}/toolbox/*.ini
%{bash_completions_dir}/ujust
%{zsh_completions_dir}/_ujust
%{fish_completions_dir}/ujust.fish

%changelog
* Mon Aug 04 2025 renner <renner0@posteo.de> - 0.49
- Add %check for .just files

* Sat Jun 28 2025 renner <renner0@posteo.de> - 0.48
- Add alias to davinci-resolve

* Tue Jun 03 2025 omid-1985 <omid.1985@gmail.com> - 0.47
- Add brew autoremove and cleanup to clean-system recipe

* Thu May 22 2025 renner0e <Renner03@protonmail.com> - 0.46
- Generate ujust shell completions at build time

* Wed May 21 2025 coxde <63153334+coxde@users.noreply.github.com> - 0.45
- Fix fish completion directory

* Sun May 18 2025 renner0e <Renner03@protonmail.com> - 0.45
- move brew.sh to ublue-brew

* Mon May 12 2025 coxde <63153334+coxde@users.noreply.github.com> - 0.44
- Add fish ujust completion

* Tue May 06 2025 renner0e <Renner03@protonmail.com> - 0.43
- Change arch-distrobox tag to arch-toolbox

* Wed Feb 26 2025 Robert Sturla <robertsturla@outlook.com> - 0.41
- Make 60-custom.just an optional import
- Remove default 60-custom.just from the package

* Mon Feb 17 2025 Tulip Blossom <tulilirockz@outlook.com> - 0.39
- Remove ublue-os-just.sh from /etc/profile.d

* Sun Feb 09 2025 renner0e <Renner03@protonmail.com> - 0.38
- Added ujust tab completion file for zsh generated from just --completions zsh

* Fri Nov 29 2024 HikariKnight <hk@bazzite.gg> - 0.37
- Remove obs-studio-portable

* Fri Sep 20 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.36
- Remove no longer needed brew commands, now on image

* Fri May 31 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.35
- Make toggle-updates smarter and detect if ublue-update is installed

* Sat May 18 2024 m2Giles <69128853+m2Giles@users.noreply.github.com> - 0.34
- Fix missing sourcefile for just split out

* Wed May 15 2024 m2Giles <69128853+m2Giles@users.noreply.github.com> - 0.33
- Split brew just file out

* Wed May 01 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.32
- Add powerstat

* Tue Apr 30 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.31
- Add LUKS TPM autounlock support

* Sun Mar 24 2024 gerblesh <101901964+gerblesh@users.noreply.github.com> - 0.30
- Add brew config to /etc/profile.d

* Fri Feb 23 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.29
- Add option to use toolbox in ujust

* Thu Feb 22 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.28
- Remove nix justfile

* Mon Jan 29 2024 RJ Trujillo <eyecantcu@pm.me> - 0.27
- Add bluefin-cli and wolfi-toolbox to distrobox assemble config

* Mon Jan 29 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.26
- Improve versatility of user-motd

* Sat Jan 27 2024 Benjamin Sherman <benjamin@holyarmy.org> - 0.25
- Add user-motd and just toggle

* Sat Jan 20 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.24
- Add default distrobox manifests as part of rpm

* Thu Jan 18 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.23
- Added tooling for distrobox

* Sun Jan 14 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.22
- Added sourcable libraries for just recipes

* Wed Jan 10 2024 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.21
- Added ujust tab completion file generated from just --completions bash

* Thu Jan 04 2024 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.20
- Update with support for the newest version of just

* Wed Dec 20 2023 HikariKnight <2557889+HikariKnight@users.noreply.github.com> - 0.10
- Add ugum, a helper for user input for use in just

* Tue Nov 28 2023 RJ Trujillo <eyecantcu> - 0.9
- Copy nix justfile to correct location and restore ujust

* Sat Nov 25 2023 RJ Trujillo <eyecantcu@pm.me> - 0.8
- Integrate justfile for nix

* Fri Oct 13 2023 bri <284789+b-@users.noreply.github.com> - 0.7
- Add ujust runner
- Add chsh task

* Mon Oct 2 2023 ArtikusHG <24320212+ArtikusHG@users.noreply.github.com> - 0.6
- Add commands to disable and enable automatic updates to 60-updates.just

* Sat Sep 23 2023 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.5
- Remove fish shell support

* Thu Sep 21 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.4
- Correct justfile include paths

* Thu Sep 21 2023 Kyle Gospodnetich <me@kylegospodneti.ch> - 0.3
- Modify just files to be numbered for ordered loading
- Move to using a single master justfile
- Clean up previous installs to point to new file
- Add support for fish shell

* Sat May 13 2023 Benjamin Sherman <benjamin@holyarmy.org> - 0.2
- Refactor directory structure
- Rename justfile to main.just
- Add nvidia.just and custom.just
- Make profile script intelligent about including nvidia.just

* Sun Mar 05 2023 Joshua Stone <joshua.gage.stone@gmail.com> - 0.1
- Add justfile integration
