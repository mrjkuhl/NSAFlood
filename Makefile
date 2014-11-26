#!/usr/bin/make -f

INSTALLDATA= install -c -m 644
CONFDIR= /etc/nsaflood

KEYS= privatekey publickey
MAN= nsaflood.1.gz

.PHONY : install
install : installbin installconfig installinfo clean

.PHONY : installbin
installbin:
	install -c nsaflood /usr/local/bin

.PHONY : installconfig
installconfig : makekeys
	mkdir -p $(CONFDIR)/pubkeys
	touch $(CONFDIR)/peertab
	$(INSTALLDATA) privatekey $(CONFDIR)
	$(INSTALLDATA) publickey $(CONFDIR)
	$(INSTALLDATA) nsaflood.conf $(CONFDIR)

.PHONY : installinfo
installinfo : makeman
	$(INSTALLDATA) $(MAN) /usr/share/man/man1

.PHONY : makekeys
makekeys :
	openssl genrsa -out privatekey 4096
	openssl rsa -in privatekey -out publickey -outform PEM -pubout

.PHONY : makeman
makeman :
	gzip -c nsaflood.1 > $(MAN)

.PHONY : clean
clean :
	rm $(KEYS) $(MAN)
