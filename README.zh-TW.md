# TextToVoicevox 🍂

🌐 **[English](README.en.md)** ｜ **[日本語](README.md)** ｜ 繁體中文（本頁）

把 PDF、圖片、電子書、青空文庫的日文，交給 VOICEVOX 的聲音（ずんだもん等）唸給你聽的免費桌面軟體。全部在你自己的電腦裡完成，不會把檔案上傳到網路。

我是 rakuyou211，一個人做軟體的業餘開發者。一開始只是想讓電腦把書和長長的 PDF 唸給我聽，就這樣做到了現在。還有很多不夠完美的地方，下面會老實寫出來。

> ⚠️ **先說清楚：軟體的畫面（按鈕和選單）目前只有日文。** 讀出來的內容也是日文。比較適合已經看得懂一些日文的人，例如正在學日文、想聽自然日文發音的人。

▶ **3 分鐘看懂怎麼用**：[TextToVoicevox 使用教學（YouTube・3 分鐘・日文）](https://youtu.be/ZJlJh9jPQIY)

▶ **實際操作影片**：[介紹影片（YouTube・36 秒・日文）](https://youtu.be/AWVs6Evw4E0)　／　[ずんだもん唸太宰治《人間失格》（Shorts）](https://youtube.com/shorts/ETyigWasQPU)

---

## 適合誰

- **正在學日文的人**：把日文文章（課本、小說、新聞截圖）變成自然的日文語音。試聽時會用假名顯示「它是怎麼唸的」，可以拿來確認漢字的讀音。
- **想用耳朵讀日本文學的人**：直接讀取 [青空文庫](https://www.aozora.gr.jp/)（著作權已過期的日本名著，免費公開）的文字，會自動去掉注音標記。
- **眼睛累、不想再盯著小字的人**：掃描的 PDF、拍下來的書頁，都能變成聲音。

---

## 可以做什麼

- **從畫面直接讀**：用滑鼠框住螢幕上的文字（電子書、PDF、網頁），馬上唸出來（Ctrl+R ／ ⌘R）。
- **支援多種檔案**：PDF（含掃描檔）、圖片（PNG・JPG 等）、`.txt`、`.docx`、`.epub`。
- **離線 OCR**：圖片和掃描檔的文字辨識，使用系統內建的功能（Windows 用 Windows.Media.Ocr，Mac 用 Apple Vision），不上傳。
- **用 VOICEVOX 的聲音朗讀**：在自己的電腦上產生語音，可調整語速、音高等。
- **一行換一個角色**：在行首寫 `@ずんだもん:` 之類的，就能換成別的聲音，做對話朗讀也很方便。
- **輸出音檔與字幕**：隨時可存成 WAV；另外也能輸出 MP3・M4A，以及有章節的有聲書 M4B（Windows 需要另裝 ffmpeg；Mac 只有 MP3 需要）。還能同時輸出對齊的 `.srt` 字幕。
- **讀音字典**：唸錯的詞登錄一次就會記住。

---

## 使用前的三個步驟

1. **安裝並開啟 VOICEVOX**：VOICEVOX 是另一套免費軟體，負責產生聲音，本軟體沒有內附。請從 [VOICEVOX 官方網站](https://voicevox.hiroshiba.jp/) 下載安裝，並保持開啟。
2. **安裝本軟體（建議用一行指令）**
   - **Windows**：在「開始」按右鍵 →「終端機」，貼上這一行後按 Enter：
     ```powershell
     irm https://raw.githubusercontent.com/rakuyou211-blip/TextToVoicevox/main/install.ps1 | iex
     ```
   - **Mac**：打開「終端機」，貼上這一行後按 Return：
     ```bash
     curl -fsSL https://raw.githubusercontent.com/rakuyou211-blip/TextToVoicevox/main/install.sh | bash
     ```
   沒有 Python 的話，會先詢問要不要安裝。完成後桌面（Mac 是 Launchpad）會出現 **TextToVoicevox**。
3. **開始使用**：在「1. 📥 入力ファイル」加入檔案 → 按「▶ テキスト抽出 実行」取出文字 → 選擇聲音後按「▶ 試聴」或「🔊 音声を生成」。

也可以從 [Releases](https://github.com/rakuyou211-blip/TextToVoicevox/releases/latest) 下載 zip。詳細步驟請看 [英文 README](README.en.md)。

> 老實說：目前不是一鍵安裝的 `.exe`／`.app`，需要 Python。第一次設定時會連網下載元件，之後就完全離線。

---

## 隱私

- 不收集使用資料、不需要註冊帳號、沒有廣告。
- 原始碼全部公開（MIT 授權）。
- 文字辨識和語音合成都在你的電腦裡完成。

---

## 關於 VOICEVOX 的聲音（請一定要看）

聲音來自 **VOICEVOX** 以及各角色的聲音資料庫，有各自的使用條款。**公開使用做出來的聲音時，大多數角色都需要標示來源**（例如「VOICEVOX:ずんだもん」）。各角色的規定不同，請以官方條款為準。本軟體的作者沒有這些聲音的權利。

朗讀有著作權的書並公開音檔，可能會侵害著作權。請用在自己聽的範圍內，或使用青空文庫這類著作權已過期的作品。

---

## 授權

本軟體以 **MIT 授權** 公開，不提供任何保證。

---

一個人慢慢做的軟體 🍂。不管是「我這樣用」還是「卡在這裡」，一句話的感想都很歡迎：[感想表單](https://github.com/rakuyou211-blip/TextToVoicevox/issues/new?template=feedback.yml)（中文、英文、日文都可以）。
