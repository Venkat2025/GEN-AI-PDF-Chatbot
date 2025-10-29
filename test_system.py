import requests
import time
import os

BACKEND = "http://localhost:8000"

def health():
    try:
        r = requests.get(BACKEND + "/")
        print("Health:", r.status_code, r.text)
    except Exception as e:
        print("Backend not running:", e)

if __name__ == "__main__":
    health()
    if not os.path.exists("Bank-Policy-Development-pol-fin.pdf"):
        print("Put a test PDF named Bank-Policy-Development-pol-fin.pdf in the project root.")
    else:
        with open("Bank-Policy-Development-pol-fin.pdf","rb") as f:
            files = {"file":("test.pdf", f, "application/pdf")}
            r = requests.post(BACKEND + "/upload", files=files)
            print("Upload:", r.status_code, r.text)
            time.sleep(1)
            r2 = requests.post(BACKEND + "/chat", json={"message":"What is this document about?"})
            print("Chat:", r2.status_code, r2.text)
            r3 = requests.get(BACKEND + "/documents")
            print("Documents:", r3.status_code, r3.text)
