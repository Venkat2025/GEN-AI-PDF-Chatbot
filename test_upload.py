import requests
import os

BACKEND = "http://localhost:8000"

def test_upload(pdf_path):
    if not os.path.exists(pdf_path):
        print("PDF not found:", pdf_path)
        return
    with open(pdf_path, "rb") as f:
        files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
        r = requests.post(f"{BACKEND}/upload", files=files)
    print("Status:", r.status_code)
    print("Response:", r.text)

if __name__ == "__main__":
    test_upload("Bank-Policy-Development-pol-fin.pdf")
