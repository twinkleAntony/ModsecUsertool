import configparser
import subprocess
from functions.functions import run_command
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

def restart_waf():
    success_restart = run_command(["systemctl", "restart", "nginx.service"], shell=False)
    if success_restart:
        print("Service restarted.")
        run_command(["systemctl", "status", "nginx.service"], shell=False)
        return
    else:
        print("Error restarting services.")
        return


