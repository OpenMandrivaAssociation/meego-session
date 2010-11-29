Name: meego-session
Summary: MeeGo User Experience Startup Scripts
Group: Graphical desktop/Other
Version: 0.13
Release: %mkrel 1
License: GPLv2
URL: http://www.moblin.org
Source0: http://git.moblin.org/cgit.cgi/%{name}/snapshot/moblin-session-%{version}.tar.bz2
Patch0: moblin-session-0.13-meego.patch
Requires: telepathy-mission-control
Requires: meego-ux-settings
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Description: %{summary}

%prep
%setup -q -n moblin-session-%{version}
%patch0 -p1 -b .meego
cat > 10meego <<EOF
NAME=MeeGo
DESC=MeeGo Desktop Environment
EXEC=%{_sysconfdir}/xdg/meego/xinitrc
SCRIPT:
exec %{_sysconfdir}/xdg/meego/xinitrc
EOF
cat > startmeego <<EOF
#!/bin/sh
exec startx %{_sysconfdir}/X11/Xsession %{_sysconfdir}/xdg/meego/xinitrc
EOF

%build
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm -f %{buildroot}%{_datadir}/xsessions/moblin.desktop
install -d %{buildroot}%{_sysconfdir}/X11/wmsession.d
install -m755 10meego %{buildroot}%{_sysconfdir}/X11/wmsession.d/
install -m755 startmeego %{buildroot}%{_bindir}/
chmod 755 %{buildroot}%{_sysconfdir}/xdg/meego/xinitrc

%find_lang %{name}

mkdir -p %{buildroot}/%{_datadir}/doc/%{name}-%{version}
for f in `ls %{buildroot}/%{_datadir}/doc/`; do
	if [ -f %{buildroot}/%{_datadir}/doc/$f ]; then
		mv %{buildroot}/%{_datadir}/doc/$f %{buildroot}/%{_datadir}/doc/%{name}-%{version}
	fi
done

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/startmeego
%{_sysconfdir}/xdg/meego/xinitrc
%{_sysconfdir}/X11/wmsession.d/10meego
