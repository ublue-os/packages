Name:           uwelcome
Version:        0.5.1
Release:        1%{?dist}
Summary:        Configurable CLI Banner made for your favorite Linux systems
Vendor:         projectbluefin
URL:            https://github.com/%{vendor}/%{name}
Source0:        %{url}/archive/refs/tags/v{version}.tar.gz
License:        Apache-2.0

BuildRequires:  golang
Provides:       %{name} = %{version}

%description
%{summary}

%prep
%autosetup

%build
go build -v -o %{name}

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

%check
go test -v ./...

%files
%{_bindir}/%{name}
%changelog
%autochangelog
