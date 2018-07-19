RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	${RPMBUILD} -ba onemetre-power-server.spec
	${RPMBUILD} -ba onemetre-power-client.spec
	${RPMBUILD} -ba python34-warwick-observatory-power.spec
	mv build/noarch/*.rpm .
	rm -rf build

