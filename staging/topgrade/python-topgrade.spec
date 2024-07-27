Name:           python-topgrade
Version:        14.0.1
Release:        %autorelease
Summary:        Upgrade all the things

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        GPL-3.0
URL:            https://pypi.org/project/topgrade/
Source:         %{pypi_source topgrade}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  cargo
BuildRequires:  rust

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'topgrade' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-topgrade
Summary:        %{summary}

%description -n python3-topgrade %_description


%prep
%autosetup -p1 -n topgrade-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


%check
%pyproject_check_import


%files -n python3-topgrade -f %{pyproject_files}


%changelog
%autochangelog