import configparser
import subprocess
import shlex  # Used for splitting the command string

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read('config.ini')


# Function to run system commands
def run_command(command, shell=True):
    process = None
    try:
        process = subprocess.Popen(command, shell=shell, stderr=subprocess.PIPE, text=True)
        _, error_output = process.communicate()

        if process.returncode == 0:
            print(f"Command executed successfully: {' '.join(command)}")
        else:
            print(f"Error executing command: {' '.join(command)}")
            print(f"Exit code: {process.returncode}")
            print(f"Error output:\n{error_output}")

    except Exception as e:
        print(f"Exception while executing command: {' '.join(command)}")
        print(e)
        return False, b'', b''
    finally:
        # Wait for the process to complete
        if process and process.returncode is None:
            process.wait()

    return process.returncode == 0, _, error_output


# Function to get user input
def get_user_input(prompt):
    return input(prompt).strip()
