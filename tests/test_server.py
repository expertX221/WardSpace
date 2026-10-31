import unittest, tempfile, threading, json
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from http.server import ThreadingHTTPServer
import server
class SessionTests(unittest.TestCase):
 def test_session_history_and_idempotency(self):
  with tempfile.TemporaryDirectory() as folder:
   old=server.DB;server.DB=Path(folder)/'test.db'
   http=ThreadingHTTPServer(('127.0.0.1',0),server.Handler)
   threading.Thread(target=http.serve_forever,daemon=True).start()
   url='http://127.0.0.1:'+str(http.server_port)+'/api/events'
   try:
    for session in ['a','b']:
     e=dict(id=session,type='note',session=session,data={'text':'demo'})
     for _ in range(2):
      with urlopen(Request(url,data=json.dumps(e).encode(),headers={'Content-Type':'application/json'})) as response:self.assertEqual(response.status,200)
    with urlopen(url+'?session=a') as response:
     rows=json.load(response);self.assertEqual(len(rows),1);self.assertEqual(rows[0]['session'],'a')
    with self.assertRaises(HTTPError) as error:urlopen(url)
    self.assertEqual(error.exception.code,400)
   finally:http.shutdown();http.server_close();server.DB=old
