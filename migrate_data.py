#!/usr/bin/env python3
"""
資料遷移腳本：將現有的SQLite資料遷移到新的資料庫結構
"""

import json
import os
import sys
from datetime import datetime

# 添加專案路徑
sys.path.insert(0, os.path.dirname(__file__))

from src.database import db
from src.models.task import Task

def migrate_from_json():
    """從JSON檔案遷移資料"""
    json_file = os.path.join(os.path.dirname(__file__), 'excel_data.json')
    
    if not os.path.exists(json_file):
        print(f"找不到資料檔案: {json_file}")
        return
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"開始遷移 {len(data)} 筆資料...")
    
    # 初始化資料庫
    db.init_db()
    
    migrated_count = 0
    
    for item in data:
        try:
            # 創建新任務
            task = Task(
                stage=item.get('階段', ''),
                milestone=item.get('里程碑', ''),
                start_date=item.get('開始日期', ''),
                end_date=item.get('結束日期', ''),
                content=item.get('內容說明', ''),
                holiday_impact=item.get('假期影響', ''),
                dependencies=item.get('相依關係', ''),
                responsible=item.get('負責單位/人', ''),
                risks=item.get('風險/備註', '')
            )
            
            # 保存任務
            saved_task = task.save()
            if saved_task:
                migrated_count += 1
                print(f"✓ 遷移成功: {task.milestone}")
            else:
                print(f"✗ 遷移失敗: {task.milestone}")
                
        except Exception as e:
            print(f"✗ 遷移錯誤: {item.get('里程碑', 'Unknown')} - {str(e)}")
    
    print(f"\n遷移完成！成功遷移 {migrated_count} 筆資料")

def verify_migration():
    """驗證遷移結果"""
    print("\n驗證遷移結果...")
    
    try:
        tasks = Task.get_all()
        print(f"資料庫中共有 {len(tasks)} 筆任務")
        
        # 按階段統計
        stage_counts = {}
        for task in tasks:
            stage = task.stage
            stage_counts[stage] = stage_counts.get(stage, 0) + 1
        
        print("\n各階段任務數量:")
        for stage, count in stage_counts.items():
            print(f"  {stage}: {count} 筆")
            
    except Exception as e:
        print(f"驗證失敗: {str(e)}")

if __name__ == "__main__":
    print("Wonder Charge 活動管理系統 - 資料遷移工具")
    print("=" * 50)
    
    migrate_from_json()
    verify_migration()
    
    print("\n遷移完成！")

