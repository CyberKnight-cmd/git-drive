# Git-Drive: A Git-Inspired Backup Tool for Google Drive

## 📌 Project Description

**Git-Drive** is my hands-on journey to understand the core logic behind version control systems like Git. By building a file synchronizer from scratch, I am learning how to detect file changes, manage state, and interact with external APIs. This script uses the Google Drive API to create an intelligent backup system that mirrors a local folder to the cloud.

---

## ✨ Features

✅ **Git-like Change Detection:** Intelligently detects which files are new, modified, or have been deleted since the last sync.  
✅ **Efficient Syncing:** Only uploads or updates files that have actually changed, saving bandwidth and time.  
✅ **State Management:** Keeps a local `state.json` file to remember the last synced state of every file.  
✅ **Secure Authentication:** Uses the official Google API OAuth 2.0 flow to securely connect to your Google account without ever storing your password.

---

## ⚙️ How It Works

The script operates in a cycle:

1. **Scan Local:** Scans the target local directory to build a "current state" map of all files and their last-modified times.  
2. **Load Previous State:** Loads the "last known state" from the `state.json` file.  
3. **Compare & Diff:** Compares the current state to the last known state to create three lists: `ADDED`, `MODIFIED`, and `DELETED` files.  
4. **Act on Changes:** Connects to the Google Drive API and performs necessary actions:
   - Uploads new files.
   - Updates modified files.
   - Trashes deleted files on Google Drive.
5. **Save New State:** Saves the "current state" to `state.json`, making it the "last known state" for the next run.

---

## 🚀 Setup and Usage

### 1. Prerequisites

- Python 3.8 or newer
- `pip` (Python’s package installer)

---

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/Git-Drive.git
cd Git-Drive
````

---

### 3. Install Dependencies

Install the necessary Google Client libraries:

```bash
pip install google-api-python-client google-auth-oauthlib
```

---

### 4. Get Google Drive API Credentials

This is the most important setup step:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project.
3. Enable the **Google Drive API** for your project.
4. Go to **Credentials**, click **+ CREATE CREDENTIALS**, and choose **OAuth client ID**.
5. Select **Desktop app** as the application type.
6. Click **DOWNLOAD JSON**. Rename the downloaded file to `credentials.json` and place it in the root of this project folder.

---

### 5. Configure the Script

Open the main Python script (e.g., `sync_script_step2.py`) in a text editor and change the following variable to point to the folder you want to back up:

```python
# The local directory you want to sync.
DIRECTORY_TO_TRACK = "path/to/your/folder"
```

---

### 6. Run the Script

Execute the script from your terminal:

```bash
python your_script_name.py
```

* **First Run:** Your web browser will open, asking you to log in to your Google Account and grant permission. Click **Allow**. This will create a `token.json` file in your project folder, which securely stores your login for future runs.
* **Subsequent Runs:** The script will use the `token.json` file to authenticate automatically without opening the browser.

---

## 📈 Project Status & Roadmap

This project is currently in development. The core logic for detecting and uploading new files is complete.

### Next Steps:

* [ ] Implement logic to update modified files
* [ ] Implement logic to trash deleted files on Google Drive
* [ ] Replicate local folder structure on Google Drive
* [ ] Create a simple command-line alias (like `drive-update`) for easy execution

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## ✍️ Author

**Cyber Knight** – *Git-Drive Developer*

Feel free to ⭐️ the repo if you find it helpful!

