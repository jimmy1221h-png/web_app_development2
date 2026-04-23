"""
個人記帳簿 - 路由設計實作
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Record

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    [GET] 檢視首頁
    - 取得所有的收支紀錄列表
    - 計算當月的總支出與總收入
    - 渲染 index.html
    """
    records = Record.get_all()
    
    # 為了簡化 MVP，這裡直接計算所有記錄的總計。若資料量大，建議在 Model 層用語法 (如 SUM) 處理。
    total_income = sum(r['amount'] for r in records if r['type'] == 'income')
    total_expense = sum(r['amount'] for r in records if r['type'] == 'expense')
    
    return render_template('index.html', records=records, total_income=total_income, total_expense=total_expense)

@main_bp.route('/record/add', methods=['GET', 'POST'])
def add_record():
    """
    [GET] 顯示新增收支的表單頁面
    [POST] 接收表單資料，驗證後新增至資料庫
    """
    if request.method == 'POST':
        data = {
            'type': request.form.get('type'),
            'amount': request.form.get('amount'),
            'date': request.form.get('date'),
            'category': request.form.get('category'),
            'note': request.form.get('note')
        }
        
        # 必填欄位驗證
        if not data['type'] or not data['amount'] or not data['date'] or not data['category']:
            flash('請填寫所有必填欄位 (收支類型、金額、日期、分類)', 'error')
            return render_template('form.html', record=data, is_edit=False)
            
        # 金額格式驗證
        try:
            data['amount'] = int(data['amount'])
            if data['amount'] <= 0:
                raise ValueError
        except ValueError:
            flash('金額必須是大於零的整數', 'error')
            return render_template('form.html', record=data, is_edit=False)
            
        # 寫入資料庫
        if Record.create(data):
            flash('收支紀錄新增成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('系統發生錯誤，新增失敗，請稍後再試', 'error')
            return render_template('form.html', record=data, is_edit=False)

    return render_template('form.html', is_edit=False)

@main_bp.route('/record/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    """
    [GET] 根據 id 查詢該筆紀錄，並顯示編輯表單頁面
    [POST] 接收表單資料，驗證後更新資料庫中該筆紀錄
    """
    record = Record.get_by_id(id)
    
    if not record:
        flash('找不到該筆紀錄！', 'error')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        data = {
            'type': request.form.get('type'),
            'amount': request.form.get('amount'),
            'date': request.form.get('date'),
            'category': request.form.get('category'),
            'note': request.form.get('note')
        }
        
        if not data['type'] or not data['amount'] or not data['date'] or not data['category']:
            flash('請填寫所有必填欄位', 'error')
            data['id'] = id
            return render_template('form.html', record=data, is_edit=True)
            
        try:
            data['amount'] = int(data['amount'])
            if data['amount'] <= 0:
                raise ValueError
        except ValueError:
            flash('金額必須是大於零的整數', 'error')
            data['id'] = id
            return render_template('form.html', record=data, is_edit=True)
            
        if Record.update(id, data):
            flash('收支紀錄更新成功！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('系統發生錯誤，更新失敗，請稍後再試', 'error')
            data['id'] = id
            return render_template('form.html', record=data, is_edit=True)

    return render_template('form.html', record=record, is_edit=True)

@main_bp.route('/record/delete/<int:id>', methods=['POST'])
def delete_record(id):
    """
    [POST] 刪除指定 id 的收支紀錄
    """
    if Record.delete(id):
        flash('紀錄已成功刪除', 'success')
    else:
        flash('刪除失敗，請稍後再試', 'error')
        
    return redirect(url_for('main.index'))
