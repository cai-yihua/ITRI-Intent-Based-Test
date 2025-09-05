# ITRI-Intent-Based-Test

## 專案簡介
本專案基於 ITRI-Intent-Based 意圖網管系統，目的為測試意圖網管系統能否正常執行各項功能。

## 測試說明與前提
本測試基於意圖網管系統進行測試，測試前須確保：
1. 意圖網管系統需存在
2. 測試環境為 Windows

## 目錄結構（摘要）
```
Intent-Based-Test-Report/
│
├── .venv/              # 虛擬環境
│
├── Code/               # 測試程式碼與依賴
│   ├── Intent-Based-Test-Report.py
│   ├── requirements.txt
│   ├── chromedriver.exe
│   └── .env
│
├── Log/                # 測試報告輸出 (範例結果)
│   ├── log.html
│   └── ...
│
└── report/             # 測試報告輸出 (執行測試後的測試報告)
    └── report_YYYYMMDD_hhmmss
```

## 設置測試環境
### 拉取ITRI-Intent-Based&-Test環境設定&安裝套件
```bash
git clone https://github.com/cai-yihua/ITRI-Intent-Based-Test.git
cd ITRI-Intent-Based-Test
```

### 切換專案版本
```bash
git tag
git checkout <tag>
```

### 環境設定&安裝套件
```bash
python -m venv .venv
.venv\Scripts\activate

cd .\Code\

python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install -r requirements.txt
```

### 創建 .env
```bash
New-Item .env -ItemType File
```

## 執行測試腳本
```bash
python .\Intent-Based-Test-Report.py
```