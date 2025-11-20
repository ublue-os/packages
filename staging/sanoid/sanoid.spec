%global version 2.2.0
%global git_tag v%{version}

# Enable with systemctl "enable sanoid.timer"
%global _with_systemd 1

Name:		   sanoid
Version:	   %{version}
Release:	   1%{?dist}.ucore3
BuildArch:	   noarch
Summary:	   A policy-driven snapshot management tool for ZFS file systems
Group:		   Applications/System
License:	   GPLv3
URL:		   https://github.com/jimsalterjrs/sanoid
Source0:	   https://github.com/jimsalterjrs/%{name}/archive/%{git_tag}/%{name}-%{version}.tar.gz

Requires:	   perl-interpreter, mbuffer, lzop, pv, perl-Config-IniFiles, perl-Capture-Tiny, perl-Sys-Hostname
%if 0%{?_with_systemd}
Requires:      systemd >= 212

BuildRequires: systemd
%endif

%description
Sanoid is a policy-driven snapshot management
tool for ZFS file systems. You can use Sanoid
to create, automatically thin, and monitor snapshots
and pool health from a single eminently
human-readable TOML configuration file.

%prep
%setup -q

%build
echo "Nothing to build"

%install
%{__install} -D -m 0644 sanoid.defaults.conf %{buildroot}/etc/sanoid/sanoid.defaults.conf
%{__install} -d %{buildroot}%{_sbindir}
%{__install} -m 0755 sanoid syncoid findoid sleepymutex %{buildroot}%{_sbindir}

%if 0%{?_with_systemd}
%{__install} -d %{buildroot}%{_unitdir}
%endif

%if 0%{?fedora}
%{__install} -D -m 0644 sanoid.conf %{buildroot}%{_docdir}/%{name}/examples/sanoid.conf
%endif
%if 0%{?rhel}
%{__install} -D -m 0644 sanoid.conf %{buildroot}%{_docdir}/%{name}-%{version}/examples/sanoid.conf
%endif

%if 0%{?_with_systemd}
cat > %{buildroot}%{_unitdir}/%{name}.service <<EOF
[Unit]
Description=Snapshot ZFS Pool
Requires=zfs.target
After=zfs.target
Wants=sanoid-prune.service
Before=sanoid-prune.service
ConditionFileNotEmpty=/etc/sanoid/sanoid.conf

[Service]
Environment=TZ=UTC
Type=oneshot
ExecStart=/usr/sbin/sanoid --take-snapshots --verbose
EOF

cat > %{buildroot}%{_unitdir}/%{name}-prune.service <<EOF
[Unit]
Description=Cleanup ZFS Pool
Requires=zfs.target
After=zfs.target sanoid.service
ConditionFileNotEmpty=/etc/sanoid/sanoid.conf

[Service]
Environment=TZ=UTC
Type=oneshot
ExecStart=/usr/sbin/sanoid --prune-snapshots --verbose

[Install]
WantedBy=sanoid.service
EOF

cat > %{buildroot}%{_unitdir}/%{name}.timer <<EOF
[Unit]
Description=Run Sanoid Every 15 Minutes

[Timer]
OnCalendar=*:0/15
Persistent=true

[Install]
WantedBy=timers.target
EOF

%else
%if 0%{?fedora}
%{__install} -D -m 0644 sanoid.conf %{buildroot}%{_docdir}/%{name}/examples/sanoid.conf
%endif
%if 0%{?rhel}
echo "* * * * * root %{_sbindir}/sanoid --cron" > %{buildroot}%{_docdir}/%{name}-%{version}/examples/sanoid.cron
%endif
%endif

%post
%{?_with_systemd:%{_bindir}/systemctl daemon-reload || :}

%postun
%{?_with_systemd:%{_bindir}/systemctl daemon-reload || :}

%files
%doc CHANGELIST VERSION README.md FREEBSD.readme
%license LICENSE
%{_sbindir}/sanoid
%{_sbindir}/syncoid
%{_sbindir}/findoid
%{_sbindir}/sleepymutex
%dir %{_sysconfdir}/%{name}
%config %{_sysconfdir}/%{name}/sanoid.defaults.conf
%if 0%{?fedora}
%{_docdir}/%{name}
%endif
%if 0%{?rhel}
%{_docdir}/%{name}-%{version}
%endif
%if 0%{?_with_systemd}
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-prune.service
%{_unitdir}/%{name}.timer
%endif

%changelog
* Thu Nov 20 2025 Benjamin Sherman <benjamin@holyarmy.org> - 2.2.0.ucore3
- Safely handle container installs where systemd is not running
* Wed Oct 13 2024 John McGee <john@johnmcgee.net> - 2.2.0.ucore2
- Correct typo in systemctl description
* Wed Oct 09 2024 John McGee <john@johnmcgee.net> - 2.2.0.ucore1
- Correct systemctl scripts Exec path
* Tue Mar 19 2024 John McGee <john@johnmcgee.net> - 2.2.0.ucore
- Remove perl requirement to remove build tools
- Add perl-interpreter and perl-Sys-Hostname requirements
- Correct systemd units to incluide sanoid-prune
* Tue Jul 18 2023 Christoph Klaffl <christoph@phreaker.eu> - 2.2.0
- Bump to 2.2.0
* Tue Nov 24 2020 Christoph Klaffl <christoph@phreaker.eu> - 2.1.0
- Bump to 2.1.0
* Wed Oct 02 2019 Christoph Klaffl <christoph@phreaker.eu> - 2.0.3
- Bump to 2.0.3
* Wed Sep 25 2019 Christoph Klaffl <christoph@phreaker.eu> - 2.0.2
- Bump to 2.0.2
* Tue Dec 04 2018 Christoph Klaffl <christoph@phreaker.eu> - 2.0.0
- Bump to 2.0.0
* Sat Apr 28 2018 Dominic Robinson <github@dcrdev.com> - 1.4.18-1
- Bump to 1.4.18
* Thu Aug 31 2017 Dominic Robinson <github@dcrdev.com> - 1.4.14-2
- Add systemd timers
* Wed Aug 30 2017 Dominic Robinson <github@dcrdev.com> - 1.4.14-1
- Version bump
* Wed Jul 12 2017 Thomas M. Lapp <tmlapp@gmail.com> - 1.4.13-1
- Version bump
- Include FREEBSD.readme in docs
* Wed Jul 12 2017 Thomas M. Lapp <tmlapp@gmail.com> - 1.4.9-1
- Version bump
- Clean up variables and macros
- Compatible with both Fedora and Red Hat
* Sat Feb 13 2016 Thomas M. Lapp <tmlapp@gmail.com> - 1.4.4-1
- Initial RPM Package
