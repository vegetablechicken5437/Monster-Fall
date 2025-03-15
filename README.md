# Monster Fall

**Monster Fall** 是一款使用 Pygame 開發的動作小遊戲。在遊戲中，你需要躲避隨機出現的怪物、收集加分道具，並挑戰自己刷新高分！

![](https://github.com/vegetablechicken5437/Monster-Fall/blob/main/monster_fall_demo.gif)

## 遊戲特色

- **流暢體驗：** 遊戲以 240 FPS 執行，提供順暢的操作感受。
- **動態障礙：** 隨機生成的怪物與加分物件讓每次遊戲都有不同的挑戰。
- **音效控制：** 畫面右上角有音量切換圖示，可方便地控制遊戲音效。
- **高分記錄：** 最高分記錄儲存在使用者的家目錄中，記錄檔名稱為 `.monster_fall_record.txt`，確保每次遊玩都能保存你的最佳成績。
- **完整資源：** 所有圖片與音樂資源均已包含，且遊戲可使用 PyInstaller 打包成獨立執行檔。

## 安裝與使用

### 前置需求

- Python 3.x  
- [Pygame](https://www.pygame.org/news)  

請先使用 pip 安裝 Pygame：
```
pip install pygame
```

### 下載專案
使用 Git Clone 下載專案：
```
git clone https://github.com/你的GitHub帳號/monster_fall.git
cd monster_fall
```

### 運行遊戲
在專案目錄下執行：
```
python monster_fall.py
```
遊戲將以視窗方式啟動，使用鍵盤操作角色，並利用畫面上的按鈕來控制遊戲流程及音量開關。

## 打包成執行檔
如果你希望讓其他使用者不需要額外安裝 Python 或 Pygame，即可直接執行遊戲，可使用 PyInstaller 進行打包。

### 安裝 PyInstaller：
```
pip install pyinstaller
```

### 打包指令（以 Windows 為例，macOS/Linux 請使用冒號作分隔符）：
```
pyinstaller --onefile --windowed --add-data "image;image" --add-data "music;music" monster_fall.py
```
打包完成後，執行檔會出現在 dist 資料夾中。
建議不要將打包後的執行檔 (.exe) 直接上傳到 GitHub，而是可以利用 GitHub Releases 功能上傳執行檔，保持 Git 儲存庫只包含源碼及資源檔案。

### 高分記錄處理
遊戲使用一個記錄檔來儲存最高分，該記錄檔會存放在使用者的家目錄下，檔名為 .monster_fall_record.txt。
這樣能夠確保記錄檔持久存在，同時避免因為打包後無法寫入資源目錄而產生問題。

