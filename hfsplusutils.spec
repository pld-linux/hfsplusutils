#
# Conditional build:
%bcond_with	shared_libs	# with shared library (API not installed though, binaries size doesn't differ much)
#
Summary:	HFS+ volume utils
Summary(pl.UTF-8):	Narzędzia do woluminów HFS+
Name:		hfsplusutils
Version:	1.0.4
Release:	1
License:	GPL v2+
Group:		Applications/System
Source0:	ftp://ftp.penguinppc.org/users/hasi/hfsplus_%{version}.src.tar.bz2
# Source0-md5:	18fa1efb5432469357ffa6bfa7c08fcd
Patch0:		%{name}-nullisnotachar.patch
Patch1:		%{name}-errno.patch
Patch2:		%{name}-includes.patch
Patch3:		%{name}-gcc4.patch
Patch4:		memset.patch
Patch5:		%{name}-am.patch
URL:		http://www.penguinppc.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HFS+ volume utils.

%description -l pl.UTF-8
Narzędzia do woluminów HFS+.

%prep
%setup -q -n hfsplus-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# if building shared library, install it to /lib (for /sbin/fsck.hfsplus)
%configure \
%if %{with shared_libs}
	--libdir=/%{_lib} \
	--disable-static \
%else
	--disable-shared
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man{1,8}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# API not exported, so don't package other devel stuff
%if %{with shared_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhfsp.{la,so}
%else
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhfsp.{la,a}
%endif

# move to /sbin to allow separate %{_prefix}
mv $RPM_BUILD_ROOT%{_bindir}/hpfsck $RPM_BUILD_ROOT/sbin/fsck.hfsplus
ln -s /sbin/fsck.hfsplus $RPM_BUILD_ROOT%{_bindir}/hpfsck

cp -p doc/man/hfsp.man $RPM_BUILD_ROOT%{_mandir}/man1/hfsp.1
for a in hpcd hpcopy hpfsck hpls hpmkdir hpmount hppwd hprm hpumount; do
	echo '.so hfsp.1' > $RPM_BUILD_ROOT%{_mandir}/man1/$a.1
done
echo '.so man1/hfsp.1' > $RPM_BUILD_ROOT%{_mandir}/man8/fsck.hfsplus.8

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%if %{with shared_libs}
%attr(755,root,root) /%{_lib}/libhfsp.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libhfsp.so.0
%endif
%attr(755,root,root) /sbin/fsck.hfsplus
%attr(755,root,root) %{_bindir}/hpcd
%attr(755,root,root) %{_bindir}/hpcopy
%attr(755,root,root) %{_bindir}/hpfsck
%attr(755,root,root) %{_bindir}/hpls
%attr(755,root,root) %{_bindir}/hpmkdir
%attr(755,root,root) %{_bindir}/hpmount
%attr(755,root,root) %{_bindir}/hppwd
%attr(755,root,root) %{_bindir}/hprm
%attr(755,root,root) %{_bindir}/hpumount
%{_mandir}/man1/hfsp.1*
%{_mandir}/man1/hpcd.1*
%{_mandir}/man1/hpcopy.1*
%{_mandir}/man1/hpfsck.1*
%{_mandir}/man1/hpls.1*
%{_mandir}/man1/hpmkdir.1*
%{_mandir}/man1/hpmount.1*
%{_mandir}/man1/hppwd.1*
%{_mandir}/man1/hprm.1*
%{_mandir}/man1/hpumount.1*
%{_mandir}/man8/fsck.hfsplus.8*
