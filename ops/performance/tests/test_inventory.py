import json, os, tempfile, unittest
from ops.performance.inventory import scan_source, reconcile, _runtime_routes

class InventoryTest(unittest.TestCase):
    def source(self, text):
        d=tempfile.mkdtemp(); p=os.path.join(d,'DemoController.java');
        with open(p,'w') as f: f.write(text)
        return d
    def test_arrays_and_comments(self):
        d=self.source('''@RestController\n@RequestMapping(path={"/a", "/b"})\nclass DemoController {\n // @GetMapping("/fake")\n @RequestMapping(value={"/x", "/y"}, method={RequestMethod.PUT, RequestMethod.DELETE})\n public String run() { return "// literal"; }\n}''')
        routes, ds, _=scan_source(d); self.assertEqual([], [d for d in ds if d['fatal']]); self.assertEqual(8,len(routes)); self.assertIn(('PUT','/a/x'), {(x['method'],x['path']) for x in routes})
    def test_missing_method_is_any(self):
        d=self.source('@RequestMapping("/root")\nclass DemoController { @RequestMapping("/x") public void x() {} }'); routes,ds,_=scan_source(d); self.assertFalse(ds); self.assertEqual('ANY',routes[0]['method'])
    def test_nonliteral_fails_closed(self):
        d=self.source('@RequestMapping(BASE + "/x")\nclass DemoController { @GetMapping(PATH) public void x() {} }'); routes,ds,_=scan_source(d); self.assertTrue(ds); self.assertEqual([],routes)
    def test_inheritance_fails_closed(self):
        d=self.source('@RequestMapping("/root")\nclass DemoController extends BaseController { @GetMapping("/x") public void x() {} }'); _,ds,_=scan_source(d); self.assertTrue(any(x['code']=='unsupported_inheritance' for x in ds))
    def test_runtime_management_and_unknown(self):
        rt={'contexts':{'application':{'mappings':{'dispatcherServlets':{'dispatcherServlet':[{'predicate':'{GET [/actuator/health]}','handler':'Health'}, {'predicate':'{GET [/missing]}','handler':'X'}]}}}}}
        got={(x['method'],x['path']) for x in _runtime_routes(rt)}; self.assertIn(('GET','/actuator/health'),got)
        result=reconcile([{'method':'GET','path':'/actuator/health'}],{'profile':'grey','api_commit':'c','api_tree':'t'},dict(rt, profile='grey', api_commit='c', api_tree='t', capture_content_sha256='h'), {'commit':'c','tree':'t'},'grey'); self.assertFalse(result['ok']); self.assertTrue(any(x['code']=='runtime_unknown' for x in result['diagnostics']))
    def test_profile_and_binding(self):
        result=reconcile([],{'profile':'prod','api_commit':'c','api_tree':'wrong'},{'profile':'grey','api_commit':'c','api_tree':'right','capture_content_sha256':'h'}, {'commit':'c','tree':'right'},'grey'); self.assertFalse(result['ok']); self.assertTrue(any(x['code']=='profile_mismatch' for x in result['diagnostics']))
    def test_json_media_is_not_stream_exemption(self):
        d=self.source('@RequestMapping("/media/upload")\nclass DemoController { @PostMapping("/x") public void x() {} }'); routes,ds,_=scan_source(d); self.assertFalse(ds); self.assertIn(('POST','/media/upload/x'), {(x['method'],x['path']) for x in routes})

if __name__=='__main__': unittest.main()
