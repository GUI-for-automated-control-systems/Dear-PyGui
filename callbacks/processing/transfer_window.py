import os

import dearpygui.dearpygui as dpg


def transfer(ssh_client):
    path_from = dpg.get_value('from')
    path_to = dpg.get_value('to')
    file_name = os.path.basename(path_from)

    if not path_to.endswith("/"):
        path_to += "/"

    path_to += file_name
    ssh_client.send_file_to_server(path_from, path_to)