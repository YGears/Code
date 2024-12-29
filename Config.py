import subprocess
import sys

def install_requirements():
    #install requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    #list requirements
    print("\nInstalled requirements: \n=======================\n")
    subprocess.check_call([sys.executable, "-m", "pip", "list"])


def call_functions():
    install_requirements()
call_functions()


