from app import db
from .manager import Manager, ManagerGroup
from .product import Product, ProductGroup, GroupTarget
from .transaction import Transaction
from .client_relation import ClientRelation
from .adjustment import Adjustment
from .fixed_income import FixedIncome
from .private_fund import PrivateFund

def init_db():
    db.create_all()

def drop_db():
    db.drop_all() 