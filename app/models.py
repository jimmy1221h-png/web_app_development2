import sqlite3
import os

# 設定資料庫路徑 (專案根目錄的 instance/database.db)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    建立並回傳資料庫連線
    使用 sqlite3.Row 讓查詢結果能以字典欄位名稱方式存取
    """
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

class Record:
    """收支紀錄 Model"""

    @staticmethod
    def create(data):
        """
        新增一筆收支記錄
        :param data: dict 包含 'type', 'amount', 'date', 'category', 'note'
        :return: 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            if conn is None: return False
            
            conn.execute(
                "INSERT INTO records (type, amount, date, category, note) VALUES (?, ?, ?, ?, ?)",
                (data['type'], data['amount'], data['date'], data['category'], data.get('note', ''))
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating record: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_all():
        """
        取得所有收支記錄
        :return: 回傳 dict 的列表，若發生錯誤回傳空列表
        """
        conn = None
        try:
            conn = get_db_connection()
            if conn is None: return []
            
            # 依照日期由新到舊排序
            records = conn.execute("SELECT * FROM records ORDER BY date DESC, id DESC").fetchall()
            return [dict(row) for row in records]
        except sqlite3.Error as e:
            print(f"Error fetching all records: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_by_id(record_id):
        """
        取得單筆收支記錄
        :param record_id: 記錄的 ID (整數)
        :return: 回傳包含該筆資料的 dict，若找不到或發生錯誤回傳 None
        """
        conn = None
        try:
            conn = get_db_connection()
            if conn is None: return None
            
            record = conn.execute("SELECT * FROM records WHERE id = ?", (record_id,)).fetchone()
            return dict(record) if record else None
        except sqlite3.Error as e:
            print(f"Error fetching record {record_id}: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update(record_id, data):
        """
        更新指定的收支記錄
        :param record_id: 記錄的 ID (整數)
        :param data: dict 包含 'type', 'amount', 'date', 'category', 'note'
        :return: 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            if conn is None: return False
            
            conn.execute(
                "UPDATE records SET type = ?, amount = ?, date = ?, category = ?, note = ? WHERE id = ?",
                (data['type'], data['amount'], data['date'], data['category'], data.get('note', ''), record_id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating record {record_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete(record_id):
        """
        刪除指定的收支記錄
        :param record_id: 記錄的 ID (整數)
        :return: 成功回傳 True，失敗回傳 False
        """
        conn = None
        try:
            conn = get_db_connection()
            if conn is None: return False
            
            conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting record {record_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()
