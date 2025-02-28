import subprocess
import logging

def run_command(command_list):
    """
    Helper function to run a subprocess command and capture its output.
    """
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Command timed out."
    except Exception as e:
        return f"Error: {str(e)}"

def run_nmap(target: str) -> str:
    """
    Executes an nmap scan on the given target.
    """
    command = ["nmap", "-sV", target]
    logging.info(f"Running nmap on {target}")
    return run_command(command)

def run_gobuster(target: str) -> str:
    """
    Executes a gobuster directory scan on the given target.
    """
    # Note: Adjust the wordlist path as needed.
    command = ["gobuster", "dir", "-u", f"http://{target}", "-w", "/usr/share/wordlists/dirb/common.txt"]
    logging.info(f"Running gobuster on {target}")
    return run_command(command)

def run_ffuf(target: str) -> str:
    """
    Executes an ffuf scan for directory fuzzing on the given target.
    """
    # Note: Adjust the wordlist path as needed.
    command = ["ffuf", "-u", f"http://{target}/FUZZ", "-w", "/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt"]
    logging.info(f"Running ffuf on {target}")
    return run_command(command)

def run_sqlmap(target: str) -> str:
    """
    Executes a sqlmap test on the given target.
    """
    # Note: This example assumes a vulnerable endpoint for demonstration.
    command = ["sqlmap", "-u", f"http://{target}/vulnerable", "--batch"]
    logging.info(f"Running sqlmap on {target}")
    return run_command(command)
