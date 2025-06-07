# 📷 Email Webcam Detection WebApp

A real-time Python application that uses your webcam to detect motion and send an **email alert** with a snapshot of the 
detected activity. Built using **OpenCV**, **Python’s threading**, and **SMTP emailing**, the app captures a frame when 
motion is detected and emails it to a specified address. After sending the email, the captured images are 
cleaned up automatically.

---
## 🧰 Features

- 📸 Real-time motion detection using your webcam
- ✉️ Sends an email with an image when motion is detected
- 🧹 Cleans up saved images after sending the email
- 🔐 Uses environment variables for storing email credentials (via `.env` file)
- 🧵 Threading used for non-blocking image sending and cleanup

---

## 🗂️ Project Structure

```text
Email-Webcam-Detection-Webapp/
│
├── main.py              # Main script: captures video, detects motion, sends email
├── emailing.py          # Handles email sending logic with image attachment
├── .env                 # Environment variables (not pushed to GitHub)
├── images/              # Stores captured images before cleanup
└── README.md            # You’re reading it!
```
---

## 🚀 How It Works

1. **`main.py`**:
   - Starts your webcam.
   - Captures the first frame as a baseline.
   - Continuously compares incoming frames against the baseline.
   - If a significant change (motion) is detected:
     - Saves a snapshot of the frame to the `images/` directory.
     - Sends the image as an email via a separate thread.
     - Deletes all images in the `images/` folder after email is sent.

2. **`emailing.py`**:
   - Loads credentials securely from `.env`.
   - Attaches the image to an email.
   - Sends the email through **Gmail SMTP**.
   - Can be run independently for testing.

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tanu100894/Email-Webcam-Detection-Webapp.git
cd Email-Webcam-Detection-Webapp
```

### 2. Create a Virtual Environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, here are the minimum dependencies:

```bash
pip install opencv-python python-dotenv
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory with the following contents:

```env
sender_email=your_email@gmail.com
receiver_email=recipient_email@gmail.com
password=your_email_password_or_app_password
```
💡 If using Gmail, generate an **App Password** instead of using your main password.

---

## 🖥️ Running the App

Run the motion detector:

```bash
python main.py
```
💡 Press `q` to stop the webcam feed.

---

## 🧪 Test Email Function Separately

You can test email sending directly using:

```bash
python emailing.py
```
💡 This will send a predefined image (make sure the image exists at `images/19.png`).

---

## 📂 Output

- Detected motion images are saved in the `images/` directory temporarily.
- After the email is sent, the folder is cleaned up automatically using a background thread.

---

## 🧼 Cleaning

Cleanup of the `images/` folder is automatically handled after motion is detected and the image is sent.

You do not need to manually delete these files.

---

## ⚙️ Customization

You can customize:
- Motion sensitivity by adjusting contour area threshold (< 10000)
- Email subject/content
- Triggering frequency (currently sends one image after each motion ends)

---

## 🧩 Possible Improvements

- Add GUI using Streamlit or Tkinter
- Motion area tracking or bounding box logs
- Upload images to cloud storage
- Log events to a file or database
