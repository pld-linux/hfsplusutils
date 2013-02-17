# TODO
# - why disable shared?
Summary:	HFS+ volume utils
Summary(pl.UTF-8):	Narzędzia do woluminów HFS+
Name:		hfsplusutils
Version:	1.0.4
Release:	0.2
License:	GPL
Group:		Applications/System
Source0:	ftp://ftp.penguinppc.org/users/hasi/hfsplus_%{version}.src.tar.bz2
# Source0-md5:	18fa1efb5432469357ffa6bfa7c08fcd
Patch0:		%{name}-nullisnotachar.patch
Patch1:		%{name}-errno.patch
Patch2:		%{name}-includes.patch
Patch3:		%{name}-gcc4.patch
Patch4:		memset.patch
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}

%configure \
	--disable-shared
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/sbin,%{_mandir}/man1}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhfsp.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libhfsp.a

# move to /sbin to allow separate %{_prefix}
mv $RPM_BUILD_ROOT%{_bindir}/hpfsck $RPM_BUILD_ROOT/sbin/fsck.hfsplus
ln -s /sbin/fsck.hfsplus $RPM_BUILD_ROOT%{_bindir}/hpfsck

cp -p doc/man/hfsp.man $RPM_BUILD_ROOT%{_mandir}/man1/hfsp.1
for a in hpcd hpcopy hpfsck hpls hpmkdir hpmount hppwd hprm hpumount fsck.hfsplus; do
	echo '.so hfsp.1' > $RPM_BUILD_ROOT%{_mandir}/man1/$a.1
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS README
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
%{_mandir}/man1/*
