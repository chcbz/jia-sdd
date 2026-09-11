# R04 local-header/central-directory counterexample

Root ran a bounded standalone probe against the exact `010a1022` `OutputContentInspector.java` and `OutputUploadException.java` sources. Their Git/source SHA-256 association and fixture hashes are in `observation.json`. Only those sources plus `ZipStructureProbe.java` were compiled with the task-owned Java 21 `javac` into `/tmp/cyf-od02-zip-structure-probe/classes`; no API source was changed and no Gradle, database, object storage, scanner or live HTTP request was involved.

Both fixtures contain harmless `visible.txt` (2 bytes) and a local `hidden.txt` record (1,024 repeated `x` bytes). The malformed fixture keeps only the first central-directory entry and adjusts the EOCD count/size/offset to that directory. Its second local record remains physically present.

With a 64-byte member limit and 4,096-byte tree limit:

```text
valid-two-members.zip central=2 local=2 REJECTED OUTPUT_ARCHIVE_LIMIT
unlisted-local-member.zip central=1 local=2 ACCEPTED application/zip
```

`ZipFile` enumerates the central directory; `ZipInputStream` sees both local records. The current inspector counts only the former and therefore does not establish complete local/central consistency or account for every physical archive member. This was sent to the independent reviewer for R04 disposition. It demonstrates a content-inspector gap, not that malware or this archive reaches READY in a full deployed system.

Reproduction command shape: `javac -d PROBE_CLASSES` with the two named candidate source files and the preserved probe, then `java -cp PROBE_CLASSES cn.jia.agent.output.service.ZipStructureProbe valid-two-members.zip unlisted-local-member.zip`. Use the task-owned JDK or the same supported Java 21. The printed labels are fixed test filenames; no user content or credentials were used.
