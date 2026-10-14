import {catalogRequest} from './bountyRequestCatalog.js'
const scope={conversationId:'42',conversationGeneration:'7',taskId:'task-1'}
const step={stepId:'step-1',stepNumber:'1',taskId:'task-1',assignmentRevision:'1',targetAgentId:'agent-1',kind:'EXECUTE',state:'ADMITTED',stateVersion:'0',executionIntentId:'intent-1',executionId:null,executionState:'WAITING_ADMISSION'}
const req={requestId:'request-1',requestRevision:'1',conversationId:'42',conversationGeneration:'7',userMessageId:'101',state:'PLANNING',stateVersion:'0',turns:[],steps:[step]}
const turn={turnId:'turn-1',requestId:'request-other',requestRevision:'1',conversationId:'43',conversationGeneration:'9',targetAgentId:'agent-other',contextSnapshotId:'snap-1',dispatchId:'disp-1',route:'CHAT',state:'PUBLISHED',stateVersion:'1',lastDeltaSeq:'0',terminalReason:null,finalMessageId:'102',createdAt:'1',updatedAt:'1'}
const cases=[['valid_unbound_EXECUTE_step',req,true],['valid_nonexecution_CHAT_step',{...req,steps:[{...step,kind:'CHAT',state:'WAITING_USER',executionIntentId:null,executionId:null,executionState:null}]},true],['foreign_turn_scope',{...req,steps:[],turns:[turn]},false],['incomplete_turn_view',{...req,steps:[],turns:[{turnId:'turn-1',stateVersion:'1'}]},false]]
const results=cases.map(([id,input,expected])=>({id,expected,actual:Boolean(catalogRequest(input,scope))}))
console.log(JSON.stringify({sourceCommit:'1993b888391c2c7ce707dc60da743810f25f17df',scope,results,mismatches:results.filter(v=>v.actual!==v.expected).length},null,2))
process.exitCode=results.some(v=>v.actual!==v.expected)?1:0
