# CareConnect

A clinic appointment system built with Flask. Patients book appointments with doctors, and doctors set the times they are available.

## How to run
1. Install Python.
2. Open a terminal in this folder and run:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

3. Open http://127.0.0.1:5000 in your browser.

The database (SQLite) is created automatically the first time you run it.

## How to use it
1. Click **I am a Doctor**, create a doctor account, log in, and add your available days and times under **My Availability**.
2. Log out. Click **I am a Patient**, create a patient account and log in.
3. Go to **Find a Doctor**, open a doctor, choose a date and a free time, then confirm.
4. The doctor can log in again to see the appointment and mark it as completed or cancelled.
