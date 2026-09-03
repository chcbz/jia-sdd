# Public beta dependency hardening design

Status: draft. Prefer the smallest semver-compatible lockfile update. Do not weaken or remove DOMPurify, do not enable custom-element handling/hooks/IN_PLACE without a separate security design, and do not use force-upgrade automation. Any source behavior change requires Web review and a new exact-tree release artifact.
