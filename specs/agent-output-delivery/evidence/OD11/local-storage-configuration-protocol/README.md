# Real local storage configuration protocol

Using the already running isolated MinIO of the tested release and a new local-only bucket, a standard-library AWS4 implementation verified create bucket, unversioned state, hard quota set/get and20-byte PUT/GET. Anonymous object GET returned403. A2KiB PUT against a1KiB test quota returned400/XMinioAdminBucketQuotaExceeded; the bucket quota was restored to512MiB. These are bounded protocol cases, not cumulative/concurrent quota exhaustion proof or production acceptance. Credentials were read only in memory; no credentials/headers appear in reports. Existing R1 artifacts/buckets were unchanged.

The exact MinIO release go.mod pins madmin-go/v3 v3.0.109; its official quota-commands.go confirms the v3 admin path and size/quotatype payload. Source SHA a7ffa10557d998a42250e60329b3795e3bf8b17661d24e6bb7fabbf4b1533d85. No production bucket or setting has been changed.
