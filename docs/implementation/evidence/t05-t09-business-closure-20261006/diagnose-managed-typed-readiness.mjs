import assert from 'node:assert/strict';
import {ManagedHost} from '/home/isp/apps/codex-ws-agent/current/managed-host.mjs';
import {resolveManagedRuntimeProfile} from '/home/isp/apps/codex-ws-agent/current/agent-client.mjs';
import {buildTypedDeliberationDeclaration} from '/home/isp/apps/codex-ws-agent/current/juyiting-typed-outcome.mjs';
// Pure in-memory diagnostic. No ManagedHost constructor, account initialization,
// socket, runtime registration, model turn, file write, or credentials.
const host={multiOwner:true,codexBin:'/usr/local/bin/codex',workspacePolicyId:'test-workspace-policy',identityKey:()=> 'fixture-identity'};
const request={ownerJiacn:'fixture-owner',agentId:'agt_00000000000000000000000000000001',intentId:'hri_00000000-0000-0000-0000-000000000001',apiKey:'noncredential-fixture',tenantId:'0',clientId:'fixture-client'};
const profile=ManagedHost.prototype.profileFor.call(host,request,{home:'/var/tmp/not-created-home',workdir:'/var/tmp/not-created-workdir'});
const intended={fastChatEnabled:true,appServerEnabled:true,typedDeliberationEnabled:true,chatEngine:'app-server',chatSandbox:'read-only',chatToolPolicy:'read-only-constrained',chatWorkdir:'/var/tmp/not-created-chat'};
const actual=resolveManagedRuntimeProfile(profile,intended);
const keys=['fastChatEnabled','appServerEnabled','typedDeliberationEnabled','chatEngine','chatSandbox','chatToolPolicy','chatWorkdir'];
assert.equal(buildTypedDeliberationDeclaration(actual,null),null);
assert.equal(actual.typedDeliberationEnabled,undefined);
const report={at:new Date().toISOString(),scope:'pure source diagnostic, not business acceptance',sourceCommit:'4e70c4fc90aaf72ee6a1e58aae7703853af449f1',profileConstructor:'ManagedHost.profileFor',composition:'resolveManagedRuntimeProfile',intended,actual:Object.fromEntries(keys.map(k=>[k,actual[k]??null])),declaration:buildTypedDeliberationDeclaration(actual,null),finding:'Managed runtime composition does not carry the CHAT/typed flags even when supplied in the configured source profile.',providerCalls:0,liveWrites:0};
console.log(JSON.stringify(report,null,2));
