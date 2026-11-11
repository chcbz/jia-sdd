import cn.jia.agent.service.PersonalWorkspaceExecutionService.*;
import cn.jia.agent.api.WorkspaceExecutionWire;
import java.util.List;
import tools.jackson.databind.json.JsonMapper;
class Probe {public static void main(String[] a) throws Exception {
var command=new RuntimeCommand("task","run",List.of(),List.of(new RuntimeOutput("output_1","outputs/result.txt","text/plain",1000,"/internal/agent/tasks/task/runs/run/outputs/output_1/content")));
var original=new RuntimeQueuedCommand(1,"command.dispatch","message","command","tenant","client","owner","task","run","agent","WORKSPACE_FILE_EXECUTE","edit",command);
System.out.println(JsonMapper.builder().build().writeValueAsString(WorkspaceExecutionWire.from(original)));
}}
