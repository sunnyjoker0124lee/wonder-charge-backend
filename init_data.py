import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.main import app, db
from src.models.task import Task

def init_database():
    with app.app_context():
        # 清空現有資料
        Task.query.delete()
        
        # 讀取初始資料
        with open('excel_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 插入初始資料
        for item in data:
            task = Task(
                stage=item.get('階段', ''),
                startDate=item.get('開始日', ''),
                endDate=item.get('結束日', ''),
                milestone=item.get('里程碑', ''),
                description=item.get('內容說明', ''),
                holidayImpact=item.get('假期影響', ''),
                dependencies=item.get('相依關係', ''),
                responsible=item.get('負責單位/人', ''),
                risks=item.get('風險/備註', '')
            )
            db.session.add(task)
        
        db.session.commit()
        print(f"成功初始化 {len(data)} 筆資料")

if __name__ == '__main__':
    init_database()

