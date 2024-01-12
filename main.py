from functions.install_packages import run_installation
from functions.compile_install_modsec import compile_and_install_modsec
from functions.compile_install_connector import compile_and_install_connector
from functions.get_modsec_config import get_modsec_config
from functions.get_owasp_crs import get_owasp_crs
from functions.setup_modsec_config import modify_modsecurity_conf
from functions.setup_modsec_config import create_or_modify_main_conf
from functions.secure_web_app import update_nginx_config
from functions.restart_waf import restart_waf


def print_menu():
    title = "ModSec NGINX WAF"
    box_width = 80  # Adjust the box width as needed
    box_height = 40  # Adjust the box height as needed

    print(f"\n{'#' * box_width}")
    print(f"{' ' * (box_width // 2 - len(title) // 2)}\033[91m {title} \033[0m{' ' * (box_width // 2 - len(title) // 2)}\n")

    menu_items = [
        "1. Setup ModSec NGINX WAF",
        "2. Secure Web Server / Web App",
        "3. Restart WAF",
        "4. Exit"
    ]

    for item in menu_items:
        print(item)

    print(f"{'#' * box_width}\n")

def run():
    while True:
        print_menu()
        user_input = input("\nEnter your choice (1-4): ")

        if user_input == '1':
            print("Setting up ModSec NGINX WAF...")
            run_installation()
            compile_and_install_modsec()  # Call the function for ModSecurity compilation and installation
            compile_and_install_connector()
            get_modsec_config()
            get_owasp_crs()
            modify_modsecurity_conf()
            create_or_modify_main_conf()



        elif user_input == '2':
            print("Securing Web Server / Web App...")
            nginx_config_path = '/etc/nginx/sites-available/default'
            nginx_main_config_path = '/etc/nginx/nginx.conf'
            user_uri = input("Enter the URI to protect (eg. http://www.eample.com): ")
            update_nginx_config(nginx_config_path, nginx_main_config_path, user_uri)



        elif user_input == '3':
            print("Restarting WAF...")
            restart_waf()

        elif user_input == '4':
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def main():
    run()

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("Exited due to {}".format(err))

