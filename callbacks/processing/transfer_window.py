import os

import dearpygui.dearpygui as dpg


def open_file_dialog(sender, app_data):
    dpg.show_item("file_dialog_id")


def set_selected_file(sender, app_data):
    selected_file_path = list(app_data['selections'].values())[0]
    dpg.set_value("from", selected_file_path)


def transfer(ssh_client):
    path_from = dpg.get_value('from')
    path_to = dpg.get_value('to')
    file_name = os.path.basename(path_from)

    if not path_to.endswith("/"):
        path_to += "/"

    path_to += file_name
    ssh_client.send_file_to_server(path_from, path_to)