"""Own ephemeral loopback transport to exact current-thread socket; never controls mysqld."""
from pathlib import Path
import json,socket,threading,selectors,os,subprocess,time
E=Path('/home/isp/wsps/cyf/evidence/u3-finalization-schema-check-truth-v1')
SOCKET='/var/tmp/cyf-jyt-mmd-mysql-20260929-thread01a0dde8/mysql.sock'
assert str(Path(SOCKET).resolve())==SOCKET
identity=subprocess.check_output(['mysql','--no-defaults','--socket='+SOCKET,'-u','root','--batch','--skip-column-names','-e','SELECT @@socket,@@datadir,@@version,@@port,@@skip_networking;'],universal_newlines=True).strip().split('\t')
assert identity==[SOCKET,'/var/tmp/cyf-jyt-mmd-mysql-20260929-thread01a0dde8/data/','8.0.21','0','1']
listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM);listener.bind(('127.0.0.1',0));listener.listen();port=listener.getsockname()[1]
manifest=E/'mysql-proxy-current-owner-v1.json';manifest.write_text(json.dumps({'owner_thread':'01a0dde8-fd03-7ee0-be21-293ca13bb336','pid':os.getpid(),'address':'127.0.0.1','port':port,'upstream_socket':SOCKET,'mysql_identity':identity,'production_or_foreign_server':False,'shutdown':'exact owner stop file only after JDBC verification ends; no signal/server control'},indent=2)+'\n')
stop=E/('mysql-proxy-stop-'+str(os.getpid()));state={'connections':0,'errors':[]};clients=set();lock=threading.Lock()
def bridge(client):
 server=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);selector=selectors.DefaultSelector()
 try:
  server.connect(SOCKET);selector.register(client,selectors.EVENT_READ,server);selector.register(server,selectors.EVENT_READ,client)
  while True:
   events=selector.select()
   for key,mask in events:
    data=key.fileobj.recv(65536)
    if not data:return
    key.data.sendall(data)
 except (BrokenPipeError,ConnectionResetError):pass
 except Exception as exc:
  with lock:state['errors'].append(repr(exc))
 finally:
  selector.close();client.close();server.close()
  with lock:clients.discard(threading.current_thread())
listener.settimeout(0.2)
print('READY '+str(port),flush=True)
while not stop.exists():
 try:client,_=listener.accept()
 except socket.timeout:continue
 t=threading.Thread(target=bridge,args=(client,),daemon=True)
 with lock:clients.add(t);state['connections']+=1
 t.start()
listener.close()
while True:
 with lock:active=list(clients)
 if not active:break
 for t in active:t.join(0.2)
manifest=E/'mysql-proxy-terminal-v1.json';manifest.write_text(json.dumps(dict(state,owner_pid=os.getpid(),port=port,own_listener_closed=True,upstream_mysqld_untouched=True),indent=2)+'\n');print('CLOSED '+str(port),flush=True)
