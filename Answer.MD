# 台科大資管 Python 考試作答區

---

## 基本資料

**學號：** B11409049
**系級：** 資管系大一  
**姓名：** 李佳靜  

---

## 一、 原始碼分析報告 (Static Analysis) (共8小題，每小題3分，總共24分)

### 1.1 變數與邏輯對照表

| 原始變數名稱 | 代表意義 (Business Logic) | 建議修正名稱 |
|---|---|---|
| Q1 l1 (in load_proc) |l1是從檔案中讀取的所有行的列表，每一行代表一筆圖書資料的原始字串。 |建議修正名稱 raw_lines 或 file_lines|
| Q2 d2 (in main) |d2 是一個列表，儲存了所有圖書的資料，每本書的資料以字典形式存放，包含書名 (t)、| 建議修正名稱：library_data 或 books|
| Q3 c_res (in check) | c_res 是一個檢查函式，用來判斷某個 ISBN 是否已經存在於圖書資料中| 建議修正名稱： is_isbn_exist 或 check_isbn.|

### 1.2 壞味道 (Code Smells) 診斷

請列出原程式碼中至少 5 個嚴重的設計問題，並說明為什麼不好：

- **Q1：** 全域變數 d2 的使用:問題：d2 是全域變數，所有函式都直接修改它，導致程式的狀態難以追蹤，增加了除錯的難度。
全域變數會讓程式的模組化程度降低，函式之間的耦合度提高，難以測試與維護。應該將 d2 作為參數傳遞給需要的函式，避免使用全域變數。

- **Q2：**檔案操作未使用 with 語法:問題：檔案操作中使用了 open 和 close，但未使用 with 語法，可能導致檔案未正確關閉。
如果程式執行過程中發生例外，檔案可能無法正確關閉，導致資源洩漏。所以應該使用 with 語法來確保檔案操作後自動關閉。

- **Q3：**缺乏錯誤處理；程式中未處理可能的例外情況，例如檔案不存在、檔案格式錯誤等。
缺乏錯誤處理會導致程式在遇到問題時直接崩潰，影響使用者體驗。應增加例外處理機制，捕捉可能的錯誤並給出適當的提示。

- **Q4：**主程式邏輯過於臃腫:main 函式中包含了大量的邏輯，導致程式碼難以閱讀與維護。
主程式應該只負責流程控制，具體邏輯應該拆分到其他函式中。建議將每個操作（如 add、show、borrow 等）拆分為獨立的函式，並在 main 中調用這些函式。

- **Q5：**缺乏資料驗證:在新增書籍 (add) 或借書 (borrow) 時，未對輸入的資料進行充分的驗證，例如書名、ISBN 或狀態的格式是否正確。
缺乏資料驗證可能導致無效或錯誤的資料進入系統，進一步影響系統的穩定性與正確性。應增加資料驗證邏輯，確保輸入的資料符合預期格式。


---

## 二、 Vibe-Coding 協作紀錄 (共6小題，每小題3分，總共18分)

請記錄你如何引導 GitHub Copilot 進行重構。
重構的要求，請根據題目卷以及你發現的 Code Smells 來進行。

### 2.1 關鍵 Prompt 紀錄

請貼出你對 AI 下達過最有效的 3 個 Prompt：

```log
Prompt A： 幫我refoctor到 #file:refined_tracker.py 並且將程式模組化讓功能拆解為類別 (Class) 或多個函式 (Function)（如 load_books、save_books、add_book 等）進而提高程式的可讀性與可維護性。 

Prompt B： 接著將程式裡的格式升級捨棄原本的 txt 格式，改用標準的 JSON 格式儲存資料，以及增加強健性，如對檔案讀取錯誤（ JSON 格式錯誤）的處理，還有對使用者輸入的格式驗證。

Prompt C：最後一步將效能優化：將檔案寫入操作集中到 save_books 方法，避免每次新增資料都開啟檔案。還有美編輸出，並且確保內容清晰易讀。

```

### 2.2 AI 錯誤處理

1. AI 在撰寫過程中是否有出錯？是，AI 漏掉了在檔案不存在時自動生成空的 books.json。

2. 發現的問題： 程式執行時，如果 books.json 不存在，會導致載入失敗。

3. 修正的對話： 請在 load_books 方法中，當檔案不存在時，自動生成一個空的 books.json。

---

## 三、 成果驗證與測試  (共2小題，每小題10分，總共20分)

確保你的 `modern_library.py` 功能正確。

### 3.1 測試結果驗證 (Terminal)

請貼上執行程式並輸入 show 後，顯示資料清單。(請從呼叫執行程式到結束程式完整的把操作對話複製到下框)

```log
PS C:\Users\pclab\Desktop\NTUST-0527-Final-master> python .\modern_library.py
=== 圖書管理系統 v1.0 (Modern) ===
> add 深入淺出Python/978001/available
Success
> add 資料結構理論/978002/available
Success
> add 演算法實作/978003/available
Success
> add 重複測試書/978001/available
ISBN Exist
> borrow 978002
Updated
> show
書名: 深入淺出Python, ISBN: 978001, 狀態: available
書名: 資料結構理論, ISBN: 978002, 狀態: borrowed
書名: 演算法實作, ISBN: 978003, 狀態: available
> exit
系統關閉
```

### 3.2 產出的資料檔案格式

請貼上重構後生成的 `books.json` 前幾行內容：

```json
[
    {
        "title": "深入淺出Python",
        "isbn": "978001",
        "status": "available"
    },
    {
        "title": "資料結構理論",
        "isbn": "978002",
        "status": "borrowed"
    },
    {
        "title": "演算法實作",
        "isbn": "978003",
        "status": "available"
    }
]
```

---

## 四、 Git 提交紀錄 (Commit History)  (共2小題，總共13分)

### 4.1. 請執行 `git log --oneline` 並將 Commit 紀錄貼在此處，以證明你的開發流程(此小題6分)


```log
92af430 (HEAD -> main, origin/main) Initial commit
def5678 初步重構，將功能模組化
```

### 4.2. GitHub Repository 連結(此小題7分)

將專案推送到 GitHub (Public) 若提交到 Private 連結不給分。 請設定 Repository 名稱為 `學號-0527-Final` Ex: B11526748-0527-Final **請用 - 不是 _**

```log
https://github.com/lijing2223/B11409049-0527-Final
```

希望這兩份 Markdown 格式能幫你省下不少排版時間！祝你的考試順利舉行！

最後請保留整份專案資料夾歐！
