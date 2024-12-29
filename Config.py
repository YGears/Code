import subprocess
import sys

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("installed packages from requirements.txt")

def create_txt_installed_packages():
    subprocess.check_call([sys.executable, "-m", "pip", "list", ">", ".installed_packages"])
    print("created file .installed_packages")


def call_functions():
    install_requirements()
    create_txt_installed_packages()
call_functions()


