

# 🚀 GH Scraper

## 🔍 How it Works (Simple Terms)

Instead of just looking at a developer's profile page, this script digs into their **digital footprint** across GitHub:

1.  **Scanning Recent Activity:** It checks the developer's most recent code "pushes." When code is uploaded, a work email is often attached to the background metadata of that specific save (commit).
2.  **The Automatic Fallback:** If a developer hasn't been active recently, the script scans the history of the **projects they own** to find the email used during the initial build.
3.  **Smart Filtering:** It identifies and discards "fake" privacy emails (like `user@noreply.github.com`), searching until it finds a **real, reachable email address**.

**The Result:** In our initial test, we achieved a **74% success rate**.

-----

## 🛠️ Prerequisites

Before running the script, ensure you have the following:

  * **Python 3 installed** on your computer.
  * **A GitHub Personal Access Token (PAT):**
      * Go to **GitHub Settings \> Developer Settings \> Personal Access Tokens (Tokens classic)**.
      * Generate a new token (no specific scopes/permissions are required for public data).
      * **Copy and save this token.**

-----

## 📂 Project Setup

1.  **Create a Folder:** Create a folder on your computer named `github_scraper`.
2.  **Create `users.txt`:** Inside the folder, create a text file named `users.txt`. Paste the GitHub URLs you want to scan (one per line, e.g., `https://github.com/username`).
3.  **Create `fetch_emails.py`:** Create a Python file with the scraper code.
4.  **Add your Token:** Open `fetch_emails.py` and replace `"your_github_token_here"` with your actual GitHub token.

**Your folder structure should look like this:**

```text
github_scraper/
├── users.txt
└── fetch_emails.py
```

-----

## 🚀 How to Run the Script

### **For macOS Users**

1.  Open the **Terminal** app.
2.  Navigate to your folder: type `cd` followed by a space, then drag your folder into the terminal window and hit **Enter**.
3.  Install the required library:
    ```bash
    pip3 install requests
    ```
4.  Run the script:
    ```bash
    python3 fetch_emails.py
    ```

### **For Windows Users**

1.  Open **Command Prompt (CMD)** or **PowerShell**.
2.  Navigate to your folder: type `cd` followed by a space, then type the path to your folder (e.g., `cd C:\Users\Name\Desktop\github_scraper`) and hit **Enter**.
3.  Install the required library:
    ```bash
    pip install requests
    ```
4.  Run the script:
    ```bash
    python fetch_emails.py
    ```

-----

## 📊 Output

Once the script finishes, a new file named `github_emails.csv` will appear in your folder. This file contains:

  * **GitHub URL**
  * **Username**
  * **Verified Email** (or "Not Found" if the user has strict privacy settings).

## ⚠️ Important Notes

  * **Rate Limits:** The script includes a small delay between requests to respect GitHub’s security rules. It will take approximately 10–15 minutes to process 800 users.
  * **Privacy:** This tool only accesses **publicly available metadata**. It cannot find emails for users who have never pushed code publicly or who have successfully scrubbed their Git history.

