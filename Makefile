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
	${RPMBUILD} -ba clasp-power-data.spec
	${RPMBUILD} -ba goto-power-data.spec
	mv build/noarch/*.rpm .
	rm -rf build
