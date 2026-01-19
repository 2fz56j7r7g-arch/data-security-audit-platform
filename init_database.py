#!/usr/bin/env python3
"""
数据库初始化脚本（修正版）
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, User, AuditLog

def init_database():
    """初始化数据库"""
    app = create_app()
    
    with app.app_context():
        print("📊 检查数据库状态...")
        
        # 检查现有表
        inspector = db.inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if existing_tables:
            print(f"📊 数据库已存在 {len(existing_tables)} 张表")
            print(f"   现有表: {', '.join(existing_tables)}")
            
            # 检查是否有用户数据
            try:
                user_count = User.query.count()
                print(f"👤 现有用户数: {user_count}")
                
                if user_count > 0:
                    print("⚠️  数据库已有数据，跳过初始化")
                    return
            except:
                print("⚠️  查询用户表失败，继续初始化...")
        
        # 创建所有表
        print("🔄 创建数据表...")
        db.create_all()
        print("✅ 数据表创建成功！")
        
        # 创建默认用户
        print("👤 创建默认用户...")
        
        default_users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'role': 'admin',
                'password': 'Admin123!'
            },
            {
                'username': 'auditor', 
                'email': 'auditor@example.com',
                'role': 'auditor',
                'password': 'Auditor123!'
            },
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'role': 'user',
                'password': 'User123!'
            }
        ]
        
        for user_data in default_users:
            # 检查用户是否已存在
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user:
                print(f"   ⚠️  用户 {user_data['username']} 已存在，跳过")
                continue
            
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
            print(f"   ✅ 创建用户: {user_data['username']} ({user_data['role']})")
        
        db.session.commit()
        print("✅ 默认用户创建完成！")
        
        # 验证
        users = User.query.all()
        print(f"📋 当前用户总数: {len(users)}")
        for user in users:
            print(f"   - {user.username} ({user.email}) - 角色: {user.role}")

if __name__ == '__main__':
    init_database()
