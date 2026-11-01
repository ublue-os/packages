# SPDX-License-Identifier: GPL-2.0-only

Name:           gc570d
# renovate: datasource=github-releases depName=neoyagami/OpenGC570D
Version:        1.0.5
Release:        1%{?dist}
Summary:        Integration files for the OpenGC570D capture-card driver
License:        GPL-2.0-only
URL:            https://github.com/neoyagami/OpenGC570D
Source0:        %{url}/archive/refs/tags/v%{version}/OpenGC570D-%{version}.tar.gz

BuildArch:      noarch
Provides:       %{name}-kmod-common = %{version}-%{release}
Requires:       %{name}-kmod >= %{version}
Recommends:     wireplumber

%description
Documentation and WirePlumber integration for the experimental OpenGC570D
Linux driver for the AVerMedia Live Gamer DUO GC570D PCIe capture card.

The matching kernel-module RPM is built separately for the exact distribution
kernel from the same released source archive.

%prep
%autosetup -n OpenGC570D-%{version}

%build
# No architecture-independent files need to be built.

%check
test -f config/wireplumber/51-gc570d.conf
grep -F 'AVerMedia Live Gamer DUO' config/wireplumber/51-gc570d.conf

%install
install -D -m 0644 config/wireplumber/51-gc570d.conf \
    %{buildroot}%{_datadir}/wireplumber/wireplumber.conf.d/51-gc570d.conf

%files
%license LICENSE
%doc README.md NOTICE.md MAINTAINERS.md SECURITY.md CONTRIBUTING.md
%doc docs/DATA_PROVENANCE.md docs/INSTALL.md docs/LEGAL.md
%doc docs/PACKAGING.md docs/REVERSE_ENGINEERING.md docs/STATUS.md docs/USAGE.md
%{_datadir}/wireplumber/wireplumber.conf.d/51-gc570d.conf

%changelog
* Sat Oct 24 2026 neoyagami <neoyagami@gmail.com> - 1.0.5-1
- Add the initial Universal Blue common package
- Install documentation and the system WirePlumber capture policy
