import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Tutorial") as main:
    dpg.add_loading_indicator()

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.set_primary_window(main, True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()