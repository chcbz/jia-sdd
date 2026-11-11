'use strict';
const fs = require('node:fs');
const crypto = require('node:crypto');
const WebSocket = require('/home/isp/wsps/cyf/web/node_modules/ws');
const root = '/var/tmp/cyf-voice-realtime-20260930';
const config = JSON.parse(fs.readFileSync(0, 'utf8'));
if (config.base !== 'https://codex.chcbz.net/v1' || !config.key) throw Error('Invalid fixed target configuration');
const target = 'wss://codex.chcbz.net/v1/realtime?model=gpt-realtime';
const input = fs.readFileSync(root + '/input.pcm');
const summary = {started_at: new Date().toISOString(), target, authorization: 'User explicitly allowed one real voice test with existing account quota; no purchase or production activation', automatic_retries: 0, connection_attempts: 1, websocket_open: false, audio_input_bytes_sent: 0, response_create_count: 0, event_types: [], usage: null, status: 'STARTING', production_changed: false};
let finished = false, initialized = false, sent = false, transcript = '', audio = [], modern = true;
function safe(value) {
  return JSON.stringify(value).split(config.key).join('<redacted>').replace(/Bearer\s+[^\s"\\]+/g, 'Bearer <redacted>');
}
function log(value) {fs.appendFileSync(root + '/events.jsonl', safe({at:new Date().toISOString(), ...value}) + '\n', {mode:0o600});}
function wav(pcm) {
 const b=Buffer.alloc(44);b.write('RIFF');b.writeUInt32LE(36+pcm.length,4);b.write('WAVE',8);b.write('fmt ',12);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(24000,24);b.writeUInt32LE(48000,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(pcm.length,40);return Buffer.concat([b,pcm]);
}
function finish(status, extra={}) {
 if(finished)return; finished=true;
 Object.assign(summary, extra, {status, ended_at:new Date().toISOString(), output_transcript:transcript, output_audio_bytes:audio.reduce((n,b)=>n+b.length,0)});
 if(audio.length) {
  const pcm=Buffer.concat(audio);fs.writeFileSync(root+'/output.wav',wav(pcm),{mode:0o600});
  summary.output_wav_sha256=crypto.createHash('sha256').update(fs.readFileSync(root+'/output.wav')).digest('hex');
  summary.output_audio_seconds=pcm.length/48000;
 }
 fs.writeFileSync(root+'/result.json',safe(summary)+'\n',{mode:0o600});console.log(safe(summary));
 if(ws.readyState===WebSocket.OPEN)ws.close(1000,'Single authorized test finished');
}
const ws = new WebSocket(target, {headers:{Authorization:'Bearer '+config.key}, followRedirects:false, perMessageDeflate:false, handshakeTimeout:config.connectTimeoutMillis});
ws.on('open',()=>{summary.websocket_open=true;log({type:'transport.open'});});
ws.on('unexpected-response',(request,response)=>{
 const chunks=[];response.on('data',c=>chunks.push(c));
 response.on('end',()=>{
  const body=Buffer.concat(chunks).toString('utf8'); let error;
  try{const obj=JSON.parse(body);error=obj.error||obj;}catch{error={body_excerpt:body.slice(0,2048)};}
  log({type:'transport.handshake_rejected',status:response.statusCode,error});
  finish('HANDSHAKE_REJECTED',{http_status:response.statusCode,error,headers:{'content-type':response.headers['content-type'],'x-request-id':response.headers['x-request-id'],'x-cpa-version':response.headers['x-cpa-version']}});
  request.destroy();
 });
});
ws.on('error',err=>{log({type:'transport.error',message:err.message});finish('TRANSPORT_ERROR',{transport_error:err.message});});
ws.on('close',(code,reason)=>{log({type:'transport.close',code,reason:reason.toString()});finish('CLOSED_WITHOUT_COMPLETE_RESPONSE',{close_code:code});});
ws.on('message',raw=>{
 let event;try{event=JSON.parse(raw.toString());}catch{log({type:'non_json_event'});return;}
 summary.event_types.push(event.type);
 if(event.type==='error'){log({type:event.type,error:event.error});finish('PROTOCOL_OR_UPSTREAM_ERROR',{error:event.error});return;}
 log({type:event.type,event_id:event.event_id});
 if(event.type==='session.created'&&!initialized){
  initialized=true;modern=Boolean(event.session?.audio);
  summary.session_model=event.session?.model;summary.protocol=modern?'realtime_ga':'realtime_beta';
  const instruction='Repeat exactly the words spoken in the input audio. Do not add anything else.';
  const session=modern?{type:'realtime',output_modalities:['audio'],instructions:instruction,audio:{input:{format:{type:'audio/pcm',rate:24000},turn_detection:null},output:{format:{type:'audio/pcm',rate:24000}}}}:{modalities:['text','audio'],instructions:instruction,input_audio_format:'pcm16',output_audio_format:'pcm16',turn_detection:null};
  ws.send(JSON.stringify({type:'session.update',session}));
 }
 if(event.type==='session.updated'&&!sent){
  sent=true;ws.send(JSON.stringify({type:'input_audio_buffer.append',audio:input.toString('base64')}));summary.audio_input_bytes_sent=input.length;
  ws.send(JSON.stringify({type:'input_audio_buffer.commit'}));
  ws.send(JSON.stringify({type:'response.create',response:modern?{output_modalities:['audio']}:{modalities:['text','audio']}}));summary.response_create_count=1;
 }
 if(['response.audio.delta','response.output_audio.delta'].includes(event.type))audio.push(Buffer.from(event.delta,'base64'));
 if(['response.audio_transcript.delta','response.output_audio_transcript.delta'].includes(event.type))transcript+=event.delta||'';
 if(event.type==='response.done'){
  summary.usage=event.response?.usage||null;summary.response_status=event.response?.status;
  finish(event.response?.status==='completed'&&audio.length?'AUDIO_RESPONSE_RECEIVED':'RESPONSE_NOT_VERIFIED',{status_details:event.response?.status_details});
 }
});
