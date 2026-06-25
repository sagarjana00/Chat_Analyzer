<div align="center">

```
██╗    ██╗██╗  ██╗ █████╗ ████████╗███████╗ █████╗ ██████╗ ██████╗
██║    ██║██║  ██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
██║ █╗ ██║███████║███████║   ██║   ███████╗███████║██████╔╝██████╔╝
██║███╗██║██╔══██║██╔══██║   ██║   ╚════██║██╔══██║██╔═══╝ ██╔═══╝
╚███╔███╔╝██║  ██║██║  ██║   ██║   ███████║██║  ██║██║     ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
                    CHAT ANALYZER  💬
```

**Turn your WhatsApp exports into beautiful insights.**
Supports group chats, personal chats, `.txt` and `.zip` — Android & iOS.

---

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>

---

## 📌 Overview

WhatsApp Chat Analyzer is an open-source analytics dashboard built entirely in Python. Export any WhatsApp conversation, drop the file in, and get instant visual breakdowns of message patterns, word usage, emoji habits, activity heatmaps, and more — for every participant or the group as a whole.

> **Privacy first.** Your data is processed in-memory and never stored or sent anywhere.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Top Statistics** | Total messages, words, media files, and links shared |
| 📅 **Monthly Timeline** | Message volume trends across months |
| 📆 **Daily Timeline** | Day-by-day activity over the full chat history |
| 🗺️ **Activity Map** | Busiest days of the week and months of the year |
| 🔥 **Hourly Heatmap** | Weekly activity heatmap — find the peak chat hours |
| ☁️ **Word Cloud** | Most-used words rendered as a visual cloud |
| 🔤 **Top 25 Words** | Horizontal bar chart of word frequency |
| 😄 **Emoji Analysis** | Emoji frequency table and pie chart |
| 👤 **User Breakdown** | Who talks the most — bar chart + percentage table |
| 📥 **CSV Export** | Download the full report or any individual section |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│   .txt export   ·   .zip export   ·   paste text fallback  │
└───────────────────────────┬─────────────────────────────────┘
                            │  bytes.decode()
                   utf-8 → utf-8-sig → latin-1 → cp1252
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                    preprocessor.py                          │
│  1. Normalize  (\u202f \u2009 \xa0 â€¯ → space)            │
│  2. Regex split  (timestamps → dates + messages)           │
│  3. pd.to_datetime  (dayfirst=True, errors=coerce)         │
│  4. Feature engineering  (year month day hour period …)    │
└───────────────────────────┬─────────────────────────────────┘
                            │  pandas DataFrame
┌───────────────────────────▼─────────────────────────────────┐
│                       helper.py                             │
│  fetch_stats · timelines · activity_heatmap                │
│  wordcloud · top_words · emoji_helper · most_busy_users    │
└───────────────────────────┬─────────────────────────────────┘
                            │  figures + DataFrames
┌───────────────────────────▼─────────────────────────────────┐
│                        app.py  (Streamlit)                  │
│  st.pyplot · st.dataframe · st.expander · st.download      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Library | Purpose |
|---|---|---|
| **Frontend** | `streamlit` | Web UI, sidebar, file uploader, download buttons |
| **Data** | `pandas` | DataFrame processing, groupby, feature engineering |
| **Parsing** | `re` (stdlib) | Regex timestamp extraction for all export formats |
| **Charts** | `matplotlib` | Line, bar, horizontal bar, pie charts |
| **Heatmap** | `seaborn` | Pivot-table weekly activity heatmap |
| **NLP** | `wordcloud` | Word frequency cloud generation |
| **NLP** | `emoji` | Emoji detection and frequency counting |
| **NLP** | `urlextract` | URL extraction from messages |
| **Deploy** | `Streamlit Cloud` | Zero-config cloud hosting |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Local installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

### Exporting your WhatsApp chat

**Android**
1. Open WhatsApp → tap the chat → ⋮ (three dots) → **More** → **Export chat**
2. Choose **Without Media**
3. Save the `.txt` file or the `.zip` — both work

**iOS**
1. Open WhatsApp → tap the chat → contact name → **Export Chat**
2. Choose **Without Media**
3. Share / save the `.zip` file

---

## 📁 Project Structure

```
whatsapp-chat-analyzer/
│
├── app.py               # Main Streamlit application
├── preprocessor.py      # Chat parser — regex, encoding, feature engineering
├── helper.py            # Analytics functions — stats, charts, NLP
├── requirements.txt     # Python dependencies
├── .streamlit/
│   └── config.toml      # Streamlit server config (upload size limit)
└── README.md
```

---

## 🔍 How the Parser Works

WhatsApp timestamps look different depending on the platform and locale:

```
# Android (most common)
15/07/2023, 8:41 pm - User: Hello

# Android with seconds
15/07/2023, 8:41:22 pm - User: Hello

# 24-hour format
15/07/2023, 20:41 - User: Hello
```

The parser handles all of these with a single regex pattern, followed by a Unicode normalization step that fixes the narrow no-break space (`\u202f`) that WhatsApp inserts between the time and `am/pm` — a character that looks identical to a regular space but breaks naive parsers.

```python
# Normalize before parsing
data = data.replace('â€¯', ' ')    # mojibake form (common on Android uploads)
data = data.replace('\u202f', ' ') # narrow no-break space
data = data.replace('\u2009', ' ') # thin space
data = data.replace('\xa0',   ' ') # non-breaking space

# Match all timestamp variants
pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:[aApP][mM])?\s-\s'
```

---

## ⚙️ Configuration

`.streamlit/config.toml` controls the upload size limit:

```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
```

Increase `maxUploadSize` (in MB) if you have very large group chats.

---

## 🤝 Contributing

Contributions are welcome. To get started:

```bash
# Fork the repo, then:
git checkout -b feature/your-feature-name
# make your changes
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
# open a Pull Request
```

**Ideas for contributions:**
- Sentiment analysis per user
- Language detection
- Response time analysis
- fix/improve mobile view
- Dark mode toggle
- Support for Telegram exports


---

<div align="center">

Made with ❤️ and Python

⭐ Star this repo if you found it useful!

</div>

---
👨‍💻 Author

Sagar Jana
