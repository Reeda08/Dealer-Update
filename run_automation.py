import subprocess


print("\nStarting Full Automation Workflow...**\n")


print("\n Running stockdownload.py to download the inventory file.\n")
subprocess.run(["python", "stockdownload.py"], check=True)

print("\n Running process.py to download the inventory file.\n")
subprocess.run(["python", "process.py"], check=True)

print("\n Running vista.py to download the inventory file.\n")
subprocess.run(["python", "vista.py"], check=True)

print("\n Running Filter.py to download the inventory file.\n")
subprocess.run(["python", "Filter.py"], check=True)

print("\n Running compare.py to download the inventory file.\n")
subprocess.run(["python", "compare.py"], check=True)

print("\n Running update.py to download the inventory file.\n")
subprocess.run(["python", "update.py"], check=True)