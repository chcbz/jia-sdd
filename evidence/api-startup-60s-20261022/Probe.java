package cn.jia.chat.archive.content;
import com.fasterxml.jackson.databind.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
public class Probe {
 public static void main(String[] args) throws Exception {
  ObjectMapper mapper=new ObjectMapper(); ArchiveManifestLoader candidate=new ArchiveManifestLoader();
  StringBuilder all=new StringBuilder(); for(char c=0;c<128;c++) all.append(c);
  for(String s:new String[]{"",all.toString(),"水滸傳\u2028\u2029😀"})
   if(!Arrays.equals((mapper.writeValueAsString(s)+"\n").getBytes(StandardCharsets.UTF_8),candidate.canonicalJsonBytes(mapper.valueToTree(s)))) throw new AssertionError("escaping");
  byte[] manifest=ArchiveManifestLoader.readRequiredResource(ArchiveManifestLoader.MANIFEST_RESOURCE);
  byte[] golden=ArchiveManifestLoader.readRequiredResource(ArchiveManifestLoader.GOLDEN_SUMMARY_RESOURCE);
  JsonNode tree=mapper.readTree(manifest); int[] strings={0}; count(tree,strings);
  System.out.println("canonical_string_visits="+strings[0]);
  for(int i=0;i<4;i++) {
   if(i%2==0){ baseline(manifest,golden); candidate(manifest,golden); }
   else { candidate(manifest,golden); baseline(manifest,golden); }
  }
  manifest[manifest.length-2]^=1;
  try { candidate.parseAndValidate(manifest,golden);throw new AssertionError("corruption accepted"); }
  catch(ArchiveContentException expected){}
  System.out.println("escape_parity_full_fixture_digests_corruption=PASS");
 }
 static void count(JsonNode n,int[] count){ if(n.isObject()){n.fields().forEachRemaining(e->{count[0]++;count(e.getValue(),count);});} else if(n.isArray()) n.forEach(v->count(v,count)); else if(n.isTextual()) count[0]++; }
 static void baseline(byte[] m,byte[] g){long t=System.nanoTime();var b=new BaselineArchiveManifestLoader().parseAndValidate(m,g);System.out.println("baseline_load_ms="+(System.nanoTime()-t)/1e6);if(b.manifest().readerParagraphCount()!=3677)throw new AssertionError();}
 static void candidate(byte[] m,byte[] g){long t=System.nanoTime();var b=new ArchiveManifestLoader().parseAndValidate(m,g);System.out.println("candidate_load_ms="+(System.nanoTime()-t)/1e6);if(b.manifest().readerParagraphCount()!=3677)throw new AssertionError();}
}
