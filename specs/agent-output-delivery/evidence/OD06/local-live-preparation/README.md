# Isolated live R1 preparation

Created a dedicated empty MySQL database and MinIO bucket; exact names are in resources.json. No product schema or fixtures have been installed and no API has started at this point.

The application.properties.template is an unverified launch draft. Use an explicit spring.config.location so bundled dev/production destinations are not inherited. Inject task-owned credentials from 0600 local files into the child environment; do not archive them. HTTP binds loopback10018, MySQL13306, Redis16379, MinIO19000 and ClamAV13310. The ChatClient provider points at unused loopback19999 because ChatClientConfig unconditionally requires a builder; this does not prove model invocation or a running application. Unused LDAP/Elasticsearch/Rabbit endpoints remain loopback placeholders.

After the frozen API candidate passes independent review, the sole verification operator must resolve the actual bean/schema/auth startup graph, then exercise trusted dispatch and the accepted client. Keep startup, component-test, live-HTTP, browser and release evidence distinct.
