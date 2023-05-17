import tkinter as tk
import subprocess
import platform
import os
from tkinter import filedialog
from tkinter import ttk
import re
import time

def check_dependency(dependency):
    try:
        subprocess.check_output([dependency, '-h'])
        return True
    except OSError:
        return False

def select_file():
    file_path = filedialog.asksaveasfilename(
        title="Сохранить Handshake",
        defaultextension=".cap",
        filetypes=[("Capture files", "*.cap")]
    )
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def is_apt_available():
    try:
        subprocess.check_output(['apt', '--version'])
        return True
    except OSError:
        return False
def is_dnf_available():
    try:
        subprocess.check_output(['dnf', '--version'])
        return True
    except OSError:
        return False
def is_yum_available():
    try:
        subprocess.check_output(['yum', '--version'])
        return True
    except OSError:
        return False
def is_pacman_available():
    try:
        subprocess.check_output(['pacman', '--version'])
        return True
    except OSError:
        return False

def install_aircrack_ng():
    echofail = ""
    echo = "echo Установка зависимостей..."
    if is_apt_available():
        command = "sudo apt-get install -y aircrack-ng"
    elif is_dnf_available():
        command = "sudo dnf install -y aircrack-ng"
    elif is_yum_available():
        command = "sudo yum install -y aircrack-ng"
    elif is_pacman_available():
        command = "sudo pacman -S --noconfirm aircrack-ng"
    else:
       echofail = "echo Менеджер пакетов не определен или не поддерживается"
    commands = [
        echo,
        command,
        echofail
    ]
    command_string = ';'.join(commands)
    process = subprocess.Popen(command_string, shell=True)
    process.wait
    time.sleep(3)
    print("Подождите немного, программа запускается...")
    time.sleep(2)
       
'''
def install_aircrack_ng():
    system = platform.system()
    if system == "Linux":
        package_manager = subprocess.check_output(['apt', 'dnf', 'yum', 'pacman']).decode().strip()
        if package_manager == "/usr/bin/apt":
            command = "sudo apt-get install -y aircrack-ng airmon-ng airodump-ng aireplay-ng"
        elif package_manager == "/usr/bin/dnf" or package_manager == "/usr/bin/yum":
            command = "sudo dnf install -y aircrack-ng airmon-ng airodump-ng aireplay-ng" if package_manager == "/usr/bin/dnf" else "sudo yum install -y aircrack-ng airmon-ng airodump-ng aireplay-ng"
        elif package_manager == "/usr/bin/pacman":
            command = "sudo pacman -S --noconfirm aircrack-ng airmon-ng airodump-ng aireplay-ng"
        else:
            print("Unable to determine package manager.")
            return
    elif system == "Darwin":
        command = "brew install aircrack-ng airmon-ng airodump-ng aireplay-ng"
    else:
        print(f"Неподдерживаемая система: {system}")
        return
    echo = "Установка зависимостей..."
    subprocess.Popen("{}; {}").format(echo, command)
'''
def get_interface_list():
    result = subprocess.run(["iwconfig"], capture_output=True, text=True)
    interfaces = re.findall(r"(\w+)\s+IEEE", result.stdout)
    return interfaces

def wireless_interfaces():
    try:
        output = subprocess.check_output(['ifconfig']).decode('utf-8')
        interfaces = []
        lines = output.split('\n')
        for line in lines:
            if 'wlp' in line or 'wlan' in line:
                interface = line.split(' ')[0].rstrip(':')
                interfaces.append(interface)
        return interfaces
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []


def get_default_terminal_command():
    # Try to get the default terminal command on Linux
    # based on the DE (Desktop Environment) or WM (Window Manager) in use
    de = os.environ.get('DESKTOP_SESSION')
    wm = os.environ.get('XDG_CURRENT_DESKTOP')

    if de:
        if 'gnome' in de.lower():
            return 'gnome-terminal'
        elif 'kde' in de.lower():
            return 'konsole'
        elif 'plasma' in de.lower():
            return 'konsole'
        elif 'xfce' in de.lower():
            return 'xfce4-terminal'
        elif 'cinnamon' in de.lower():
            try:
                return 'gnome-terminal'
            except Exception as e:
                pass
            else:
                return 'xfce4-terminal'
        elif 'mate' in de.lower():
            return 'mate-terminal'
        elif 'lxde' in de.lower():
            return 'lxterminal'
        elif 'lxqt' in de.lower():
            return 'qterminal'
        elif 'budgie' in de.lower():
            try:
                return 'gnome-terminal'
            except Exception as e:
                pass
            else:
                return 'tilix'
        elif 'deepin' in de.lower():
            return 'deepin-terminal'
    elif wm:
        if 'gnome' in wm.lower():
            return 'gnome-terminal'
        elif 'kde' in wm.lower():
            return 'konsole'
        elif 'plasma' in wm.lower():
            return 'konsole'
        elif 'xfce' in wm.lower():
            return 'xfce4-terminal'
        elif 'cinnamon' in wm.lower():
            try:
                return 'gnome-terminal'
            except Exception as e:
                pass
            else:
                return 'xfce4-terminal'
        elif 'cinnamon' in wm.lower():
            return 'gnome-terminal'
        elif 'mate' in wm.lower():
            return 'mate-terminal'
        elif 'lxde' in wm.lower():
            return 'lxterminal'
        elif 'lxqt' in wm.lower():
            return 'qterminal'
        elif 'budgie' in wm.lower():
            try:
                return 'gnome-terminal'
            except Exception as e:
                pass
            else:
                return 'tilix'
        elif 'deepin' in wm.lower():
            return 'deepin-terminal'
    else:
    # If we couldn't determine the default terminal command, fall back to 'x-terminal-emulator'
        return 'x-terminal-emulator'

def open_terminal(command):
    terminal = get_default_terminal_command()
    subprocess.Popen([terminal, '-e', 'bash', '-c', command])

install_choice = input("Хотите ли вы установить зависимости? (y/n): ")
if install_choice.lower() == 'y':
    install_aircrack_ng()

def update_interface_list():
    interfaces = get_interface_list()
    interface_var.set(interfaces[0])
    interface_list = get_interface_list()
    interface_combobox['values'] = interface_list
    if interface_list:
        interface_var.set(interface_list[0])


def start_monitor_mode():
    interface = interface_var.get()
    command = f"sudo airmon-ng start {interface}"
    terminal = get_default_terminal_command()
    cmd = subprocess.Popen([terminal, '-e', 'bash', '-c', command])
    cmd.wait()
    update_interface_list()


def stop_monitor_mode():
    interface = interface_var.get().split()[0]
    command = f"sudo airmon-ng stop {interface}"
    terminal = get_default_terminal_command()
    cmd = subprocess.Popen([terminal, '-e', 'bash', '-c', command])
    cmd.wait()
    update_interface_list()

def start_packet_capture():
    interface = interface_combobox.get()
    if not interface:
        tk.messagebox.showwarning("Ошибка!", "Пожалуйста выбе�