import cn.jia.agent.output.service.ClamAvOutputMalwareScanner;
import java.io.*;
import java.net.ServerSocket;
import java.nio.file.*;
import java.nio.charset.StandardCharsets;
public class ScannerAdapterProbe {
 public static void main(String[] args)throws Exception {
  byte[] fixture=Files.readAllBytes(Path.of(args[0]));
  var scanner=new ClamAvOutputMalwareScanner("127.0.0.1",13310);
  var clean=scanner.scan(new ByteArrayInputStream(fixture),fixture.length);
  if(!clean.clean()||clean.engineVersion()==null||clean.engineVersion().isBlank())throw new AssertionError("clean fixture not scanned");
  byte[] eicar="X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*".getBytes(StandardCharsets.US_ASCII);
  var infected=scanner.scan(new ByteArrayInputStream(eicar),eicar.length);
  if(infected.clean()||infected.signature()==null||infected.signature().isBlank())throw new AssertionError("EICAR not rejected");
  boolean limited=false;
  try{scanner.scan(new ByteArrayInputStream(fixture),fixture.length-1);}catch(IOException expected){limited=true;}
  if(!limited)throw new AssertionError("size limit bypassed");
  int closedPort;try(ServerSocket unused=new ServerSocket(0)){closedPort=unused.getLocalPort();}
  boolean unavailable=false;
  try{new ClamAvOutputMalwareScanner("127.0.0.1",closedPort).scan(new ByteArrayInputStream(fixture),fixture.length);}catch(IOException expected){unavailable=true;}
  if(!unavailable)throw new AssertionError("unavailable scanner did not fail");
  System.out.println("{\"clean_fixture\":true,\"eicar_rejected\":true,\"byte_limit_enforced\":true,\"unavailable_throws_ioexception\":true}");
 }
}
