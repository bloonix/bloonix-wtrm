CONFIG=Makefile.config

include $(CONFIG)

default: build

build:

	for file in \
		bin/bloonix-wtrm \
		etc/init/bloonix-wtrm \
		etc/init/bloonix-wtrm.service \
		etc/bloonix/wtrm/nginx.conf \
	; do \
		cp $$file.in $$file; \
		sed -i "s!@@PERL@@!$(PERL)!g" $$file; \
		sed -i "s!@@PREFIX@@!$(PREFIX)!g" $$file; \
		sed -i "s!@@CACHEDIR@@!$(CACHEDIR)!g" $$file; \
		sed -i "s!@@CONFDIR@@!$(CONFDIR)!g" $$file; \
		sed -i "s!@@RUNDIR@@!$(RUNDIR)!g" $$file; \
		sed -i "s!@@USRLIBDIR@@!$(USRLIBDIR)!" $$file; \
		sed -i "s!@@SRVDIR@@!$(SRVDIR)!g" $$file; \
		sed -i "s!@@LOGDIR@@!$(LOGDIR)!g" $$file; \
	done;

test:

install:

	# Base Bloonix directories
	for d in $(CACHEDIR) $(LOGDIR) $(RUNDIR) ; do \
		./install-sh -d -m 0750 -o $(USERNAME) -g $(GROUPNAME) $$d/bloonix; \
	done;

	./install-sh -d -m 0755 $(PREFIX)/bin;
	./install-sh -d -m 0755 -o root -g $(GROUPNAME) $(SRVDIR)/bloonix;
	./install-sh -d -m 0755 -o root -g $(GROUPNAME) $(SRVDIR)/bloonix/wtrm;
	./install-sh -d -m 0755 -o root -g root $(CONFDIR)/bloonix;
	./install-sh -d -m 0755 -o root -g root $(CONFDIR)/bloonix/wtrm;

	for file in \
		bloonix-wtrm \
	; do \
		./install-sh -c -m 0755 bin/$$file $(PREFIX)/bin/$$file; \
	done;

	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix/etc/wtrm;
	./install-sh -c -m 0644 etc/bloonix/wtrm/main.conf $(USRLIBDIR)/bloonix/etc/wtrm/main.conf;
	./install-sh -c -m 0644 etc/bloonix/wtrm/nginx.conf $(USRLIBDIR)/bloonix/etc/wtrm/nginx.conf;

	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix/etc/init.d;
	./install-sh -c -m 0755 etc/init/bloonix-wtrm $(USRLIBDIR)/bloonix/etc/init.d/bloonix-wtrm;

	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix/etc/systemd;
	./install-sh -c -m 0755 etc/init/bloonix-wtrm.service $(USRLIBDIR)/bloonix/etc/systemd/bloonix-wtrm.service;

	if test -d /usr/lib/systemd/system ; then \
		./install-sh -c -m 0644 etc/init/bloonix-wtrm.service /usr/lib/systemd/system/; \
	elif test -d /etc/init.d ; then \
		./install-sh -c -m 0755 etc/init/bloonix-wtrm $(INITDIR)/bloonix-wtrm; \
	fi;

	if test "$(BUILDPKG)" = "0" ; then \
		if test ! -e "$(CONFDIR)/bloonix/wtrm/main.conf" ; then \
			./install-sh -c -m 0640 -o root -g $(GROUPNAME) etc/bloonix/wtrm/main.conf $(CONFDIR)/bloonix/wtrm/main.conf; \
		fi; \
		if test ! -e "$(CONFDIR)/bloonix/wtrm/nginx.conf" ; then \
			./install-sh -c -m 0640 -o root -g $(GROUPNAME) etc/bloonix/wtrm/nginx.conf $(CONFDIR)/bloonix/wtrm/nginx.conf; \
		fi; \
	fi;

clean:

