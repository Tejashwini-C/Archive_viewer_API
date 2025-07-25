import subprocess

# Run both test files together and generate a single HTML report
subprocess.run([
    "pytest",
    "test_01_onboarding.py",
    "test_02_userCreation.py",
    "--html=combined_report.html",
    "--self-contained-html"
], check=True)
