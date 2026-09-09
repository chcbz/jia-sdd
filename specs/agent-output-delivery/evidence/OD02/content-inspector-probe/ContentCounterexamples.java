package cn.jia.agent.output.service;
import cn.jia.agent.output.OutputUploadException;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.zip.*;
public class ContentCounterexamples {
 public static void main(String[] args)throws Exception{
  int sampleLimit=2*1024*1024;
  byte[] full=new byte[sampleLimit+2];Arrays.fill(full,(byte)'a');
  byte[] ending="中".getBytes(StandardCharsets.UTF_8);System.arraycopy(ending,0,full,sampleLimit-1,3);
  String fullResult=OutputContentInspector.requireAllowed("report.txt","text/plain",full,true);
  String partialResult;
  try{partialResult=OutputContentInspector.requireAllowed("report.txt","text/plain",Arrays.copyOf(full,sampleLimit),false);}
  catch(OutputUploadException e){partialResult=e.code();}
  ByteArrayOutputStream packed=new ByteArrayOutputStream();
  long expandedBytes=201L*1024*1024;
  try(ZipOutputStream zip=new ZipOutputStream(packed)){
   zip.putNextEntry(new ZipEntry("payload.bin"));byte[] chunk=new byte[8192];
   for(long written=0;written<expandedBytes;written+=chunk.length)zip.write(chunk,0,(int)Math.min(chunk.length,expandedBytes-written));
   zip.closeEntry();
  }
  byte[] archive=packed.toByteArray();long headerSize;
  try(ZipInputStream zip=new ZipInputStream(new ByteArrayInputStream(archive))){headerSize=zip.getNextEntry().getSize();}
  String zipResult;
  try{zipResult=OutputContentInspector.requireAllowed("data.zip","application/zip",archive,true);}
  catch(OutputUploadException e){zipResult=e.code();}
  System.out.println("{\"valid_full_utf8\":\""+fullResult+"\",\"partial_utf8_result\":\""+partialResult+"\",\"sample_bytes\":"+sampleLimit+",\"zip_declared_entry_size\":"+headerSize+",\"zip_compressed_bytes\":"+archive.length+",\"zip_actual_expanded_bytes\":"+expandedBytes+",\"zip_result\":\""+zipResult+"\"}");
 }
}
