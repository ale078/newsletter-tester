# 📰 Newsletter Testing Automator

**Version:** 1.0.0 (Pilot)

Automator for testing and simulating email newsletter opens and article clicks across Desktop and Mobile Web environments using Playwright and Streamlit.

---

## 🚀 Key Features

- **Cross-Platform Emulation**: Simulates realistic opens and link visits on both Desktop (Chromium) and Mobile Web (iPhone / Mobile Safari).
- **Automated Article Link Discovery**: Automatically identifies and filters content and article links within the email body, omitting unsubscribe, social media, and administrative links.
- **Interactive Web Dashboard**: Streamlit-based UI to configure campaigns, trigger real-time executions, and inspect live progress.
- **Execution History & Reports**: Persistent SQLite storage tracking successful/failed opens and clicks, error logs, and clicked URLs.
- **Scheduled Background Execution**: Built-in scheduler for daily recurrent campaign testing.
- **Standalone Testing Script**: Lightweight CLI script (`test_single.py`) for rapid link validation without launching the web server.

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ale078/newsletter-tester.git
   cd newsletter-tester
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS / Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**:
   ```bash
   playwright install chromium
   ```

---

## 💻 Usage

### 1. Launch Web Dashboard (Streamlit)
To start the user interface:
```bash
streamlit run app.py
```
- Open your browser at `http://localhost:8501`.
- Go to **Create Campaign** to enter the newsletter URL and desired open/click counts.
- Go to **Campaigns & Execution** to view registered campaigns and click **Run Test Now**.
- Go to **Reports & History** to review metrics and execution history.

### 2. Standalone Quick Test (CLI)
To run a fast test without the web UI:
1. Open `test_single.py`.
2. Update `newsletter_url` with your target email link.
3. Run:
   ```bash
   python test_single.py
   ```

### 3. Run Daily Scheduler
To start the daily background runner:
```bash
python scheduler.py
```

---

## 📁 Project Structure

```text
newsletter-tester/
├── app.py              # Streamlit web dashboard
├── automator.py        # Playwright automation engine (Opens & Clicks)
├── database.py         # SQLite schema, migrations & persistence
├── scheduler.py        # Daily recurring task scheduler
├── test_single.py      # Standalone quick test CLI script
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 📄 License

MIT License.
