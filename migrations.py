#!/usr/bin/env python3
"""
数据库迁移/维护脚本
"""
from app import create_app
from app.models import db, User, AuditLog

def show_database_status():
    """显示数据库状态"""
    app = create_app()
    
    with app.app_context():
        print("📊 数据库状态报告")
        print("=" * 40)
        
        # 表信息
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📁 数据表数量: {len(tables)}")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"   {table}: {len(columns)} 个字段")
        
        # 用户统计
        user_count = User.query.count()
        print(f"👤 用户总数: {user_count}")
        
        # 审计日志统计
        log_count = AuditLog.query.count()
        print(f"📝 审计日志总数: {log_count}")
        
        # 显示用户列表
        print("\n👥 用户列表:")
        users = User.query.all()
        for user in users:
            logs_count = AuditLog.query.filter_by(user_id=user.id).count()
            print(f"   {user.username} ({user.email}) - 角色: {user.role} - 日志数: {logs_count}")

if __name__ == '__main__':
    show_database_status()
