from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'cyf-api-flow-deploy';s=p.read_text()
s=s.replace("native_need(set(value) == NATIVE_APPROVAL_KEYS | ({'consumed_at'} if value['consumed'] else set()))", "native_need(set(value) == NATIVE_APPROVAL_KEYS | ({'consumed_at'} if value['consumed'] else set()) | ({'rollback_policy'} if 'rollback_policy' in value else set()))\n    native_need(value.get('rollback_policy', 'compatible') in ('compatible', 'forward-only'), 'invalid LOCAL rollback policy')")
s=s.replace("    native_need(type(value) is dict and set(value) == keys and type(value['schema_version']) is int\n                and value['schema_version'] == 4", "    if type(value) is dict and 'rollback_policy' in value:\n        keys.add('rollback_policy')\n    native_need(type(value) is dict and set(value) == keys and type(value['schema_version']) is int\n                and value['schema_version'] == 4")
s=s.replace("    native_need(native_binding(approval) == value['binding_sha256'], 'LOCAL record binding mismatch')", "    if 'rollback_policy' in value:\n        approval['rollback_policy'] = value['rollback_policy']\n    native_need(native_binding(approval) == value['binding_sha256'], 'LOCAL record binding mismatch')")
assert s!=p.read_text();p.write_text(s)
p=root/'cyf-api-flow-install';s=p.read_text();needle='if [[ -z "$RUN_ID" ]]; then\n  LOCAL_ROLLBACK_POLICY='
s=s.replace(needle,'''if [[ -n "$RUN_ID" && ! "$RUN_ID" =~ ^[0-9]+$ ]]; then
  # Persist policy in the source binding: an incompatible migration must never
  # restart the old JAR on failure, including a later recovery invocation.
  LOCAL_ROLLBACK_POLICY="$(transaction_python "$APPROVAL_PATH" <<'PYNATIVE'
import sys
approval = validator['native_read_approval'](Path(sys.argv[1]))
print(approval.get('rollback_policy', 'compatible'))
PYNATIVE
)" || fail 'LOCAL rollback policy is invalid'
  if [[ "$LOCAL_ROLLBACK_POLICY" == forward-only ]]; then
    export CYF_API_FLOW_FORWARD_ONLY=1
  else
    unset CYF_API_FLOW_FORWARD_ONLY
  fi
elif [[ -z "$RUN_ID" ]]; then
  LOCAL_ROLLBACK_POLICY=''')
s=s.replace("    validator['native_record'](payload, path.parent / 'backups')", "    if 'rollback_policy' in approval:\n        payload['rollback_policy'] = approval['rollback_policy']\n    validator['native_record'](payload, path.parent / 'backups')")
assert s!=p.read_text();p.write_text(s)

p=root/'cyf-api-flow-install';s=p.read_text().replace("    open_keys = validator['NATIVE_APPROVAL_KEYS']\n", "    open_keys = validator['NATIVE_APPROVAL_KEYS'] | ({'rollback_policy'} if 'rollback_policy' in approval else set())\n");p.write_text(s)
