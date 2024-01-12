import configparser
import subprocess
from functions.functions import run_command
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

def get_modsec_config():
    SRC_DIR = "/usr/local/src/"
    MODSEC_CONFIG_DIR = "/etc/nginx/modsec/"
    MODSEC_CONF_URL = "https://raw.githubusercontent.com/SpiderLabs/ModSecurity/v3/master/modsecurity.conf-recommended"
    UNICODE_MAPPING_URL = "https://raw.githubusercontent.com/SpiderLabs/ModSecurity/master/unicode.mapping"

    os.chdir(SRC_DIR)
    print(f"Current Working Directory: {os.getcwd()}")

    
    # Download and Set up the appropriate ModSecurity configuration file.

    # Create ModSecurity config directory if it doesn't exist
    os.makedirs(MODSEC_CONFIG_DIR, exist_ok=True)

    # Download modsecurity.conf-recommended 
    run_command(["wget", "-O", f"{MODSEC_CONFIG_DIR}/modsecurity.conf", f"{MODSEC_CONF_URL}"], shell=False)


    # Download unicode mapping file
    run_command(["wget", "-O", f"{MODSEC_CONFIG_DIR}/unicode.mapping", f"{UNICODE_MAPPING_URL}"], shell=False)





