SELECT tc.constraint_name,tc.enforced,cc.check_clause
FROM information_schema.table_constraints tc
JOIN information_schema.check_constraints cc
  ON cc.constraint_schema=tc.constraint_schema AND cc.constraint_name=tc.constraint_name
WHERE tc.constraint_schema=DATABASE() AND tc.table_name IN ('chat_typed_outcome','chat_typed_pending_question','chat_typed_proposal','chat_typed_admission')
  AND tc.constraint_type='CHECK';
