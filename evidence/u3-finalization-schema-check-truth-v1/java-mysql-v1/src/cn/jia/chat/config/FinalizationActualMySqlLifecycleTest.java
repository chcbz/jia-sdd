package cn.jia.chat.config;

import cn.jia.agent.config.AgentSelectedOutputFinalizationSchemaInitializer;
import org.junit.jupiter.api.*;
import org.springframework.context.support.GenericApplicationContext;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import org.springframework.dao.DataIntegrityViolationException;
import java.lang.reflect.InvocationTargetException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.sql.SQLException;
import java.util.List;
import static org.junit.jupiter.api.Assertions.*;

/** Exact own fixture only; genuine JDBC/metadata/Spring lifecycle, no Provider or application beans. */
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class FinalizationActualMySqlLifecycleTest {
    static final String SOCKET="/var/tmp/cyf-jyt-mmd-mysql-20260929-thread01a0dde8/mysql.sock";
    static String prefix,database,oldDatabase,repairedDatabase;
    static JdbcTemplate fresh;
    static JdbcTemplate jdbc(String db){
        assertTrue(db.matches("mmd_(javamysql|final)_[a-f0-9]{8}_[0-9]{8}_[0-9]{6}"));
        return new JdbcTemplate(new DriverManagerDataSource(prefix+db+"?sslMode=DISABLED&allowPublicKeyRetrieval=true","root",""));
    }
    @BeforeAll static void seed() throws Exception {
        prefix=System.getProperty("mmd.fixture.jdbcPrefix");database=System.getProperty("mmd.fixture.database");
        oldDatabase=System.getProperty("mmd.fixture.oldDatabase");repairedDatabase=System.getProperty("mmd.fixture.repairedDatabase");
        assertTrue(prefix.matches("jdbc:mysql://127\\.0\\.0\\.1:[0-9]+/"));
        assertTrue(database.startsWith("mmd_javamysql_169aab6f_"));
        assertEquals("mmd_final_939d9121_20260930_184124",oldDatabase);
        assertEquals("mmd_final_8289c1a3_20260930_184353",repairedDatabase);
        fresh=jdbc(database);
        assertEquals(SOCKET,fresh.queryForObject("SELECT @@socket",String.class));
        assertEquals("/var/tmp/cyf-jyt-mmd-mysql-20260929-thread01a0dde8/data/",fresh.queryForObject("SELECT @@datadir",String.class));
        assertEquals("8.0.21",fresh.queryForObject("SELECT VERSION()",String.class));
        assertEquals(0,fresh.queryForObject("SELECT @@port",Integer.class));
        assertEquals(1,fresh.queryForObject("SELECT @@skip_networking",Integer.class));
        assertEquals(0,fresh.queryForObject("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()",Integer.class));
        for(String name:List.of("agent_task_meta","chat_conversation"))
            fresh.execute(Files.readString(Path.of(System.getProperty("mmd.fixture.seed."+name))));
    }
    static final class CountingCore extends ChatSchemaInitializer {
        int attempts;CountingCore(JdbcTemplate jdbc){super(jdbc);}
        @Override void initializeSchema(){attempts++;super.initializeSchema();}
    }
    static final class CountingDeliberation extends ChatDeliberationSchemaInitializer {
        int attempts;CountingDeliberation(JdbcTemplate jdbc){super(jdbc);}
        @Override void initializeSchema() throws Exception {attempts++;super.initializeSchema();}
    }
    static GenericApplicationContext context(JdbcTemplate jdbc){
        var context=new GenericApplicationContext();
        // Register consumers first: their InitializingBean callback must establish source readiness
        // without an ApplicationRunner having run. No mocks, external application scans or Providers.
        context.registerBean(ChatSelectedOutputFinalizationSchemaInitializer.class,()->new ChatSelectedOutputFinalizationSchemaInitializer(
                jdbc,context.getBean(ChatSchemaReadiness.class)));
        context.registerBean(ChatConversationArchiveSchemaInitializer.class,()->new ChatConversationArchiveSchemaInitializer(
                jdbc,context.getBean(ChatSchemaReadiness.class)));
        context.registerBean(AgentSelectedOutputFinalizationSchemaInitializer.class,()->new AgentSelectedOutputFinalizationSchemaInitializer(jdbc));
        context.registerBean(ChatSchemaReadiness.class,()->new ChatSchemaReadiness(context.getBean(ChatSchemaInitializer.class),
                context.getBean(ChatDeliberationSchemaInitializer.class)));
        context.registerBean(ChatSchemaInitializer.class,()->new CountingCore(jdbc));
        context.registerBean(ChatDeliberationSchemaInitializer.class,()->new CountingDeliberation(jdbc));
        return context;
    }
    @Test @Order(1) void actualMysqlInitializingBeanMakesCoreDeliberationFinalizationAndArchiveReadyBeforeRunners() throws Exception {
        for(int restart=0;restart<2;restart++){
            try(var context=context(fresh)){
                context.refresh();
                var core=(CountingCore)context.getBean(ChatSchemaInitializer.class);
                var deliberation=(CountingDeliberation)context.getBean(ChatDeliberationSchemaInitializer.class);
                assertEquals(1,core.attempts);assertEquals(1,deliberation.attempts);
                for(String name:List.of("chat_request","chat_interaction_step","chat_conversation_asset",
                        "chat_selected_output_finalization","chat_selected_output_finalization_item",
                        "agent_selected_output_finalization","chat_conversation_archive_operation"))
                    assertEquals(1,fresh.queryForObject("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE() AND table_name=?",Integer.class,name));
                core.run(null);deliberation.run(null);context.getBean(ChatSchemaReadiness.class).ensureInitialized();
                context.getBean(ChatSelectedOutputFinalizationSchemaInitializer.class).afterPropertiesSet();
                context.getBean(AgentSelectedOutputFinalizationSchemaInitializer.class).afterPropertiesSet();
                context.getBean(ChatConversationArchiveSchemaInitializer.class).afterPropertiesSet();
                assertEquals(1,core.attempts);assertEquals(1,deliberation.attempts);
            }
        }
    }
    static void checks(JdbcTemplate jdbc,boolean agent) throws Exception {
        var type=agent?AgentSelectedOutputFinalizationSchemaInitializer.class:ChatSelectedOutputFinalizationSchemaInitializer.class;
        var method=agent?type.getDeclaredMethod("validateChecks",JdbcTemplate.class):type.getDeclaredMethod("validateChecks",JdbcTemplate.class,String.class);
        method.setAccessible(true);
        try{if(agent)method.invoke(null,jdbc);else method.invoke(null,jdbc,"chat_selected_output_finalization");}
        catch(InvocationTargetException failure){if(failure.getCause() instanceof RuntimeException cause)throw cause;throw failure;}
    }
    @Test @Order(2) void realOldEnforcedSameNamedChecksAreRejectedReadOnlyWithoutAutomaticRepair() throws Exception {
        var old=jdbc(oldDatabase);
        var before=old.queryForList("SELECT constraint_name,check_clause FROM information_schema.check_constraints WHERE constraint_schema=DATABASE() ORDER BY constraint_name");
        assertEquals(3,old.queryForObject("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()",Integer.class));
        for(boolean agent:List.of(true,false)){
            var denied=assertThrows(IllegalStateException.class,()->checks(old,agent));
            assertTrue(denied.getMessage().contains("check definition drift"));
        }
        assertEquals(before,old.queryForList("SELECT constraint_name,check_clause FROM information_schema.check_constraints WHERE constraint_schema=DATABASE() ORDER BY constraint_name"));
        assertEquals(3,old.queryForObject("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()",Integer.class));
    }
    @Test @Order(3) void actualRepairedExistingMysqlDefinitionsPassReadOnlyValidation() throws Exception {
        var repaired=jdbc(repairedDatabase);checks(repaired,true);checks(repaired,false);
        assertEquals(3,repaired.queryForObject("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=DATABASE()",Integer.class));
    }
    static void mysqlCheckDenies(String sql){
        var error=assertThrows(DataIntegrityViolationException.class,()->fresh.execute(sql));
        assertInstanceOf(SQLException.class,error.getMostSpecificCause());
        assertEquals(3819,((SQLException)error.getMostSpecificCause()).getErrorCode());
    }
    @Test @Order(4) void actualJavaInitializedDdlRejectsAllThreeProvenImpossibleNullStates(){
        mysqlCheckDenies("INSERT INTO agent_selected_output_finalization(operation_id,tenant_id,client_id,owner_jiacn,task_id,immutable_digest,source_facts_digest,expected_task_version,expected_assignment_revision,conversation_id,conversation_generation,target_agent_id,grant_id,grant_version,run_id,summary,lease_token,lease_work_item_version,delivery_id,manifest_artifact_id,phase,version,created_at,updated_at) VALUES('op-1','0','client-1','owner-1','task-1',REPEAT('a',64),REPEAT('b',64),7,7,'100',3,'agent-1','grant-1',2,'run-1','chosen','fixture-only-lease',NULL,'delivery-1','manifest-1','LEASED',0,1,1)");
        for(String outcome:List.of("pending','SUBMITTED","completed','TASK_COMPLETED"))
            mysqlCheckDenies("INSERT INTO chat_selected_output_finalization(operation_id,tenant_id,owner_jiacn,client_id,task_id,idempotency_key,request_digest,conversation_id,expected_task_version,expected_assignment_revision,summary,state,stage,state_version,delivery_id,delivery_state,task_state,task_version,retryable,created_at,updated_at) VALUES('op-1','0','owner-1','client-1','task-1','key-0001',REPEAT('b',64),'100',7,7,'chosen','"+outcome+"',1,'delivery-1',NULL,'completed',10,0,1,1)");
        assertEquals(0,fresh.queryForObject("SELECT COUNT(*) FROM agent_selected_output_finalization",Integer.class));
        assertEquals(0,fresh.queryForObject("SELECT COUNT(*) FROM chat_selected_output_finalization",Integer.class));
    }
    @Test @Order(5) void actualInitializerLocksAreReleasedAndFixtureIdentityRemainsExact(){
        for(String lock:List.of("cyf:agent:selected-output-finalization:v1","cyf:chat:selected-output-finalization:v1","cyf:chat-deliberation:v2"))
            assertEquals(1,fresh.queryForObject("SELECT IS_FREE_LOCK(?)",Integer.class,lock));
        assertEquals(SOCKET,fresh.queryForObject("SELECT @@socket",String.class));
        assertEquals(0,fresh.queryForObject("SELECT @@port",Integer.class));
    }
}
