Summary: Bloonix wtrm daemon
Name: bloonix-wtrm
Version: 0.6
Release: 1%{dist}
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
Requires: openssl
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

%if 0%{?with_systemd}
install -p -D -m 0644 %{buildroot}%{blxdir}/etc/systemd/bloonix-wtrm.service %{buildroot}%{_unitdir}/bloonix-wtrm.service
%else
install -p -D -m 0755 %{buildroot}%{blxdir}/etc/init.d/bloonix-wtrm %{buildroot}%{initdir}/bloonix-wtrm
%endif

%pre
getent group bloonix >/dev/null || /usr/sbin/groupadd bloonix
getent passwd bloonix >/dev/null || /usr/sbin/useradd \
    bloonix -g bloonix -s /sbin/nologin -d /var/run/bloonix -r

%post
if [ ! -e "/etc/bloonix/wtrm/main.conf" ] ; then
    mkdir -p /etc/bloonix/wtrm
    chown root:root /etc/bloonix /etc/bloonix/wtrm
    chmod 755 /etc/bloonix /etc/bloonix/wtrm
    cp -a /usr/lib/bloonix/etc/wtrm/main.conf /etc/bloonix/wtrm/main.conf
    chown root:bloonix /etc/bloonix/wtrm/main.conf
    chmod 640 /etc/bloonix/wtrm/main.conf
fi

if [ ! -e "/etc/bloonix/wtrm/pki" ] ; then
    echo "create /etc/bloonix/wtrm/pki/*"
    mkdir -p /etc/bloonix/wtrm/pki
    chown root:bloonix /etc/bloonix/wtrm/pki
    chmod 750 /etc/bloonix/wtrm/pki
    openssl req -new -x509 -nodes -out /etc/bloonix/wtrm/pki/server.cert -keyout /etc/bloonix/wtrm/pki/server.key -batch
    chown root:bloonix /etc/bloonix/wtrm/pki/server.key /etc/bloonix/wtrm/pki/server.cert
    chmod 640 /etc/bloonix/wtrm/pki/server.key /etc/bloonix/wtrm/pki/server.cert
fi

%if 0%{?with_systemd}
%systemd_post bloonix-wtrm.service
systemctl condrestart bloonix-wtrm.service
%else
/sbin/chkconfig --add bloonix-wtrm
/sbin/service bloonix-wtrm condrestart &>/dev/null
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun bloonix-wtrm.service
%else
if [ $1 -eq 0 ]; then
    /sbin/service bloonix-wtrm stop &>/dev/null || :
    /sbin/chkconfig --del bloonix-wtrm
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%dir %attr(0755, root, root) %{blxdir}
%dir %attr(0755, root, root) %{blxdir}/etc
%dir %attr(0755, root, root) %{blxdir}/etc/wtrm
%{blxdir}/etc/wtrm/main.conf
%dir %attr(0755, root, root) %{blxdir}/etc/systemd
%{blxdir}/etc/systemd/bloonix-wtrm.service
%dir %attr(0755, root, root) %{blxdir}/etc/init.d
%{blxdir}/etc/init.d/bloonix-wtrm
%dir %attr(0750, bloonix, bloonix) %{logdir}
%dir %attr(0750, bloonix, bloonix) %{rundir}

%{_bindir}/bloonix-wtrm

%if 0%{?with_systemd}
%{_unitdir}/bloonix-wtrm.service
%else
%{initdir}/bloonix-wtrm
%endif

%dir %attr(0755, root, root) %{docdir}
%doc %attr(0444, root, root) %{docdir}/ChangeLog
%doc %attr(0444, root, root) %{docdir}/LICENSE

%changelog
* Tue Aug 18 2015 Jonny Schulz <js@bloonix.de> - 0.6-1
- Fixed %preun section in spec file.
* Sat Mar 21 2015 Jonny Schulz <js@bloonix.de> - 0.5-1
- Switched from FCGI to Bloonix::IO::SIPC.
* Mon Mar 09 2015 Jonny Schulz <js@bloonix.de> - 0.4-1
- Path /srv/bloonix/wtrm removed.
* Thu Jan 29 2015 Jonny Schulz <js@bloonix.de> - 0.3-2
- Fixed %preun.
* Wed Nov 26 2014 Jonny Schulz <js@bloonix.de> - 0.3-1
- First DEB/RPM release.
