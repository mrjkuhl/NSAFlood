
1.1.2
-----
6/8/2014

Bugs:
- NSAFlood now checks for, and deletes $GARBAGEFILE before writing to 
$GARBAGEFILE.

1.1.1	
-----
6/8/2014

Misc:

- Added man page
- Added install script
- Added CHANGELOG.md
- Edited Usage section of README.md

- Removed the INSTALL file
- Removed the README file
- Removed the CHANGELOG file

1.1	
---
6/6/2014

Features:

- Added a new option which controls the bandwidth usage of the program,
  --bandwidth and -b.
- Added a new option which allows for the use of keyfiles for
  authentication.

- Removed the encryption of the garbage file by openssl.

Misc:

- Compressed several blocks of echo calls down to one call each.
- Added the file CHANGELOG.
- Added the Usage section to README and README.md.
- Formatted README and README.md to only have 80 characters of text on 
  any single line.
