Summary:  Midgard Apache module
Name: mod_midgard
Version: 1.2.1
Release: 5mdk
URL: http://www.midgard-project.org/
Packager: Jean-Michel Dault <jmdault@netrevolution.com>
Vendor: Midgard Project <http://www.midgard-project.org>
Source: mod_midgard-%{version}.tar.bz2
Source1: %{name}.conf
Copyright: distributable
Group: System Environment/Daemons
Requires: mysql-shared-libs, apache = 1.3.9, midgard-lib = %{version}
Provides: mod_midgard
BuildRoot: /var/tmp/%{name}-root

%prep
%setup

%description
Midgard is a freely-available Web application development and
publishing platform based on the popular PHP scripting language. It is
an Open Source development project, giving you the freedom to create
your solutions in an open environment. Midgard is the tool for
creating, modifying and maintaining dynamic database-enabled web
services.

%description
Midgard jest wolnodostêpn± platform± rozwoju i publikowania aplikacji 
opart± na popularnym jêzyku skryptowym, PHP. Jest to projekt Open Source,
umo¿liwiaj±cy uzytkownikowi tworzenie rozwi±zañ w otwartym ¶rodowisku.
Midgard jest narzêdziem do tworzenia, modyfikacji i utrzymywania 
dynamicznych, wykorzystuj±cych bazy danych serwisów WWW.



%build
CFLAGS=$RPM_OPT_FLAGS PATH=/usr/sbin/:$PATH LDFLAGS="-L/usr/lib/mysql -lmidgard -lmysqlclient" ./configure --with-midgard=/usr/
make

%install
mkdir -p $RPM_BUILD_ROOT/home/httpd/html/
mkdir -p $RPM_BUILD_ROOT/usr/lib/apache/
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf/addon-modules/

cp midgard-root.php3 $RPM_BUILD_ROOT/home/httpd/html/
cp *.so $RPM_BUILD_ROOT/usr/lib/apache/

cp %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf/addon-modules/


%post
echo "Include conf/addon-modules/%{name}.conf" >> /etc/httpd/conf/httpd.conf
if [ -f /etc/httpd/httpd.pid ]; then 
   /usr/sbin/apachectl restart
fi

%postun
if [ `uname` = "Linux" ]; then perl="/usr/bin/perl"; fi
if [ `uname` = "SunOS" ]; then perl="/usr/local/bin/perl"; fi
$perl -pi -e "s|Include conf/addon-modules/%{name}.conf\n||g;" \
	/etc/httpd/conf/httpd.conf
if [ -f /etc/httpd/httpd.pid ]; then 
   /usr/sbin/apachectl restart
fi


%files
%config /home/httpd/html/midgard-root.php3
/usr/lib/apache/mod_midgard.so
/etc/httpd/conf/addon-modules/%{name}.conf

%changelog

* Mon Sep 06 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- put in Group: System Environment/Daemons
- re-build for EAPI 2.4.2 and mm 1.0.11

* Fri Sep 03 1999 Jean-Michel Dault <jmdault@netrevolution.com>
- updated to 1.2.1
- fixed dependancies
