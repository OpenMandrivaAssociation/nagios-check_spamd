%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	Spamd monitoring script for use with Nagios
Name:		nagios-check_spamd
Version:	0.01
Release:	7
License:	Apache License
Group:		Networking/Other
URL:		http://www.apache.org/
Source0:	http://svn.apache.org/repos/asf/spamassassin/trunk/contrib/check_spamd
Requires:	nagios-plugins
Requires:	perl(Time::HiRes)
Requires:	perl(Mail::SpamAssassin::Client)
Requires:	perl(Mail::SpamAssassin::Timeout)
BuildArch:  noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The purpose of this program is to provide a tool to monitor the status of
"spamd" server processes. spamd is the daemonized version of the spamassassin
executable, both provided in the SpamAssassin distribution.

This program is designed for use, as a plugin, with the Nagios service
monitoring software available from http://nagios.org. It might be compatible
with other service monitoring packages. It is also useful as a command line
utility or as a component of a custom shell script.

%prep
%setup -q -c -T

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/nagios/plugins
install -m 755 %{SOURCE0} %{buildroot}%{_datadir}/nagios/plugins

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_spamd.cfg <<'EOF'
define command {
	command_name    check_spamd
	command_line    %{_datadir}/nagios/plugins/check_spamd -H $HOSTADDRESS$ -c $ARG1$ -p $ARG2$ -t $ARG3$ -w $ARG4$
}
EOF

%if %mdkversion < 200900
%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_spamd.cfg
%{_datadir}/nagios/plugins/check_spamd


%changelog
* Sat Dec 11 2010 Oden Eriksson <oeriksson@mandriva.com> 0.01-6mdv2011.0
+ Revision: 620465
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 0.01-5mdv2010.0
+ Revision: 440228
- rebuild

* Mon Dec 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.01-4mdv2009.1
+ Revision: 314657
- now a noarch package
- use a herein document for configuration
- reply on filetrigger for reloading nagios

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 0.01-4mdv2009.0
+ Revision: 253534
- rebuild
- fix summary-ended-with-dot

* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.01-2mdv2008.1
+ Revision: 163162
- whoops!, it can't be a noarch package :-)

* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.01-1mdv2008.1
+ Revision: 163156
- import nagios-check_spamd


* Wed Feb 06 2008 Oden Eriksson <oeriksson@mandriva.com> 0.01-1mdv2008.1
- initial Mandriva package
