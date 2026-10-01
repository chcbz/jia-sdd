import cn.jia.chat.archive.config.ArchiveSchemaCatalog;
import java.nio.file.*;
public class NormalizeChecks {
 public static void main(String[] args) throws Exception {
  var a=ArchiveSchemaCatalog.normalizeCheck(Files.readString(Path.of(args[0])));
  var b=ArchiveSchemaCatalog.normalizeCheck(Files.readString(Path.of(args[1])));
  System.out.println("expected="+a);
  System.out.println("actual="+b);
  System.out.println("equal="+a.equals(b));
 }
}
