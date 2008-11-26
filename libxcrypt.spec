Summary:	Crypt Library for DES, MD5, and Blowfish
Name:		libxcrypt
Version:	3.0.2
Release:	1
License:	LGPL v2+, Public Domain, Freeware
Group:		Libraries
Source0:	ftp://ftp.suse.com/pub/people/kukuk/libxcrypt/%{name}-%{version}.tar.bz2
# Source0-md5:	56cf4285086f26649b8792b53fe8b00f
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, and passwords with blowfish
encryption.

%package devel
Summary:	Header files and develpment documentation for libxcrypt
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains the header files to develop software using
libxcrypt.

%package static
Summary:	Static libxcrypt library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
This package contains the static library used for development.

%prep
%setup -q

%build
%configure \
	--libdir=/%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/%{_lib}/lib*.{l,}a $RPM_BUILD_ROOT%{_libdir}
sed -i -e 's#/%{_lib}#%{_libdir}#g' $RPM_BUILD_ROOT%{_libdir}/*.la

for lib in $RPM_BUILD_ROOT/%{_lib}/lib*.so.*; do
	lib=$(echo $lib | sed -e "s#$RPM_BUILD_ROOT##g")
	slib=$(basename $lib | sed -e 's#\.so\..*#.so#g')
	ln -sf $lib $RPM_BUILD_ROOT%{_libdir}/$slib
done

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README*
%attr(755,root,root) /%{_lib}/libxcrypt.so.*
%dir  /%{_lib}/xcrypt
%attr(755,root,root) /%{_lib}/xcrypt/libxcrypt*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxcrypt.so
%{_includedir}/xcrypt.h
%{_libdir}/*.la

%files static
%defattr(644,root,root,755)
%{_libdir}/libxcrypt.a
