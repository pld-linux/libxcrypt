Summary:	Crypt Library for DES, MD5, and Blowfish
Summary(pl.UTF-8):	Biblioteka szyfrująca hasła obsługująca DES, MD5 i Blowfish
Name:		libxcrypt
Version:	4.4.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/besser82/libxcrypt/releases
Source0:	https://github.com/besser82/libxcrypt/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	13e9f41b9881956c529a028b636ff22b
Patch0:		%{name}-xcrypt.patch
URL:		https://github.com/besser82/libxcrypt
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.14
BuildRequires:	libtool >= 2:2
BuildRequires:	pkgconfig >= 1:0.27
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%undefine	__cxx

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
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--includedir=%{_includedir}/xcrypt \
	--disable-werror \
	--disable-xcrypt-compat-files
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libxcrypt.so.* $RPM_BUILD_ROOT/%{_lib}
ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libxcrypt.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libxcrypt.so

# PLD doesn't need Owl compatibility
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libowcrypt.*
# packaged with glibc-devel
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man3/crypt{,_r,_ra,_rn}.3*

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog LICENSING NEWS README.md THANKS TODO.md
%attr(755,root,root) /%{_lib}/libxcrypt.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libxcrypt.so.2

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxcrypt.so
%{_libdir}/libxcrypt.la
%{_includedir}/xcrypt
%{_pkgconfigdir}/libcrypt.pc
%{_pkgconfigdir}/libxcrypt.pc
%{_mandir}/man3/crypt_checksalt.3*
%{_mandir}/man3/crypt_gensalt*.3*
%{_mandir}/man3/crypt_preferred_method.3*
%{_mandir}/man5/crypt.5*

%files static
%defattr(644,root,root,755)
%{_libdir}/libxcrypt.a
