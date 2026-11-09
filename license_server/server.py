"""HUNTARES licensing API. Run behind HTTPS reverse proxy. Python 3.9+ stdlib."""
import os, sqlite3, json, time, secrets, hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone

DB = os.environ.get('HUNTARES_DB', 'licenses.sqlite3')
ADMIN = os.environ.get('HUNTARES_ADMIN_KEY', '')
if len(ADMIN) < 24:
    raise SystemExit('Set HUNTARES_ADMIN_KEY to a random secret of at least 24 characters')

def db():
    c=sqlite3.connect(DB, timeout=10)
    c.execute('PRAGMA journal_mode=WAL')
    c.execute('CREATE TABLE IF NOT EXISTS keys (key TEXT PRIMARY KEY, name TEXT, type TEXT, created INTEGER, expires INTEGER, active INTEGER)')
    c.execute('CREATE TABLE IF NOT EXISTS activations (key TEXT, device_id TEXT, model TEXT, last_seen INTEGER, PRIMARY KEY(key,device_id))')
    c.commit(); return c

def stamp(n):
    return datetime.fromtimestamp(n, timezone.utc).strftime('%Y-%m-%d %H:%M UTC') if n else 'Бессрочно'

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if int(self.headers.get('Content-Length','0')) > 16384: return self.reply({'ok':False,'error':'Too large'},413)
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))))
            if not isinstance(data,dict): raise ValueError('Invalid JSON')
            with db() as c:
                result=self.handle(c,data)
            self.reply(result)
        except (ValueError,TypeError) as e: self.reply({'ok':False,'error':str(e)},400)
        except Exception: self.reply({'ok':False,'error':'Server error'},500)
    def reply(self, obj, status=200):
        raw=json.dumps(obj,ensure_ascii=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def handle(self,c,d):
        route=self.path
        key=str(d.get('key',''))
        if route=='/activate':
            if hmac.compare_digest(key,ADMIN): return {'ok':True,'admin':True}
            device=str(d.get('device_id',''))[:64]
            model=str(d.get('model',''))[:120]
            if not device or len(device)<16: return {'ok':False,'error':'Invalid device'}
            item=c.execute('SELECT type,expires,active FROM keys WHERE key=?',(key,)).fetchone()
            if not item or not item[2]: return {'ok':False,'error':'Ключ не найден или отключён'}
            if item[1] and item[1]<int(time.time()):return {'ok':False,'error':'Срок ключа истёк'}
            if item[0]=='hwid':
                bound=c.execute('SELECT device_id FROM activations WHERE key=? LIMIT 1',(key,)).fetchone()
                if bound and bound[0]!=device:return {'ok':False,'error':'Ключ привязан к другому устройству'}
            c.execute('INSERT INTO activations VALUES (?,?,?,?) ON CONFLICT(key,device_id) DO UPDATE SET model=excluded.model,last_seen=excluded.last_seen',(key,device,model,int(time.time())))
            return {'ok':True,'admin':False}
        if route.startswith('/admin/'):
            if not hmac.compare_digest(str(d.get('admin_key','')),ADMIN):return {'ok':False,'error':'Нет прав администратора'}
            if route=='/admin/create':
                name=str(d.get('name','')).strip()[:60]
                typ=str(d.get('type',''))
                days=int(d.get('days','0'))
                if not name or typ not in ('hwid','universal') or not 0<=days<=3650:return {'ok':False,'error':'Некорректные параметры'}
                new_key='HNT-'+secrets.token_urlsafe(24)
                now=int(time.time());expires=now+days*86400 if days else 0
                c.execute('INSERT INTO keys VALUES (?,?,?,?,?,1)',(new_key,name,typ,now,expires))
                return {'ok':True,'key':new_key}
            if route=='/admin/list':
                rows=c.execute('SELECT key,name,type,created,expires,active FROM keys ORDER BY created DESC LIMIT 1000').fetchall()
                return {'ok':True,'keys':[dict(key=r[0],name=r[1],type=r[2],created=stamp(r[3]),expires=stamp(r[4]),active=bool(r[5])) for r in rows]}
            if route=='/admin/details':
                row=c.execute('SELECT name,type,expires,active FROM keys WHERE key=?',(key,)).fetchone()
                if not row:return {'ok':False,'error':'Ключ не найден'}
                devices=c.execute('SELECT device_id,model,last_seen FROM activations WHERE key=? ORDER BY last_seen DESC',(key,)).fetchall()
                return {'ok':True,'name':row[0],'type':row[1],'expires':stamp(row[2]),'active':bool(row[3]),'devices':[dict(device_id=r[0],model=r[1],last_seen=stamp(r[2])) for r in devices]}
            if route=='/admin/revoke':
                c.execute('UPDATE keys SET active=0 WHERE key=?',(key,))
                return {'ok':True}
        return {'ok':False,'error':'Unknown route'}

if __name__=='__main__':
    db().close()
    ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('PORT','8765'))),Handler).serve_forever()
