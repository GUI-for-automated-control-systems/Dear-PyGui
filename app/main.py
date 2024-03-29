import time

import dearpygui.dearpygui as dpg
import threading

from callbacks.switch_window.switch_window import (open_main_window,
                                                   open_console_window,
                                                   open_monitoring_window,
                                                   open_transfer_window)
from ssh_processing.SSHProcessing import SSHProcessing

from callbacks.processing.main_window import close, connect_ssh
from callbacks.processing.transfer_window import transfer, open_file_dialog, set_selected_file
from callbacks.processing.console_window import print_command_result

WIDTH = 1680
HEIGHT = 1080

ssh = SSHProcessing()


dpg.create_context()
dpg.create_viewport(title='VMmanager', width=WIDTH, height=HEIGHT)
dpg.setup_dearpygui()


def monitoring():
    time.sleep(10)
    dpg.show_item('progress')
    dpg.hide_item('loading_on_monitor')

    global ssh
    while True:
        output = ssh.get_top_output()
        cpu = 0.0
        mem = 0.0
        top = ''
        if output:
            for line in output[7:]:
                top += line
                mem += float(line.split()[9])
                cpu += float(line.split()[8])
                dpg.set_value('cpu_bar', cpu / 100)
                dpg.set_value('mem_bar', mem / 100)
        dpg.set_value('top', top)
        mem = 0
        cpu = 0


with dpg.font_registry():
    default_font = dpg.add_font("../font/JetBrainsMono-Medium.ttf", 20)


with dpg.window(show=False, label='Monitoring') as monitoring_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=lambda: open_main_window(main_window,
                                                                   monitoring_window,
                                                                   transfer_window,
                                                                   console_window))
    dpg.add_text(default_value='Description: shows a real-time view of running processes in Linux and displays kernel-managed tasks.')
    dpg.add_separator()
    dpg.add_loading_indicator(tag='loading_on_monitor')
    with dpg.group(tag='progress', show=False):
        dpg.add_progress_bar(default_value=0.0, tag='cpu_bar', overlay='cpu')
        dpg.add_progress_bar(default_value=0.0, tag='mem_bar', overlay='mem')
        dpg.add_text(default_value='    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND')
    dpg.add_text(default_value='', tag='top')

with dpg.window(show=False, label='Transfer files') as transfer_window:
    dpg.bind_font(default_font)

    dpg.add_button(label="Back", callback=lambda: open_main_window(main_window,
                                                                   monitoring_window,
                                                                   transfer_window,
                                                                   console_window))
    dpg.add_text('Description: Easily transfer files from your local machine to a remote server.')
    dpg.add_separator()

    dpg.add_spacer(height=10)
    dpg.add_button(label="Browse", callback=open_file_dialog)
    dpg.add_input_text(default_value='', hint='From', tag='from', readonly=True)
    dpg.add_input_text(default_value='/root/file', hint='To', tag='to')
    dpg.add_spacer(height=30)
    dpg.add_button(label='Transfer', callback=lambda: transfer(ssh))
    dpg.add_text(default_value='', tag='transfer_message')


with dpg.file_dialog(directory_selector=False, show=False, callback=set_selected_file, id="file_dialog_id", width=700,
                     height=400):
    dpg.add_file_extension(".*")
    dpg.add_file_extension("", color=(150, 255, 150, 255))
    dpg.add_file_extension("Source files (*.cpp *.h *.hpp){.cpp,.h,.hpp}", color=(0, 255, 255, 255))
    dpg.add_file_extension(".h", color=(255, 0, 255, 255))
    dpg.add_file_extension(".py", color=(0, 255, 0, 255))


with dpg.window(show=False, label='Console') as console_window:
    dpg.bind_font(default_font)
    dpg.add_button(label="Back", callback=lambda: open_main_window(main_window, monitoring_window, transfer_window, console_window))
    dpg.add_spacer(height=10)
    dpg.add_text('Command line mod')
    dpg.add_separator()
    dpg.add_text('Description: Interactive command-line interface for system control and monitoring. '
                 '\nWarning: Only command output is returned; commands opening files like nano or vi may disrupt '
                 'scripts.'
                 '\nExercise caution to prevent unintended consequences.')
    dpg.add_separator()
    dpg.add_spacer(height=10)
    dpg.add_input_text(hint='command', tag='command')
    dpg.add_spacer(height=10)
    dpg.add_button(label='Execute', callback=lambda: print_command_result(ssh))
    dpg.add_spacer(height=10)
    dpg.add_text('', tag='command_res')


with dpg.window(show=True, label='Connect', width=500, height=1080) as main_window:
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

    dpg.add_loading_indicator(tag='loading_on_main', show=False)
    with dpg.group(horizontal=False, tag='info', show=False):
        dpg.add_spacer(height=30)
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

dpg.show_viewport()

thread = threading.Thread(target=monitoring)
thread.start()

dpg.start_dearpygui()
dpg.destroy_context()
