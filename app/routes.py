"""
個人記帳簿 - 路由設計骨架
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
# 預計匯入的 Model，例如：from .models import db, Record

# 依據架構設計，使用 Blueprint 來集中管理路由
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    [GET] 檢視首頁
    - 取得所有的收支紀錄列表
    - 計算當月的總支出與總收入
    - 渲染 index.html
    """
    pass

@main_bp.route('/record/add', methods=['GET', 'POST'])
def add_record():
    """
    [GET] 顯示新增收支的表單頁面
    [POST] 接收表單資料，驗證後新增至資料庫
    - 若成功：重導向至首頁
    - 若失敗：重新渲染 form.html 顯示錯誤訊息
    """
    pass

@main_bp.route('/record/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    """
    [GET] 根據 id 查詢該筆紀錄，並顯示編輯表單頁面
    [POST] 接收表單資料，驗證後更新資料庫中該筆紀錄
    - 若成功：重導向至首頁
    - 若失敗 (如查無 id)：重導向至首頁或報錯
    """
    pass

@main_bp.route('/record/delete/<int:id>', methods=['POST'])
def delete_record(id):
    """
    [POST] 刪除指定 id 的收支紀錄
    - 執行刪除後重導向至首頁
    """
    pass
