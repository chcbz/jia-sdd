import java.nio.file.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import javax.tools.*;
import com.sun.source.util.JavacTask;
class JavaSyntaxCheck {
 public static void main(String[] args) throws Exception {
  var compiler=ToolProvider.getSystemJavaCompiler();
  var diagnostics=new DiagnosticCollector<JavaFileObject>();
  var paths=Files.readAllLines(Path.of(args[0]), StandardCharsets.UTF_8);
  try(var manager=compiler.getStandardFileManager(diagnostics, Locale.ROOT, StandardCharsets.UTF_8)) {
   var task=(JavacTask)compiler.getTask(null,manager,diagnostics,List.of("-proc:none","--release","21"),null,manager.getJavaFileObjectsFromStrings(paths));
   int parsed=0; for(var tree:task.parse()) parsed++;
   long errors=diagnostics.getDiagnostics().stream().filter(x->x.getKind()==Diagnostic.Kind.ERROR).count();
   diagnostics.getDiagnostics().forEach(System.out::println);
   System.out.println("JAVA_PARSE_ONLY files="+parsed+" errors="+errors+" TYPECHECK_NOT_RUN");
   System.exit(errors==0?0:1);
  }
 }
}
