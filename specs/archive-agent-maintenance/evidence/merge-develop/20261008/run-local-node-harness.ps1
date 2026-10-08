$ErrorActionPreference='Stop'
$b='C:\tmp\aam-merge-develop-20261008'
$r='C:\Users\Think\.codex\worktrees\archive-agent-maintenance\cyf-web-kit'
$c='C:\Users\Think\.codex\worktrees\archive-agent-maintenance\isp-install'
$out=Join-Path $b 'node-local-harness-attempt3'
if(Test-Path -LiteralPath $out){throw 'fresh output required'}
New-Item -ItemType Directory -Path $out|Out-Null
$webBefore=(git -C "$r\web" write-tree).Trim();$clientBefore=(git -C $c write-tree).Trim()
if($webBefore -ne '11d2f205cc5e60e5de886e001575449efc700900' -or $clientBefore -ne '08b26571ffc5bda3083997948b48c3084313305a'){throw 'freeze drift'}
if((git -C "$r\web" diff --name-only) -or (git -C $c diff --name-only)){throw 'source not frozen'}
Set-Location "$c\conf\codex-ws-agent"
node --test test/module-import-scanner.test.mjs 2>&1 | Tee-Object -FilePath "$out\client-scanner-test.log"
$clientExit=$LASTEXITCODE
node --input-type=module -e "import {scanRuntimeModuleClosure} from './test/module-import-scanner.mjs'; console.log(JSON.stringify(scanRuntimeModuleClosure(process.cwd()),null,2))" 2>&1 | Tee-Object -FilePath "$out\client-runtime-module-closure.log"
$closureExit=$LASTEXITCODE
Set-Location "$r\web"
$command=Get-Content -Raw "$r\specs\archive-agent-maintenance\evidence\merge-develop\20261008\web-local-attempt2\command.json"|ConvertFrom-Json
$arguments=@($command.arguments)+@('tests/juyiting-bounty-inline-results.test.js')
$env:CYF_MERGE_WEB_RESULT="$out\web-component-result.json"
@{started_at=(Get-Date).ToString('o');arguments=$arguments;web_staged_tree=$webBefore;client_staged_tree=$clientBefore;client_scope='scanner six unit tests plus actual module closure; Linux installer/full tests separate';real_runtime_e2e=$false} | ConvertTo-Json -Depth 6 | Set-Content "$out\command.json" -Encoding utf8
node @arguments 2>&1 | Tee-Object -FilePath "$out\web-component-test.log"
$webExit=$LASTEXITCODE
npm run build 2>&1 | Tee-Object -FilePath "$out\web-build.log"
$buildExit=$LASTEXITCODE
git diff -- src/auto-imports.d.ts src/components.d.ts | Set-Content "$out\web-generated-typing-noise.diff" -Encoding utf8
git restore --source=HEAD --worktree -- src/auto-imports.d.ts src/components.d.ts
$webAfter=(git -C "$r\web" write-tree).Trim();$clientAfter=(git -C $c write-tree).Trim()
@{web_tree_before=$webBefore;web_tree_after=$webAfter;client_tree_before=$clientBefore;client_tree_after=$clientAfter;source_unchanged=($webBefore -eq $webAfter -and $clientBefore -eq $clientAfter);web_unstaged=@(git -C "$r\web" diff --name-only);client_unstaged=@(git -C $c diff --name-only);client_scanner_exit=$clientExit;client_closure_exit=$closureExit;web_test_exit=$webExit;web_build_exit=$buildExit;whole_feature_accepted=$false} | ConvertTo-Json -Depth 5 | Set-Content "$out\result.json" -Encoding utf8
if($clientExit -or $closureExit -or $webExit -or $buildExit){exit 1}