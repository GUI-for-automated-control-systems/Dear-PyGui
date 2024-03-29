import dearpygui.dearpygui as dpg


def close(ssh_client):
    ssh_client.close()
    dpg.hide_item('monitoring')
    dpg.hide_item('Exit')
    dpg.hide_item('info')
    dpg.set_value(1, '')
    dpg.set_value("text_widget", f'Connect to VM: False')


def connect_ssh(ssh_client):
    host = dpg.get_value(1)
    port = dpg.get_value(2)
    username = dpg.get_value(3)
    password = dpg.get_value(4)

    connected = ssh_client.connect(host, port, username, password)
    if connected:
        dpg.show_item('loading_on_main')
        dpg.set_value("text_widget", f'Connect to VM: True')   # <------------------------[
        dpg.show_item('monitoring')
        dpg.show_item('Exit')
    else:
        dpg.set_value("text_widget", f'Connect to VM: False')
