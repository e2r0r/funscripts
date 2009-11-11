#!/usr/bin/perl

exit if fork();
while(1) {system("svn up /root/192.168.8.192");sleep(5)};
