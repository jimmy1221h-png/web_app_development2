# 流程圖設計 (FLOWCHART)

這份文件基於 PRD 與 ARCHITECTURE 的規劃，視覺化了個人記帳簿系統的「使用者操作路徑」與「資料處理流程」，確保在實作前釐清所有的步驟與邏輯。

## 1. 使用者流程圖 (User Flow)

這張圖描述了使用者進入網站後，可以進行的各種操作路徑：

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁<br/>收支列表與當月統計]
    B --> C{要執行什麼操作？}
    
    C -->|點擊「新增」| D[填寫新增收支表單]
    D --> E{送出表單}
    E -->|驗證成功| B
    E -->|驗證失敗| D
    
    C -->|點選某筆「編輯」| F[填寫編輯收支表單]
    F --> G{送出修改}
    G -->|成功| B
    G -->|失敗| F
    
    C -->|點選某筆「刪除」| H{跳出確認視窗}
    H -->|確認刪除| B
    H -->|取消| B
```

## 2. 系統序列圖 (Sequence Diagram)

以下以最核心的「新增一筆收支」為例，展示前端瀏覽器、後端 Flask 控制器以及 SQLite 資料庫之間的互動流程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Controller
    participant DB as SQLite 資料庫

    User->>Browser: 填寫「新增收支」表單並送出
    Browser->>Flask: POST /record/add (表單資料)
    
    Flask->>Flask: 驗證欄位 (金額是否為數字、必填是否填寫等)
    
    alt 資料驗證成功
        Flask->>DB: INSERT INTO records (儲存資料)
        DB-->>Flask: 回傳成功
        Flask-->>Browser: HTTP 302 重導向至首頁 (/)
        
        Note over Browser, DB: 重新讀取首頁資料
        Browser->>Flask: GET /
        Flask->>DB: SELECT * FROM records (取得最新列表)
        DB-->>Flask: 回傳紀錄清單
        Flask-->>Browser: 渲染 index.html 並顯示成功提示
    else 資料驗證失敗
        Flask-->>Browser: 重新渲染 form.html 並顯示錯誤提示
    end
```

## 3. 功能清單對照表

這是後續實作 API 與路由 (Routes) 時的重要參考表：

| 功能名稱 | 描述 | URL 路由路徑 | HTTP 方法 |
| --- | --- | --- | --- |
| 檢視首頁 | 顯示全部收支列表與當月的總計資訊 | `/` | `GET` |
| 顯示新增表單 | 呈現新增收支的空白填寫頁面 | `/record/add` | `GET` |
| 處理新增資料 | 接收表單提交，驗證並寫入資料庫 | `/record/add` | `POST` |
| 顯示編輯表單 | 帶入舊有資料，呈現編輯頁面 | `/record/edit/<int:id>` | `GET` |
| 處理編輯資料 | 接收表單提交，驗證並更新該筆紀錄 | `/record/edit/<int:id>` | `POST` |
| 處理刪除要求 | 將指定的收支紀錄從資料庫中移除 | `/record/delete/<int:id>` | `POST` |
