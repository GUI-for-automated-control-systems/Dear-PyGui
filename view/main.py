import dearpygui.dearpygui as dpg
from ssh_processing.connect import SSHProcessing

WIDTH = 1000
HEIGHT = 600


ssh_manager = SSHProcessing()


dpg.create_context()
dpg.create_viewport(title='VMmanager', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()


with dpg.font_registry():
    default_font = dpg.add_font("../font/JetBrainsMono-Medium.ttf", 24)


def connect_ssh(manager):
    host = dpg.get_value(1)
    port = dpg.get_value(2)
    username = dpg.get_value(3)
    password = dpg.get_value(4)

    connected = manager.connect(host, port, username, password)
    if connected:
        dpg.set_value("text_widget", f'Connect to VM: True')
        dpg.configure_item("Monitoring", enabled=True)
        dpg.configure_item("Console", enabled=True)
        dpg.show_item('Monitoring')
        dpg.show_item('Console')
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
    dpg.configure_item(main_window, show=False)
    dpg.configure_item(console_window, show=False)
    dpg.set_primary_window(monitoring_window, True)


def open_main_window():
    dpg.configure_item(monitoring_window, show=False)
    dpg.configure_item(main_window, show=True)
    dpg.configure_item(console_window, show=False)
    dpg.set_primary_window(main_window, True)


def open_console_window():
    dpg.configure_item(monitoring_window, show=False)
    dpg.configure_item(main_window, show=False)
    dpg.configure_item(console_window, show=True)
    dpg.set_primary_window(console_window, True)


with dpg.window(show=False) as monitoring_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=open_main_window)


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
    dpg.add_input_text(hint='host', tag=1)
    dpg.add_input_int(default_value=22, tag=2)
    dpg.add_input_text(hint='username', tag=3)
    dpg.add_input_text(hint='password', tag=4)
    dpg.add_spacer(height=10)
    dpg.add_button(label="Connect", callback=lambda: connect_ssh(ssh_manager))
    dpg.add_spacer(height=30)

    with dpg.group(horizontal=True):
        monitoring_button = dpg.add_button(label="Monitoring", tag='Monitoring', callback=open_monitoring_window,
                                           enabled=False, show=False)
        console_button = dpg.add_button(label="Console", tag='Console', callback=open_console_window, enabled=False,
                                        show=False)

dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
