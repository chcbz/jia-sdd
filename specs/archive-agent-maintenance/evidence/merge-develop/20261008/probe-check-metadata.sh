#!/usr/bin/env bash
set -euo pipefail
base=/tmp/cyf-aam-merge-develop-20261008
[ "$(mysql --no-defaults --socket="$base/mysql-attempt2.sock" -u root -N -B -e 'SELECT @@datadir')" = "$base/mysql-data-attempt2/" ]
mysql --no-defaults --socket="$base/mysql-attempt2.sock" -u root -N -B <<'SQL'
CREATE DATABASE cyf_check_metadata_aam_merge_20261008;
CREATE TABLE cyf_check_metadata_aam_merge_20261008.probe (sha256 CHAR(64) CHARACTER SET ascii COLLATE ascii_bin NOT NULL, byte_length BIGINT NOT NULL, revision BIGINT NOT NULL, mime_type VARCHAR(100) CHARACTER SET ascii COLLATE ascii_bin NOT NULL, state VARCHAR(16) CHARACTER SET ascii COLLATE ascii_bin NOT NULL, CONSTRAINT chk_probe_sha CHECK (sha256 REGEXP '^[0-9a-f]{64}$'), CONSTRAINT chk_probe_bytes CHECK ((byte_length >= 1) AND (revision >= 1)), CONSTRAINT chk_probe_mime CHECK (mime_type='text/plain'), CONSTRAINT chk_probe_state CHECK (state IN ('PENDING','DELETE_PENDING','REFERENCED','DELETED'))) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_bin;
SELECT CONSTRAINT_NAME,CHECK_CLAUSE FROM information_schema.CHECK_CONSTRAINTS WHERE CONSTRAINT_SCHEMA='cyf_check_metadata_aam_merge_20261008';
SQL
