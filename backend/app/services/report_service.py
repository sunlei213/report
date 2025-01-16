from datetime import datetime
from sqlalchemy import func, and_
from decimal import Decimal
from app.models.transaction import Transaction
from app.models.adjustment import Adjustment  # 添加调整数据模型
from app.models.manager import Manager
from app.models.product import Product, ProductGroup, GroupTarget
from app.models.client_relation import ClientRelation

class ReportService:
    @staticmethod
    def generate_monthly_report(month):
        """生成月度报表"""
        year = int(month[:4])
        month_num = int(month[4:])
        start_date = datetime(year, month_num, 1)
        if month_num == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month_num + 1, 1)

        # 获取所有客户经理(按组和排序)
        managers = Manager.query.order_by(Manager.group_id, Manager.order).all()
        
        # 获取所有产品组(按排序)
        product_groups = ProductGroup.query.order_by(ProductGroup.order).all()
        
        # 获取分成关系
        fenchen_map = {r.account: r.fenchen for r in ClientRelation.query.all()}

        # 构建产品代码到产品组的映射
        product_group_map = {}
        for group in product_groups:
            for product in group.products:
                product_group_map[product.code] = group.id

        # 准备报表数据
        daily_data = []
        key_data = []
        total_stats = {}  # 合计数据

        # 初始化合计数据
        for group in product_groups:
            total_stats[group.id] = {
                'amount': Decimal('0'),
                'count': set(),  # 使用集合存储账号,避免重复
                'target': Decimal('0')
            }

        for manager in managers:
            # 获取该客户经理的所有交易和调整数据
            transactions = Transaction.query\
                .filter(and_(
                    Transaction.manager_id == manager.id,
                    Transaction.date >= start_date,
                    Transaction.date < end_date
                ))\
                .all()
                
            adjustments = Adjustment.query\
                .filter(and_(
                    Adjustment.manager_id == manager.id,
                    Adjustment.date >= start_date,
                    Adjustment.date < end_date
                ))\
                .all()

            # 按产品组统计数据
            group_stats = {}
            for group in product_groups:
                group_stats[group.id] = {
                    'amount': Decimal('0'),
                    'count': set(),  # 使用集合存储账号
                    'target': Decimal('0'),
                    'adjustment': Decimal('0')  # 添加调整金额统计
                }

            # 获取目标
            targets = GroupTarget.query\
                .filter(and_(
                    GroupTarget.manager_id == manager.id,
                    GroupTarget.year == year
                ))\
                .all()
            
            for target in targets:
                group_stats[target.product_group_id]['target'] = target.target
                total_stats[target.product_group_id]['target'] += target.target

            # 统计交易数据
            account_amounts = {}  # 按账号和产品组累计金额
            for tx in transactions:
                # 查找产品所属组
                group_id = None
                if tx.product_id and tx.product:
                    group_id = tx.product.group_id
                elif tx.product_code in product_group_map:
                    group_id = product_group_map[tx.product_code]
                
                if group_id:
                    # 计算分成后金额
                    fenchen = fenchen_map.get(tx.account, Decimal('1'))
                    amount = tx.amount * fenchen
                    
                    # 累计金额
                    key = (tx.account, group_id)
                    if key not in account_amounts:
                        account_amounts[key] = Decimal('0')
                    account_amounts[key] += amount
                    
                    # 更新统计数据
                    group_stats[group_id]['amount'] += amount
                    total_stats[group_id]['amount'] += amount

            # 统计调整数据
            for adj in adjustments:
                # 查找产品所属组
                group_id = None
                if adj.product_id and adj.product:
                    group_id = adj.product.group_id
                elif adj.product_code in product_group_map:
                    group_id = product_group_map[adj.product_code]
                
                if group_id:
                    # 计算分成后金额
                    fenchen = fenchen_map.get(adj.account, Decimal('1'))
                    amount = adj.amount * fenchen
                    
                    # 累计调整金额
                    group_stats[group_id]['adjustment'] += amount
                    total_stats[group_id]['adjustment'] += amount
                    
                    # 更新总金额
                    group_stats[group_id]['amount'] += amount
                    total_stats[group_id]['amount'] += amount
                    
                    # 如果是正向调整,也要计入户数统计
                    if amount > 0:
                        key = (adj.account, group_id)
                        if key not in account_amounts:
                            account_amounts[key] = Decimal('0')
                        account_amounts[key] += amount

            # 统计有效户数
            for (account, group_id), amount in account_amounts.items():
                min_amount = Decimal('0')
                # 查找该组下所有产品的最小金额
                for product in product_groups[group_id].products:
                    if product.min_amount > min_amount:
                        min_amount = product.min_amount
                
                if amount >= min_amount:
                    group_stats[group_id]['count'].add(account)
                    total_stats[group_id]['count'].add(account)

            # 生成报表行
            row = {
                '客户经理': manager.name,
                '所属组': manager.group.name
            }
            
            # 添加各产品组的数据
            for group in product_groups:
                stats = group_stats[group.id]
                prefix = group.name
                row[f'{prefix}金额'] = float(stats['amount'])
                row[f'{prefix}调整'] = float(stats['adjustment'])  # 添加调整金额列
                row[f'{prefix}户数'] = len(stats['count'])
                if stats['target'] > 0:
                    row[f'{prefix}完成率'] = float(stats['amount'] / stats['target'])
                else:
                    row[f'{prefix}完成率'] = 0

            # 根据金额判断是否为重点数据
            is_key = any(stats['amount'] >= 10000000 for stats in group_stats.values())
            if is_key:
                key_data.append(row)
            daily_data.append(row)

        # 添加合计行
        total_row = {
            '客户经理': '合计',
            '所属组': ''
        }
        
        for group in product_groups:
            stats = total_stats[group.id]
            prefix = group.name
            total_row[f'{prefix}金额'] = float(stats['amount'])
            total_row[f'{prefix}调整'] = float(stats['adjustment'])  # 添加调整金额列
            total_row[f'{prefix}户数'] = len(stats['count'])
            if stats['target'] > 0:
                total_row[f'{prefix}完成率'] = float(stats['amount'] / stats['target'])
            else:
                total_row[f'{prefix}完成率'] = 0

        daily_data.append(total_row)
        if key_data:
            key_data.append(total_row)

        # 构建表头
        headers = ['客户经理', '所属组']
        for group in product_groups:
            prefix = group.name
            headers.extend([
                f'{prefix}金额',
                f'{prefix}调整',  # 添加调整金额列
                f'{prefix}户数',
                f'{prefix}完成率'
            ])

        return {
            'daily': {
                'headers': headers,
                'rows': daily_data
            },
            'key': {
                'headers': headers,
                'rows': key_data
            }
        } 