import cn.jia.agent.platform.*;
import cn.jia.chat.archive.config.ArchiveSchemaInitializer;
import cn.jia.chat.archive.maintenance.config.*;
import cn.jia.chat.archive.maintenance.store.JdbcArchiveMaintenanceStore;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.jdbc.datasource.init.ResourceDatabasePopulator;
import org.springframework.core.io.ClassPathResource;
import java.nio.file.*;
import java.util.*;
public class CurrentMysqlProbe {
  static int passed=0, failed=0;
  interface Checked {void run() throws Exception;}
  static void test(String name, Checked c){try{c.run();passed++;System.out.println("PASS "+name);}catch(Throwable e){failed++;System.out.println("FAIL "+name+" "+e.getClass().getSimpleName()+": "+e.getMessage());}}
  static void require(boolean x,String name){if(!x)throw new AssertionError(name);}
  public static void main(String[] args)throws Exception{
    String password=Files.readAllLines(Path.of(args[0])).stream().filter(x->x.startsWith("password=")).findFirst().orElseThrow().substring(9);
    var ds=new DriverManagerDataSource("jdbc:mysql://127.0.0.1:34061/aam_stage4?useSSL=false&allowPublicKeyRetrieval=true&connectionTimeZone=UTC","aam_test",password);
    var jdbc=new JdbcTemplate(ds);
    System.out.println("RUNTIME MySQL "+jdbc.queryForObject("SELECT VERSION()",String.class));
    test("content-schema-real-metadata-and-migration-idempotence",()->{var init=new ArchiveSchemaInitializer(jdbc);init.initialize();init.initialize();});
    test("maintenance-schema-real-metadata-and-idempotence",()->{var init=new ArchiveMaintenanceSchemaInitializer(jdbc,new JdbcArchiveMaintenanceStore(jdbc),new ArchiveMaintenanceProperties());init.initialize();init.initialize();});
    test("platform-schema-real-metadata-and-idempotence",()->{var init=new PlatformSkillSchemaInitializer(jdbc);init.afterPropertiesSet();init.afterPropertiesSet();});
    test("transport-schema-frozen-ddl",()->new ResourceDatabasePopulator(new ClassPathResource("db/agent-command-transport-schema.sql")).execute(ds));
    var store=new JdbcPlatformInstallationStore(jdbc);
    var scope=new PlatformInstallationStore.Scope("0","client-fixture","owner-fixture");
    byte[] reg=new byte[32];Arrays.fill(reg,(byte)1);
    String sha="a".repeat(64);String resultSha="b".repeat(64);
    var key=new PlatformInstallationStore.ResolutionKey(scope,"PLATFORM_PROVISIONED","agent-fixture","archive-maintainer","1.0.0",sha,1L,"runtime-fixture",reg);
    var installations=new ArrayList<PlatformInstallationStore.Installation>();
    test("fixture-1001-newer-failures-plus-old-success",()->{
      for(int i=0;i<1002;i++){
        String id="mysql-fixture-"+i;
        var row=new PlatformInstallationStore.Installation(id,scope,"actor-fixture","key-"+i,sha,"agent-fixture",1L,"runtime-fixture",reg,"archive-maintainer","1.0.0",sha,"challenge-"+i,"command-"+i,"REQUESTED",null,null,1L,1000L+i);
        store.insert(row);store.finish(scope,id,1L,i==0?"SUCCEEDED":"FAILED",resultSha,i==0?null:"TEST_FAILURE");installations.add(row);
        jdbc.update("INSERT INTO agent_command_delivery(command_id,owner_jiacn,task_id,target_agent_id,command_type,command_payload,command_payload_hash,status,expires_at,tenant_id,client_id) VALUES(?,?,?,?,?,?,?, ?,?,?,?)",row.commandId(),scope.owner(),id,row.agentId(),"PLATFORM_SKILL_INSTALL","{}".getBytes(),reg,i==0?"SUCCEEDED":"FAILED",9999999999999L,scope.tenant(),scope.client());
      }
      require(jdbc.queryForObject("SELECT COUNT(*) FROM agent_platform_skill_installation WHERE actor_id='actor-fixture'",Integer.class)==1002,"fixture count");
    });
    test("jdbc-old-valid-success-not-hidden-by-1001-failures",()->{var found=store.verifiedCandidate(key);require(found!=null&&found.installation().id().equals("mysql-fixture-0"),"old success must win");});
    test("jdbc-different-binding-no-proof-or-history",()->{var k=new PlatformInstallationStore.ResolutionKey(scope,key.origin(),key.agentId(),key.skillKey(),key.skillVersion(),sha,2L,key.runtimeInstanceId(),reg);require(store.verifiedCandidate(k)==null&&store.latestHistorical(k)==null,"different binding leaked");});
    test("jdbc-different-runtime-no-proof-or-history",()->{var k=new PlatformInstallationStore.ResolutionKey(scope,key.origin(),key.agentId(),key.skillKey(),key.skillVersion(),sha,1L,"other-runtime",reg);require(store.verifiedCandidate(k)==null&&store.latestHistorical(k)==null,"different runtime leaked");});
    test("jdbc-different-registration-no-proof-or-history",()->{byte[] other=reg.clone();other[0]=2;var k=new PlatformInstallationStore.ResolutionKey(scope,key.origin(),key.agentId(),key.skillKey(),key.skillVersion(),sha,1L,key.runtimeInstanceId(),other);require(store.verifiedCandidate(k)==null&&store.latestHistorical(k)==null,"different registration leaked");});
    test("jdbc-different-owner-no-proof-or-history",()->{var k=new PlatformInstallationStore.ResolutionKey(new PlatformInstallationStore.Scope("0",scope.client(),"other-owner"),key.origin(),key.agentId(),key.skillKey(),key.skillVersion(),sha,1L,key.runtimeInstanceId(),reg);require(store.verifiedCandidate(k)==null&&store.latestHistorical(k)==null,"different owner leaked");});
    test("jdbc-different-digest-no-proof-or-history",()->{var k=new PlatformInstallationStore.ResolutionKey(scope,key.origin(),key.agentId(),key.skillKey(),key.skillVersion(),"c".repeat(64),1L,key.runtimeInstanceId(),reg);require(store.verifiedCandidate(k)==null&&store.latestHistorical(k)==null,"different digest leaked");});
    test("jdbc-history-exact-latest",()->require(store.latestHistorical(key).id().equals("mysql-fixture-1001"),"history ordering"));
    test("mysql-check-constraint-is-enforced",()->{boolean rejected=false;try{jdbc.update("UPDATE agent_platform_skill_installation SET origin='MARKET' WHERE installation_id='mysql-fixture-0'");}catch(org.springframework.dao.DataAccessException e){rejected=true;}require(rejected,"invalid origin accepted");});
    test("mysql-unique-idempotency-is-enforced",()->{boolean rejected=false;try{store.insert(installations.getFirst());}catch(org.springframework.dao.DuplicateKeyException e){rejected=true;}require(rejected,"duplicate accepted");});
    System.out.println("SUMMARY passed="+passed+" failed="+failed+" skipped=0");if(failed!=0)System.exit(1);
  }
}