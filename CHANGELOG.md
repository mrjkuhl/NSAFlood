
1.3.1
-----
6/17/2014

nsaflood:
- Fixed $KEYFILE.
- Refactored argument handling.
- Added --help argument for usage.

nsaf-sched:
- Fixed all scheduler variables.
- Refactored argument handling.
- Added --help argument for usage.

1.3.0
-----
6/17/2014

nsaflood:
- Refactored argument handling.
- Added -V and --version arguments, which return the version and licensing information.

nsaf-sched:
- Refactored argument handling.
- Added -V and --version arguments, which return the version and licensing information.

nsaflood.1:
- Added "EXIT STATUS" section.

nsaf-sched.1:
- Added "EXIT STATUS" section.

1.2.0
-----
6/13/2014

New:
- Added nsaf-sched, NSAFlood scheduler.
- Added nsaf-sched man page.

Install
- Updated according to nsaf-sched addition.

nsaflood.1
- Added mention of nsaf-sched in Description section

Readme
- Updated Usage section to include nsaf-sched.

1.1.3
-----
6/10/2014

Bugs:
- NSAFlood now uses mktemp to handle $GARBAGEFILE.

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
