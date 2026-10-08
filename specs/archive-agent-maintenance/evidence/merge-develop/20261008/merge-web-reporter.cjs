const fs = require('node:fs');
module.exports = class MergeEvidenceReporter {
 constructor(runner) {
  const failures=[],tests=[];
  runner.on('test end',t=>tests.push({title:t.fullTitle(),file:t.file,state:t.state,duration:t.duration}));
  runner.on('fail',(t,e)=>failures.push({title:t.fullTitle(),file:t.file,message:e.message,stack:e.stack}));
  runner.once('end',()=>{
   const output={finished_at:new Date().toISOString(),stats:runner.stats,tests,failures,scope:'component/source merge verification, not real Runtime or business acceptance'};
   if(!process.env.CYF_MERGE_WEB_RESULT)throw new Error('evidence output path required');
   fs.writeFileSync(process.env.CYF_MERGE_WEB_RESULT,JSON.stringify(output,null,2)+'\n');
   console.log('WEB_COMPONENT_RESULT '+JSON.stringify(runner.stats));
   for(const f of failures)console.log('FAIL '+f.title+' '+f.message);
  });
 }
};