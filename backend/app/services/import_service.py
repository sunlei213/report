from datetime import datetime
import pandas as pd
from app import db
from app.models.transaction import Transaction
from app.models.manager import Manager
from app.models.client_relation import ClientRelation
from typing import List, Dict

class ImportService:
    """数据导入服务"""
    
    @staticmethod
    def import_daily_transactions(file_path: str) -> Dict:
        """
        导入日常委托数据
        
        Args:
            file_path: Excel文件路径
        
        Returns:
            Dict: 导入结果统计
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, dtype={
                '交易日期': str,
                '客户编号': str,
                '产品代码': str
            })
            
            # 重命名列
            df.columns = [
                'date', 'stock', 'stock_name', 'name',
                'no', 'quantity', 'price', 'money', 'account'
            ]
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            transactions = []
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                    
                trans = Transaction(
                    date=row['date'],
                    account=row['account'],
                    product_code=row['stock'],
                    manager_id=managers[row['name']],
                    amount=row['money'],
                    type='normal'
                )
                transactions.append(trans)
            
            # 批量插入数据
            db.session.bulk_save_objects(transactions)
            db.session.commit()
            
            return {
                'status': 'success',
                'total': len(transactions),
                'message': f'成功导入{len(transactions)}条交易记录'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': str(e)
            }

    @staticmethod
    def import_fixed_income(file_path: str) -> Dict:
        """
        导入固收产品数据
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            Dict: 导入结果统计
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, dtype={
                '申请日期': str,
                '客户代码': str
            })
            
            # 重命名列
            df.columns = ['date', 'no', 'account', 'name', 'money']
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            transactions = []
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                    
                trans = Transaction(
                    date=row['date'],
                    account=row['account'],
                    product_code='FIXED_INCOME', # 固定收益产品统一代码
                    manager_id=managers[row['name']],
                    amount=row['money'],
                    type='fixed'
                )
                transactions.append(trans)
            
            # 批量插入数据
            db.session.bulk_save_objects(transactions)
            db.session.commit()
            
            return {
                'status': 'success',
                'total': len(transactions),
                'message': f'成功导入{len(transactions)}条固收记录'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': str(e)
            }

    @staticmethod
    def import_private_fund(file_path: str) -> Dict:
        """
        导入私募产品数据
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            Dict: 导入结果统计
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path)
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            transactions = []
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                    
                trans = Transaction(
                    date=row['date'],
                    account=row['account'],
                    product_code=row['product_code'],
                    manager_id=managers[row['name']],
                    amount=row['amount'],
                    type='private'
                )
                transactions.append(trans)
            
            # 批量插入数据
            db.session.bulk_save_objects(transactions)
            db.session.commit()
            
            return {
                'status': 'success',
                'total': len(transactions),
                'message': f'成功导入{len(transactions)}条私募记录'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': str(e)
            }

    @staticmethod
    def import_client_relations(file_path: str) -> Dict:
        """
        导入客户关系数据
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            Dict: 导入结果统计
        """
        try:
            df = pd.read_excel(file_path, dtype={'account': str})
            df.columns = ['account', 'name', 'fenchen']
            
            managers = {m.name: m.id for m in Manager.query.all()}
            
            relations = []
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                    
                relation = ClientRelation(
                    account=row['account'],
                    manager_id=managers[row['name']],
                    fenchen=row['fenchen']
                )
                relations.append(relation)
            
            # 清除旧数据并插入新数据
            ClientRelation.query.delete()
            db.session.bulk_save_objects(relations)
            db.session.commit()
            
            return {
                'status': 'success',
                'total': len(relations),
                'message': f'成功更新{len(relations)}条客户关系'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': str(e)
            } 