import { mkdtempSync, writeFileSync, readFileSync, existsSync, lstatSync, rmSync, symlinkSync } from 'node:fs'
import { resolve } from 'node:path'
import { tmpdir } from 'node:os'
import { OutputDeliveryQueue, OutputRunLock } from '/home/chc/wsps/cyf-worktrees/output-client/conf/codex-ws-agent/output-queue.mjs'
const profile={agentId:'review-agent',profileId:'review-profile'},runId='1'.repeat(32),outputId='2'.repeat(32)
const terminalIntent={mode:'command',commandId:'cmd-review',commandFingerprint:'a'.repeat(64),payload:{status:'completed'},outcome:{status:'completed',exitCode:0,errorMessage:''}}
function fixture(options={}){
 const root=mkdtempSync(resolve(tmpdir(),'od06-review-'))
 const queue=new OutputDeliveryQueue({rootDir:root,profile,apiBaseUrl:'https://example.test',ticketProvider:async()=>({token:'unused'}),now:()=>100,snapshotRetentionMs:0,...options}).initialize()
 const dir=queue.snapshotDirectory(runId),file=resolve(dir,`${outputId}.txt`)
 writeFileSync(file,'private bytes',{mode:0o600})
 const record=queue.enqueue({outputContext:{runId,source:{type:'TASK',id:'task-review'}},snapshot:{outputs:[{outputId,title:'output',name:'result.txt',mime:'text/plain',size:13,sha256:'a'.repeat(64),snapshotPath:file}]},mode:'command',terminalIntent})
 return {root,queue,record,dir,file,path:resolve(queue.queueDir,`${runId}.json`)}
}
function complete(f){ f.record.state='PUBLISHED';f.record.outputs.forEach(x=>x.state='PUBLISHED');f.record.terminalNotified=true;f.record.publicationConfirmedAt=1;f.record.terminalNotifiedAt=1;f.queue.write(f.record) }
{
 const scheduled=[];const f=fixture({schedule:(callback,delay)=>{scheduled.push({callback,delay});return scheduled.length},clearSchedule:()=>{}})
 const lock=new OutputRunLock({rootDir:f.queue.rootDir,namespace:'delivery',runId}).acquire()
 try{for(let i=0;i<3;i++){await f.queue.resume()};console.log('BUSY_ACTIVE_DELIVERY_SCHEDULER',JSON.stringify({delays:scheduled.map(x=>x.delay),nextAttemptAt:JSON.parse(readFileSync(f.path)).nextAttemptAt}))}finally{f.queue.stop();lock.release();rmSync(f.root,{recursive:true,force:true})}
}
{
 const f=fixture();complete(f);delete f.record.commandEvidence;f.queue.write(f.record)
 const result=f.queue.cleanupRetention();let evidenceError
 try{f.queue.resolveCommandEvidence({runId,source:f.record.source,agentId:profile.agentId,commandId:terminalIntent.commandId,fingerprint:terminalIntent.commandFingerprint,terminal:true})}catch(e){evidenceError=e.code}
 console.log('CORRUPT_COMMAND_EVIDENCE_RETENTION',JSON.stringify({result,snapshotStillExists:existsSync(f.file),evidenceError}))
 rmSync(f.root,{recursive:true,force:true})
}
{
 const f=fixture();complete(f);rmSync(f.dir,{recursive:true});symlinkSync(resolve(f.root,'nonexistent-external-dir'),f.dir)
 const result=f.queue.cleanupRetention()
 console.log('DANGLING_RUN_DIRECTORY_SYMLINK',JSON.stringify({result,linkStillExists:lstatSync(f.dir).isSymbolicLink(),archived:existsSync(resolve(f.queue.archiveDir,`${runId}.json`))}))
 rmSync(f.root,{recursive:true,force:true})
}
