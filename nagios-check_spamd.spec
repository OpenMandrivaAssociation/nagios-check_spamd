%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	Spamd monitoring script for use with Nagios
Name:		nagios-check_spamd
Version:	0.01
Release:	%mkrel 5
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
