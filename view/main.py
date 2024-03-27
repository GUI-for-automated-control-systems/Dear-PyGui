import dearpygui.dearpygui as dpg
from service.SSHProcessing import SSHProcessing

from callbacks.main_window import close, connect_ssh
from callbacks.transfer_window import transfer
from callbacks.console_window import print_command_result

WIDTH = 1000
HEIGHT = 600

ssh = SSHProcessing()


dpg.create_context()
dpg.create_viewport(title='VMmanager', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()


with dpg.font_registry():
    default_font = dpg.add_font("../font/JetBrainsMono-Medium.ttf", 24)


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
    dpg.add_button(label='Transfer', callback=lambda: transfer(ssh))


with dpg.window(show=False) as console_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=open_main_window)
    dpg.add_spacer(height=10)
    dpg.add_text('Command line mod')
    dpg.add_input_text(hint='command', tag='command')
    dpg.add_spacer(height=10)
    dpg.add_button(label='Execute', callback=lambda: print_command_result(ssh))
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
        dpg.add_button(label="Connect", callback=lambda: connect_ssh(ssh))
        dpg.add_button(label="Exit", tag='Exit', callback=lambda: close(ssh), show=False)
    dpg.add_spacer(height=30)

    with dpg.group(horizontal=True, tag='monitoring', show=False):
        monitoring_button = dpg.add_button(label="Monitoring", callback=open_monitoring_window)
        console_button = dpg.add_button(label="Console", callback=open_console_window)
        transfer_button = dpg.add_button(label="Transfer file", callback=open_transfer_window)

    with dpg.group(horizontal=False, tag='info', show=False):
        dpg.add_separator()
        dpg.add_text('Distributive')
        dpg.add_separator()
        dpg.add_text(tag='distributive')
        dpg.add_separator()
        dpg.add_text('Memory')
        dpg.add_separator()
        dpg.add_text(tag='memory')
        dpg.add_separator()
        dpg.add_text('CPU')
        dpg.add_separator()
        dpg.add_text(tag='cpu')
        dpg.add_separator()
        dpg.add_text('Uptime')
        dpg.add_separator()
        dpg.add_text(tag='uptime')

dpg.set_primary_window(main_window, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
