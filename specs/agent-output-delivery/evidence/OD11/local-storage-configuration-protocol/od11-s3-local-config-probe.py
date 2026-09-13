import datetime,hashlib,hmac,http.client,json
from pathlib import Path
from urllib.parse import urlencode

ENDPOINT='127.0.0.1:19000'

def request(method,path,query,body,credentials):
    now=datetime.datetime.now(datetime.timezone.utc);stamp=now.strftime('%Y%m%dT%H%M%SZ');date=now.strftime('%Y%m%d')
    q=urlencode(sorted(query.items()));digest=hashlib.sha256(body).hexdigest()
    canonical_headers='host:'+ENDPOINT+'\nx-amz-content-sha256:'+digest+'\nx-amz-date:'+stamp+'\n'
    signed='host;x-amz-content-sha256;x-amz-date'
    canonical='\n'.join([method,path,q,canonical_headers,signed,digest]);scope=date+'/us-east-1/s3/aws4_request'
    to_sign='AWS4-HMAC-SHA256\n'+stamp+'\n'+scope+'\n'+hashlib.sha256(canonical.encode()).hexdigest()
    key=('AWS4'+credentials['secret_key']).encode()
    for part in [date,'us-east-1','s3','aws4_request']:key=hmac.new(key,part.encode(),hashlib.sha256).digest()
    signature=hmac.new(key,to_sign.encode(),hashlib.sha256).hexdigest()
    headers={'Host':ENDPOINT,'x-amz-content-sha256':digest,'x-amz-date':stamp,'Authorization':'AWS4-HMAC-SHA256 Credential='+credentials['access_key']+'/'+scope+', SignedHeaders='+signed+', Signature='+signature}
    connection=http.client.HTTPConnection('127.0.0.1',19000,timeout=10)
    try:
        connection.request(method,path+('?' + q if q else ''),body=body,headers=headers)
        response=connection.getresponse();data=response.read(65537)
        assert len(data)<=65536
        return response.status,data
    finally:connection.close()

if __name__=='__main__':
    import sys,uuid
    credentials=json.loads(Path(sys.argv[1]).read_text())
    bucket='cyf-od11-config-'+uuid.uuid4().hex[:12]
    report={'scope':'Real isolated local S3/admin configuration protocol; no production change','bucket':bucket,'checks':[]}
    for label,method,path,query,data in [
        ('create','PUT','/'+bucket,{},b''),
        ('versioning','GET','/'+bucket,{'versioning':''},b''),
        ('quota_set','PUT','/minio/admin/v3/set-bucket-quota',{'bucket':bucket},json.dumps({'size':536870912,'quotatype':'hard'}).encode()),
        ('quota_get','GET','/minio/admin/v3/get-bucket-quota',{'bucket':bucket},b''),
        ('put','PUT','/'+bucket+'/probe.txt',{},b'output-config-probe\n'),
        ('get','GET','/'+bucket+'/probe.txt',{},b'')]:
        status,body=request(method,path,query,data,credentials)
        row={'case':label,'status':status,'bytes':len(body),'bodySha256':hashlib.sha256(body).hexdigest()}
        if label=='quota_get' and status==200:row['quota']=json.loads(body)
        report['checks'].append(row)
        if status not in (200,204):break
    Path('/tmp/od11-s3-local-config-probe.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
