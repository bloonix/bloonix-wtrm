Summary: Bloonix wtrm daemon
Name: bloonix-wtrm
Version: 0.3
Release: 2%{dist}
License: Commercial
Group: Utilities/System
Distribution: RHEL and CentOS

Packager: Jonny Schulz <js@bloonix.de>
Vendor: Bloonix

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: http://download.bloonix.de/sources/%{name}-%{version}.tar.gz
Requires: bloonix-core
Requires: bloonix-fcgi
Requires: bloonix-plugins-wtrm
Requires: perl-JSON-XS
Requires: perl(Getopt::Long)
Requires: perl(JSON)
Requires: perl(Log::Handler)
Requires: perl(Params::Validate)
Requires: perl(Time::HiRes)
AutoReqProv: no

%description
bloonix-wtrm provides the bloonix wtrm.

%define with_systemd 0
%define initdir %{_sysconfdir}/init.d
%define mandir8 %{_mandir}/man8
%define docdir %{_docdir}/%{name}-%{version}
%define blxdir /usr/lib/bloonix
%define confdir /usr/lib/bloonix/etc/bloonix
%define logdir /var/log/bloonix
%define rundir /var/run/bloonix
%define pod2man /usr/bin/pod2man

%prep
%setup -q -n %{name}-%{version}

%build
%{__perl} Configure.PL --prefix /usr --build-package
%{__make}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
mkdir -p ${RPM_BUILD_ROOT}%{docdir}
install -d -m 0750 ${RPM_BUILD_ROOT}%{logdir}
install -d -m 0750 ${RPM_BUILD_ROOT}%{rundir}
install -c -m 0444 LICENSE ${RPM_BUILD_ROOT}%{docdir}/
install -c -m 0444 ChangeLog ${RPM_BUILD_ROOT}%{docdir}/

%if %{?with_systemd}
install -p -D -m 0644 %{buildroot}%{blxdir}/etc/systemd/bloonix-wtrm.service %{buildroot}%{_unitdir}/bloonix-wtrm.service
%else
install -p -D -m 0755 %{buildroot}%{blxdir}/etc/init.d/bloonix-wtrm %{buildroot}%{initdir}/bloonix-wtrm
%endif

%pre
getent group bloonix >/dev/null || /usr/sbin/groupadd bloonix
getent passwd bloonix >/dev/null || /usr/sbin/useradd \
    bloonix -g bloonix -s /sbin/nologin -d /var/run/bloonix -r

%post
%if %{?with_systemd}
systemctl preset bloonix-wtrm.service
systemctl condrestart bloonix-wtrm.service
%else
/sbin/chkconfig --add bloonix-wtrm
/sbin/service bloonix-wtrm condrestart &>/dev/null
%endif

if [ ! -e "/etc/bloonix/wtrm/main.conf" ] ; then
    mkdir -p /etc/bloonix/wtrm
    chown root:root /etc/bloonix /etc/bloonix/wtrm
    chmod 755 /etc/bloonix /etc/bloonix/wtrm
    cp -a /usr/lib/bloonix/etc/wtrm/main.conf /etc/bloonix/wtrm/main.conf
    chown root:bloonix /etc/bloonix/wtrm/main.conf
    chmod 640 /etc/bloonix/wtrm/main.conf
fi

if [ -e "/etc/nginx/conf.d" ] && [ ! -e "/etc/nginx/conf.d/bloonix-wtrm.conf" ] ; then
    install -c -m 0644 /usr/lib/bloonix/etc/wtrm/nginx.conf /etc/nginx/conf.d/bloonix-wtrm.conf
fi

%preun
if [ $1 -eq 0 ]; then
%if %{?with_systemd}
systemctl --no-reload disable bloonix-wtrm.service
systemctl stop bloonix-wtrm.service
systemctl daemon-reload
%else
    /sbin/service bloonix-wtrm stop &>/dev/null || :
    /sbin/chkconfig --del bloonix-wtrm
%endif
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%dir %attr(0755, root, root) %{blxdir}
%dir %attr(0755, root, root) %{blxdir}/etc
%dir %attr(0755, root, root) %{blxdir}/etc/wtrm
%{blxdir}/etc/wtrm/main.conf
%{blxdir}/etc/wtrm/nginx.conf
%dir %attr(0755, root, root) %{blxdir}/etc/systemd
%{blxdir}/etc/systemd/bloonix-wtrm.service
%dir %attr(0755, root, root) %{blxdir}/etc/init.d
%{blxdir}/etc/init.d/bloonix-wtrm
%dir %attr(0750, bloonix, bloonix) %{logdir}
%dir %attr(0750, bloonix, bloonix) %{rundir}

%{_bindir}/bloonix-wtrm

%if %{?with_systemd} == 1
%{_unitdir}/bloonix-wtrm.service
%else
%{initdir}/bloonix-wtrm
%endif

%dir %attr(0755, root, root) %{docdir}
%doc %attr(0444, root, root) %{docdir}/ChangeLog
%doc %attr(0444, root, root) %{docdir}/LICENSE

%changelog
* Thu Jan 29 2015 Jonny Schulz <js@bloonix.de> - 0.3-2
- Fixed %preun.
* Wed Nov 26 2014 Jonny Schulz <js@bloonix.de> - 0.3-1
- First DEB/RPM release.
