DROP TABLE IF EXISTS records;

CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL, -- 'income' (收入) 或是 'expense' (支出)
    amount INTEGER NOT NULL,
    date TEXT NOT NULL, -- 格式: YYYY-MM-DD
    category TEXT NOT NULL,
    note TEXT
);
