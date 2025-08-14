import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Database:
    def __init__(self):
        # 從環境變數獲取資料庫連接資訊
        self.database_url = os.getenv('DATABASE_URL')
        
        # 如果沒有設定DATABASE_URL，使用本地SQLite作為後備
        if not self.database_url:
            import sqlite3
            self.use_sqlite = True
            self.db_path = os.path.join(os.path.dirname(__file__), '..', 'tasks.db')
        else:
            self.use_sqlite = False
    
    def get_connection(self):
        """獲取資料庫連接"""
        if self.use_sqlite:
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        else:
            return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def init_db(self):
        """初始化資料庫表格"""
        if self.use_sqlite:
            self._init_sqlite()
        else:
            self._init_postgresql()
    
    def _init_sqlite(self):
        """初始化SQLite資料庫"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stage TEXT NOT NULL,
                milestone TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                content TEXT,
                holiday_impact TEXT,
                dependencies TEXT,
                responsible TEXT,
                risks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _init_postgresql(self):
        """初始化PostgreSQL資料庫"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                stage VARCHAR(255) NOT NULL,
                milestone VARCHAR(255) NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                content TEXT,
                holiday_impact TEXT,
                dependencies TEXT,
                responsible TEXT,
                risks TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def execute_query(self, query, params=None):
        """執行查詢並返回結果"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                if self.use_sqlite:
                    # 將sqlite3.Row轉換為字典
                    return [dict(row) for row in results]
                else:
                    # psycopg2的RealDictCursor已經返回字典
                    return [dict(row) for row in results]
            else:
                conn.commit()
                return cursor.rowcount
        
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def insert_and_return(self, query, params=None):
        """插入資料並返回新插入的記錄"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if self.use_sqlite:
                # SQLite使用lastrowid
                new_id = cursor.lastrowid
                conn.commit()
                # 查詢新插入的記錄
                cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_id,))
                result = cursor.fetchone()
                return dict(result) if result else None
            else:
                # PostgreSQL使用RETURNING
                if not query.upper().endswith('RETURNING *'):
                    query += ' RETURNING *'
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchone()
                conn.commit()
                return dict(result) if result else None
        
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

# 全域資料庫實例
db = Database()

