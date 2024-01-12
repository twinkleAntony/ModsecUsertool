import configparser
import subprocess
from functions.functions import run_command

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Get the packages file path from the configuration
PACKAGES_FILE_PATH = config['Paths']['PACKAGES_FILE_PATH']


# Functions to install system packages

def install_packages(package_names):
    # resynchronize the package index files from their sources
    update_command = "DEBIAN_FRONTEND=noninteractive apt-get update"
    success_update = run_command(update_command)

    if not success_update:
        print("Error updating package index. Exiting installation.")
        return

    # Install packages
    command = f"DEBIAN_FRONTEND=noninteractive apt-get install -y --fix-missing {' '.join(package_names)}"
    success_install = run_command(command)

    if success_install:
        print("Packages successfully installed.")
    else:
        print("Error installing packages.")

def install_packages_from_file(file_path):
    with open(file_path, "r") as file:
        package_lines = [line.strip() for line in file if not line.strip().startswith("#")]

    install_packages(package_lines)


def run_installation():
    install_packages_from_file(PACKAGES_FILE_PATH)
