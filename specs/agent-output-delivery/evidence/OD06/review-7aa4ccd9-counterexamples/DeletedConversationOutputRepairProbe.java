import cn.jia.chat.dao.ChatConversationDao;
import cn.jia.chat.entity.ChatConversationEntity;
import cn.jia.chat.mapper.ChatConversationMapper;
import cn.jia.chat.output.ConversationOutputSourceAuthorizer;
import cn.jia.chat.output.ConversationOutputVersionProvider;
import cn.jia.agent.output.OutputSourceAccessMode;
import cn.jia.agent.output.OutputAuthorizationException;
import cn.jia.agent.output.OutputDeliveryException;
import org.apache.ibatis.annotations.Select;
import java.lang.reflect.Proxy;
import java.util.ArrayList;
import java.util.List;

public class DeletedConversationOutputRepairProbe {
  interface Action { void run() throws Exception; }
  static List<String> failures = new ArrayList<>();
  static int checked;
  static ChatConversationEntity row(boolean deleted) {
    var row = new ChatConversationEntity();
    row.setId(101L); row.setTenantId("owner"); row.setClientId("client");
    row.setJiacn("owner"); row.setTargetAgentId("agent-1");
    row.setDeletedAt(deleted ? 10L : null); row.setLifecycleGeneration(deleted ? 2L : 1L);
    return row;
  }
  static ChatConversationDao dao(boolean snapshotDeleted, boolean lockedDeleted) {
    return (ChatConversationDao) Proxy.newProxyInstance(ChatConversationDao.class.getClassLoader(),
      new Class<?>[]{ChatConversationDao.class}, (proxy, method, params) -> {
        if (method.getName().equals("findExactOwnedById")) return row((Boolean)params[4] ? lockedDeleted : snapshotDeleted);
        throw new UnsupportedOperationException(method.getName());
      });
  }
  static void check(String name, boolean denied, Action action) {
    checked++;
    try {
      action.run();
      System.out.println(name + "=ALLOWED");
      if (denied) failures.add(name + " unexpectedly allowed");
    } catch (OutputAuthorizationException | OutputDeliveryException expected) {
      System.out.println(name + "=DENIED:" + expected.getClass().getSimpleName());
      if (!denied) failures.add(name + " unexpectedly denied");
    } catch (Exception other) { failures.add(name + " unexpected failure:" + other); }
  }
  public static void main(String[] args) throws Exception {
    for (var mode : new OutputSourceAccessMode[]{OutputSourceAccessMode.MUTATION, OutputSourceAccessMode.RECEIPT_READ}) {
      check(mode + "_DELETED_SNAPSHOT", true, () -> new ConversationOutputSourceAuthorizer(dao(true,true),null).lockAndAuthorize("owner","client","101","agent-1",mode));
      check(mode + "_DELETED_AFTER_LOCK", true, () -> new ConversationOutputSourceAuthorizer(dao(false,true),null).lockAndAuthorize("owner","client","101","agent-1",mode));
      check(mode + "_LIVE", false, () -> new ConversationOutputSourceAuthorizer(dao(false,false),null).lockAndAuthorize("owner","client","101","agent-1",mode));
    }
    for (boolean locked : new boolean[]{false,true}) {
      check("OWNER_DELETED_lock="+locked,true,()->new ConversationOutputVersionProvider(dao(true,true),null).requireOwner("owner","client","owner","101",locked));
      check("OWNER_LIVE_lock="+locked,false,()->new ConversationOutputVersionProvider(dao(false,false),null).requireOwner("owner","client","owner","101",locked));
    }
    String sql=String.join(" ",ChatConversationMapper.class.getMethod("findExactOwnedById",String.class,String.class,String.class,Long.class,boolean.class).getAnnotation(Select.class).value()).replaceAll("\\s+"," ");
    boolean filter=sql.contains("AND deleted_at IS NULL"), forUpdate=sql.contains("<if test=\"forUpdate\">FOR UPDATE</if>");
    checked+=2;
    System.out.println("SQL_DELETED_FILTER="+filter);System.out.println("SQL_LOCK_BRANCH="+forUpdate);
    if(!filter||!forUpdate)failures.add("actual SQL lifecycle/lock branch missing");
    System.out.println("CHECKED="+checked+" FAILURES="+failures.size());
    if(!failures.isEmpty())throw new AssertionError(String.join("; ",failures));
  }
}
