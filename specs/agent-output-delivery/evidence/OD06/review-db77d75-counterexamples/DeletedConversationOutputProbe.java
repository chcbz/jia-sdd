import cn.jia.chat.dao.ChatConversationDao;
import cn.jia.chat.entity.ChatConversationEntity;
import cn.jia.chat.mapper.ChatConversationMapper;
import cn.jia.chat.output.ConversationOutputSourceAuthorizer;
import cn.jia.chat.output.ConversationOutputVersionProvider;
import cn.jia.agent.output.OutputSourceAccessMode;
import org.apache.ibatis.annotations.Select;
import java.lang.reflect.Proxy;

public class DeletedConversationOutputProbe {
  public static void main(String[] args) throws Exception {
    ChatConversationEntity row = new ChatConversationEntity();
    row.setId(101L); row.setTenantId("owner"); row.setClientId("client");
    row.setJiacn("owner"); row.setTargetAgentId("agent-1");
    row.setDeletedAt(System.currentTimeMillis()); row.setLifecycleGeneration(2L);
    ChatConversationDao dao = (ChatConversationDao) Proxy.newProxyInstance(
      ChatConversationDao.class.getClassLoader(), new Class<?>[]{ChatConversationDao.class},
      (proxy, method, params) -> {
        if (method.getName().equals("findExactOwnedById")) return row;
        throw new UnsupportedOperationException(method.getName());
      });
    var source = new ConversationOutputSourceAuthorizer(dao, null);
    var permission = source.lockAndAuthorize("owner", "client", "101", "agent-1", OutputSourceAccessMode.MUTATION);
    System.out.println("DELETED_CONVERSATION_MUTATION_ALLOWED=" + permission.sourceId());
    var version = new ConversationOutputVersionProvider(dao, null);
    version.requireOwner("owner", "client", "owner", "101", false);
    System.out.println("DELETED_CONVERSATION_OUTPUT_READ_OWNER_ALLOWED=true");
    String sql = String.join(" ", ChatConversationMapper.class.getMethod("findExactOwnedById", String.class, String.class, String.class, Long.class, boolean.class).getAnnotation(Select.class).value());
    System.out.println("EXACT_OWNER_SQL_FILTERS_DELETED_AT=" + sql.contains("deleted_at"));
  }
}
