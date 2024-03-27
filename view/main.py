import os

import dearpygui.dearpygui as dpg
from service.SSHProcessing import SSHProcessing

WIDTH = 1000
HEIGHT = 600

ssh_manager = SSHProcessing()


dpg.create_context()
dpg.create_viewport(title='VMmanager', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()


with dpg.font_registry():
    default_font = dpg.add_font("../font/JetBrainsMono-Medium.ttf", 24)


def transfer():
    path_from = dpg.get_value('from')
    path_to = dpg.get_value('to')
    file_name = os.path.basename(path_from)

    if not path_to.endswith("/"):
        path_to += "/"

    path_to += file_name
    ssh_manager.send_file_to_server(path_from, path_to)


def close():
    global ssh_manager
    ssh_manager.close()
    dpg.hide_item('monitoring')
    dpg.hide_item('Exit')
    dpg.hide_item('info')
    dpg.set_value(1, '')
    dpg.set_value("text_widget", f'Connect to VM: False')


def connect_ssh(manager: SSHProcessing):
    host = dpg.get_value(1)
    port = dpg.get_value(2)
    username = dpg.get_value(3)
    password = dpg.get_value(4)

    connected = manager.connect(host, port, username, password)
    if connected:
        dpg.set_value("text_widget", f'Connect to VM: True')   # <------------------------[
        dpg.show_item('monitoring')
        dpg.show_item('Exit')
        dist, mem, cpu, uptime = manager.get_vm_info()
        dpg.set_value('distributive', dist)
        dpg.set_value('memory', mem)
        dpg.set_value('cpu', cpu)
        dpg.set_value('uptime', uptime)
        dpg.show_item('info')

    else:
        dpg.set_value("text_widget", f'Connect to VM: False')


def print_command_result():
    command = dpg.get_value('command')
    result = ssh_manager.execute_command(command)
    if result is not None:
        dpg.set_value('command_res', result)
    else:
        print("Command execution failed.")


def open_monitoring_window():
    dpg.configure_item(monitoring_window, show=True)
    dpg.configure_item(transfer_window, show=False)
    dpg.configure_item(main_window, show=False)
    dpg.configure_item(console_window, show=False)
    dpg.set_primary_window(monitoring_window, True)


def open_main_window():
    dpg.configure_item(monitoring_window, show=False)
    dpg.configure_item(transfer_window, show=False)
    dpg.configure_item(main_window, show=True)
    dpg.configure_item(console_window, show=False)
    dpg.set_primary_window(main_window, True)


def open_transfer_window():
    dpg.configure_item(monitoring_window, show=False)
    dpg.configure_item(main_window, show=False)
    dpg.configure_item(console_window, show=False)
    dpg.configure_item(transfer_window, show=True)
    dpg.set_primary_window(transfer_window, True)


def open_console_window():
    dpg.configure_item(transfer_window, show=False)
    dpg.configure_item(monitoring_window, show=False)
    dpg.configure_item(main_window, show=False)
    dpg.configure_item(console_window, show=True)
    dpg.set_primary_window(console_window, True)


with dpg.window(show=False) as monitoring_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=open_main_window)


with dpg.window(show=False) as transfer_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=open_main_window)
    dpg.add_spacer(height=10)
    dpg.add_input_text(default_value='/home/egor/python-app/test.py', hint='From', tag='from')
    dpg.add_input_text(default_value='/root', hint='To', tag='to')
    dpg.add_spacer(height=30)
    dpg.add_button(label='Transfer', callback=transfer)


with dpg.window(show=False) as console_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=open_main_window)
    dpg.add_spacer(height=10)
    dpg.add_text('Command line mod')
    dpg.add_input_text(hint='command', tag='command')
    dpg.add_spacer(height=10)
    dpg.add_button(label='Execute', callback=print_command_result)
    dpg.add_spacer(height=30)
    dpg.add_text('Result:')
    dpg.add_text('', tag='command_res')


with dpg.window() as main_window:
    dpg.bind_font(default_font)
    text_widget = dpg.add_text(f'Connect to VM:', tag="text_widget")
    dpg.add_spacer(height=10)
    dpg.add_input_text(default_value='192.168.40.16', hint='host', tag=1)
    dpg.add_input_int(default_value=22, tag=2)
    dpg.add_input_text(default_value='root', hint='username', tag=3)
    dpg.add_input_text(hint='password', tag=4)
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_button(label="Connect", callback=lambda: connect_ssh(ssh_manager))
        dpg.add_button(label="Exit", tag='Exit', callback=close, show=False)
    dpg.add_spacer(height=30)

    with dpg.group(horizontal=True, tag='monitoring', show=False):
        monitoring_button = dpg.add_button(label="Monitoring", callback=open_monitoring_window)
        console_button = dpg.add_button(label="Console", callback=open_console_window)
        transfer_button = dpg.add_button(label="Transfer file", callback=open_transfer_window)

    with dpg.group(horizontal=False, tag='info', show=False):
        dpg.add_separator()
        dpg.add_text('Distributive')
        dpg.add_separator()
        dpg.add_text('', tag='distributive')
        dpg.add_separator()
        dpg.add_text('Memory')
        dpg.add_separator()
        dpg.add_text('', tag='memory')
        dpg.add_separator()
        dpg.add_text('CPU')
        dpg.add_separator()
        dpg.add_text('', tag='cpu')
        dpg.add_separator()
        dpg.add_text('Uptime')
        dpg.add_separator()
        dpg.add_text('', tag='uptime')

dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
