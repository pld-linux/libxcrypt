#
# Conditional build:
%bcond_without	default_crypt	# build as default libcrypt provider

Summary:	Crypt Library for DES, MD5, and Blowfish
Summary(pl.UTF-8):	Biblioteka szyfrująca hasła obsługująca DES, MD5 i Blowfish
Name:		libxcrypt
Version:	4.4.26
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/besser82/libxcrypt/releases
Source0:	https://github.com/besser82/libxcrypt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	4036f4dda35ad8d18b894da426dbf7cd
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
Obsoletes:	glibc-libcrypt
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

%if %{with default_crypt}
%define		libname		libcrypt
%define		libver		1
%else
%define		libname		libxcrypt
%define		libver		2
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
Conflicts:	glibc-devel-doc < 6:2.34-7

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

%prep
%setup -q
%{!?with_default_crypt:%patch0 -p1}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
%if %{with default_crypt}
	--enable-obsolete-api=glibc \
	--enable-obsolete-api-enosys=yes \
%else
	--includedir=%{_includedir}/xcrypt \
	--disable-xcrypt-compat-files \
%endif
	--disable-werror
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/%{libname}.so.* $RPM_BUILD_ROOT/%{_lib}
ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/%{libname}.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/%{libname}.so

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

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%posttrans
if [ ! -L /%{_lib}/%{libname}.so.%{libver} ]; then
	%{__rm} -f /%{_lib}/%{libname}.so.%{libver}
	/sbin/ldconfig
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSING NEWS README.md THANKS TODO.md
%attr(755,root,root) /%{_lib}/%{libname}.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/%{libname}.so.%{libver}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{libname}.so
%if %{with default_crypt}
%{_includedir}/crypt.h
%{_includedir}/xcrypt.h
%attr(755,root,root) %{_libdir}/libxcrypt.so
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
%if %{with default_crypt}
%{_libdir}/libxcrypt.a
%endif
