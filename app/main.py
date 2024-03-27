import dearpygui.dearpygui as dpg

from callbacks.switch_window.switch_window import (open_main_window,
                                                   open_console_window,
                                                   open_monitoring_window,
                                                   open_transfer_window)
from ssh_processing.SSHProcessing import SSHProcessing

from callbacks.processing.main_window import close, connect_ssh
from callbacks.processing.transfer_window import transfer, open_file_dialog, set_selected_file
from callbacks.processing.console_window import print_command_result

WIDTH = 1000
HEIGHT = 600

ssh = SSHProcessing()


dpg.create_context()
dpg.create_viewport(title='VMmanager', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()


with dpg.font_registry():
    default_font = dpg.add_font("../font/JetBrainsMono-Medium.ttf", 24)


with dpg.window(show=False) as monitoring_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=lambda: open_main_window(main_window,
                                                                   monitoring_window,
                                                                   transfer_window,
                                                                   console_window))

with dpg.window(show=False) as transfer_window:
    dpg.bind_font(default_font)

    dpg.add_button(label="Back", callback=lambda: open_main_window(main_window,
                                                                   monitoring_window,
                                                                   transfer_window,
                                                                   console_window))

    dpg.add_spacer(height=10)
    dpg.add_button(label="Browse", callback=open_file_dialog)
    dpg.add_input_text(default_value='', hint='From', tag='from', readonly=True)
    dpg.add_input_text(default_value='', hint='To', tag='to')
    dpg.add_spacer(height=30)
    dpg.add_button(label='Transfer', callback=lambda: transfer(ssh))


with dpg.file_dialog(directory_selector=False, show=False, callback=set_selected_file, id="file_dialog_id", width=700,
                     height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255))
    dpg.add_file_extension(".py", color=(0, 255, 0, 255))


with dpg.window(show=False) as console_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=lambda: open_main_window(main_window, monitoring_window, transfer_window, console_window))
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
        monitoring_button = dpg.add_button(label="Monitoring", callback=lambda: open_monitoring_window(main_window,
                                                                                                       monitoring_window,
                                                                                                       transfer_window,
                                                                                                       console_window))

        console_button = dpg.add_button(label="Console", callback=lambda: open_console_window(main_window,
                                                                                              monitoring_window,
                                                                                              transfer_window,
                                                                                              console_window))

        transfer_button = dpg.add_button(label="Transfer file", callback=lambda: open_transfer_window(main_window,
                                                                                                      monitoring_window,
                                                                                                      transfer_window,
                                                                                                      console_window))

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
