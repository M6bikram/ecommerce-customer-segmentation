# Complete Beginner's Guide: Running the Dashboard + Uploading to GitHub

This guide assumes you know nothing about Streamlit or Git. Follow it top to bottom.

---

## PART 1: What is Streamlit? (30 seconds)

Streamlit is a Python library that turns a plain Python script into a
web dashboard — with buttons, charts, and file uploads — without you
writing any HTML/CSS/JavaScript. Your `app.py` file already has all
the Streamlit code in it. You just need to install it and run one
command.

---

## PART 2: Running the Dashboard on Your Computer

### Step 1: Install Python (skip if already installed)

Check if you already have it:
- **Windows**: open Command Prompt (search "cmd" in Start Menu), type `python --version`
- **Mac**: open Terminal (search "Terminal" in Spotlight), type `python3 --version`

If it shows a version number like `Python 3.11.x`, skip to Step 2.

If not installed:
1. Go to https://www.python.org/downloads/
2. Download the latest version (3.11 or higher)
3. Run the installer
4. **IMPORTANT (Windows only)**: On the first install screen, check the
   box that says "Add Python to PATH" before clicking Install
5. After installing, close and reopen your terminal/cmd, and re-check
   `python --version`

### Step 2: Extract the zip file

1. Find `E-Commerce-Customer-Segmentation.zip` in your Downloads folder
2. Right-click → "Extract All" (Windows) or double-click (Mac)
3. You'll get a folder called `ecommerce-segmentation`
4. Move this folder somewhere easy to find, e.g. your Desktop

### Step 3: Open a terminal INSIDE that folder

This is the part beginners usually get stuck on. Two ways to do it:

**Easy way (Windows):**
1. Open the `ecommerce-segmentation` folder in File Explorer
2. Click on the address bar at the top (where the folder path is shown)
3. Type `cmd` and press Enter — a terminal opens already inside that folder

**Easy way (Mac):**
1. Open the `ecommerce-segmentation` folder in Finder
2. Right-click inside the folder (on empty space) → "New Terminal at Folder"
   (if you don't see this option, open Terminal normally, then type `cd ` with
   a space, drag the folder into the terminal window, and press Enter)

**Manual way (works everywhere):**
```
cd Desktop/ecommerce-segmentation
```
(adjust the path to wherever you put the folder)

Verify you're in the right place by typing:
```
dir        (Windows)
ls         (Mac/Linux)
```
You should see `app.py`, `requirements.txt`, `datasets`, etc.

### Step 4: Create a virtual environment (recommended, keeps things clean)

A virtual environment is just an isolated box for this project's Python
packages, so they don't clash with anything else on your computer.

```
python -m venv venv
```

Activate it:
- **Windows**: `venv\Scripts\activate`
- **Mac/Linux**: `source venv/bin/activate`

You'll know it worked because your terminal line will now start with `(venv)`.

*(If this feels confusing, you can skip this step entirely — it's optional. Just proceed to Step 5 without it.)*

### Step 5: Install the required packages

```
pip install -r requirements.txt
```

This downloads Streamlit, Pandas, Scikit-learn, Plotly, etc. Takes 1-3
minutes depending on your internet.

### Step 6: Run the dashboard

```
streamlit run app.py
```

Your browser should automatically open to `http://localhost:8501` showing
your dashboard. If it doesn't open automatically, copy that URL into
your browser manually.

**To stop the app:** go back to the terminal and press `Ctrl + C`.

### Step 7: Use the dashboard

- The sidebar on the left has the dataset selector — the real Kaggle
  dataset is selected by default
- Scroll down to see: customer overview → EDA charts → elbow/silhouette
  method → cluster visualization → business insights → download buttons
- Everything is interactive — try changing the number of clusters with
  the slider and watch the charts update

---

## PART 3: Putting the Project on GitHub

GitHub is where you host your code online so you can share a link,
show it in interviews/assignments, and have a backup.

### Step 1: Create a GitHub account (skip if you have one)

1. Go to https://github.com
2. Sign up with an email, username, and password

### Step 2: Install Git on your computer

Check if you already have it: type `git --version` in your terminal.

If not installed:
- **Windows**: download from https://git-scm.com/download/win and install
  with default options
- **Mac**: type `git --version` in Terminal — if not installed, it will
  prompt you to install Xcode Command Line Tools; click Install

### Step 3: Tell Git who you are (one-time setup)

```
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```
(use the same email as your GitHub account)

### Step 4: Create a new repository on GitHub

1. Go to https://github.com and log in
2. Click the **+** icon (top right) → "New repository"
3. Repository name: `ecommerce-customer-segmentation`
4. Keep it **Public** (so you can share the link)
5. Do **NOT** check "Add a README file" (you already have one)
6. Click "Create repository"
7. GitHub will show you a page with commands — keep this page open,
   you'll need the URL shown there (it looks like
   `https://github.com/yourusername/ecommerce-customer-segmentation.git`)

### Step 5: Upload your project from the terminal

Make sure your terminal is still inside the `ecommerce-segmentation`
folder (same as Part 2, Step 3), then run these commands one by one:

```
git init
git add .
git commit -m "Initial commit: E-commerce customer segmentation project"
git branch -M main
git remote add origin https://github.com/yourusername/ecommerce-customer-segmentation.git
git push -u origin main
```

Replace the URL in the `git remote add origin` line with the actual
URL GitHub showed you in Step 4.

**If it asks you to log in:** GitHub no longer accepts your regular
password from the terminal. You'll need a "Personal Access Token"
instead:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name, check the box next to `repo`, click "Generate token"
4. Copy the token (it's shown only once)
5. When the terminal asks for a password, paste this token instead

### Step 6: Verify

Go to `https://github.com/yourusername/ecommerce-customer-segmentation`
in your browser — you should see all your files there.

### Step 7 (Optional but impressive): Deploy a live, shareable dashboard link

Instead of just sharing code, you can get a real live URL your
evaluator can click and use, for free:

1. Go to https://share.streamlit.io
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch `main`, and main file path `app.py`
5. Click "Deploy"
6. Wait 1-2 minutes — you'll get a public URL like
   `https://yourname-ecommerce-segmentation.streamlit.app`

This link works from any device with no installation — great for
submitting alongside your GitHub repo link.

---

## Quick Command Reference (once everything is set up)

Every time you want to work on this project again:

```
cd Desktop/ecommerce-segmentation
venv\Scripts\activate          (Windows)   OR   source venv/bin/activate   (Mac)
streamlit run app.py
```

Every time you make changes and want to update GitHub:

```
git add .
git commit -m "describe what you changed"
git push
```

(If you deployed to Streamlit Cloud, it auto-updates a minute or two
after you push.)
