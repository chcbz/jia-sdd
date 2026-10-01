import cn.jia.chat.archive.maintenance.config.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import java.nio.file.*;
import java.util.*;
public class FrozenMysqlMetadata {
 public static void main(String[] args)throws Exception{
  String password=Files.readAllLines(Path.of(args[0])).stream().filter(x->x.startsWith("password=")).findFirst().orElseThrow().substring(9);
  var jdbc=new JdbcTemplate(new DriverManagerDataSource("jdbc:mysql://127.0.0.1:34061/aam_frozen?useSSL=false&allowPublicKeyRetrieval=true","aam_test",password));
  for(var entry:ArchiveMaintenanceSchemaCatalog.expected().tables().entrySet()){
   var actual=new TreeMap<String,String>();
   for(var row:jdbc.queryForList("SELECT INDEX_NAME,NON_UNIQUE,GROUP_CONCAT(COLUMN_NAME ORDER BY SEQ_IN_INDEX) AS cols FROM information_schema.STATISTICS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=? GROUP BY INDEX_NAME,NON_UNIQUE",entry.getKey()))actual.put(row.get("INDEX_NAME").toString(),row.get("NON_UNIQUE")+":"+row.get("cols"));
   if(!actual.equals(entry.getValue().indexes())){var unexpected=new TreeMap<>(actual);unexpected.keySet().removeAll(entry.getValue().indexes().keySet());System.out.println("INDEX_DIFFERENCE "+entry.getKey()+" extra="+unexpected+" expected="+entry.getValue().indexes()+" actual="+actual);}
  }
  var normalize=Class.forName("cn.jia.agent.platform.PlatformSkillSchemaContract").getDeclaredMethod("normalize",String.class);normalize.setAccessible(true);
  for(var row:jdbc.queryForList("SELECT CONSTRAINT_NAME,CHECK_CLAUSE FROM information_schema.CHECK_CONSTRAINTS WHERE CONSTRAINT_SCHEMA=DATABASE() AND CONSTRAINT_NAME LIKE 'ck_platform_install_%'")){
   String clause=row.get("CHECK_CLAUSE").toString();System.out.println("PLATFORM_CHECK "+row.get("CONSTRAINT_NAME")+" metadata="+clause+" normalized="+normalize.invoke(null,clause));
  }
 }
}