NSAFlood
--------

This directory contains the 1.2.0 release of NSAFlood, hereby entitled "Spooky Agent."

About
-----

NSAFlood is a BASH program which aims to be used as a weapon against Internet 
surveillance. NSAFlood achieves this goal through the transfer of encrypted data
 between two or more computers connected to the Internet.

Installation
------------

To install NSAFlood, you must execute the install script as root.

Usage
-----

	nsaflood -b=2048 -k=/home/user/.ssh/privkey -s=10 -h=user@remotehost

See the man page for documentation.

To schedule nsaflood in the crontab, log in to root and use the nsaf-sched 
program.

	nsaf-sched -b=2048 -k=/home/user/.ssh/privkey -s=1000 -h-user@remotehost
	nsaf-sched --list -h=user@remotehost
	nsaf-sched --delete=7

See the nsaf-sched man page for documentation.

Licensing
---------

This program is subject to the terms of the GNU General Public License v3, the 
text of which is contained within the file COPYING.

Verifying
---------

To verify the integrity of the archive contents, you need to check the signature
 of the MD5SUMS file, then compare the individual file sums, like follows:

	gpg --verify MD5SUMS.sig MD5SUMS
	sha512sum file

If you do not have the public key needed to verify the MD5SUMS signature, 
download it as so:

	gpg --keyserver keys.gnupg.net --recv-key 0x01139e11ff940f07
