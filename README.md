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

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/yonlysuraj/InvincixDaily.git
cd InvincixDaily
