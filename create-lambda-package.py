#!/usr/bin/env python3
"""Create Lambda deployment package"""

import zipfile
import os
from pathlib import Path

def create_lambda_zip():
    print("Creating Lambda deployment package...")

    zip_path = "lambda-function.zip"
    package_dir = "backend/package"
    app_file = "backend/app.py"

    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add all files from package directory
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_dir)
                zipf.write(file_path, arcname)
                if len(zipf.namelist()) % 100 == 0:
                    print(f"  Added {len(zipf.namelist())} files...")

        # Add app.py
        zipf.write(app_file, "app.py")

    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ Created {zip_path} ({size_mb:.2f} MB)")
    print(f"   Total files: {len(zipf.namelist())}")

if __name__ == "__main__":
    create_lambda_zip()
