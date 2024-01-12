import re
import os
from functions.functions import run_command
from functions.backup import backup

def update_nginx_config(nginx_config, nginx_main_config, user_uri):
    # Backup the nginx configuration files
    backup_paths = [backup(file_path) for file_path in [nginx_config, nginx_main_config]]

    if not all(backup_paths):
        print("Backup failed. Exiting.")
        return

    # Check if load_module directive is present in the top-level context of nginx_main_config
    with open(nginx_main_config, 'r') as main_conf_file:
        nginx_main_content = main_conf_file.read()

    if 'load_module' not in nginx_main_content:
        # If not present, add it at the beginning of the file
        nginx_main_content = f"load_module /etc/nginx/modules/ngx_http_modsecurity_module.so;\n{nginx_main_content}"

        # Write the updated content back to nginx_main_config
        with open(nginx_main_config, 'w') as main_conf_file:
            main_conf_file.write(nginx_main_content)

    # Load the nginx configuration file
    with open(nginx_config, 'r') as file:
        nginx_content = file.read()

    # Check if modsecurity directives are present in the server block
    if 'modsecurity on;' not in nginx_content or 'modsecurity_rules_file /etc/nginx/modsec/main.conf;' not in nginx_content:
        # If not present, add them at the beginning of the server block
        nginx_content = re.sub(r'^\s*server {', r'server {\n    modsecurity on;\n    modsecurity_rules_file /etc/nginx/modsec/main.conf;', nginx_content, count=1, flags=re.MULTILINE)
        print("ModSec enabled in nginx configuration.")

    # Check if location block is present inside the server block
    location_block_pattern = re.compile(r'\s*location / {\s*([^}]*)\s*}')
    match = location_block_pattern.search(nginx_content)

    if match:
        # If present, add or replace the proxy_pass directive inside the location block
        location_block_content = match.group(1)
        proxy_pass_pattern = re.compile(r'\s*proxy_pass\s+([^;]+);')
        proxy_pass_match = proxy_pass_pattern.search(location_block_content)

        if proxy_pass_match:
            # If proxy_pass directive is present, replace it
            location_block_content = proxy_pass_pattern.sub(fr'proxy_pass {user_uri};', location_block_content)
        else:
            # If proxy_pass directive is not present, add it
            location_block_content = f'\n    proxy_pass {user_uri};\n{location_block_content}'

        # Replace the original location block content with the modified content
        nginx_content = location_block_pattern.sub(fr'location / {{\n    {location_block_content}\n}}', nginx_content, count=1)

        print("proxy_pass directive added successfully.")
    else:
        print("Error: 'location /' block not found in nginx configuration.")

    # Write the updated content back to the nginx configuration file
    with open(nginx_config, 'w') as file:
        file.write(nginx_content)

