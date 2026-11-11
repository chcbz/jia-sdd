# HOST R8 common parser correction

R7 all on88453c6b/tree3a416412 passed build-contract and locks, then ordinary deploy-api14 failed SHOW_HELP unbound under set-u. Full evidence /tmp/cyf-host-adapt-r7.SVJuDg; failed cache104e8591bb6f31802b5d89d8471b58584c6a9f6ad6c4bd70a442f7e91a98fb3a. No completed transaction. Controller stopped count2 before this bounded authorization.

Root cause common.sh604–638 parse_common_args initializes input/execute/positionals but only assigns SHOW_HELP in help branch. API deploy/build/verify assume numeric defined SHOW_HELP. Caller workaround would leave stale/inherited help state; fix deterministic initialization inside common parser for every invocation.

Original HOST Writer owns ONLY common.sh plus existing test-api-host-adaptation.sh (or existing test-common.sh if required and explicitly reported). Add regression source for noargs, explicit input, dryrun, execute, help/-h, repeated help-to-normal calls and inherited SHOW_HELP value reset. Preserve parsing/unknown-argument behavior and execution approval gates. Pure source-common/parse-only env-i microprobe allowed (no artifact lookup, adapters, canonical, selector, network/build/production). Static/tinycleancommit -> fresh sharedcommon delta review and Web dependency impact -> one newtree all. Do not change production callers merely to hide unbound variable.

This changes accepted common digest, so final HOST/Web tool pins and byte-exact integration MUST reference newly accepted common bytes. Prior common2adc digest is historical, not automatically final. Web R4 fixture correction remains disjoint; no Web-owned files by HOST. Current merged e86 remains immutable. All prior source safety/transaction findings remain closed and should not be broadly redesigned.
