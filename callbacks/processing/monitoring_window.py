import dearpygui.dearpygui as dpg
import time


def monitoring(ssh):
    time.sleep(10)
    while True:
        output = ssh.get_top_output()
        top = ''
        if output:
            for line in output[6:28]:
                top += line.strip() + '\n'
        dpg.set_value('top', top)
