import requests
from bs4 import BeautifulSoup
import subprocess
from tabulate import tabulate
import sys
import platform
import socket
from colorama import Fore, Style

# Functions for showing OS information and IP addresses
def show_os_info():
    # Get the OS information
    os_name = platform.system()
    os_version = platform.version()
    machine = platform.machine()
    processor = platform.processor()
    node = platform.node()
    os_release = platform.release()
    distribution = platform.platform()
    python_version = platform.python_version()

    # Print OS information with color
    print(Fore.YELLOW + "Operating System Information:" + Style.RESET_ALL)
    print(f"Name: {Fore.CYAN}{os_name}{Style.RESET_ALL}")
    print(f"Version: {Fore.CYAN}{os_version}{Style.RESET_ALL}")
    print(f"Machine: {Fore.CYAN}{machine}{Style.RESET_ALL}")
    print(f"Processor: {Fore.CYAN}{processor}{Style.RESET_ALL}")
    print(f"Node: {Fore.CYAN}{node}{Style.RESET_ALL}")
    print(f"Release: {Fore.CYAN}{os_release}{Style.RESET_ALL}")
    print(f"Distribution: {Fore.CYAN}{distribution}{Style.RESET_ALL}")
    print(f"Python Version: {Fore.CYAN}{python_version}{Style.RESET_ALL}")

def get_local_ip():
    # Get the local IP address
    local_ip = socket.gethostbyname(socket.gethostname())
    return local_ip

def get_public_ip():
    # Use an external service to fetch the public IP address
    try:
        response = requests.get("https://api.ipify.org")
        public_ip = response.text
    except requests.RequestException as e:
        print(Fore.RED + "Failed to retrieve public IP:", e + Style.RESET_ALL)
        public_ip = None
    return public_ip

def show_ip_addresses():
    local_ip = get_local_ip()
    public_ip = get_public_ip()

    # Print IP addresses with color
    print(Fore.YELLOW + "IP Addresses:" + Style.RESET_ALL)
    print(f"Local IP Address: {Fore.GREEN}{local_ip}{Style.RESET_ALL}")
    if public_ip:
        print(f"Public IP Address: {Fore.GREEN}{public_ip}{Style.RESET_ALL}")
    else:
        print(Fore.RED + "Unable to retrieve public IP address." + Style.RESET_ALL)

# Main function for searching PyPI and installing packages
def search_pypi(query):
    url = f"https://pypi.org/search/?q={query}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        package_results = soup.find_all('a', class_='package-snippet')
        packages = []
        for index, result in enumerate(package_results, start=1):
            package_name = result.find('span', class_='package-snippet__name').text.strip()
            package_description = result.find('p', class_='package-snippet__description').text.strip()
            package_versions = result.find('span', class_='package-snippet__version').text.strip()
            package_link = "https://pypi.org" + result['href']
            packages.append([index, package_name, package_versions, package_description, package_link])

        print(tabulate(packages, headers=["#", "Package Name", "Version", "Description", "Install Link"], tablefmt="grid"))
        
        # Prompt user to choose a package by number
        print("Enter the number of the package you want to install (or enter 0 to exit): ")
        choice = int(input())
        if choice == 0:
            return  # Exit the function
        elif 1 <= choice <= len(package_results):
            chosen_package = packages[choice - 1]
            package_name = chosen_package[1]
            print(f"Installing package: {package_name}")
            subprocess.run(["pip", "install", package_name])
        else:
            print("Invalid choice. Please enter a number within the range.")
        
        # After installing or selecting, prompt for a new query
        new_query = input("Enter a new package name to search for (or type 'exit' to quit): ")
        if new_query.lower() == 'exit':
            return  # Exit the function
        else:
            search_pypi(new_query)

    else:
        print("Failed to retrieve search results.")

def show_help():
    # Display script usage and help information with color
    print(Fore.YELLOW + "Usage: python script.py <package_name>" + Style.RESET_ALL)
    print(Fore.YELLOW + "Example: python script.py requests" + Style.RESET_ALL)
    print(Fore.YELLOW + "This script searches PyPI for the given package name and displays the search results." + Style.RESET_ALL)

# Check if command-line argument is provided
if len(sys.argv) > 1:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        show_help()
    else:
        query = sys.argv[1] 
        search_pypi(query)
else:
    # If no command-line argument is provided, display OS information and IP addresses
    show_os_info()
    show_ip_addresses()
    print('''
====================================================
          HELP : --help or -h
====================================================
    ''')

print ('''
======================================================
                    TEAM : BEN MHIDI 54
                    EDIT BY : DARK ADMIN
======================================================
''')
