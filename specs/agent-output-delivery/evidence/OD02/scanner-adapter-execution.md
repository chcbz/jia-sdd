# Production scanner adapter probe

Root executed the retained `scanner-adapter-probe/ScannerAdapterProbe.java` harness against the current compiled `ClamAvOutputMalwareScanner` on 2026-09-09 at 21:52 UTC, using Temurin 21 javac/java and a 128-MiB heap. Compilation and execution exited 0. The service/API classpaths and their relevant source/class hashes are recorded in `scanner-adapter-probe.json`. No Gradle command or product source edit was made.

The clean input was the exact canonical `fixtures.json` sampleFile: `report.md`, 13 bytes, SHA-256 `ecf701f727d9e2d77c4aa49ac6fbbcc997278aca010bddeeb961c10cf54d435a`. The real local ClamAV daemon at port 13310 accepted it; the adapter returned a nonempty engine version. The same adapter rejected EICAR, enforced a 12-byte bound against the 13-byte fixture, and threw IOException when pointed at a closed local port.

All four component checks passed. They do not prove that scanner unavailability leaves a database upload VERIFYING, that retry survives restart, or that a successful scan commits READY with correct quota. Those application tests remain required. This is separate from the archived storage JUnit test; do not add these probe cases to its suite count or to OD01 results.

The harness is reproducible after compiling the API worktree: compile the retained Java file into a temporary directory with the service/API class directories on `javac -cp`; run `java -Xmx128m` with that temporary directory plus the same classpath and a file containing the exact canonical sample bytes. The original invocation used a temporary sample file generated directly from `fixtures.json`; the harness itself does not load local credentials.
