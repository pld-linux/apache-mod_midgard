%define         mod_name        midgard
%define		arname		mod_midgard
Summary:	Midgard Apache module
Summary(pl):	Modu³ Midgard do Apache
Name:		apache-mod_midgard
Version:	1.4.1_5
Release:	0.1
License:	distributable
Vendor:		Midgard Project <http://www.midgard-project.org>
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	%{arname}-%{version}.tar.bz2
#Source0:	http://www.midgard-project.org/attachment/434f392e6f87e1e76202f00695dd251f/599f017caa73216fbf3d676ff086d37f/%{arname}-1.4.1-5.tar.bz2
Patch0:		%{arname}-conf.patch
URL:		http://www.midgard-project.org/
Requires:	midgard-lib = %{version}, apache >= 1.3.12
Provides:	mod_midgard
BuildRequires:	midgard-lib-devel = %{version}
BuildRequires:	expat-devel
BuildRequires:	mysql-devel
BuildRequires:	apache >= 1.3.12
BuildRequires:	apache-devel >= 1.3.12
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _pkglibdir      %(%{_sbindir}/apxs -q LIBEXECDIR)
%define         _sysconfdir     /etc/httpd

%prep
%setup -q -n %{arname}-%{version}
%patch0 -p1

%description
Midgard is a freely-available Web application development and
publishing platform based on the popular PHP scripting language. It is
an Open Source development project, giving you the freedom to create
your solutions in an open environment. Midgard is the tool for
creating, modifying and maintaining dynamic database-enabled web
services.

%description -l pl
Midgard jest wolnodostêpn± platform± rozwoju i publikowania aplikacji
opart± na popularnym jêzyku skryptowym, PHP. Jest to projekt Open
Source, umo¿liwiaj±cy u¿ytkownikowi tworzenie rozwi±zañ w otwartym
¶rodowisku. Midgard jest narzêdziem do tworzenia, modyfikacji i
utrzymywania dynamicznych, wykorzystuj±cych bazy danych serwisów WWW.

%build
./configure \
	--with-apxs=/usr/sbin/apxs \
	--with-mysql \
	--with-midgar \
	--with-expat
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install midgard-root.php $RPM_BUILD_ROOT%{_pkglibdir}
install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install midgard.conf $RPM_BUILD_ROOT%{_sysconfdir}

gzip -9nf AUTHORS COPYING ChangeLog INSTALL INSTALL.ru NEWS README README.ru

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
echo "Include %{_sysconfdir}/%{mod_name}.conf" >> %{_sysconfdir}/httpd.conf
if [ -f /var/lock/subsys/httpd ]; then
    /etc/rc.d/init.d/httpd restart 1>&2
fi
	
%preun
if [ "$1" = "0" ]; then
    %{_sbindir}/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
    %__perl -pi -e "s|Include %{_sysconfdir}/%{mod_name}.conf\n||g;" \
            %{_sysconfdir}/httpd.conf
    if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
    fi
fi

%files
%defattr(644,root,root,755)
%config %{_pkglibdir}/midgard-root.php
%config(noreplace) %{_sysconfdir}/midgard.conf
%attr(755,root,root) %{_pkglibdir}/mod_midgard.so
%doc *.gz
