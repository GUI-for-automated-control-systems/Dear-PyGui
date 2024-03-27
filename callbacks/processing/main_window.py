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
        dpg.set_value("text_widget", f'Connect to VM: True')   # <------------------------[
        dpg.show_item('monitoring')
        dpg.show_item('Exit')

        dist, mem, cpu, uptime = ssh_client.get_vm_info()
        dpg.set_value('distributive', dist)
        dpg.set_value('memory', mem)
        dpg.set_value('cpu', cpu)
        dpg.set_value('uptime', uptime)
        dpg.show_item('info')

        while True:
            output = ssh_client.get_top_output()
            if output:
                for line in output[7:28]:
                    dpg.set_value('top', line.strip())
            else:
                print("Failed to get top output. Retrying...")

    else:
        dpg.set_value("text_widget", f'Connect to VM: False')
