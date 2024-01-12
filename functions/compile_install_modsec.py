import configparser
import subprocess
from functions.functions import run_command
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

def compile_and_install_modsec():
    SRC_DIR = "/usr/local/src/"
    MODSEC_DIR = "ModSecurity"

    # Change directory to the source directory
    os.chdir(SRC_DIR)

    # Check if ModSecurity directory already exists
    if os.path.exists(os.path.join(SRC_DIR, MODSEC_DIR)):
        print("ModSecurity repository already exists. Updating...")
        # Change directory to ModSecurity
        os.chdir(MODSEC_DIR)

        # Print current working directory after changing
        print(f"Current Working Directory: {os.getcwd()}")

        # Pull the latest changes
        success = run_command(["git", "pull", "--recurse-submodules"], shell=False)

        if not success:
            print("Error during Git pull.")
            return
    else:
        # Clone ModSecurity repository
        success = run_command(["git", "clone", "--recurse-submodules", "--depth", "1", "-b", "v3/master", "--single-branch", "https://github.com/SpiderLabs/ModSecurity"], shell=False)

        if not success:
            print("Error during Git clone.")
            return

        # Change directory to ModSecurity after cloning
        os.chdir(MODSEC_DIR)

        # Print current working directory after changing
        print(f"Current Working Directory: {os.getcwd()}")

    # Run build.sh script
    run_command(["./build.sh"])

    # Run configure
    run_command(["./configure"])

    # Run make with progress display
    run_command("make -j 8", shell=True)

    # Run make install with progress display
    run_command("make install", shell=True)
