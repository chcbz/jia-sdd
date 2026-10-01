import cn.jia.chat.archive.maintenance.config.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import java.nio.file.*;
import java.util.*;
public class CurrentMysqlChecks {
 public static void main(String[] args)throws Exception{
  String password=Files.readAllLines(Path.of(args[0])).stream().filter(x->x.startsWith("password=")).findFirst().orElseThrow().substring(9);
  var jdbc=new JdbcTemplate(new DriverManagerDataSource("jdbc:mysql://127.0.0.1:34061/aam_stage4?useSSL=false&allowPublicKeyRetrieval=true","aam_test",password));
  var normalize=ArchiveMaintenanceSchemaCatalog.class.getDeclaredMethod("normalizeCheck",String.class);normalize.setAccessible(true);
  for(var entry:ArchiveMaintenanceSchemaCatalog.expected().tables().entrySet()){
   var actual=new TreeMap<String,String>();
   for(var row:jdbc.queryForList("SELECT tc.CONSTRAINT_NAME,tc.ENFORCED,cc.CHECK_CLAUSE FROM information_schema.TABLE_CONSTRAINTS tc JOIN information_schema.CHECK_CONSTRAINTS cc ON cc.CONSTRAINT_SCHEMA=tc.CONSTRAINT_SCHEMA AND cc.CONSTRAINT_NAME=tc.CONSTRAINT_NAME WHERE tc.CONSTRAINT_SCHEMA=DATABASE() AND tc.TABLE_NAME=? AND tc.CONSTRAINT_TYPE='CHECK'",entry.getKey()))actual.put(row.get("CONSTRAINT_NAME").toString(),row.get("ENFORCED")+":"+normalize.invoke(null,row.get("CHECK_CLAUSE").toString()));
   if(!actual.equals(entry.getValue().checks()))System.out.println("CHECK_DIFFERENCE "+entry.getKey()+" expected="+entry.getValue().checks()+" actual="+actual);
  }
 }
}