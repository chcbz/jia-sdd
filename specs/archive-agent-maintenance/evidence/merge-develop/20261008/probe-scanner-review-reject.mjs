import { relativeModuleSpecifiers } from 'file:///C:/Users/Think/.codex/worktrees/archive-agent-maintenance/isp-install/conf/codex-ws-agent/test/module-import-scanner.mjs'
import { writeFileSync } from 'node:fs'
const source = "if (true) {\n  import('./missing.mjs')\n  {}\n}"
const result = {at:new Date().toISOString(),source,specifiers:relativeModuleSpecifiers(source),expected:['./missing.mjs'],scope:'read-only scanner P2 reproduction, not executing the example module'}
writeFileSync('C:/tmp/aam-merge-develop-20261008/scanner-review-reject-reproduction.json',JSON.stringify(result,null,2)+'\n')
console.log(JSON.stringify(result))