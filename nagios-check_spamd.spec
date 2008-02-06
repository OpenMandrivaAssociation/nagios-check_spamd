Summary:	Spamd monitoring script for use with Nagios, etc.
Name:		nagios-check_spamd
Version:	0.01
Release:	%mkrel 1
License:	Apache License
Group:		Networking/Other
URL:		http://www.apache.org/
Source0:	http://svn.apache.org/repos/asf/spamassassin/trunk/contrib/check_spamd
Source1:	check_spamd.cfg
Requires:	nagios
Requires:	perl(Time::HiRes)
Requires:	perl(Mail::SpamAssassin::Client)
Requires:	perl(Mail::SpamAssassin::Timeout)
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-buildroot

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

cp %{SOURCE0} check_spamd
cp %{SOURCE1} check_spamd.cfg

perl -pi -e "s|_LIBDIR_|%{_libdir}|g" *.cfg

%build

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_spamd %{buildroot}%{_libdir}/nagios/plugins/
install -m0644 *.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/

%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_spamd.cfg
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_spamd

