from pathlib import Path
p=Path('/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-entry-finalization-integration-v1')
f=p/'agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentSelectedOutputFinalizationServiceImpl.java'
s=f.read_text();a='if (absent.getReason()!=AgentTaskCollaborationException.Reason.NOT_FOUND) throw absent;';assert s.count(a)==1;s=s.replace(a,'if (absent.getReason()!=AgentTaskCollaborationException.Reason.NOT_FOUND) throw translate(absent);');f.write_text(s)
f=p/'chat/jia-chat-service/src/main/java/cn/jia/chat/api/AgentTaskSelectedOutputFinalizationController.java'
s=f.read_text();s=s.replace('String conversation=text(root,"conversationId",100),summary=text(root,"summary",4000);','String conversation=bodyIdentifier(root,"conversationId"),summary=text(root,"summary",4000);');s=s.replace('text(item,"requestId",100),text(item,"stepId",100),\n                        text(item,"outputId",100)','bodyIdentifier(item,"requestId"),bodyIdentifier(item,"stepId"),\n                        bodyIdentifier(item,"outputId")');needle='    private static String sha(JsonNode n,String field)';assert needle in s;s=s.replace(needle,'    private static String bodyIdentifier(JsonNode n,String field){String value=text(n,field,100);identifier(value,100);return value;}\n'+needle);f.write_text(s)
f=p/'chat/jia-chat-service/src/chatDeliberationTest/java/cn/jia/chat/service/ChatSelectedOutputFinalizationServiceTest.java'
s=f.read_text();a='''        when(f.store.create(anyString(),anyString(),anyString(),anyString(),eq("task-1"),eq(Fixture.KEY),anyString(),
                anyString(),anyLong(),anyLong(),anyString(),anyList())).thenReturn(accepting);''';b='''        // Preserve the real deterministic operation identity/digest emitted by submit. A static
        // op-1 here would fail validateView before exercising the intended acceptance race.
        f.resumeAt(accepting);''';assert a in s;s=s.replace(a,b)
a='''        when(f.store.create(anyString(),anyString(),anyString(),anyString(),eq("task-1"),eq(Fixture.KEY),anyString(),
                anyString(),anyLong(),anyLong(),anyString(),anyList())).thenReturn(submitted);''';assert a in s;s=s.replace(a,'        f.resumeAt(submitted);')
a='''        void advanceByArguments(){''';b='''        void resumeAt(ChatSelectedOutputFinalizationStore.Operation checkpoint){
            when(store.create(anyString(),anyString(),anyString(),anyString(),eq("task-1"),eq(KEY),anyString(),
                    anyString(),anyLong(),anyLong(),anyString(),anyList())).thenAnswer(i->
                    new ChatSelectedOutputFinalizationStore.Operation(i.getArgument(3),"task-1",KEY,i.getArgument(6),
                            i.getArgument(7),i.getArgument(8),i.getArgument(9),i.getArgument(10),checkpoint.state(),
                            checkpoint.stage(),checkpoint.stateVersion(),checkpoint.deliveryId(),checkpoint.deliveryState(),
                            checkpoint.taskState(),checkpoint.taskVersion(),checkpoint.errorCode(),checkpoint.retryable(),
                            i.getArgument(11)));
        }
        void advanceByArguments(){''';assert a in s;s=s.replace(a,b)
a='''        assertEquals("FINALIZATION_DELIVERY_CHANGES_REQUESTED",receipt.errorCode());
        verify(f.agent,never()).accept(any(),anyString(),anyString(),anyString());
    }

    @Test
    void changesRequestedRemainsTruthful''';b='''        assertEquals("FINALIZATION_DELIVERY_CHANGES_REQUESTED",receipt.errorCode());
        assertEquals("running",receipt.taskState());assertEquals("10",receipt.taskVersion());
        verify(f.agent,never()).accept(any(),anyString(),anyString(),anyString());
        verifyNoInteractions(f.deliberations,f.steps,f.executions);
        verify(f.store).advance(anyString(),anyString(),anyString(),any(),eq("pending"),eq("ACCEPTING"),
                eq("delivery-1"),eq("changes_requested"),eq("running"),eq(10L),isNull(),eq(false));
    }

    @Test
    void changesRequestedRemainsTruthful''';assert a in s;s=s.replace(a,b)
a='''        assertEquals("FINALIZATION_INTERNAL_ERROR",receipt.errorCode());assertTrue(receipt.retryable());
        verify(f.agent,never()).accept(any(),anyString(),anyString(),anyString());''';b='''        assertEquals("FINALIZATION_INTERNAL_ERROR",receipt.errorCode());assertTrue(receipt.retryable());
        verify(f.agent,never()).accept(any(),anyString(),anyString(),anyString());
        verify(f.store,never()).advance(anyString(),anyString(),anyString(),any(),eq("pending"),anyString(),
                nullable(String.class),nullable(String.class),anyString(),anyLong(),nullable(String.class),anyBoolean());''';assert a in s;s=s.replace(a,b);f.write_text(s)
# Expand controller boundary regression across all actual identifiers, retaining originals.
f=p/'chat/jia-chat-service/src/chatDeliberationTest/java/cn/jia/chat/api/AgentTaskSelectedOutputFinalizationControllerTest.java';s=f.read_text();a='''    private static MockHttpServletRequest request(String json){''';b='''    @Test
    void everyBodyIdentifierIsValidatedBeforeServiceWhileHumanTextMayContainSlashes(){
        for(String[] pair:List.of(new String[]{"100","conv/1"},new String[]{"req-1","req/1"},
                new String[]{"step-1","step/1"},new String[]{"out-1","out/1"})){
            assertThrows(RuntimeException.class,()->controller.submit("task-1","12345678",
                    request(minimalBody("0").replace("\\\""+pair[0]+"\\\"","\\\""+pair[1]+"\\\"")),authentication));
        }
        verifyNoInteractions(service);
        assertEquals(HttpStatus.ACCEPTED,controller.submit("task-1","12345678",
                request(minimalBody("0").replace("\\\"title\\\"","\\\"title/a\\\"")),authentication).getStatusCode());
    }

'''+a;assert a in s;s=s.replace(a,b);f.write_text(s)
print('Applied scoped ACL translation, four controller identifier boundaries, identity-faithful race fixtures and stronger retained assertions.')
