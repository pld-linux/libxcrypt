Summary:	Crypt Library for DES, MD5, and Blowfish
Summary(pl.UTF-8):	Biblioteka szyfrująca hasła obsługująca DES, MD5 i Blowfish
Name:		libxcrypt
Version:	3.0.2
Release:	3
License:	LGPL v2.1+ (library), LGPL v2.1+/Public Domain (plugins)
Group:		Libraries
Source0:	ftp://ftp.suse.com/pub/people/kukuk/libxcrypt/%{name}-%{version}.tar.bz2
# Source0-md5:	56cf4285086f26649b8792b53fe8b00f
Patch0:		%{name}-noWerror.patch
Patch1:		%{name}-libc-lock.patch
BuildRequires:	sed >= 4.0
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
%patch1 -p1

%build
%configure \
	--libdir=/%{_lib}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT/%{_lib}/libxcrypt.{so,la,a} $RPM_BUILD_ROOT%{_libdir}
sed -i -e 's#/%{_lib}#%{_libdir}#g' $RPM_BUILD_ROOT%{_libdir}/libxcrypt.la
ln -snf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libxcrypt.so.*.*.*) $RPM_BUILD_ROOT%{_libdir}/libxcrypt.so

%{__rm} $RPM_BUILD_ROOT/%{_lib}/xcrypt/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
# COPYING specifies licenses for particular plugins
%doc COPYING ChangeLog NEWS README*
%attr(755,root,root) /%{_lib}/libxcrypt.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libxcrypt.so.2
%dir /%{_lib}/xcrypt
%attr(755,root,root) /%{_lib}/xcrypt/libxcrypt_*.so*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxcrypt.so
%{_libdir}/libxcrypt.la
%{_includedir}/xcrypt.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libxcrypt.a
