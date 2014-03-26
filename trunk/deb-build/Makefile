DIR_ORIGIN = ../src
DIR_BASE_INSTALL = /opt/apt-satellites

all: install

install:
	PS4="CMD:\${0}:pid=\${$}: "
	set -x
	test -d $(DESTDIR)/usr/bin/ || install --directory --owner=root --group=root --mode=755 --verbose $(DESTDIR)/usr/bin/
	test -d $(DESTDIR)/$(DIR_BASE_INSTALL) || install --directory --owner=root --group=root --mode=755 --verbose $(DESTDIR)/$(DIR_BASE_INSTALL)
	install --owner=root --group=root --mode=755 --verbose $(DIR_ORIGIN)/apt-compare-versions $(DESTDIR)/usr/bin/apt-compare-versions
	install --owner=root --group=root --mode=755 --verbose $(DIR_ORIGIN)/deb-repack $(DESTDIR)/usr/bin/deb-repack
	install --owner=root --group=root --mode=644 --verbose $(DIR_ORIGIN)/constant.py $(DESTDIR)/$(DIR_BASE_INSTALL)/constant.py

clean:
	echo "INFO:${0}:pid=${$}: Nothing to be done for cleanup after this DEB package build."
