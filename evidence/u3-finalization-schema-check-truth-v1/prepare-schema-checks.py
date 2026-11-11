from pathlib import Path
import json,hashlib
root=Path('/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-entry-finalization-integration-v1')
e=Path('/home/isp/wsps/cyf/evidence/u3-finalization-schema-check-truth-v1')
f=Path('/home/isp/wsps/cyf/evidence/u1u3-entry-finalization-integration-v1/mysql-check-clause-snapshots-v1.json')
snapshot=json.loads(f.read_text());good=snapshot['snapshots'][1]['check_clauses']
def norm(s):
 s=s.replace("\\'","'");out=[];quoted=False;i=0
 while i<len(s):
  c=s[i]
  if c=="'":quoted=not quoted;out.append(c)
  elif quoted:out.append(c)
  elif s[i:i+8].lower()=='_utf8mb4':i+=7
  elif not c.isspace() and c!='`':out.append(c.lower())
  i+=1
 return ''.join(out)
def j(s):return json.dumps(s,ensure_ascii=False)
paths=[]
for module,pkg,clazz,checks in [('agent/jia-agent-service','cn.jia.agent.config','AgentSelectedOutputFinalizationSchemaInitializer',{'chk_asof_lease':good['chk_asof_lease']}),('chat/jia-chat-service','cn.jia.chat.config','ChatSelectedOutputFinalizationSchemaInitializer',{'chk_csof_progress':good['chk_csof_progress'],'chk_csof_terminal':good['chk_csof_terminal']})]:
 source=root/module/'src/main/java'/Path(*pkg.split('.'))/(clazz+'.java');s=source.read_text()
 needle='    private final JdbcTemplate jdbc;'
 literals=',\n'.join('            '+j(k)+', '+j(norm(v)) for k,v in checks.items())
 constants='''    // Evidence: actual MySQL8.0.21 old/repaired finalization checks admitted/rejected NULL
    // differently while sharing constraint names and ENFORCED=YES. Compare only these
    // three proven-sensitive definitions; preserve boolean grouping and binary literals.
    private static final Map<String,String> REQUIRED_CHECK_EXPRESSIONS=Map.of(
'''+literals+');\n'
 assert needle in s;s=s.replace(needle,constants+needle)
 old='''SELECT constraint_name,enforced FROM information_schema.table_constraints
                WHERE constraint_schema=DATABASE() AND table_name=? AND constraint_type='CHECK' '''.rstrip()
 new='''SELECT t.constraint_name,t.enforced,c.check_clause
                FROM information_schema.table_constraints t
                JOIN information_schema.check_constraints c
                  ON c.constraint_schema=t.constraint_schema AND c.constraint_name=t.constraint_name
                WHERE t.constraint_schema=DATABASE() AND t.table_name=? AND t.constraint_type='CHECK' '''.rstrip()
 assert old in s;s=s.replace(old,new)
 if clazz.startswith('Agent'):
  s=s.replace('''        Map<String,String> actual=new LinkedHashMap<>();
        for(Map<String,Object> row:jdbc.queryForList("""
                SELECT t.constraint_name''','''        Map<String,String> actual=new LinkedHashMap<>();
        Map<String,String> clauses=new LinkedHashMap<>();
        for(Map<String,Object> row:jdbc.queryForList("""
                SELECT t.constraint_name''')
  old='''""",TABLE))actual.put(text(row,"constraint_name"),text(row,"enforced"));'''
 else:
  s=s.replace('''        Map<String,String> actual=new LinkedHashMap<>();
        for(Map<String,Object> row:jdbc.queryForList("""
                SELECT t.constraint_name''','''        Map<String,String> actual=new LinkedHashMap<>();
        Map<String,String> clauses=new LinkedHashMap<>();
        for(Map<String,Object> row:jdbc.queryForList("""
                SELECT t.constraint_name''')
  old='''""",table))actual.put(text(row,"constraint_name"),text(row,"enforced"));'''
 arg='TABLE' if clazz.startswith('Agent') else 'table'
 new='''""",'''+arg+''')){
            String name=text(row,"constraint_name");
            actual.put(name,text(row,"enforced"));clauses.put(name,text(row,"check_clause"));
        }'''
 assert old in s;s=s.replace(old,new)
 old='''            throw new IllegalStateException("'''+('Selected-output finalization' if clazz.startswith('Agent') else 'Finalization')+''' check drift: "+check);
    }'''
 add='''            throw new IllegalStateException("'''+('Selected-output finalization' if clazz.startswith('Agent') else 'Finalization')+''' check drift: "+check);
        for(var required:REQUIRED_CHECK_EXPRESSIONS.entrySet())'''+('' if clazz.startswith('Agent') else '''if(CHECKS.get(table).contains(required.getKey()))''')+'''
            if(!required.getValue().equals(compactCheckExpression(clauses.get(required.getKey()))))
                throw new IllegalStateException("Finalization check definition drift: "+required.getKey());
    }

    private static String compactCheckExpression(String source){
        if(source==null)return null;
        String value=source.replace("\\\\'","'");StringBuilder result=new StringBuilder();boolean quoted=false;
        for(int i=0;i<value.length();i++){
            char c=value.charAt(i);
            if(c=='\\\''){quoted=!quoted;result.append(c);}
            else if(quoted)result.append(c);
            else if(value.regionMatches(true,i,"_utf8mb4",0,8))i+=7;
            else if(!Character.isWhitespace(c)&&c!='`')result.append(Character.toLowerCase(c));
        }
        return result.toString();
    }'''
 assert old in s;s=s.replace(old,add);source.write_text(s);paths.append(str(source))
 resource=root/module/'src/test/resources/mmd-finalization-schema-checks-mysql8021.json';resource.parent.mkdir(parents=True,exist_ok=True);resource.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n');paths.append(str(resource))
 testSourceDir='src/test/java' if clazz.startswith('Agent') else 'src/chatDeliberationTest/java'
 test=root/module/testSourceDir/Path(*pkg.split('.'))/(clazz+'Test.java');s=test.read_text()
 method='''        var method='''+clazz+'''.class.getDeclaredMethod("validateChecks",JdbcTemplate.class'''+(');' if clazz.startswith('Agent') else ',String.class);')
 invoke='''method.invoke(null,jdbc'''+(');' if clazz.startswith('Agent') else ',"chat_selected_output_finalization");')
 names=['chk_asof_versions','chk_asof_digest','chk_asof_phase','chk_asof_lease'] if clazz.startswith('Agent') else ['chk_csof_versions','chk_csof_key','chk_csof_delivery_state','chk_csof_state','chk_csof_stage','chk_csof_progress','chk_csof_outcome','chk_csof_terminal']
 checkName=list(checks)[0]
 more='''    @Test
    void actualRepairedMysqlCheckDefinitionsAreAcceptedDespiteCaseInsensitiveMetadataLabels() throws Exception {
        invokeChecks(actualCheckRows(1,null,null));
    }

    @Test
    void actualOldSameNamedEnforcedMysqlChecksFailBeforeActivation() throws Exception {
        var failure=assertThrows(IllegalStateException.class,()->invokeChecks(actualCheckRows(0,null,null)));
        assertTrue(failure.getMessage().contains("check definition drift"));
    }

    @Test
    void requiredGuardTextInsideAlwaysTrueExpressionCannotHideDefinitionDrift() throws Exception {
        var rows=actualCheckRows(1,"'''+checkName+'''",clause(1,"'''+checkName+'''")+" OR 1=1");
        assertThrows(IllegalStateException.class,()->invokeChecks(rows));
    }

    @Test
    void nullCheckDefinitionNeverCountsAsEnforcedRequiredInvariant() throws Exception {
        assertThrows(IllegalStateException.class,()->invokeChecks(actualCheckRows(1,"'''+checkName+'''",null)));
    }

    @Test
    void checkLiteralCaseAndWhitespaceAreNotErasedByMetadataNormalization() throws Exception {
        String original=clause(1,"'''+checkName+'''");
        String changed=original.replace("'''+('LEASED' if clazz.startswith('Agent') else 'SUBMITTED')+'''","'''+('leased' if clazz.startswith('Agent') else 'submitted')+'''");
        assertNotEquals(original,changed);
        assertThrows(IllegalStateException.class,()->invokeChecks(actualCheckRows(1,"'''+checkName+'''",changed)));
        changed=original.replace("'''+('LEASED' if clazz.startswith('Agent') else 'SUBMITTED')+'''","'''+('LE ASED' if clazz.startswith('Agent') else 'SUB MITTED')+'''");
        assertThrows(IllegalStateException.class,()->invokeChecks(actualCheckRows(1,"'''+checkName+'''",original.replace("'''+('LEASED' if clazz.startswith('Agent') else 'SUBMITTED')+'''","'''+('LE ASED' if clazz.startswith('Agent') else 'SUB MITTED')+'''"))));
    }

    @Test
    void unenforcedCorrectDefinitionStillFailsClosed() throws Exception {
        var rows=actualCheckRows(1,null,null);rows.getFirst().put("ENFORCED","NO");
        assertThrows(IllegalStateException.class,()->invokeChecks(rows));
    }

    private static String clause(int snapshot,String check) throws Exception {
        try(var in=new org.springframework.core.io.ClassPathResource("mmd-finalization-schema-checks-mysql8021.json").getInputStream()){
            return new tools.jackson.databind.ObjectMapper().readTree(in).get("snapshots").get(snapshot)
                    .get("check_clauses").get(check).textValue();
        }
    }
    private static List<Map<String,Object>> actualCheckRows(int snapshot,String overrideCheck,String overrideValue) throws Exception {
        List<Map<String,Object>> rows=new ArrayList<>();
        for(String name:List.of('''+', '.join(j(n) for n in names)+''')){
            Map<String,Object> row=new LinkedHashMap<>();row.put("CONSTRAINT_NAME",name);row.put("ENFORCED","YES");
            String value='''+('name.equals("chk_asof_lease")' if clazz.startswith('Agent') else 'name.equals("chk_csof_progress")||name.equals("chk_csof_terminal")')+'''?clause(snapshot,name):null;
            row.put("CHECK_CLAUSE",name.equals(overrideCheck)?overrideValue:value);rows.add(row);
        }return rows;
    }
    private static void invokeChecks(List<Map<String,Object>> rows) throws Exception {
        var jdbc=mock(JdbcTemplate.class);
        when(jdbc.queryForList(anyString(),any(Object[].class))).thenReturn(rows);
'''+method+'''
        method.setAccessible(true);
        try{'''+invoke+'''}catch(InvocationTargetException failure){
            if(failure.getCause() instanceof RuntimeException cause)throw cause;
            throw failure;
        }
    }

'''
 needle='    private static void invokeIndexes';assert needle in s;s=s.replace(needle,more+needle);test.write_text(s);paths.append(str(test))
(e/'schema-check-source-manifest-v1.json').write_text(json.dumps({'baseline_commit':'f93febe983afe3619e1b5057937d9db330adece0','actual_mysql_snapshot_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'changed_paths':paths,'constraint_expression_scope':['chk_asof_lease','chk_csof_progress','chk_csof_terminal'],'reason':'Actual old enforced same-named CHECK clauses admit three impossible NULL states. Compare definitions with semantic grouping and binary literals preserved; no ALTER/DROP/DML, no arbitrary numerical checks.'},indent=2)+'\n')
print('Wrote scoped two initializers/two tests/two actual MySQL fixture resources.')
