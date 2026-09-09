# OD02 real MySQL DDL contract probe

Root executed an isolated probe on local MySQL 8.0.45 at 2026-09-09 21:57 UTC, exit 0. It used the installed PyMySQL module and mode-0600 local MySQL credential file in-process. No credential value was printed, no Gradle command ran, and no API source file or existing database was changed.

The input was the exact draft `agent/jia-agent-mapper/src/main/resources/db/output-delivery-002-object-schema.sql`, SHA-256 `034edf2a133a65510be51d3bf78e5fc716a2cc76d3ca65dc55300b3b542492fd`. The root schema contract digest was `a3b4cceb2bbffa9053aba80c6fd1ed00e8e3cc70a5febd70b861ee7ed05ffc7f`. The detailed table counts and outcome are in `mysql-ddl-contract-probe.json`.

The inline Python probe created a random database under the `cyf_od02_root_` prefix, executed all eight CREATE TABLE IF NOT EXISTS statements twice, and compared information_schema metadata with the contract. It checked exact column sets, types, nullability, explicitly declared defaults, primary-key order, unique and ordinary index column sequences, InnoDB and `utf8mb4_0900_bin` table collation. All eight tables matched. The same connection then dropped only the database it had created; the report confirms removal.

This proves the observed DDL executes and matches those structural contract fields on the local MySQL version. It does not execute the production `OutputObjectSchemaInitializer`, inject incompatible installed schemas, test check-constraint behavior or prove upload/receipt/quota transactions. Production initializer drift rejection and application concurrency tests remain required. The API DDL was uncommitted during this probe; its recorded hash must be associated with the eventual candidate or explicitly superseded.
