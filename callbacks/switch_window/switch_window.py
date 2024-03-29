import dearpygui.dearpygui as dpg


def open_monitoring_window(main_window, monitoring_window, transfer_window, console_window):
    dpg.configure_item(monitoring_window, show=True)
    dpg.configure_item(transfer_window, show=True)
    dpg.configure_item(main_window, show=True)
    dpg.configure_item(console_window, show=True)
    # dpg.set_primary_window(monitoring_window, True)


def open_main_window(main_window, monitoring_window, transfer_window, console_window):
    dpg.configure_item(monitoring_window, show=True)
    dpg.configure_item(transfer_window, show=True)
    dpg.configure_item(main_window, show=True)
    dpg.configure_item(console_window, show=False)
    # dpg.set_primary_window(main_window, True)


def open_transfer_window(main_window, monitoring_window, transfer_window, console_window):
    ...
    dpg.configure_item(monitoring_window, show=True)
    dpg.configure_item(main_window, show=True)
    dpg.configure_item(console_window, show=True)
    dpg.configure_item(transfer_window, show=True)
    # dpg.set_primary_window(transfer_window, True)


def open_console_window(main_window, monitoring_window, transfer_window, console_window):
    dpg.configure_item(transfer_window, show=True)
    dpg.configure_item(monitoring_window, show=True)
    dpg.configure_item(main_window, show=True)
    dpg.configure_item(console_window, show=True)
    # dpg.set_primary_window(console_window, True)