import { resolveCodexAppServerSchemaContract, CODEX_APP_SERVER_SCHEMA_CONTRACTS } from './app-server-adapter.mjs'
import { typedDeliberationAdapterReady, buildTypedDeliberationDeclaration } from './juyiting-typed-outcome.mjs'
const cases=[]
for (const key of ['codex-cli-unknown', '__proto__', 'constructor', 'toString', 'hasOwnProperty', 'valueOf', ' __proto__ ']) {
 const profile={appServerSchemaContractId:key,typedDeliberationEnabled:true,fastChatEnabled:true,appServerEnabled:true,chatEngine:'app-server',chatSandbox:'read-only',chatToolPolicy:'read-only-constrained'}
 let contract=null,error=null
 try { contract=resolveCodexAppServerSchemaContract(profile) } catch (e) { error={code:e.code,message:e.message} }
 const adapter={closed:false,readback:{initialize:{},schema:{measured:true}}}
 const ready=typedDeliberationAdapterReady(profile,adapter)
 const declaration=buildTypedDeliberationDeclaration(profile,adapter)
 cases.push({key,registeredOwnKey:Object.hasOwn(CODEX_APP_SERVER_SCHEMA_CONTRACTS,key.trim()),rejected:!!error,error,resolvedType:typeof contract,resolvedFields:contract?{contractId:contract.contractId??null,cliVersion:contract.cliVersion??null,bundleSha256:contract.bundleSha256??null}:null,ready,declarationState:declaration.state,pass:!!error&&!ready&&declaration.state==='UNAVAILABLE'})
}
const controls=['codex-cli-0.153.4','codex-cli-0.159.2'].map(key=>({key,contract:resolveCodexAppServerSchemaContract({appServerSchemaContractId:key})}))
console.log(JSON.stringify({scope:'No engine startup; readiness with synthetic incomplete measured readback only; does not demonstrate remote exploit',cases,controls,pass:cases.every(c=>c.pass)},null,2))
process.exitCode=cases.every(c=>c.pass)?0:1
