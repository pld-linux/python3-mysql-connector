#
# Conditional build:
%bcond_with		tests		# build with tests (requires mysql server)
%bcond_without	python3		# build without python3

%define		pname	mysql-connector
Summary:	The MySQL Client/Protocol implemented in Python
Name:		python-%{pname}
Version:	0.3.2
Release:	1
License:	GPL v2
Group:		Libraries/Python
Source0:	http://launchpad.net/myconnpy/0.3/%{version}/+download/mysql-connector-python-%{version}-devel.tar.gz
# Source0-md5:	2ffdfa21c0a870cc7080f9f9a5ee3d87
URL:		https://launchpad.net/myconnpy/
BuildRequires:	python-modules
%{?with_python3:BuildRequires:	python3-modules}
BuildRequires:	rpm-pythonprov
%pyrequires_eq	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MySQL Connector/Python is implementing the MySQL Client/Server
protocol completely in Python. No MySQL libraries are needed, and no
compilation is necessary to run this Python DB API v2.0 compliant
driver. An interface to the popular MySQL database server for Python.

%package -n python3-%{pname}
Summary:	The MySQL Client/Protocol implemented in Python
Group:		Development/Languages/Python
%pyrequires_eq	python3-modules

%description -n python3-%{pname}
MySQL Connector/Python is implementing the MySQL Client/Server
protocol completely in Python. No MySQL libraries are needed, and no
compilation is necessary to run this Python DB API v2.0 compliant
driver. An interface to the popular MySQL database server for Python.

%prep
%setup -q -n mysql-connector-python-%{version}-devel

%build
%{__python} setup.py build
%{?with_tests:%{__python} setup.py test}

%if %{with python3}
%{__python3} setup.py build -b build-3
%{?with_tests:%{__python3} setup.py test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__python} -- setup.py \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%if %{with python3}
%{__python3} -- setup.py \
	build -b build-3 \
	install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%dir %{py_sitescriptdir}/mysql
%{py_sitescriptdir}/mysql/*.py[co]
%dir %{py_sitescriptdir}/mysql/connector
%{py_sitescriptdir}/mysql/connector/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/mysql_connector_python-*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pname}
%defattr(644,root,root,755)
%doc ChangeLog README
%{py3_sitescriptdir}/mysql*.egg-info
%dir %{py3_sitescriptdir}/mysql
%{py3_sitescriptdir}/mysql/*.py
%dir %{py3_sitescriptdir}/mysql/__pycache__
%{py3_sitescriptdir}/mysql/__pycache__/*.py[co]
%dir %{py3_sitescriptdir}/mysql/connector
%{py3_sitescriptdir}/mysql/connector/*.py
%dir %{py3_sitescriptdir}/mysql/connector/__pycache__
%{py3_sitescriptdir}/mysql/connector/__pycache__/*.py[co]
%endif