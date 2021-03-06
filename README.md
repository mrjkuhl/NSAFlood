NSAFlood
--------

This directory contains the 1.0.3 release of NSAFlood.

About
-----

NSAFlood is a program which aims to be used as a weapon against Internet 
surveillance. NSAFlood achieves this goal through the transfer of encrypted data
 between two or more computers connected to the Internet.

Installation
------------

To install NSAFlood, you must call make as root.

Usage
-----

	nsaflood -s 10 -h remotehost

See the man page for documentation.

To schedule nsaflood in the crontab, log in to root and edit the crontab as 
below:

	* 2 * * * root /usr/local/bin/nsaflood --file-size 1000 --host www.newphoenixrise.com

Licensing
---------

This program is subject to the terms of the GNU General Public License v3, the 
text of which is contained within the file COPYING.

Verifying
---------

To verify the integrity of the archive contents, you need to check the signature
 of the MD5SUMS file, then compare the individual file sums, like follows:

	gpg --verify MD5SUMS.sig MD5SUMS
	sha256sum file

If you do not have the public key needed to verify the MD5SUMS signature, 
download it as so:

	gpg --keyserver pgp.mit.edu --recv-key 0x107d24614a65e591
