RPMBUILD = rpmbuild --define "_topdir %(pwd)/build" \
        --define "_builddir %{_topdir}" \
        --define "_rpmdir %{_topdir}" \
        --define "_srcrpmdir %{_topdir}" \
        --define "_sourcedir %(pwd)"

all:
	mkdir -p build
	${RPMBUILD} -ba onemetre-power-server.spec
	${RPMBUILD} -ba onemetre-power-client.spec

	cp power power.bak
	cp light light.bak
	awk '{sub("DAEMON = .*$$","DAEMON = daemons.rasa_power"); print $0}' power.bak > power
	awk '{sub("DAEMON = .*$$","DAEMON = daemons.rasa_power"); print $0}' light.bak > light
	${RPMBUILD} -ba rasa-power-server.spec
	${RPMBUILD} -ba rasa-power-client.spec

	${RPMBUILD} -ba python36-warwick-observatory-power.spec
	mv build/noarch/*.rpm .
	rm -rf build
	mv power.bak power
	mv light.bak light

