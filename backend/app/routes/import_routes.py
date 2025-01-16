from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from app.services.import_service import ImportService

bp = Blueprint('import', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/import/daily', methods=['POST'])
def import_daily():
    """导入日常委托数据"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        result = ImportService.import_daily_transactions(filepath)
        
        # 删除临时文件
        os.remove(filepath)
        
        return jsonify(result)
    
    return jsonify({'error': '不支持的文件类型'}), 400

@bp.route('/import/fixed', methods=['POST'])
def import_fixed():
    """导入固收产品数据"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        result = ImportService.import_fixed_income(filepath)
        
        # 删除临时文件
        os.remove(filepath)
        
        return jsonify(result)
    
    return jsonify({'error': '不支持的文件类型'}), 400

@bp.route('/import/private', methods=['POST'])
def import_private():
    """导入私募产品数据"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        result = ImportService.import_private_fund(filepath)
        
        # 删除临时文件
        os.remove(filepath)
        
        return jsonify(result)
    
    return jsonify({'error': '不支持的文件类型'}), 400

@bp.route('/import/relations', methods=['POST'])
def import_relations():
    """导入客户关系数据"""
    if 'file' not in request.files:
        return jsonify({'error': '没有文件'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        result = ImportService.import_client_relations(filepath)
        
        # 删除临时文件
        os.remove(filepath)
        
        return jsonify(result)
    
    return jsonify({'error': '不支持的文件类型'}), 400 