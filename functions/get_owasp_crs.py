import configparser
import subprocess
from functions.functions import run_command
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

def get_owasp_crs():
    MODSEC_CONFIG_DIR = "/etc/nginx/modsec/"
    owasp_crs_dir = os.path.join(MODSEC_CONFIG_DIR, "owasp-modsecurity-crs")

    # STEP: Setup OWASP CRS
    os.chdir(MODSEC_CONFIG_DIR)
    print(f"Current Working Directory: {os.getcwd()}")

    # Check if owasp-modsecurity-crs directory already exists
    if os.path.exists(owasp_crs_dir):
        print("OWASP CRS repository already exists. Updating...")
        # Change directory to owasp-modsecurity-crs
        os.chdir(owasp_crs_dir)
        print(f"Current Working Directory: {os.getcwd()}")

        # Pull the latest changes
        success_pull_crs = run_command(["git", "pull"], shell=False)

        if not success_pull_crs:
            print("Error during OWASP CRS Git pull.")
    else:
        # Clone OWASP CRS repository
        success_clone_crs = run_command(["git", "clone", "https://github.com/coreruleset/coreruleset", "owasp-modsecurity-crs"], shell=False)

        if not success_clone_crs:
            print("Error during OWASP CRS clone.")

    # Move CRS setup config
    owasp_crs_setup_conf = os.path.join(owasp_crs_dir, "crs-setup.conf")
    if not os.path.exists(owasp_crs_setup_conf):
        os.rename(os.path.join(owasp_crs_dir, "crs-setup.conf.example"), owasp_crs_setup_conf)

    # Move exclusion rules before CRS
    os.chdir(os.path.join(owasp_crs_dir, "rules"))
    if not os.path.exists("REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf"):
        os.rename("REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example", "REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf")

    # Move exclusion rules after CRS
    if not os.path.exists("RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf"):
        os.rename("RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example", "RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf")
