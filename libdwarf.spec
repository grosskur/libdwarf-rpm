Name:          libdwarf
Version:       20121127
Release:       1%{?dist}
Summary:       Library to access the DWARF Debugging file format 
Group:         Development/Libraries

License:       LGPLv2
URL:           http://reality.sgiweb.org/davea/dwarf.html
Source0:       http://reality.sgiweb.org/davea/%{name}-%{version}.tar.gz

# This patch set up the proper soname
Patch0:        libdwarf-soname-fix.patch

BuildRequires: binutils-devel elfutils-libelf-devel

%package devel
Summary:       Library and header files of libdwarf
Group:         Development/Libraries
License:       LGPLv2
Requires:      %{name} = %{version}-%{release}

%package static
Summary:       Static libdwarf library
Group:         Development/Libraries
License:       LGPLv2
Requires:      %{name}-devel = %{version}-%{release}

%package tools
Summary:       Tools for accessing DWARF debugging information
Group:         Development/Tools
License:       GPLv2
Requires:      %{name} = %{version}-%{release}

%description
Library to access the DWARF debugging file format which supports
source level debugging of a number of procedural languages, such as C, C++,
and Fortran.  Please see http://www.dwarfstd.org for DWARF specification.

%description static
Static libdwarf library.

%description devel
Development package containing library and header files of libdwarf.

%description tools
C++ version of dwarfdump (dwarfdump2) command-line utilities 
to access DWARF debug information.

%prep
%setup -q -n dwarf-%{version}
%patch0 -p0 -b .soname-fix

%build
pushd libdwarf
%configure --enable-shared
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS -I. -fPIC" libdwarf.so.0.0 libdwarf.a 
ln -s libdwarf.so.0.0 libdwarf.so
ln -s libdwarf.so.0.0 libdwarf.so.0
popd

# Need to also configure dwarfdump since dwarfdump2 Makefile 
# depends on dwarfdump's Makefile
pushd dwarfdump
%configure 
popd

pushd dwarfdump2
%configure 
# Note: %{?_smp_mflags} failed to build
LD_LIBRARY_PATH="../libdwarf" make CFLAGS="$RPM_OPT_FLAGS -I. -fPIC" all
popd

%install
install -pDm 0644 libdwarf/dwarf.h         %{buildroot}%{_includedir}/libdwarf/dwarf.h
install -pDm 0644 libdwarf/libdwarf.a      %{buildroot}%{_libdir}/libdwarf.a

install -pDm 0644 libdwarf/libdwarf.h      %{buildroot}%{_includedir}/libdwarf/libdwarf.h
install -pDm 0755 libdwarf/libdwarf.so.0.0 %{buildroot}%{_libdir}/libdwarf.so.0.0
cp -pd libdwarf/libdwarf.so.0              %{buildroot}%{_libdir}/libdwarf.so.0
cp -pd libdwarf/libdwarf.so                %{buildroot}%{_libdir}/libdwarf.so
install -pDm 0755 dwarfdump2/dwarfdump     %{buildroot}%{_bindir}/dwarfdump

%post -n libdwarf -p /sbin/ldconfig

%postun -n libdwarf -p /sbin/ldconfig

%files
%doc libdwarf/ChangeLog libdwarf/README libdwarf/COPYING libdwarf/LIBDWARFCOPYRIGHT libdwarf/LGPL.txt
%{_libdir}/libdwarf.so.0*

%files static
%{_libdir}/libdwarf.a

%files devel
%doc libdwarf/*.pdf
%{_includedir}/libdwarf
%{_libdir}/libdwarf.so

%files tools
%doc dwarfdump2/README dwarfdump2/ChangeLog dwarfdump2/COPYING dwarfdump2/DWARFDUMPCOPYRIGHT dwarfdump2/GPL.txt
%{_bindir}/dwarfdump

%changelog
* Thu Nov 29 2012 Tom Hughes <tom@compton.nu> - 20121127-1
- Update to 20121127 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120410-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Tom Hughes <tom@compton.nu> - 20120410-1
- Update to 20120410 release
- Drop the 0. from the version - the dates are the upstream versions
- Remove explicit dependencies on elfutils-libelf

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110612-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110612-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 13 2011 Parag Nemade <paragn AT fedoraproject DOT org> - 0.20110612-1
- Update to 20110612 release

* Wed Mar 09 2011 Parag Nemade <paragn AT fedoraproject DOT org> - 0.20110113-1
- Update to 20110113 release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100629-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 06 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.20100629-1
- Update to 20100629 release
- Add -static subpackage as request in rh#586807

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090324-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 31 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-4
- Adding _smp_mflags for libdwarf build
- Move CFLAGS override from configure to make
 
* Mon Mar 30 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-3
- Remove AutoreqProv no

* Thu Mar 26 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 0.20090324-2
- Drop the C implementation of dwarfdump. (dwarfdump1)
- Since the doc package is small, we combined the contents into the devel package.
- Fix the version string.
- Drop the static library.
- Add release number to "Requires".
- Fix licensing (v2 instead of v2+)
- Change linking for libdwarf.so and libdwarf.so.0

* Wed Mar 25 2009 - Suravee Suthikulpanit <suravee.suthikulpanit@amd.com>
- 20090324-1
- Initial Revision
