#
# Conditional build:
%bcond_without  compat_pkg	# compat package (libcrypt.so.1 with legacy APIs)
%bcond_without  default_crypt	# libxcrypt as default libcrypt
%bcond_without  tests		# testing

Summary:	Crypt Library for DES, MD5, and Blowfish
Summary(pl.UTF-8):	Biblioteka szyfrująca hasła obsługująca DES, MD5 i Blowfish
Name:		libxcrypt
Version:	4.4.37
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/besser82/libxcrypt/releases
Source0:	https://github.com/besser82/libxcrypt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	fe793903a4937db15e1720c98cf6660d
Patch0:		%{name}-xcrypt.patch
URL:		https://github.com/besser82/libxcrypt
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.14
BuildRequires:	gcc >= 5:3.2
BuildRequires:	libltdl-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig >= 1:0.27
%if %{with default_crypt}
Provides:	crypt(blowfish)
Obsoletes:	glibc-libcrypt < 6:2.37
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine       __cxx

%if %{with default_crypt}
%define         libname		libcrypt
%else
%undefine       with_compat_pkg
%define         libname		libxcrypt
%endif

%description
libxcrypt is a replacement for libcrypt, which comes with the GNU C
Library. It supports DES crypt, MD5, and passwords with Blowfish
encryption.

%description -l pl.UTF-8
libxcrypt to zamiennik biblioteki libcrypt dostarczanej wraz z
biblioteką GNU C (libc). Obsługuje szyfrowanie haseł DES, MD5 oraz
Blowfish.

%package devel
Summary:	Header file for libxcrypt
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki libxcrypt
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%{?with_default_crypt:Conflicts:	glibc-devel-doc < 6:2.34-7}

%description devel
This package contains the header file to develop software using
libxcrypt.

%description devel -l pl.UTF-8
Ten pakiet zawiera plik nagłówkowy pozwalający na tworzenie programów
korzystających z libxcrypt.

%package static
Summary:	Static libxcrypt library
Summary(pl.UTF-8):	Statyczna biblioteka libxcrypt
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains the static libxcrypt library used for
development.

%description static -l pl.UTF-8
Ten pakiet zawiera statyczną wersję biblioteki libxcrypt.

%package compat
Summary:	Compatibility library providing legacy API functions
Summary(pl.UTF-8):	Biblioteka zgodności wstecznej dostarczająca dawne funkcje API
Requires:	%{name} = %{version}-%{release}

%description compat
This package contains the library providing the compatibility API for
applications that are linked against glibc's libcrypt, or that are
still using the unsafe and deprecated, encrypt, encrypt_r, setkey,
setkey_r, and fcrypt functions, which are still required by recent
versions of POSIX, the Single UNIX Specification, and various other
standards.

All existing binary executables linked against glibc's libcrypt should
work unmodified with the library supplied by this package.

%description compat -l pl.UTF-8
Ten pakiet zawiera bibliotekę dostarczającą API zgodności wstecznej
dla aplikacji skonsolidowanych z biblioteką libcrypt z glibc lub
nadal wykorzystujących niebezpieczne i przestarzałe funkcje encrypt,
encrypt_r, setkey, setkey_r oraz fcrypt, nadal wymagane przez obecne
wersje standardów POSIX, Single UNIX Specification i innych.

Wszystkie istniejące programy wykonywalne skonsolidowane z biblioteką
libcrypt z glibc powinny działać bez modyfikacji z biblioteką
dostarczaną przez ten pakiet.

%prep
%setup -q
%{!?with_default_crypt:%patch0 -p1}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

install -d regular
cd regular
../%configure \
	--enable-hashes=all \
%if %{with default_crypt}
	--disable-obsolete-api \
	--disable-obsolete-api-enosys \
%else
	--includedir=%{_includedir}/xcrypt \
	--disable-xcrypt-compat-files \
%endif
	--disable-werror
%{__make}

%if %{with tests}
%{__make} check
%endif
cd ..

%if %{with compat_pkg}
install -d compat
cd compat
../%configure \
	--enable-hashes=all \
	--enable-obsolete-api=glibc \
	--enable-obsolete-api-enosys \
	--disable-werror
%{__make}

%if %{with tests}
%{__make} check
%endif
cd ..
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%if %{with compat_pkg}
%{__make} -C compat install \
	DESTDIR=$RPM_BUILD_ROOT

# clean everything beside library
find $RPM_BUILD_ROOT -not -type d -not -name 'libcrypt.so.1*' -delete -print
%endif

%{__make} -C regular install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/%{libname}.so.* $RPM_BUILD_ROOT/%{_lib}
ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/%{libname}.so.2.*.*) $RPM_BUILD_ROOT%{_libdir}/%{libname}.so

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{libname}.la

%if %{without default_crypt}
# PLD doesn't need Owl compatibility
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libowcrypt.*
# packaged with glibc-devel
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/crypt{,_r,_ra,_rn}.3*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	compat -p /sbin/ldconfig
%postun	compat -p /sbin/ldconfig

%posttrans compat
if [ ! -L /%{_lib}/libcrypt.so.1 ]; then
	%{__rm} -f /%{_lib}/libcrypt.so.1
	/sbin/ldconfig
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSING NEWS README.md THANKS TODO.md
%attr(755,root,root) /%{_lib}/%{libname}.so.2.*.*
%attr(755,root,root) %ghost /%{_lib}/%{libname}.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{libname}.so
%if %{with default_crypt}
%{_includedir}/crypt.h
%else
%{_includedir}/xcrypt
%endif
%{_pkgconfigdir}/libcrypt.pc
%{_pkgconfigdir}/libxcrypt.pc
%{_mandir}/man3/crypt_checksalt.3*
%{_mandir}/man3/crypt_gensalt*.3*
%{_mandir}/man3/crypt_preferred_method.3*
%if %{with default_crypt}
%{_mandir}/man3/crypt.3*
%{_mandir}/man3/crypt_r.3*
%{_mandir}/man3/crypt_ra.3*
%{_mandir}/man3/crypt_rn.3*
%endif
%{_mandir}/man5/crypt.5*

%files static
%defattr(644,root,root,755)
%{_libdir}/%{libname}.a

%if %{with compat_pkg}
%files compat
%defattr(644,root,root,755)
%attr(755,root,root) /%{_lib}/libcrypt.so.1.*.*
%attr(755,root,root) %ghost /%{_lib}/libcrypt.so.1
%endif
