# Public image dependency feasibility

OD06 preparation only. No catalog, utility, deployment, native system library, or Gradle configuration was changed. This probe addresses the unresolved canonical build dependency gate; it is not OD02 evidence or production compatibility approval.

The current catalog uses unavailable private coordinates `org.opencv:opencv:4.5.5` and `com.sun.media:jai_imageio:1.1`. The reviewed development init substitutes cached public `org.openpnp:opencv:4.5.5-1` and OSGeo `javax.media:jai_imageio:1.1`. Both utilities are common-core compileOnly/test dependencies. A permanent reviewed catalog/repository change is a possible OD06 repair, avoiding dependence on a developer's external substitution init.

Actual standalone probe on Linux aarch64:

- Extracted only the cached OpenPnP JAR's `nu/pattern/opencv/linux/ARMv8/libopencv_java455.so` into a task-owned `/tmp` directory.
- Compiled the unchanged production `OpenCvUtil.java` and `OcrUtil.java` plus the included synthetic probe with JDK 21. Existing `FileUtil.class` was on the compile classpath solely for the uninvoked `tagMatchImage` method; it was absent from the execution classpath.
- Ran production `OpenCvUtil.threshold`, preserving its `System.loadLibrary` behavior with a process-local `java.library.path`, and checked the synthetic threshold pixels/dimensions.
- Ran production `OcrUtil.createImage` and verified all 256 RGB pixels survived its TIFF conversion. No Tesseract process or OCR recognition was invoked.
- Both javac and java exited 0; OpenCV reports 4.5.5. Exact argument arrays, output and source/JAR/native hashes are in `observation.json`.

This establishes a narrow executable compatibility example for these cached replacement artifacts on the development ARM host. It does not compare against the unavailable private JAR, test every image API, prove target-host JNI installation, fetch fresh dependencies, build the production package, or validate OCR recognition. No credentials were read or sent by the probe.

If the canonical dependency gate remains unresolved at OD06, assign the sole API writer a bounded build repair: review public coordinate/repository provenance, preserve intended dependency scopes and target-host native loading, then verify canonical packaging without the development substitution. Keep credentials restricted to their configured origin. Do not silently promote this probe or the external init to a release build.
