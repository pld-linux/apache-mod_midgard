# TODO
# - not compatible with apache2 (is it apache1 module?)
%define		mod_name	midgard
%define		arname		mod_midgard
%define 	apxs		/usr/sbin/apxs
Summary:	Midgard Apache module
Summary(pl.UTF-8):	Moduł Midgard do Apache
Name:		apache-mod_midgard
Version:	1.4.1_5
Release:	2
License:	distributable
Vendor:		Midgard Project <http://www.midgard-project.org>
Group:		Networking/Daemons/HTTP
Source0:	%{arname}-%{version}.tar.bz2
# Source0-md5:	9b00986652ed2b495aebc23ec2337bb1
#Source0:	http://www.midgard-project.org/attachment/434f392e6f87e1e76202f00695dd251f/599f017caa73216fbf3d676ff086d37f/%{arname}-1.4.1-5.tar.bz2
Patch0:		%{arname}-conf.patch
URL:		http://www.midgard-project.org/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	expat-devel
BuildRequires:	midgard-lib-devel >= 1.4.1-5
BuildRequires:	mysql-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
%requires_eq_to midgard-lib midgard-lib-devel
Provides:	mod_midgard
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%prep
%setup -q -n %{arname}-%{version}
%patch -P0 -p1

%description
Midgard is a freely-available Web application development and
publishing platform based on the popular PHP scripting language. It is
an Open Source development project, giving you the freedom to create
your solutions in an open environment. Midgard is the tool for
creating, modifying and maintaining dynamic database-enabled web
services.

%description -l pl.UTF-8
Midgard jest wolnodostępną platformą rozwoju i publikowania aplikacji
opartą na popularnym języku skryptowym, PHP. Jest to projekt Open
Source, umożliwiający użytkownikowi tworzenie rozwiązań w otwartym
środowisku. Midgard jest narzędziem do tworzenia, modyfikacji i
utrzymywania dynamicznych, wykorzystujących bazy danych serwisów WWW.

%build
./configure \
	--with-apxs=%{apxs} \
	--with-mysql \
	--with-midgar \
	--with-expat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

cp -p midgard-root.php $RPM_BUILD_ROOT%{_pkglibdir}
install -p mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p midgard.conf $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog INSTALL INSTALL.ru NEWS README README.ru
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
# FIXME
%config %{_pkglibdir}/midgard-root.php
