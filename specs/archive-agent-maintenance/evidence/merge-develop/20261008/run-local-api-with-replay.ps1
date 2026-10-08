param([string]$Attempt='api-local-attempt1')
$ErrorActionPreference='Stop'
$api='C:\Users\Think\.codex\worktrees\archive-agent-maintenance\cyf-web-kit\api'
$base='C:\tmp\aam-merge-develop-20261008'
if($Attempt -notmatch '^[a-z0-9-]+$'){throw 'invalid attempt'}
$out=Join-Path $base $Attempt
if(Test-Path -LiteralPath $out){throw 'fresh attempt required'}
New-Item -ItemType Directory -Path $out|Out-Null
$lock=$null
while(-not $lock){try{$lock=[IO.File]::Open('C:\tmp\cyf-gradle.lock',[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)}catch [IO.IOException]{Start-Sleep -Seconds 2}}
$oldJava=$env:JAVA_HOME;$oldPath=$env:PATH;$oldOpts=$env:GRADLE_OPTS
try{
 $env:JAVA_HOME='D:\software\Java\graalvm-jdk-25';$env:PATH="$env:JAVA_HOME\bin;$env:PATH";$env:GRADLE_OPTS='-Xmx128m'
 Set-Location $api
 if((& git diff --name-only)){throw 'source must be staged/frozen'}
 if((& git ls-files --unmerged)){throw 'unresolved source merge'}
 $before=(& git write-tree).Trim();$start=[DateTime]::UtcNow
 $tasks=@(':agent:jia-agent-service:archivePlatformContracts',':agent:jia-agent-service:archiveMaintenanceSecurity',':chat:jia-chat-service:archiveMaintenanceMvp',':chat:jia-chat-service:archiveRegression',':chat:jia-chat-service:mmdU2TypedInspection',':chat:jia-chat-service:chatConversationReplay')
 $args=$tasks+@('--init-script',(Join-Path $base 'force-local-tests.gradle'),'--continue','--no-daemon','--max-workers=1','-Dorg.gradle.jvmargs=-Xmx768m -XX:MaxMetaspaceSize=384m -XX:+UseSerialGC -XX:ActiveProcessorCount=2')
 @{started_utc=$start.ToString('o');api_staged_tree=$before;arguments=$args;gradle_lock='C:\tmp\cyf-gradle.lock';boundary='local Windows merge validation; any MySQL skips/POSIX failures explicit, not server full acceptance'} |ConvertTo-Json -Depth 6|Set-Content (Join-Path $out 'command.json') -Encoding utf8
 & .\gradlew.bat @args 2>&1|Tee-Object -FilePath (Join-Path $out 'gradle.log')
 $exit=$LASTEXITCODE;$suites=@()
 foreach($task in $tasks){
  $parts=$task.Trim(':').Split(':');$name=$parts[2];$dir=Join-Path $api "$($parts[0])\$($parts[1])\build\test-results\$name"; $copy=Join-Path $out $name;New-Item -ItemType Directory -Path $copy|Out-Null
  $total=0;$fail=0;$err=0;$skip=0;$stale=@();$files=@();$failedMethods=@()
  foreach($f in Get-ChildItem -LiteralPath $dir -Filter 'TEST-*.xml' -ErrorAction SilentlyContinue){
   if($f.LastWriteTimeUtc -lt $start){$stale+=$f.Name;continue}
   [xml]$x=Get-Content -LiteralPath $f.FullName
   $total += [int]$x.testsuite.tests;$fail += [int]$x.testsuite.failures;$err += [int]$x.testsuite.errors;$skip += [int]$x.testsuite.skipped
   foreach($t in $x.testsuite.testcase){if($t.failure -or $t.error){$failedMethods+="$($t.classname)#$($t.name)"}}
   $files+=@{name=$f.Name;sha256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLowerInvariant();fresh=$true};Copy-Item -LiteralPath $f.FullName -Destination $copy
  }
  $suites+=@{task=$task;tests=$total;pass=($total-$fail-$err-$skip);failures=$fail;errors=$err;skipped=$skip;fresh_xml_files=$files;stale_ignored=$stale;failure_set=$failedMethods;ran=($total -gt 0)}
 }
 $after=(& git write-tree).Trim();$dirty=@(& git diff --name-only)
 @{api_staged_tree_before=$before;api_staged_tree_after=$after;staged_source_unchanged=($before -eq $after);tracked_unstaged=$dirty;gradle_exit=$exit;natural_command_completion=$true;all_requested_tasks_have_fresh_results=(@($suites|Where-Object {-not $_.ran}).Count -eq 0);suites=$suites;server_validation=$false;whole_feature_accepted=$false} |ConvertTo-Json -Depth 10|Set-Content (Join-Path $out 'result.json') -Encoding utf8
 foreach($s in $suites){"TASK=$($s.task) TESTS=$($s.tests) PASS=$($s.pass) FAIL=$($s.failures) ERR=$($s.errors) SKIP=$($s.skipped) STALE=$($s.stale_ignored.Count)"};"GRADLE_EXIT=$exit"
 exit $exit
}finally{$env:JAVA_HOME=$oldJava;$env:PATH=$oldPath;$env:GRADLE_OPTS=$oldOpts;if($lock){$lock.Dispose()}}