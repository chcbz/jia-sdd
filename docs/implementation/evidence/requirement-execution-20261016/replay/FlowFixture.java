// Installed production DTO/Jackson serializer + synthetic values; NOT database/API acceptance.
import cn.jia.agent.service.HallRequestDraftService.*;
import cn.jia.agent.service.PersonalWorkspaceExecutionService.*;
import cn.jia.agent.api.HallDraftWire;
import java.util.*;
import tools.jackson.databind.json.JsonMapper;
class FlowFixture {
  public static void main(String[] args) throws Exception {
    var fields=new EditableFields("流程复测-合成资料", "将合成文本整理为PDF，不使用真实个人资料", "agent", "application/pdf", List.of(new cn.jia.agent.service.HallRequestDraftService.InputSelection("fixture_file",1)));
    var summary=new SourceSummary(null,null,null,null,null,null);
    var queued=new ExecutionView("fixture_execution","fixture_task","fixture_run",null,"agent","QUEUED",null,null,1,"application/pdf",List.of(),null,"PRIVATE",null,null,null);
    var completed=new ExecutionView("fixture_execution","fixture_task","fixture_run",null,"agent","OUTPUT_COMMITTED",null,null,1,"application/pdf",List.of(),null,"PRIVATE",null,null,null);
    var fixtures=new LinkedHashMap<String,Object>();
    fixtures.put("capabilities",new ExecutionCapabilities(List.of("text/plain","application/pdf"),List.of("text/plain","application/pdf"),true));
    fixtures.put("draft",HallDraftWire.from(new DraftView("fixture_draft",1,"EDITING",1,"CREATE",fields,summary,null)));
    fixtures.put("saved",HallDraftWire.from(new DraftView("fixture_draft",2,"EDITING",2,"CREATE",fields,summary,null)));
    fixtures.put("receipt",HallDraftWire.from(new SubmissionReceipt(new SubmissionReference("PRIVATE_CASE","fixture_case"),queued,null,3)));
    fixtures.put("queued",HallDraftWire.from(new CaseView("fixture_case",fields.title(),1,List.of(new CaseExecutionView(1,null,null,queued)),List.of("VIEW"),new CaseSourceRef(null))));
    fixtures.put("completed",HallDraftWire.from(new CaseView("fixture_case",fields.title(),1,List.of(new CaseExecutionView(1,null,null,completed)),List.of("VIEW"),new CaseSourceRef(null))));
    fixtures.put("results",HallDraftWire.from(new ExecutionResultsView("fixture_execution","OUTPUT_COMMITTED","fixture_manifest",List.of(new ResultItemView("output_1","fixture_output",1,"application/pdf","合成成果.pdf",12,"a".repeat(64),"AVAILABLE")),List.of("VIEW","CREATE_REVISION"))));
    System.out.println(JsonMapper.builder().build().writeValueAsString(fixtures));
  }
}
