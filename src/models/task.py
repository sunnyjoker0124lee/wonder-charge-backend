from datetime import datetime
from ..database import db

class Task:
    def __init__(self, id=None, stage=None, milestone=None, start_date=None, 
                 end_date=None, content=None, holiday_impact=None, 
                 dependencies=None, responsible=None, risks=None,
                 created_at=None, updated_at=None):
        self.id = id
        self.stage = stage
        self.milestone = milestone
        self.start_date = start_date
        self.end_date = end_date
        self.content = content
        self.holiday_impact = holiday_impact
        self.dependencies = dependencies
        self.responsible = responsible
        self.risks = risks
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        """將Task物件轉換為字典"""
        return {
            'id': self.id,
            'stage': self.stage,
            'milestone': self.milestone,
            'startDate': self.start_date,  # 保持前端期望的欄位名稱
            'endDate': self.end_date,      # 保持前端期望的欄位名稱
            'description': self.content,   # 保持前端期望的欄位名稱
            'holidayImpact': self.holiday_impact,  # 保持前端期望的欄位名稱
            'dependencies': self.dependencies,
            'responsible': self.responsible,
            'risks': self.risks,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """從字典創建Task物件"""
        return cls(
            id=data.get('id'),
            stage=data.get('stage'),
            milestone=data.get('milestone'),
            start_date=data.get('start_date') or data.get('startDate'),
            end_date=data.get('end_date') or data.get('endDate'),
            content=data.get('content') or data.get('description'),
            holiday_impact=data.get('holiday_impact') or data.get('holidayImpact'),
            dependencies=data.get('dependencies'),
            responsible=data.get('responsible'),
            risks=data.get('risks'),
            created_at=data.get('created_at'),
            updated_at=data.get('updated_at')
        )
    
    @classmethod
    def get_all(cls):
        """獲取所有任務"""
        query = "SELECT * FROM tasks ORDER BY start_date"
        results = db.execute_query(query)
        return [cls.from_dict(row) for row in results]
    
    @classmethod
    def get_by_id(cls, task_id):
        """根據ID獲取任務"""
        if db.use_sqlite:
            query = "SELECT * FROM tasks WHERE id = ?"
        else:
            query = "SELECT * FROM tasks WHERE id = %s"
        
        results = db.execute_query(query, (task_id,))
        if results:
            return cls.from_dict(results[0])
        return None
    
    def save(self):
        """保存任務（新增或更新）"""
        if self.id:
            # 更新現有任務
            if db.use_sqlite:
                query = '''
                    UPDATE tasks 
                    SET stage = ?, milestone = ?, start_date = ?, end_date = ?,
                        content = ?, holiday_impact = ?, dependencies = ?,
                        responsible = ?, risks = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                '''
                params = (self.stage, self.milestone, self.start_date, self.end_date,
                         self.content, self.holiday_impact, self.dependencies,
                         self.responsible, self.risks, self.id)
            else:
                query = '''
                    UPDATE tasks 
                    SET stage = %s, milestone = %s, start_date = %s, end_date = %s,
                        content = %s, holiday_impact = %s, dependencies = %s,
                        responsible = %s, risks = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                '''
                params = (self.stage, self.milestone, self.start_date, self.end_date,
                         self.content, self.holiday_impact, self.dependencies,
                         self.responsible, self.risks, self.id)
            
            db.execute_query(query, params)
            return self
        else:
            # 新增任務
            if db.use_sqlite:
                query = '''
                    INSERT INTO tasks (stage, milestone, start_date, end_date, content,
                                     holiday_impact, dependencies, responsible, risks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                params = (self.stage, self.milestone, self.start_date, self.end_date,
                         self.content, self.holiday_impact, self.dependencies,
                         self.responsible, self.risks)
            else:
                query = '''
                    INSERT INTO tasks (stage, milestone, start_date, end_date, content,
                                     holiday_impact, dependencies, responsible, risks)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                params = (self.stage, self.milestone, self.start_date, self.end_date,
                         self.content, self.holiday_impact, self.dependencies,
                         self.responsible, self.risks)
            
            result = db.insert_and_return(query, params)
            if result:
                return self.from_dict(result)
            return None
    
    def delete(self):
        """刪除任務"""
        if self.id:
            if db.use_sqlite:
                query = "DELETE FROM tasks WHERE id = ?"
            else:
                query = "DELETE FROM tasks WHERE id = %s"
            
            db.execute_query(query, (self.id,))
            return True
        return False
    
    @classmethod
    def delete_by_id(cls, task_id):
        """根據ID刪除任務"""
        if db.use_sqlite:
            query = "DELETE FROM tasks WHERE id = ?"
        else:
            query = "DELETE FROM tasks WHERE id = %s"
        
        rowcount = db.execute_query(query, (task_id,))
        return rowcount > 0

