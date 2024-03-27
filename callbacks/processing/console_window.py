import dearpygui.dearpygui as dpg


def print_command_result(ssh_client):
    command = dpg.get_value('command')
    result = ssh_client.execute_command(command)
    if result is not None:
        dpg.set_value('command_res', result)
    else:
        print("Command execution failed.")