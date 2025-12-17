import requests
import csv
import time
import re

# --- CONFIGURATION ---
GITHUB_TOKEN = "" # Paste your token between quotes
INPUT_FILE = "users.txt"
OUTPUT_FILE = "github_emails.csv"
# ---------------------

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def extract_username(url):
    """Extracts username from a GitHub URL."""
    match = re.search(r"github\.com/([^/]+)", url)
    return match.group(1).strip() if match else None

def is_real_email(email):
    """Filters out GitHub noreply addresses."""
    if not email: return False
    return "noreply.github.com" not in email

def get_email_from_events(username):
    """Strategy 1: Check recent public activity (fastest)."""
    url = f"https://api.github.com/users/{username}/events/public"
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            for event in response.json():
                if event['type'] == 'PushEvent':
                    commits = event.get('payload', {}).get('commits', [])
                    for commit in commits:
                        email = commit.get('author', {}).get('email')
                        if is_real_email(email):
                            return email
    except: pass
    return None

def get_email_from_repos(username):
    """Strategy 2 (FALLBACK): Check commits in user's owned repositories."""
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5"
    try:
        repo_response = requests.get(repos_url, headers=headers)
        if repo_response.status_code == 200:
            repos = repo_response.json()
            for repo in repos:
                # Get commits for each repo
                commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits?author={username}&per_page=5"
                commit_response = requests.get(commits_url, headers=headers)
                if commit_response.status_code == 200:
                    for c in commit_response.json():
                        email = c.get('commit', {}).get('author', {}).get('email')
                        if is_real_email(email):
                            return email
    except: pass
    return None

def main():
    try:
        with open(INPUT_FILE, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} not found in this folder.")
        return

    print(f"Starting search for {len(urls)} users...")

    with open(OUTPUT_FILE, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GitHub URL", "Username", "Email"])

        for i, url in enumerate(urls):
            username = extract_username(url)
            if not username: continue
            
            print(f"[{i+1}/{len(urls)}] Searching {username}...", end=" ", flush=True)
            
            # Step 1: Try Events
            email = get_email_from_events(username)
            
            # Step 2: Fallback to Repos
            if not email:
                email = get_email_from_repos(username)
            
            if email:
                print(f"FOUND: {email}")
            else:
                print("NOT FOUND")
                email = "Not Found"

            writer.writerow([url, username, email])
            
            # Pause to prevent hitting secondary rate limits
            time.sleep(0.7)

    print(f"\n✅ Done! Check your folder for '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()