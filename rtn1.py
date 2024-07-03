import os
import importlib
import glob
import time
import signal
import sys


banner = """
______     _                        _            __   _____ 
| ___ \   | |                      | |          /  | |  _  |
| |_/ /___| |_ _ __ ___  _ __   ___| |_  __   __`| | | |/' |
|    // _ \ __| '__/ _ \| '_ \ / _ \ __| \ \ / / | | |  /| |
| |\ \  __/ |_| | | (_) | | | |  __/ |_   \ V / _| |_\ |_/ /
\_| \_\___|\__|_|  \___/|_| |_|\___|\__|   \_/  \___(_)___/ 
"""

def clear():
    if os.name == 'nt': 
        os.system('cls')
    else:  
        os.system('clear')

def loading_animation():
    for i in range(1, 10):
        print("\033[31m" + " LOADING" + "\33[0m")
        print('#' * i + '.' * (9 - i))
        time.sleep(0.03) 
        clear()
def signal_handler(sig, frame):
    print("\nExecution stopped by user.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def start():
    loading_animation()
    clear()
    print(banner)

start()
prompt = "rt1> "

class Framework:
    def __init__(self):
        self.exploits = {}
        self.loaded_exploit = None
        self.load_all_exploit_descriptions()

    def load_module(self, module_type, module_path):
        try:
            if not module_path.endswith('.py'):
                module_path += '.py'
            module_name = module_path.split("/")[-1].split(".")[0]
            module = importlib.import_module(f"{module_path.replace('/', '.')[:-3]}")
            if module_type == "exploit":
                self.exploits[module_name] = module
                self.loaded_exploit = module.Exploit()
                global prompt
                prompt = f"rt1 ({module_path})> "
            print(f"Loaded {module_type.capitalize()} module '{module_name}' successfully.")
        except ImportError as e:
            print(f"Error loading {module_type} module '{module_path}': {e}")

    def show_options(self):
        if self.loaded_exploit:
            print("Available options:")
            for option, desc in self.loaded_exploit.options.items():
                value = getattr(self.loaded_exploit, option.lower(), "")
                print(f"  {option}: {value}    {desc}")

    def set_option(self, option, value):
        if self.loaded_exploit and hasattr(self.loaded_exploit, option.lower()):
            setattr(self.loaded_exploit, option.lower(), value)
            print(f"Set {option} to {value}")

    def run_exploit(self):
        if self.loaded_exploit:
            try:
                self.loaded_exploit.run()
            except Exception as e:
                print(f"Error: {e}")

    def load_all_exploit_descriptions(self):
        self.exploit_descriptions = {}
        exploit_files = glob.glob("exploits/*.py")
        for exploit_file in exploit_files:
            module_name = exploit_file.replace("/", ".")[:-3]
            try:
                module = importlib.import_module(module_name)
                description = getattr(module.Exploit, "description", "No description available.")
                self.exploit_descriptions[module_name] = description
            except ImportError as e:
                print(f"Error loading exploit '{module_name}': {e}")

    def search_exploits(self, search_term):
        print("Search results:")
        found = False
        for module_name, description in self.exploit_descriptions.items():
            if search_term.lower() in description.lower():
                highlighted_description = description.replace(
                    search_term, f"\033[44m{search_term}\033[0m"
                )
                print(f"{module_name}: {highlighted_description}")
                found = True
        if not found:
            print(f"No exploits found for '{search_term}'.")

framework = Framework()

while True:
    command = input(prompt).strip().lower()

    if command == "clear":
        clear()
    elif command == "banner":
        clear()
        print(banner)
    elif command.startswith("load exploit "):
        _, _, module_path = command.split(maxsplit=2)
        framework.load_module("exploit", module_path)
    elif command == "options":

        framework.show_options()
    elif command.startswith("set "):
        _, option, value = command.split(maxsplit=2)
        framework.set_option(option.upper(), value)
    elif command == "run":
        framework.run_exploit()

    elif command.startswith("search "):
        _, search_term = command.split(maxsplit=1)
        framework.search_exploits(search_term)
    elif command == "help":
        print("""
Available commands:
    clear            - Clear the console
    banner           - Show the banner
    load exploit     - Load an exploit module (e.g., load exploit exploits/reverse_tcp)
    options          - Show available options for the loaded exploit
    set              - Set an option for the loaded exploit (e.g., set LHOST 192.168.1.100)
    run              - Run the loaded exploit
    search           - Search for exploits (e.g., search reverse)
    help             - Show this help message
    exit             - Exit the framework
""")
    elif command == "exit":
        break
    else:
        print("Invalid command. Type 'help' for available commands.")
