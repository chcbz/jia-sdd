import cn.jia.agent.platform.*;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.datasource.DriverManagerDataSource;
import java.nio.file.*;
import java.util.*;
public class FrozenMysqlExplain {
 public static void main(String[] args)throws Exception{
  String password=Files.readAllLines(Path.of(args[0])).stream().filter(x->x.startsWith("password=")).findFirst().orElseThrow().substring(9);
  var jdbc=new JdbcTemplate(new DriverManagerDataSource("jdbc:mysql://127.0.0.1:34061/aam_frozen?useSSL=false&allowPublicKeyRetrieval=true","aam_test",password));
  byte[] reg=new byte[32];Arrays.fill(reg,(byte)1);
  var key=new PlatformInstallationStore.ResolutionKey(new PlatformInstallationStore.Scope("0","client-fixture","owner-fixture"),"PLATFORM_PROVISIONED","agent-fixture","archive-maintainer","1.0.0","a".repeat(64),1L,"runtime-fixture",reg);
  for(String name:List.of("verifiedCandidateQuery","pendingCandidateQuery","historicalCandidateQuery")){
   var method=name.equals("pendingCandidateQuery")?JdbcPlatformInstallationStore.class.getDeclaredMethod(name,PlatformInstallationStore.ResolutionKey.class,long.class):JdbcPlatformInstallationStore.class.getDeclaredMethod(name,PlatformInstallationStore.ResolutionKey.class);
   method.setAccessible(true);var query=name.equals("pendingCandidateQuery")?method.invoke(null,key,1L):method.invoke(null,key);
   var sqlMethod=query.getClass().getDeclaredMethod("sql");sqlMethod.setAccessible(true);
   var argsMethod=query.getClass().getDeclaredMethod("arguments");argsMethod.setAccessible(true);
   System.out.println("EXPLAIN "+name);
   System.out.println(jdbc.queryForObject("EXPLAIN FORMAT=JSON "+sqlMethod.invoke(query),String.class,(Object[])argsMethod.invoke(query)));
  }
 }
}