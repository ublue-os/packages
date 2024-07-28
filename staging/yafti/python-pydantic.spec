Name:           python-pydantic
Version:        1.10.2
Release:        1%{?dist}
Summary:        Data validation using Python type hinting

License:        MIT
URL:            https://github.com/samuelcolvin/pydantic
Source0:        https://github.com/samuelcolvin/pydantic/archive/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
# For check phase
BuildRequires:  python3-mypy
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(hypothesis)

%description
Data validation and settings management using python type hinting.

%package -n     python3-pydantic
Summary:        %{summary}
%{?python_provide:%python_provide python3-pydantic}
 
Requires:       python3-email-validator >= 1.0.3
Requires:       python3-ujson >= 1.35

%description -n python3-pydantic
Data validation and settings management using python type hinting.

%prep
%autosetup -n pydantic-%{version}
# Remove bundled egg-info
rm -rf pydantic.egg-info

%build
%py3_build

# Docs are in MarkDown, and should be added when mkdocs is packaged.

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-pydantic
%license LICENSE
%doc README.md docs/
%{python3_sitelib}/pydantic
%{python3_sitelib}/pydantic-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Sep 07 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.10.2-1
- Update to 1.10.2.

* Thu Sep 01 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.10.1-1
- Update to 1.10.1.

* Wed Aug 24 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.9.1-2
- Rebuilt for Python 3.11

* Thu Jun 09 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1.

* Wed Feb 02 2022 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.4-2
- Rebuilt for Python 3.10

* Tue May 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.4-1
- Update to 1.7.4; fixes CVE-2021-29510

* Wed Feb 24 2021 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.3-3
- python-email_validator is now packaged as python-email-validator...

* Tue Jan 07 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.3-2
- Review fixes.

* Mon Jan 06 2020 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.3-1
- Update to 1.3.
- Review fixes.

* Sun Nov 24 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1.

* Sat Jul 27 2019 Susi Lehtola <jussilehtola@fedoraproject.org> - 0.31-1
- Initial package.
