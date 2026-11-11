from pathlib import Path
import subprocess,sys,json,hashlib,re
sys.path.insert(0,'/tmp/ur02-java-static-parser')
from tree_sitter import Language,Parser
import tree_sitter_java
parser=Parser(Language(tree_sitter_java.language()))
wt=Path('/home/isp/wsps/worktrees/ur06-m4-mysql-e05-20261008');base='b125d70c79471be0fc9f306cc0f2e9cd85890ee4';p='agent/jia-agent-service/src/ur06EnrollMysql/'
paths=[p+'java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlAcceptanceTest.java',p+'java/cn/jia/agent/acceptance/ur06/Ur06EnrollMysqlFixture.java',p+'resources/ur06/enroll-mysql-client.mjs',p+'ur06-enroll-mysql.init.gradle', 'agent/jia-agent-service/src/ur04E05Http/java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java','agent/jia-agent-service/src/ur04E05Http/resources/ur04/e05-runtime-http-client.mjs']
def git(*args):return subprocess.check_output(['git','-C',str(wt),*args]).decode().strip()
def blob(path):return subprocess.check_output(['git','-C',str(wt),'show',base+':'+path])
def walk(node):
 yield node
 for c in node.children:yield from walk(c)
def methods(data):
 tree=parser.parse(data);assert not tree.root_node.has_error
 out={}
 for node in walk(tree.root_node):
  if node.type=='method_declaration':
   name=node.child_by_field_name('name').text.decode()
   out.setdefault(name,[]).append(data[node.start_byte:node.end_byte])
 return out
old=methods(blob(paths[0]));current=methods((wt/paths[0]).read_bytes())
foundation=[n for n,v in old.items() if v[0].startswith(b'@Test')];assert len(foundation)==7
for name in foundation:assert current[name]==old[name],name
ur04=p.replace('ur06EnrollMysql','ur04E05Http')+'java/cn/jia/agent/acceptance/ur04/Ur04E05HttpDbAcceptanceTest.java'
original=methods((wt/ur04).read_bytes());six=[n for n,v in original.items() if v[0].startswith(b'@Test')];assert len(six)==6
for name in six:assert current[name]==original[name],name
assert [n for n,v in current.items() if v[0].startswith(b'@Test')]==foundation+six
oracle=['children','hasInbox','hasTerminalFailure','http','resultPath','assertCommittedBusiness','assertCommitted','assertNoSucceeded','assertD06Sequence','assertRecoveryOnly','assertUniqueCheckpoint']
for name in oracle:assert all(current[name].count(method)==1 for method in original[name]),name
# exact unchanged original MySQL owner and DatabaseSpec process/server guard classes
def clazz(data,name):
 tree=parser.parse(data)
 for n in walk(tree.root_node):
  if n.type in ('class_declaration','record_declaration') and n.child_by_field_name('name').text.decode()==name:return data[n.start_byte:n.end_byte]
 raise AssertionError(name)
for path,name in [(paths[0],'MySql'),(paths[1],'DatabaseSpec')]:assert clazz(blob(path),name)==clazz((wt/path).read_bytes(),name),name
before=methods(blob(paths[1]));after=methods((wt/paths[1]).read_bytes())
# Entire real Spring production bean assembly unchanged, only ADDITION opaque boundary observer.
assembly=[]
for name in before:
 if before[name][0].startswith(b'@Bean'):
  assert after[name]==before[name],name;assembly.append(name)
assert len(assembly)>40
node=(wt/paths[2]).read_text();oldnode=blob(paths[2]).decode()
assert node[node.index('export async function verifyInputs'):node.index('const emit')] == oldnode[oldnode.index('export async function verifyInputs'):oldnode.index('const emit')]
assert node[node.index('async function prepare(input)'):node.index('async function prepareM4(input)')] == oldnode[oldnode.index('async function prepare(input)'):oldnode.index('async function main()')]
assert node.count('export const SOURCE =')==1
assert all(n not in node for n in ['7594', '3594240', 'f4dcd'])
init=(wt/paths[3]).read_text()
for name in foundation+six:assert init.count("'"+name+"'")==1
assert "p.tasks.register(name, Test)" in init and 'maxParallelForks = 1' in init and 'outputs.cacheIf { false }' in init
assert 'ur06M4MysqlE05:' in init and 'ur06EnrollMysql:' in init and 'failOnNoMatchingTests = true' in init
assert all(n in init for n in ['UR06_LOCAL_ACCEPTANCE','UR06_MYSQLD_BIN','UR06_CODEX_BIN'])
fixture=(wt/paths[1]).read_text()
assert 'new ResourceDatabasePopulator(new FileSystemResource(resource)).populate(c)' in fixture
assert 'agent-work-item-reassignment-e05.sql' in fixture and 'single-tenant-task-owner-ddl.sql' in fixture
assert 'CREATE TRIGGER ur06_m4_submit_rollback BEFORE INSERT' in fixture
assert 'SIGNAL SQLSTATE' in fixture and 'WORK_ITEM_SUBMITTED' in fixture
assert not re.search(r'org\.h2|SHUTDOWN|e05-http-db-h2\.sql|INSERT INTO.*information_schema|mock\(',fixture)
assert 'call.proceed()' in fixture and 'isActualTransactionActive()' in fixture
assert 'observeBatch(batches, partial.getLargeUpdateCounts())' in fixture
assert 'batches.add(observation); return added;' in fixture
for f in paths[:2]:assert not parser.parse((wt/f).read_bytes()).root_node.has_error
subprocess.run(['/usr/bin/node','--check',str(wt/paths[2])],check=True)
subprocess.run(['git','-C',str(wt),'diff','--check',base],check=True)
changed=git('diff','--name-only',base).splitlines();assert set(changed)==set(paths),(changed,paths)
pin={'payloadCommit':'5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b','tree':'d3cdc69da62bddc48af0bc86b4f32dbfa9429b60','files':285,'archiveBytes':3635200,'archiveSha256':'9b5d74b27a91579359ad0a18d241f66f19d6df13d376e3cff5dbd45b729b7687'}
proof=Path('/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/ur01-py311-cfg-source-readback/payload-C-main-readback.json'); payload=json.loads(proof.read_text())
assert all(payload[k]==v for k,v in pin.items())
assert payload['realInstall']=='NOT_RUN'
replacement={b'd91ebbf436911eac20ffb70cb92192a65c742e11':pin['payloadCommit'].encode(), b'b2e3f17ff57e21e2482c0fc54e71dbf4b92dbd82':pin['tree'].encode(),b'3c826b9e78db3bc4ca5a9eef1e9026ebeb0e34626e214a6b1b2d8bd532169b36':pin['archiveSha256'].encode(),b'3624960':b'3635200'}
logic='84b14cc7dd90dc55e26213db44911fe76d3cec81'
for path in [paths[0],paths[2],paths[4],paths[5]]:
    previous=subprocess.check_output(['git','-C',str(wt),'show',logic+':'+path]);currentBytes=(wt/path).read_bytes()
    for old,new in replacement.items(): previous=previous.replace(old,new)
    assert previous==currentBytes,('ONLY_SOURCE_LITERALS_ALLOWED_AFTER_LOGIC',path)
    assert all(old not in currentBytes for old in replacement)
for path in paths[4:]:
    previous=blob(path);expected=previous
    for old,new in replacement.items():expected=expected.replace(old,new)
    assert expected==(wt/path).read_bytes(),('UR04_NORMALIZED_WHOLE_FILE_BYTEEQ',path)
subprocess.run(['/usr/bin/node','--check',str(wt/paths[5])],check=True)
assert not parser.parse((wt/paths[4]).read_bytes()).root_node.has_error
assert git('status','--porcelain=v1','--untracked-files=all')==''
remote=git('ls-remote','origin','refs/heads/codex/ur06-m4-mysql-e05-20261008').split()[0]
assert remote==git('rev-parse','HEAD')
result={'scope':'UR06_M4_PLUS_AUTHORIZED_UR04_C_PROOF_SOURCE_ONLY','baseCommit':base,'headCommit':git('rev-parse','HEAD'),'headTree':git('rev-parse','HEAD^{tree}'),'remoteCommit':remote,'worktreeClean':True,'commits':git('rev-list','--reverse',base+'..HEAD').splitlines(),'status':'STATIC_ONLY_NOT_COMPILE_OR_ACCEPTANCE','checks':{'exactOwnedPaths':len(paths),'foundationMethodByteEqual':foundation,'originalE05MethodByteEqual':six,'originalOracleHelpersByteEqual':oracle,'originalMySqlOwnerClassByteEqual':True,'originalDatabaseSpecClassByteEqual':True,'unchangedRealBeanMethods':assembly,'foundationNodeFunctionsByteEqual':True,'fullSourceVerifierByteEqual':True,'nodeSyntax':'TWO_PASS_STATIC_ONLY','JavaGrammar':'THREE_PASS_STATIC_ONLY','UR04WholeFileNormalizedByteEqual':True,'PostM4LogicWholeFilesOnlySourceLiterals':True,'gitDiffCheck':'PASS','exactTaskFilters':'7+6'},'files':{x:hashlib.sha256((wt/x).read_bytes()).hexdigest() for x in paths},'selectors':{name:'NOT_RUN' for name in foundation+six},'compileUr06EnrollMysqlJava':'NOT_RUN','rootValidateLayering':'NOT_RUN','acceptedTarget':'NONE','sourcePin':pin,'payloadCReadback':{'path':str(proof),'sha256':hashlib.sha256(proof.read_bytes()).hexdigest()},'sourceRole':'C_ONLY_NOT_INSTALLED_NOT_ACCEPTED','harnessD':'MAIN_OWNER_HANDOFF_PENDING','production':'NOT_RUN','provider':'NOT_RUN'}
Path('/var/tmp/ur06-m4-c-source-static-20261008.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'static':'PASS_ONLY','original7ByteEqual':len(foundation),'original6ByteEqual':len(six),'oracleHelpers':len(oracle),'realBeanMethods':len(assembly),'tests':'NOT_RUN','scope':len(paths),'source':'C_ONLY_NOT_INSTALLED'}))
