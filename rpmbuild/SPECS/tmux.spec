Summary: Terminal multiplexer
Name: tmux
Version: 2.3
Release: 1%{?dist}
License: BSD
Group: Applications/System
URL: https://tmux.github.io/

Source: https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: gcc, ncurses-devel, make
BuildRequires: libevent-devel >= 1.9

%description
tmux is a "terminal multiplexer". It allows a number of terminals (or windows)
to be accessed and controlled from a single terminal. It is intended to be
a simple, modern, BSD-licensed alternative to programs such as GNU screen.

%prep
%setup -q -n %{name}-%{version}

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}" INSTALLBIN="install -p -m0755" INSTALLMAN="install -p -m0644"

# Create the socket dir
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/run/tmux/

%clean
%{__rm} -rf %{buildroot}

%pre
getent group tmux >/dev/null || groupadd -r tmux

%files
%defattr(-, root, root, 0755)
%doc CHANGES FAQ README TODO
%doc %{_mandir}/man1/tmux.1.*
%attr(2755, root, tmux) %{_bindir}/tmux
%attr(0775, root, tmux) %{_localstatedir}/run/tmux/

%changelog
* Sat Jan 28 2017 Armin Grodon <me@armingrodon.de> - 2.3-1
- Initial package.
