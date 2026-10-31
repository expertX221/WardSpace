"""WardSpace local demonstration server. Python 3.10+, no dependencies."""
import json, sqlite3, time, uuid
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from contextlib import contextmanager
from risk import assess
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).parent
DB = ROOT / 'wardspace.db'
@contextmanager
def connection():
    db = sqlite3.connect(DB)
    db.execute('CREATE TABLE IF NOT EXISTS events (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
    try:
        with db: yield db
    finally: db.close()

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path == '/api/events':
            session = parse_qs(urlsplit(self.path).query).get('session', [''])[0]
            if not session or len(session)>100: return self.reply({'error':'Session required'},400)
            with connection() as db:
                rows=db.execute('SELECT payload FROM events ORDER BY rowid DESC')
                events=(json.loads(r[0]) for r in rows)
                from itertools import islice
                self.reply(list(islice((e for e in events if e.get('session')==session),200)))
        else: super().do_GET()
    def reply(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status); self.send_header('Content-Type', 'application/json'); self.send_header('Cache-Control','no-store'); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        if self.path != '/api/events': return self.reply({'error':'Not found'},404)
        try:
            length=int(self.headers.get('Content-Length','0'))
            if length > 16384: return self.reply({'error':'Payload too large'},413)
            event=json.loads(self.rfile.read(length))
            if event.get('type') not in ['reading','note','attendance','acknowledge','response']: raise ValueError('Unknown event type')
            if not isinstance(event.get('id'),str) or len(event['id'])>100: raise ValueError('Invalid id')
            if not isinstance(event.get('session'),str) or not 1<=len(event['session'])<=100: raise ValueError('Invalid session')
            if event['type']=='reading': event['risk']=assess(event['data'], event.get('note',''))
            event['receivedAt']=time.time()
            with connection() as db:
                old=db.execute('SELECT payload FROM events WHERE id=?',(event['id'],)).fetchone()
                if old: return self.reply(json.loads(old[0]))
                db.execute('INSERT INTO events VALUES (?,?)',(event['id'],json.dumps(event)))
            self.reply(event)
        except (ValueError,KeyError,TypeError,json.JSONDecodeError) as e: self.reply({'error':str(e)},400)

if __name__=='__main__':
    print('WardSpace running at http://127.0.0.1:8000',flush=True)
    ThreadingHTTPServer(('127.0.0.1',8000),partial(Handler,directory=str(ROOT/'public'))).serve_forever()
