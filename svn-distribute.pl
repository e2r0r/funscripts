use Net::SSH::Expect;


#此处添本代码仓库需要同步的服务器组
my @cluster = ('192.168.1.191',
               '192.168.1.190',
               '192.168.1.193'
              );


foreach $svr (@cluster) {
   my $ssh = Net::SSH::Expect->new(
   host =$svr,
   password ='xxx', 
   user ='xxx',
   raw_pty =1
   );
   my $logins = $ssh->login();
   my $command = $ssh->exec('svn up /path');
   $ssh->close();
}
