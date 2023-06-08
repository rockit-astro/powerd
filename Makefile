RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	${RPMBUILD} -ba observatory-power-server.spec
	${RPMBUILD} -ba observatory-power-client.spec
	${RPMBUILD} -ba python3-warwick-observatory-power.spec
	${RPMBUILD} -ba onemetre-power-data.spec
	${RPMBUILD} -ba superwasp-power-data.spec
	${RPMBUILD} -ba halfmetre-power-data.spec
	${RPMBUILD} -ba clasp-power-data.spec
	${RPMBUILD} -ba goto-power-data.spec
	mv build/noarch/*.rpm .
	rm -rf build

install:
	@python3 setup.py install
	@cp powerd power /usr/bin/
	@cp powerd@.service /etc/systemd/system/
	@cp completion/power /etc/bash_completion.d/
	@install -d /etc/powerd
	@echo ""
	@echo "Installation complete."
	@echo "Now copy the relevant json config files to /etc/opsd/"
