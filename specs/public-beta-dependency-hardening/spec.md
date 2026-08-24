# Public beta dependency hardening

## Problem

The exact Web lockfile accepted for the 2026-08-24 account-security release contains DOMPurify, PostCSS and nanoid advisories. The accepted release exception is narrowly based on current call-path reachability and static-build boundaries; it must not become permanent debt.

## Goal

Upgrade the affected packages without `npm audit fix --force`, preserve sanitizer behavior, rebuild the public artifact, and independently verify that Markdown/Chat rendering remains XSS-safe and the static build remains reproducible.

## Scope

- Direct DOMPurify upgrade and sanitizer regression/adversarial tests.
- Lockfile-resolved PostCSS/nanoid upgrades and build-input/source-map threat checks.
- Full focused tests, production build, lockfile-keyed audit evidence and independent security review.
