%define _unpackaged_files_terminate_build 0

%define core_arches %{ix86} x86_64
Summary: The Ice base runtime and services
Name: ice
Version: 3.2b
Release: 1
License: GPL
Group:System Environment/Libraries
Vendor: ZeroC, Inc
URL: http://www.zeroc.com/
Source0: Ice-%{version}.tar.gz
Source1: IceJ-%{version}-java2.tar.gz
Source2: IcePy-%{version}.tar.gz
Source3: IceCS-%{version}.tar.gz
Source4: IceJ-%{version}-java5.tar.gz
Source5: IcePHP-%{version}.tar.gz
Source6: Ice-rpmbuild-%{version}.tar.gz
Source7:IceRuby-%{version}.tar.gz

BuildRoot: /var/tmp/Ice-%{version}-1-buildroot

%define soversion 32b

%ifarch x86_64
%define icelibdir lib64
%else
%define icelibdir lib
%endif

BuildRequires: mono-core >= 1.2.2
BuildRequires: python >= 2.3.4
BuildRequires: python-devel >= 2.3.4
BuildRequires: expat >= 1.95.7
BuildRequires: libstdc++ >= 3.4.6
BuildRequires: gcc >= 3.4.6
BuildRequires: gcc-c++ >= 3.4.6
BuildRequires: tar
BuildRequires: sed
BuildRequires: binutils >= 2.15
BuildRequires: openssl >= 0.9.7a
BuildRequires: openssl-devel >= 0.9.7a
BuildRequires: bzip2-devel >= 1.0.2
BuildRequires: bzip2-libs >= 1.0.2
BuildRequires: db45 >= 4.5.20
BuildRequires: db45-devel >= 4.5.20
BuildRequires: expat-devel >= 1.95.7
BuildRequires: php >= 5.1.4
BuildRequires: php-devel >= 5.1.4

Provides: ice-%{_arch}
%description
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%prep

#
# The Ice make system does not allow the prefix directory to be specified
# through an environment variable or a command line option.  So we edit some
# files in place with sed.
#

#
# C++, Java2 and C# are needed for any arch
#
%setup -n Ice-%{version} -q -T -D -b 0
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/Ice-%{version}/config/Make.rules

%setup -q -n IceJ-%{version}-java2 -T -D -b 1

%setup -q -n IceCS-%{version} -T -D -b 3

%ifarch noarch
#
# We only build C# for noarch
#
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IceCS-%{version}/config/Make.rules.cs
sed -i -e 's/^cvs_build.*$/cvs_build = no/' $RPM_BUILD_DIR/IceCS-%{version}/config/Make.rules.cs
%endif

%ifarch %{core_arches}
#
# There is no noarch python, php or ruby RPM
#
%setup -q -n IcePy-%{version} -T -D -b 2
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IcePy-%{version}/config/Make.rules

%setup -q -n IcePHP-%{version} -T -D -b 5 
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IcePHP-%{version}/config/Make.rules

%setup -q -n IceRuby-%{version} -T -D -b 7
sed -i -e 's/^prefix.*$/prefix = $\(RPM_BUILD_ROOT\)/' $RPM_BUILD_DIR/IceRuby-%{version}/config/Make.rules

%setup -c -q -n Ice-rpmbuild-%{version} -T -D -b 6
%endif

%ifarch noarch
#
# Since we also have Java2 for IceGridGUI.jar and the demos, Java5 is purely noarch
#
%setup -q -n IceJ-%{version}-java5 -T -D -b 4
%endif

%build

#
# We need the slice2xxx translators all the time
#
cd $RPM_BUILD_DIR/Ice-%{version}/src
gmake OPTIMIZE=yes RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""

%ifarch %{core_arches}
cd $RPM_BUILD_DIR/IcePy-%{version}
gmake  OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""

cd $RPM_BUILD_DIR/IcePHP-%{version}
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""

cd $RPM_BUILD_DIR/IceRuby-%{version}
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix=""
%endif

%ifarch noarch
#
# We only build C# for noarch
#
cd $RPM_BUILD_DIR/IceCS-%{version}/src
export PATH=$RPM_BUILD_DIR/Ice-%{version}/bin:$PATH
export LD_LIBRARY_PATH=$RPM_BUILD_DIR/Ice-%{version}/lib:$LD_LIBRARY_PATH
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT
%endif

%install

rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/lib
if test ! -d $RPM_BUILD_ROOT/%{icelibdir};
then
    mkdir -p $RPM_BUILD_ROOT/%{icelibdir}
fi

%ifarch %{core_arches}
cd $RPM_BUILD_DIR/Ice-%{version}
gmake RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix="" install
rm $RPM_BUILD_ROOT/bin/slice2vb

cd $RPM_BUILD_DIR/IcePy-%{version}
gmake ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix="" install

cd $RPM_BUILD_DIR/IcePHP-%{version}
gmake ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT install

cp -p $RPM_BUILD_DIR/IceJ-%{version}-java2/lib/IceGridGUI.jar $RPM_BUILD_ROOT/lib/IceGridGUI.jar
cp -pR $RPM_BUILD_DIR/IceJ-%{version}-java2/ant $RPM_BUILD_ROOT

cd $RPM_BUILD_DIR/IceRuby-%{version}
gmake OPTIMIZE=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT embedded_runpath_prefix="" install

#
# .NET spec files (for csharp-devel)
#
if test ! -d $RPM_BUILD_ROOT/%{icelibdir}/pkgconfig ; 
then 
    mkdir $RPM_BUILD_ROOT/%{icelibdir}/pkgconfig
fi

for f in icecs glacier2cs iceboxcs icegridcs icepatch2cs icestormcs; 
do 
    cp $RPM_BUILD_DIR/IceCS-%{version}/lib/pkgconfig/$f.pc $RPM_BUILD_ROOT/%{icelibdir}/pkgconfig 
done

#
# RPM-support files
#
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/README.Linux-RPM $RPM_BUILD_ROOT/README
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/THIRD_PARTY_LICENSE.Linux $RPM_BUILD_ROOT/THIRD_PARTY_LICENSE
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/SOURCES.Linux $RPM_BUILD_ROOT/SOURCES
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/ice.ini $RPM_BUILD_ROOT/ice.ini

mkdir -p $RPM_BUILD_ROOT/etc
cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/*.conf $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/etc/init.d
for i in icegridregistry icegridnode glacier2router
do
    cp $RPM_BUILD_DIR/Ice-rpmbuild-%{version}/$i.redhat $RPM_BUILD_ROOT/etc/init.d/$i
done
%endif

%ifarch noarch
cp -p $RPM_BUILD_DIR/IceJ-%{version}-java5/lib/Ice.jar $RPM_BUILD_ROOT/lib/Ice.jar
mkdir -p $RPM_BUILD_ROOT/lib/java2
cp -p $RPM_BUILD_DIR/IceJ-%{version}-java2/lib/Ice.jar $RPM_BUILD_ROOT/lib/java2/Ice.jar

cd $RPM_BUILD_DIR/IceCS-%{version}
export PATH=$RPM_BUILD_DIR/Ice-%{version}/bin:$PATH
export LD_LIBRARY_PATH=$RPM_BUILD_DIR/Ice-%{version}/lib:$LD_LIBRARY_PATH
gmake NOGAC=yes ICE_HOME=$RPM_BUILD_DIR/Ice-%{version} RPM_BUILD_ROOT=$RPM_BUILD_ROOT install

for f in icecs glacier2cs iceboxcs icegridcs icepatch2cs icestormcs; 
do 
    cp $RPM_BUILD_DIR/IceCS-%{version}/bin/$f.dll $RPM_BUILD_ROOT/bin
done
%endif

#
# The following commands transform a standard Ice installation directory
# structure to a directory structure more suited to integrating into a
# Linux system.
#

mkdir -p $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/lib $RPM_BUILD_ROOT/usr/lib

if test -d $RPM_BUILD_ROOT/%{icelibdir}
then
    mv $RPM_BUILD_ROOT/%{icelibdir} $RPM_BUILD_ROOT/usr/%{icelibdir}
fi

%ifarch %{core_arches}
mkdir -p $RPM_BUILD_ROOT/etc/php.d
mv $RPM_BUILD_ROOT/ice.ini $RPM_BUILD_ROOT/etc/php.d/ice.ini

mkdir -p $RPM_BUILD_ROOT/usr/%{icelibdir}/php/modules
mv $RPM_BUILD_ROOT/usr/%{icelibdir}/IcePHP.so $RPM_BUILD_ROOT/usr/%{icelibdir}/php/modules/IcePHP.so

mkdir -p $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/config $RPM_BUILD_ROOT/usr/share/Ice-%{version}

mkdir -p $RPM_BUILD_ROOT/usr/share
mv $RPM_BUILD_ROOT/slice $RPM_BUILD_ROOT/usr/share/slice

mkdir -p $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/include $RPM_BUILD_ROOT/usr/include

mkdir -p $RPM_BUILD_ROOT/usr/%{icelibdir}/Ice-%{version}
mv $RPM_BUILD_ROOT/python $RPM_BUILD_ROOT/usr/%{icelibdir}/Ice-%{version}/python

mkdir -p $RPM_BUILD_ROOT/usr/%{icelibdir}/Ice-%{version}
mv $RPM_BUILD_ROOT/ruby $RPM_BUILD_ROOT/usr/%{icelibdir}/Ice-%{version}/ruby

mkdir -p $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}
mv $RPM_BUILD_ROOT/doc $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}/doc
mv $RPM_BUILD_ROOT/README $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}/README
mv $RPM_BUILD_ROOT/ICE_LICENSE $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}/ICE_LICENSE
mv $RPM_BUILD_ROOT/LICENSE $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}/LICENSE
mv $RPM_BUILD_ROOT/THIRD_PARTY_LICENSE $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}/THIRD_PARTY_LICENSE
mv $RPM_BUILD_ROOT/SOURCES $RPM_BUILD_ROOT/usr/share/doc/Ice-%{version}/SOURCES

mkdir -p $RPM_BUILD_ROOT/usr/lib/Ice-%{version}
mv $RPM_BUILD_ROOT/ant $RPM_BUILD_ROOT/usr/lib/Ice-%{version}/ant
mv $RPM_BUILD_ROOT/usr/lib/IceGridGUI.jar $RPM_BUILD_ROOT/usr/lib/Ice-%{version}/IceGridGUI.jar
%endif

%ifarch noarch
mkdir -p $RPM_BUILD_ROOT/usr/lib/Ice-%{version}
mv $RPM_BUILD_ROOT/usr/lib/Ice.jar $RPM_BUILD_ROOT/usr/lib/Ice-%{version}/Ice.jar
mv $RPM_BUILD_ROOT/usr/lib/java2 $RPM_BUILD_ROOT/usr/lib/Ice-%{version}/java2

mkdir -p $RPM_BUILD_ROOT/usr/lib/mono/gac/icecs/%{version}.0__1f998c50fec78381
mv $RPM_BUILD_ROOT/bin/icecs.dll $RPM_BUILD_ROOT/usr/lib/mono/gac/icecs/%{version}.0__1f998c50fec78381/icecs.dll

mkdir -p $RPM_BUILD_ROOT/usr/lib/mono/gac/glacier2cs/%{version}.0__1f998c50fec78381
mv $RPM_BUILD_ROOT/bin/glacier2cs.dll $RPM_BUILD_ROOT/usr/lib/mono/gac/glacier2cs/%{version}.0__1f998c50fec78381/glacier2cs.dll

mkdir -p $RPM_BUILD_ROOT/usr/lib/mono/gac/iceboxcs/%{version}.0__1f998c50fec78381
mv $RPM_BUILD_ROOT/bin/iceboxcs.dll $RPM_BUILD_ROOT/usr/lib/mono/gac/iceboxcs/%{version}.0__1f998c50fec78381/iceboxcs.dll

mkdir -p $RPM_BUILD_ROOT/usr/lib/mono/gac/icegridcs/%{version}.0__1f998c50fec78381
mv $RPM_BUILD_ROOT/bin/icegridcs.dll $RPM_BUILD_ROOT/usr/lib/mono/gac/icegridcs/%{version}.0__1f998c50fec78381/icegridcs.dll

mkdir -p $RPM_BUILD_ROOT/usr/lib/mono/gac/icepatch2cs/%{version}.0__1f998c50fec78381
mv $RPM_BUILD_ROOT/bin/icepatch2cs.dll $RPM_BUILD_ROOT/usr/lib/mono/gac/icepatch2cs/%{version}.0__1f998c50fec78381/icepatch2cs.dll

mkdir -p $RPM_BUILD_ROOT/usr/lib/mono/gac/icestormcs/%{version}.0__1f998c50fec78381
mv $RPM_BUILD_ROOT/bin/icestormcs.dll $RPM_BUILD_ROOT/usr/lib/mono/gac/icestormcs/%{version}.0__1f998c50fec78381/icestormcs.dll

#
# Cleanup extra files
#
rm -r $RPM_BUILD_ROOT/slice
rm    $RPM_BUILD_ROOT/config/Make.rules.cs
%endif

mkdir -p $RPM_BUILD_ROOT/usr
mv $RPM_BUILD_ROOT/bin $RPM_BUILD_ROOT/usr/bin

%clean

%changelog
* Fri Dec 6 2006 ZeroC Staff
- See source distributions or the ZeroC website for more information
  about the changes in this release


%ifarch %{core_arches}
%package c++-devel
Summary: Tools for developing Ice applications in C++
Group: Development/Tools
Requires: ice = %{version}
Requires: ice-%{_arch}
%description c++-devel
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package csharp-devel
Summary: Tools for developing Ice applications in C#
Group: Development/Tools
Requires: ice-dotnet = %{version}
Requires: ice-%{_arch}
%description csharp-devel
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package java-devel
Summary: Tools for developing Ice applications in Java
Group: Development/Tools
Requires: ice-java = %{version}
Requires: ice-%{_arch}
%description java-devel
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package python
Summary: The Ice runtime for Python applications
Group: System Environment/Libraries
Requires: ice = %{version}, python >= 2.3.4
Requires: ice-%{_arch}
%description python
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package python-devel
Summary: Tools for developing Ice applications in Python
Group: Development/Tools
Requires: ice-python = %{version}
Requires: ice-%{_arch}
%description python-devel
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package ruby
Summary: The Ice runtime for Ruby applications
Group: System Environment/Libraries
Requires: ice = %{version}, ruby >= 1.8.1
Requires: ice-%{_arch}
%description ruby
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package ruby-devel
Summary: Tools for developing Ice applications in Python
Group: Development/Tools
Requires: ice-ruby = %{version}
Requires: ice-%{_arch}
%description ruby-devel
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%package php
Summary: The Ice runtime for PHP applications
Group: System Environment/Libraries
Requires: ice = %{version}, php >= 5.1.2
Requires: ice-%{_arch}
%description php
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch noarch
%package java
Summary: The Ice runtime for Java
Group: System Environment/Libraries
Requires: ice = %{version}, db45-java >= 4.5.20
%description java
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch noarch
%package dotnet
Summary: The Ice runtime for C# applications
Group: System Environment/Libraries
Requires: ice = %{version}, mono-core >= 1.2.2
%description dotnet
Ice is a modern alternative to object middleware
such as CORBA or COM/DCOM/COM+.  It is easy to learn, yet provides a
powerful network infrastructure for demanding technical applications. It
features an object-oriented specification language, easy to use C++,
Java, Python, PHP, C#, and Visual Basic mappings, a highly efficient
protocol, asynchronous method invocation and dispatch, dynamic transport
plug-ins, TCP/IP and UDP/IP support, SSL-based security, a firewall
solution, and much more.
%endif




%ifarch %{core_arches}
%files
%defattr(644, root, root, 755)

%dir /usr/share/doc/Ice-%{version}
/usr/share/doc/Ice-%{version}/ICE_LICENSE
/usr/share/doc/Ice-%{version}/LICENSE
/usr/share/doc/Ice-%{version}/README
/usr/share/doc/Ice-%{version}/SOURCES
/usr/share/doc/Ice-%{version}/THIRD_PARTY_LICENSE
%attr(755, root, root) /usr/bin/dumpdb
%attr(755, root, root) /usr/bin/transformdb
%attr(755, root, root) /usr/bin/glacier2router
%attr(755, root, root) /usr/bin/icebox
%attr(755, root, root) /usr/bin/iceboxadmin
%attr(755, root, root) /usr/bin/icecpp
%attr(755, root, root) /usr/bin/icepatch2calc
%attr(755, root, root) /usr/bin/icepatch2client
%attr(755, root, root) /usr/bin/icepatch2server
%attr(755, root, root) /usr/bin/icestormadmin
%attr(755, root, root) /usr/bin/slice2docbook
%attr(755, root, root) /usr/bin/slice2html
%attr(755, root, root) /usr/bin/icegridadmin
%attr(755, root, root) /usr/bin/icegridnode
%attr(755, root, root) /usr/bin/icegridregistry
%attr(755, root, root) /usr/bin/iceca
/usr/bin/ImportKey.class
%attr(755, root, root) /usr/%{icelibdir}/libFreeze.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libFreeze.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libGlacier2.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libGlacier2.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceBox.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceBox.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIcePatch2.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIcePatch2.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIce.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIce.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceSSL.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceSSL.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceStormService.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceStormService.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceStorm.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceStorm.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceUtil.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceUtil.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceXML.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceXML.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libSlice.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libSlice.so.%{soversion}
%attr(755, root, root) /usr/%{icelibdir}/libIceGrid.so.%{version}
%attr(755, root, root) /usr/%{icelibdir}/libIceGrid.so.%{soversion}
%dir /usr/lib/Ice-%{version}
/usr/lib/Ice-%{version}/IceGridGUI.jar
/usr/share/slice
/usr/share/doc/Ice-%{version}/doc
%dir /usr/share/Ice-%{version}
/usr/share/Ice-%{version}/templates.xml
%attr(755, root, root) /usr/share/Ice-%{version}/convertssl.py
%attr(755, root, root) /usr/share/Ice-%{version}/upgradeicegrid.py
%attr(755, root, root) /usr/share/Ice-%{version}/upgradeicestorm.py
/usr/share/Ice-%{version}/icegrid-slice.3.1.ice.gz
%attr(755, root, root) /etc/init.d/icegridregistry
%attr(755, root, root) /etc/init.d/icegridnode
%attr(755, root, root) /etc/init.d/glacier2router
/etc/icegridregistry.conf
/etc/icegridnode.conf
/etc/glacier2router.conf

%post
%postun


%else
%files

%endif


%ifarch %{core_arches}
%files c++-devel
%defattr(644, root, root, 755)

%attr(755, root, root) /usr/bin/slice2cpp
%attr(755, root, root) /usr/bin/slice2freeze
/usr/include
%attr(755, root, root) /usr/%{icelibdir}/libFreeze.so
%attr(755, root, root) /usr/%{icelibdir}/libGlacier2.so
%attr(755, root, root) /usr/%{icelibdir}/libIceBox.so
%attr(755, root, root) /usr/%{icelibdir}/libIceGrid.so
%attr(755, root, root) /usr/%{icelibdir}/libIcePatch2.so
%attr(755, root, root) /usr/%{icelibdir}/libIce.so
%attr(755, root, root) /usr/%{icelibdir}/libIceSSL.so
%attr(755, root, root) /usr/%{icelibdir}/libIceStormService.so
%attr(755, root, root) /usr/%{icelibdir}/libIceStorm.so
%attr(755, root, root) /usr/%{icelibdir}/libIceUtil.so
%attr(755, root, root) /usr/%{icelibdir}/libIceXML.so
%attr(755, root, root) /usr/%{icelibdir}/libSlice.so


%post c++-devel
%postun c++-devel


%endif


%ifarch %{core_arches}
%files csharp-devel
%defattr(644, root, root, 755)

%attr(755, root, root) /usr/bin/slice2cs
%dir /usr/share/doc/Ice-%{version}
/usr/%{icelibdir}/pkgconfig/icecs.pc
/usr/%{icelibdir}/pkgconfig/glacier2cs.pc
/usr/%{icelibdir}/pkgconfig/iceboxcs.pc
/usr/%{icelibdir}/pkgconfig/icegridcs.pc
/usr/%{icelibdir}/pkgconfig/icepatch2cs.pc
/usr/%{icelibdir}/pkgconfig/icestormcs.pc


%post csharp-devel

%ifnarch noarch

pklibdir="lib"

%ifarch x86_64
pklibdir="lib64"
%endif

for f in icecs glacier2cs iceboxcs icegridcs icepatch2cs icestormcs;
do
    sed -i.bak -e "s/^mono_root.*$/mono_root = \/usr/" /usr/$pklibdir/pkgconfig/$f.pc ; 
done
        
%endif
%postun csharp-devel


%endif


%ifarch %{core_arches}
%files java-devel
%defattr(644, root, root, 755)

%attr(755, root, root) /usr/bin/slice2java
%attr(755, root, root) /usr/bin/slice2freezej
%dir /usr/lib/Ice-%{version}
/usr/lib/Ice-%{version}/ant


%post java-devel
%postun java-devel


%endif


%ifarch %{core_arches}
%files python
%defattr(644, root, root, 755)

/usr/%{icelibdir}/Ice-%{version}/python


%post python
%postun python


%endif


%ifarch %{core_arches}
%files python-devel
%defattr(644, root, root, 755)

%attr(755, root, root) /usr/bin/slice2py


%post python-devel
%postun python-devel


%endif


%ifarch %{core_arches}
%files ruby
%defattr(644, root, root, 755)

/usr/%{icelibdir}/Ice-%{version}/ruby


%post ruby
%postun ruby


%endif


%ifarch %{core_arches}
%files ruby-devel
%defattr(644, root, root, 755)

%attr(755, root, root) /usr/bin/slice2rb


%post ruby-devel
%postun ruby-devel


%endif


%ifarch %{core_arches}
%files php
%defattr(644, root, root, 755)

%attr(755, root, root) /usr/%{icelibdir}/php/modules
/etc/php.d/ice.ini


%post php
%postun php


%endif


%ifarch noarch
%files java
%defattr(644, root, root, 755)

%dir /usr/lib/Ice-%{version}
/usr/lib/Ice-%{version}/Ice.jar
%dir /usr/lib/Ice-%{version}/java2
/usr/lib/Ice-%{version}/java2/Ice.jar


%post java
%postun java


%endif


%ifarch noarch
%files dotnet
%defattr(644, root, root, 755)

/usr/lib/mono/gac/glacier2cs/%{version}.0__1f998c50fec78381/glacier2cs.dll
/usr/lib/mono/gac/icecs/%{version}.0__1f998c50fec78381/icecs.dll
/usr/lib/mono/gac/iceboxcs/%{version}.0__1f998c50fec78381/iceboxcs.dll
/usr/lib/mono/gac/icegridcs/%{version}.0__1f998c50fec78381/icegridcs.dll
/usr/lib/mono/gac/icepatch2cs/%{version}.0__1f998c50fec78381/icepatch2cs.dll
/usr/lib/mono/gac/icestormcs/%{version}.0__1f998c50fec78381/icestormcs.dll
%attr(755, root, root) /usr/bin/iceboxnet.exe



%post dotnet
%postun dotnet


%endif

