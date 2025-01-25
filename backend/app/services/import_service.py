from datetime import datetime
import pandas as pd
from app import db
from app.models.transaction import Transaction
from app.models.manager import Manager
from app.models.client_relation import ClientRelation
from app.models.adjustment import Adjustment
from app.models.fixed_income import FixedIncome
from app.models.private_fund import PrivateFund
from app.models.product import Product
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
                '产品代码': str,
                '流水号': str
            })
            
            # 重命名列
            df.columns = [
                'date', 'stock', 'stock_name', 'name',
                'no', 'quantity', 'price', 'money', 'account',
                'serial_no'
            ]
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            transactions = []
            update_count = 0
            insert_count = 0
            
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                
                # 查找是否存在相同流水号的记录
                existing = Transaction.query.filter_by(
                    serial_no=row['serial_no']
                ).first() if row['serial_no'] else None
                
                if existing:
                    if row['撤单'] == '撤单':
                        # 如果是撤单,删除记录
                        db.session.delete(existing)
                        update_count += 1
                    else:
                        # 更新已存在的记录
                        existing.date = row['date']
                        existing.account = row['account']
                        existing.product_code = row['stock']
                        existing.product_name = row['stock_name']
                        existing.manager_id = managers[row['name']]
                        existing.amount = row['money']
                        update_count += 1
                else:
                    # 创建新记录
                    trans = Transaction(
                        date=row['date'],
                        account=row['account'],
                        product_code=row['stock'],
                        product_name=row['stock_name'],
                        manager_id=managers[row['name']],
                        amount=row['money'],
                        serial_no=row['serial_no']
                    )
                    transactions.append(trans)
                    insert_count += 1
            
            # 批量插入新数据
            if transactions:
                db.session.bulk_save_objects(transactions)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'total': update_count + insert_count,
                'updated': update_count,
                'inserted': insert_count,
                'message': f'成功更新{update_count}条、新增{insert_count}条交易记录'
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
                '客户代码': str,
                '申请编号': str
            })
            
            # 重命名列
            df.columns = ['date', 'no', 'account', 'name', 'amount']
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 生成流水号
            df['serial_no'] = df.apply(
                lambda x: f"GS_{x['date']}_{x['no']}", axis=1
            )
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            records = []
            update_count = 0
            insert_count = 0
            
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                
                # 查找是否存在相同流水号的记录
                existing = FixedIncome.query.filter_by(
                    serial_no=row['serial_no']
                ).first() if row['serial_no'] else None
                
                if existing:
                    # 更新已存在的记录
                    existing.date = row['date']
                    existing.no = row['no']
                    existing.account = row['account']
                    existing.manager_id = managers[row['name']]
                    existing.amount = row['amount']
                    update_count += 1
                else:
                    # 创建新记录
                    record = FixedIncome(
                        date=row['date'],
                        no=row['no'],
                        account=row['account'],
                        manager_id=managers[row['name']],
                        amount=row['amount'],
                        serial_no=row['serial_no']
                    )
                    records.append(record)
                    insert_count += 1
            
            # 批量插入新数据
            if records:
                db.session.bulk_save_objects(records)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'total': update_count + insert_count,
                'updated': update_count,
                'inserted': insert_count,
                'message': f'成功更新{update_count}条、新增{insert_count}条固收记录'
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
            df = pd.read_excel(file_path, dtype={
                '日期': str,
                '账号': str,
                '产品代码': str,
                '申请编号': str
            })
            
            # 重命名列
            df.columns = [
                'date', 'account', 'product_code', 'product_name',
                'name', 'amount', 'no'
            ]
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 生成流水号
            df['serial_no'] = df.apply(
                lambda x: f"SM_{x['date']}_{x['no']}", axis=1
            )
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 获取所有产品
            products = {p.code: p.id for p in Product.query.all()}
            
            # 准备批量插入的数据
            records = []
            update_count = 0
            insert_count = 0
            
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                
                # 查找是否存在相同流水号的记录
                existing = PrivateFund.query.filter_by(
                    serial_no=row['serial_no']
                ).first() if row['serial_no'] else None
                
                if existing:
                    # 更新已存在的记录
                    existing.date = row['date']
                    existing.account = row['account']
                    existing.product_code = row['product_code']
                    existing.product_name = row['product_name']
                    existing.manager_id = managers[row['name']]
                    existing.amount = row['amount']
                    existing.product_id = products.get(row['product_code'])
                    update_count += 1
                else:
                    # 创建新记录
                    record = PrivateFund(
                        date=row['date'],
                        account=row['account'],
                        product_code=row['product_code'],
                        product_name=row['product_name'],
                        manager_id=managers[row['name']],
                        amount=row['amount'],
                        serial_no=row['serial_no'],
                        product_id=products.get(row['product_code'])
                    )
                    records.append(record)
                    insert_count += 1
            
            # 批量插入新数据
            if records:
                db.session.bulk_save_objects(records)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'total': update_count + insert_count,
                'updated': update_count,
                'inserted': insert_count,
                'message': f'成功更新{update_count}条、新增{insert_count}条私募记录'
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
            # 读取Excel文件
            df = pd.read_excel(file_path, dtype={
                'account': str,
                'serial_no': str
            })
            df.columns = ['account', 'name', 'fenchen', 'serial_no']
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            relations = []
            update_count = 0
            insert_count = 0
            
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                
                # 查找是否存在相同流水号的记录
                existing = ClientRelation.query.filter_by(
                    serial_no=row['serial_no']
                ).first() if row['serial_no'] else None
                
                # 如果没有找到相同流水号的记录,尝试通过账号查找
                if not existing:
                    existing = ClientRelation.query.filter_by(
                        account=row['account']
                    ).first()
                
                if existing:
                    # 更新已存在的记录
                    existing.account = row['account']
                    existing.manager_id = managers[row['name']]
                    existing.fenchen = row['fenchen']
                    existing.serial_no = row['serial_no']
                    update_count += 1
                else:
                    # 创建新记录
                    relation = ClientRelation(
                        account=row['account'],
                        manager_id=managers[row['name']],
                        fenchen=row['fenchen'],
                        serial_no=row['serial_no']
                    )
                    relations.append(relation)
                    insert_count += 1
            
            # 批量插入新数据
            if relations:
                db.session.bulk_save_objects(relations)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'total': update_count + insert_count,
                'updated': update_count,
                'inserted': insert_count,
                'message': f'成功更新{update_count}条、新增{insert_count}条客户关系'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': str(e)
            }

    @staticmethod
    def import_adjustments(file_path: str) -> Dict:
        """
        导入调整数据
        
        Args:
            file_path: Excel文件路径
            
        Returns:
            Dict: 导入结果统计
        """
        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, dtype={
                '日期': str,
                '账号': str,
                '产品代码': str,
                '流水号': str  # 添加流水号列
            })
            
            # 重命名列
            df.columns = [
                'date', 'account', 'product_code', 'product_name',
                'name', 'amount', 'reason', 'remark', 'serial_no'
            ]
            
            # 转换日期格式
            df['date'] = pd.to_datetime(df['date']).dt.date
            
            # 获取所有客户经理
            managers = {m.name: m.id for m in Manager.query.all()}
            
            # 准备批量插入的数据
            adjustments = []
            update_count = 0
            insert_count = 0
            
            for _, row in df.iterrows():
                if row['name'] not in managers:
                    continue
                
                # 查找是否存在相同流水号的记录
                existing = Adjustment.query.filter_by(
                    serial_no=row['serial_no']
                ).first() if row['serial_no'] else None
                
                if existing:
                    # 更新已存在的记录
                    existing.date = row['date']
                    existing.account = row['account']
                    existing.product_code = row['product_code']
                    existing.product_name = row['product_name']
                    existing.manager_id = managers[row['name']]
                    existing.amount = row['amount']
                    existing.reason = row['reason']
                    existing.remark = row['remark']
                    update_count += 1
                else:
                    # 创建新记录
                    adj = Adjustment(
                        date=row['date'],
                        account=row['account'],
                        product_code=row['product_code'],
                        product_name=row['product_name'],
                        manager_id=managers[row['name']],
                        amount=row['amount'],
                        reason=row['reason'],
                        remark=row['remark'],
                        serial_no=row['serial_no']
                    )
                    adjustments.append(adj)
                    insert_count += 1
            
            # 批量插入新数据
            if adjustments:
                db.session.bulk_save_objects(adjustments)
            
            db.session.commit()
            
            return {
                'status': 'success',
                'total': update_count + insert_count,
                'updated': update_count,
                'inserted': insert_count,
                'message': f'成功更新{update_count}条、新增{insert_count}条调整记录'
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'status': 'error',
                'message': str(e)
            } 