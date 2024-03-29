import dearpygui.dearpygui as dpg
import time

# Создание окна и прогресс-баров
with dpg.window(label="Tutorial") as main:
    cpu_bar = dpg.add_progress_bar(default_value=0.1, label='CPU Usage')
    mem_bar = dpg.add_progress_bar(default_value=0.1, label='Memory Usage')

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()

# Функция для плавного изменения значений прогресс-баров
def smooth_update():
    cpu_target = 0.8  # Задаем целевые значения
    mem_target = 0.6

    cpu_current = dpg.get_value(cpu_bar)  # Получаем текущие значения
    mem_current = dpg.get_value(mem_bar)

    # Плавно увеличиваем значения до целевых
    while cpu_current < cpu_target or mem_current < mem_target:
        cpu_current += 0.01  # Инкремент значения
        mem_current += 0.01
        dpg.set_value(cpu_bar, min(cpu_current, cpu_target))  # Устанавливаем новое значение
        dpg.set_value(mem_bar, min(mem_current, mem_target))
        time.sleep(0.02)  # Делаем паузу для эффекта плавности

# Выполняем плавное обновление
smooth_update()

dpg.set_primary_window(main, True)
dpg.show_viewport()
dpg.start_dearpygui()
