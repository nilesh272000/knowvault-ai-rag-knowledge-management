import sqlite3
from pathlib import Path
DB=Path("data/knowvault.db");DB.parent.mkdir(exist_ok=True)
class Catalog:
    def __init__(self):
        self.conn=sqlite3.connect(DB,check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS documents(name TEXT PRIMARY KEY,chunks INTEGER)")
        self.conn.commit()
    def upsert(self,name,chunks):
        self.conn.execute("INSERT OR REPLACE INTO documents VALUES (?,?)",(name,chunks));self.conn.commit()
    def delete(self,name):
        self.conn.execute("DELETE FROM documents WHERE name=?",(name,));self.conn.commit()
    def all(self):
        return [{"name":r[0],"chunks":r[1]} for r in self.conn.execute("SELECT name,chunks FROM documents ORDER BY name")]
    def count(self):return self.conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
