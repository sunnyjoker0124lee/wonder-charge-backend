from flask import Blueprint, request, jsonify
from ..models.task import Task
from ..database import db
import json
import os

task_bp = Blueprint("task_bp", __name__)

@task_bp.route("/tasks", methods=["GET"])
def get_tasks():
    """獲取所有任務"""
    try:
        tasks = Task.get_all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks", methods=["POST"])
def add_task():
    """新增任務"""
    try:
        data = request.json
        
        # 創建新任務
        new_task = Task(
            stage=data.get("stage"),
            milestone=data.get("milestone"),
            start_date=data.get("startDate"),
            end_date=data.get("endDate"),
            content=data.get("description"),
            holiday_impact=data.get("holidayImpact"),
            dependencies=data.get("dependencies"),
            responsible=data.get("responsible"),
            risks=data.get("risks")
        )
        
        # 保存任務
        saved_task = new_task.save()
        if saved_task:
            return jsonify(saved_task.to_dict()), 201
        else:
            return jsonify({"error": "Failed to create task"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """更新任務"""
    try:
        # 獲取現有任務
        task = Task.get_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        data = request.json
        
        # 更新任務資料
        task.stage = data.get("stage", task.stage)
        task.milestone = data.get("milestone", task.milestone)
        task.start_date = data.get("startDate", task.start_date)
        task.end_date = data.get("endDate", task.end_date)
        task.content = data.get("description", task.content)
        task.holiday_impact = data.get("holidayImpact", task.holiday_impact)
        task.dependencies = data.get("dependencies", task.dependencies)
        task.responsible = data.get("responsible", task.responsible)
        task.risks = data.get("risks", task.risks)
        task.completed = data.get("completed", task.completed)
        
        # 保存更新
        updated_task = task.save()
        return jsonify(updated_task.to_dict())
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks/<int:task_id>/toggle-complete", methods=["PUT"])
def toggle_task_complete(task_id):
    """切換任務完成狀態"""
    try:
        # 獲取現有任務
        task = Task.get_by_id(task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        # 切換完成狀態
        task.completed = not task.completed
        
        # 保存更新
        updated_task = task.save()
        return jsonify(updated_task.to_dict())
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """刪除任務"""
    try:
        # 嘗試刪除任務
        success = Task.delete_by_id(task_id)
        if success:
            return jsonify({"message": "Task deleted successfully"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/tasks/batch-delete", methods=["DELETE"])
def batch_delete_tasks():
    """批量刪除任務"""
    try:
        data = request.json
        task_ids = data.get("taskIds", [])
        
        if not task_ids:
            return jsonify({"error": "No task IDs provided"}), 400
        
        deleted_count = 0
        errors = []
        
        for task_id in task_ids:
            try:
                success = Task.delete_by_id(task_id)
                if success:
                    deleted_count += 1
                else:
                    errors.append(f"Task {task_id} not found")
            except Exception as e:
                errors.append(f"Error deleting task {task_id}: {str(e)}")
        
        result = {
            "message": f"Successfully deleted {deleted_count} tasks",
            "deleted_count": deleted_count,
            "total_requested": len(task_ids)
        }
        
        if errors:
            result["errors"] = errors
        
        return jsonify(result), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route("/import-data", methods=["POST", "GET"])
def import_data():
    """匯入Excel資料到資料庫"""
    try:
        # 找到 excel_data.json 檔案
        json_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'excel_data.json')
        
        if not os.path.exists(json_file):
            return jsonify({"error": f"找不到資料檔案: {json_file}"}), 404
        
        # 讀取JSON資料
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 清空現有資料（可選）
        # Task.delete_all()  # 如果需要清空現有資料，取消註解這行
        
        migrated_count = 0
        errors = []
        
        for item in data:
            try:
                # 創建新任務
                task = Task(
                    stage=item.get('階段', ''),
                    milestone=item.get('里程碑', ''),
                    start_date=item.get('開始日', ''),  # 修正欄位名稱
                    end_date=item.get('結束日', ''),    # 修正欄位名稱
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
                else:
                    errors.append(f"保存失敗: {task.milestone}")
                    
            except Exception as e:
                errors.append(f"處理錯誤: {item.get('里程碑', 'Unknown')} - {str(e)}")
        
        # 返回結果
        result = {
            "message": f"資料匯入完成！成功匯入 {migrated_count} 筆資料",
            "imported_count": migrated_count,
            "total_count": len(data),
            "errors": errors
        }
        
        if errors:
            result["warning"] = f"有 {len(errors)} 筆資料匯入時發生錯誤"
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"匯入失敗: {str(e)}"}), 500

