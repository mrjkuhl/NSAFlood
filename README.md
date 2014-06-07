				NSAFlood
				========

	This directory contains the 1.0 release of NSAFlood

About
-----

NSAFlood is a BASH program which aims to be used as a weapon against Internet surveillance. NSAFlood achieves this goal through the transfer of encrypted data between two or more computers connected to the Internet.

Installation
------------

Instructions to install this program are contained within the file INSTALL.

Licensing
---------

This program is subject to the terms of the GNU General Public License v3, the text of which is contained within the file COPYING.

Verifying
---------

To verify the integrity of the archive contents, you need to check the signature of the MD5SUMS file, then compare the individual file sums, like follows:

```Shell
gpg --verify MD5SUMS.SIG MD5SUMS
sha512sum file
```

If you do not have the public key needed to verify the MD5SUMS signature, download it as so:

```Shell
gpg --keyserver keys.gnupg.net --recv-key 0x01139e11ff940f07
```
