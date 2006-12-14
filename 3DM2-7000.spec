Summary:	3DM2 Management Utility
Name:		3DM2-7000
Version:	9.3.0.7
Release:	1
License:	comercial
Group:		Development/Libraries
Source0:	http://www.3ware.com/download/Escalade7000Series/%{version}/3DM2-Linux-%{version}.tgz
# Source0-md5:	49b699c1f26eac174df56c860ee7ff47
NoSource:	0
Source1:	http://www.3ware.com/download/Escalade7000Series/%{version}/%{version}_Release_Notes_Web.pdf
# Source1-md5:	b79add47a9d6905d7fdf611f063ca071
NoSource:	1
Source2:	3dm2-7000.init
URL:		http://www.pers.pl
ExclusiveArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
3DM2 Management Utility for 3ware RAID controllers. 
It supports Escalade 7000/8000 series controlers and 
AMCC 3ware 9550SX/9590SE.

%prep
%setup -q -c -n 3DM2
tar -xvzf 3dm-lnx.tgz
tar -xvzf 3dm-help.tgz
tar -xvzf 3dm-msg.tgz
cp %{SOURCE1} .

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/3dm2
install -d $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d
install -d $RPM_BUILD_ROOT%{_datadir}/3dm2/msg
cp -a en $RPM_BUILD_ROOT%{_datadir}/3dm2
cp *_msg_en $RPM_BUILD_ROOT%{_datadir}/3dm2/msg
cp 3dm2.x86 $RPM_BUILD_ROOT%{_sbindir}/3dm2
cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/3dm2

cat > $RPM_BUILD_ROOT/%{_sysconfdir}/3dm2/3dm2.conf << EOF
Port 888
EmailEnable 0
EmailSender [none]
EmailServer [none]
EmailRecipient [none]
EmailSeverity 3
ROpwd twOmwmsK8lKk2
ADMINpwd twOmwmsK8lKk2
RemoteAccess 0
Language 0
Logger 0
Refresh 5
BGRate 3333333333333333
MsgPath /usr/share/3dm2/msg
Help /usr/share/3dm2/en
OEM 0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
/sbin/chkconfig --add 3dm2
%service 3dm2 restart "3DM2 Utility"

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del 3dm2
	%service 3dm2 stop
fi            

%files
%defattr(644,root,root,755)
%doc version.3dm license.txt %{version}_Release_Notes_Web.pdf
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/3dm2
%attr(644,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/3dm2/3dm2.conf
%dir %{_datadir}/3dm2
%dir %{_datadir}/3dm2/msg
%dir %{_datadir}/3dm2/en
%dir %{_datadir}/3dm2/en/images
%{_datadir}/3dm2/msg/*msg*
%{_datadir}/3dm2/en/*.html
%{_datadir}/3dm2/en/*.css
%{_datadir}/3dm2/en/images/*.gif
%{_datadir}/3dm2/en/images/*.png
%{_datadir}/3dm2/en/images/*.jpg
%attr(744,root,root) %{_sysconfdir}/rc.d/init.d/3dm2
