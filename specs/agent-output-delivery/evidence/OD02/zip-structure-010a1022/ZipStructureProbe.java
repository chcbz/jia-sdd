package cn.jia.agent.output.service;
import java.nio.file.*; import java.util.zip.*; import java.io.*;
public class ZipStructureProbe {
 public static void main(String[] args) throws Exception {
  for (String arg: args) {
   Path p=Path.of(arg); byte[] b=Files.readAllBytes(p); int local=0,central;
   try (ZipFile z=new ZipFile(p.toFile())) { central=z.size(); }
   try (ZipInputStream z=new ZipInputStream(new ByteArrayInputStream(b))) { while(z.getNextEntry()!=null){local++; z.readAllBytes();} }
   String verdict;
   try { verdict="ACCEPTED "+OutputContentInspector.requireAllowed("probe.zip","application/zip",b,true,64L,4096L); }
   catch(cn.jia.agent.output.OutputUploadException ex) { verdict="REJECTED "+ex.code(); }
   System.out.println(p.getFileName()+" central="+central+" local="+local+" "+verdict);
  }
 }
}
