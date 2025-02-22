# 🚀 InvincixDaily - Automated Attendance Check-In & Check-Out

## 📌 Overview
**InvincixDaily** is a Python automation script that uses **Selenium** to automatically log in to the Invincix attendance portal, perform **daily check-in at 10:00 AM** and **check-out at 7:30 PM**, and log the status. The script runs in a headless Chrome browser and can be scheduled using **GitHub Actions** or **Cron Jobs**.

---

## ⚡ Features
- ✅ **Automated Check-In & Check-Out** via Selenium
- ✅ **Headless Execution** using Chrome
- ✅ **Secure Login** (credentials stored as environment variables)
- ✅ **Error Handling & Logging** (`checkin.log` & `checkout.log`)
- ✅ **Screenshot Capture on Failure**
- ✅ **Prevents Duplicate Runs** (Does not run if already checked in/out)
- ✅ **Easy Deployment** via **GitHub Actions** or **Cron Jobs**

---

## 🛠️ Installation & Setup

### **1⃣ Clone the Repository**
```sh
git clone https://github.com/yonlysuraj/InvincixDaily.git
cd InvincixDaily
```

### **2⃣ Create a Virtual Environment (Optional but Recommended)**
```sh
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
venv\Scripts\activate  # On Windows
```

### **3⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

If `requirements.txt` does not exist, install manually:
```sh
pip install selenium webdriver-manager
```

### **4⃣ Install Google Chrome & ChromeDriver**
```sh
sudo apt update && sudo apt install -y google-chrome-stable
```
Install **ChromeDriver**:
```sh
wget https://chromedriver.storage.googleapis.com/$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
```
Verify installation:
```sh
chromedriver --version
```

### **5⃣ Set Environment Variables**
Before running, set your login credentials:
```sh
export EMAIL="your-email@domain.com"
export PASSWORD="your-secure-password"
```
For **permanent storage**, add them to `~/.bashrc`:
```sh
echo 'export EMAIL="your-email@domain.com"' >> ~/.bashrc
echo 'export PASSWORD="your-secure-password"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Usage

### **Manual Check-In**
```sh
python3 checkin.py
```

### **Manual Check-Out**
```sh
python3 checkout.py
```

### **View Logs**
```sh
cat checkin.log  # Check-in logs
cat checkout.log  # Check-out logs
```

### **Force Re-run (If Skipped)**
```sh
rm last_checkin.txt  # Forces check-in script to run
rm last_checkout.txt  # Forces check-out script to run
```

### **Capture Screenshot on Errors**
If the script fails, it captures a screenshot for debugging:
```sh
ls *.png
```
To view the error screenshot:
```sh
xdg-open error_checkin.png  # On Linux
open error_checkin.png  # On Mac
```

---

## ⌛ Automate with Crontab (Run Daily)

### **1⃣ Open Crontab**
```sh
crontab -e
```

### **2⃣ Add These Lines**
```
0 10 * * * /usr/bin/python3 /home/ubuntu/InvincixDaily/checkin.py >> /home/ubuntu/checkin.log 2>&1
30 19 * * * /usr/bin/python3 /home/ubuntu/InvincixDaily/checkout.py >> /home/ubuntu/checkout.log 2>&1
```

### **3⃣ Restart Cron Service**
```sh
sudo systemctl restart cron
```

### **4⃣ Verify If Crontab is Running**
```sh
crontab -l
```

### **5⃣ Check Logs to Confirm Execution**
```sh
tail -f checkin.log
tail -f checkout.log
```

---

## 🔄 Automate with GitHub Actions (Alternative to Cron)

### **1⃣ Add GitHub Secrets**
Go to **GitHub Repo → Settings → Secrets** and add:
- `EMAIL` → Your email
- `PASSWORD` → Your password

### **2⃣ Commit and Push**
```sh
git add .
git commit -m "Added GitHub Actions for daily check-in and check-out"
git push origin main
```

### **3⃣ Manually Trigger the Workflow**
- Go to **GitHub Repository → Actions → Daily Attendance Automation**
- Click **"Run workflow"** to test manually.

---

## 🛠️ Troubleshooting

### **1. Script Doesn't Run Automatically?**
✔️ Check if `cron` is running:
```sh
cat /var/log/syslog | grep CRON | tail -20
```
✔️ Restart the cron service:
```sh
sudo systemctl restart cron
```
✔️ Check logs:
```sh
cat checkin.log
cat checkout.log
```

### **2. Selenium Fails?**
✔️ Ensure Chrome & ChromeDriver are installed:
```sh
google-chrome --version
chromedriver --version
```
✔️ Reinstall ChromeDriver:
```sh
sudo apt install -y google-chrome-stable
```

---

## 📚 License
This project is licensed under the **MIT License**.

---

## 🎯 Conclusion
With **InvincixDaily**, your daily check-ins and check-outs are fully automated. You can run this on a **local machine** using `cron` or on **GitHub Actions** for cloud execution. 🚀

If you have any questions, feel free to **open an issue** or **contribute** to improve the project. Happy automating! 😊

