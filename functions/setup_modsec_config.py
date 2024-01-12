import configparser
import subprocess
from functions.functions import run_command
import os

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')

def modify_modsecurity_conf():
    modsecurity_conf_path = "/etc/nginx/modsec/modsecurity.conf"
    updated_content = 'SecRuleEngine On'

    with open(modsecurity_conf_path, 'r') as modsecurity_conf_file:
        existing_content = modsecurity_conf_file.read()

    if updated_content not in existing_content:
        # Modify SecRuleEngine directive in modsecurity.conf
        run_command(["sed", "-i", f's/SecRuleEngine DetectionOnly/{updated_content}/', modsecurity_conf_path], shell=False)
        print(f"Modified {modsecurity_conf_path}.")

    else:
        print(f"SecRuleEngine is On already")

def create_or_modify_main_conf():
    main_conf_path = "/etc/nginx/modsec/main.conf"
    main_conf_content = """
Include "/etc/nginx/modsec/modsecurity.conf"

# Basic test rule
SecRule ARGS:testparam "@contains test" "id:1234,deny,status:403"

# OWASP CRS setup
Include /etc/nginx/modsec/owasp-modsecurity-crs/crs-setup.conf
Include /etc/nginx/modsec/owasp-modsecurity-crs/plugins/*-config.conf
Include /etc/nginx/modsec/owasp-modsecurity-crs/plugins/*-before.conf
Include /etc/nginx/modsec/owasp-modsecurity-crs/rules/*.conf
Include /etc/nginx/modsec/owasp-modsecurity-crs/plugins/*-after.conf
"""

    if not os.path.exists(main_conf_path):
        # Create main.conf if it doesn't exist
        with open(main_conf_path, 'w') as main_conf_file:
            main_conf_file.write(main_conf_content)
        print(f"Created {main_conf_path}.")
    else:
        # Check if the content is already present
        with open(main_conf_path, 'r') as main_conf_file:
            existing_content = main_conf_file.read()
        print(f"Main.conf already configured")

        if main_conf_content not in existing_content:
            # Append content to main.conf
            with open(main_conf_path, 'a') as main_conf_file:
                main_conf_file.write(main_conf_content)
            print(f"Modified {main_conf_path}.")

