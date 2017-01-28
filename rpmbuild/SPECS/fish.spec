Summary: Friendly interactive shell
Name: fish
Version: 2.4.0
Release: 1%{?dist}
License: GPL-2.0
Group: System/Shells
URL: https://fishshell.com/

Source: https://fishshell.com/files/%{version}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc-c++, gettext, ncurses-devel, make

Requires: bc
Requires: man
Requires: which

%if 0%{?centos_version} >= 700
Requires: hostname
%else
Requires: net-tools
%endif

%description
fish is a smart and user-friendly command line
shell for macOS, Linux, and the rest of the family.

%prep
%setup -q -n %{name}-%{version}

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%post
if ! grep %{_bindir}/fish %{_sysconfdir}/shells >/dev/null; then
    echo %{_bindir}/fish >> %{_sysconfdir}/shells
fi

%postun
if [ "$1" = 0 ]; then
    grep -v %{_bindir}/fish %{_sysconfdir}/shells > %{_sysconfdir}/fish.tmp
    mv %{_sysconfdir}/fish.tmp %{_sysconfdir}/shells
fi

%files -f %{name}.lang
%defattr(-, root, root, 0755)

%docdir %{_datadir}/doc/fish/
%{_datadir}/doc/fish

%{_mandir}/man1/*
%docdir %{_datadir}/fish/man/man1/
%{_datadir}/fish/man/man1/

%attr(0755,root,root) %{_bindir}/*

%dir %{_sysconfdir}/fish/
%config(noreplace) %{_sysconfdir}/fish/config.fish

%{_datadir}/fish/

%{_datadir}/pkgconfig/fish.pc
