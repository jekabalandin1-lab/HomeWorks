from ursina import *
import random
import winsound  # Для звуків носа та скримера
import threading  # Щоб звук скримера не фризив гру

app = Ursina()

# Налаштування вікна
window.title = "Five Nights at Raven's 3D - v2.7"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False

# Ігрові змінні
game_started = False
game_over = False
power = 100.0
time_hour = 0
doors_closed = False
vent_closed = False
cameras_open = False
jumpscare_active = False
current_cam = "1A"
session_id = 0  # Захист від накладання таймерів при перезапуску

# Позиції аніматроніків
animatronics = {
    "Raven": "1A",
    "Bonzo": "1A",
    "Technician": "1B"
}

# Текст для важливої інформації
info_label = Text(text="", position=(-0.4, 0.4), scale=2, color=color.red)

# --- 3D ОФІС ---
floor = Entity(model='cube', color=color.Color(0.1, 0.1, 0.1, 1), scale=(20, 1, 20), y=-5, z=0)
ceiling = Entity(model='cube', color=color.Color(0.15, 0.15, 0.15, 1), scale=(20, 1, 20), y=5, z=0)
wall_front = Entity(model='cube', color=color.dark_gray, scale=(20, 10, 1), z=10)
wall_left = Entity(model='cube', color=color.gray, scale=(1, 10, 20), x=-10, z=0)
wall_right = Entity(model='cube', color=color.gray, scale=(1, 10, 20), x=10, z=0)

# Декор офісу (Лівий плакат)
decor_stripe = Entity(model='cube', color=color.red, scale=(20, 0.5, 1.1), y=0, z=9.9)
poster = Entity(model='quad', color=color.black, scale=(3, 4), x=-4, y=1, z=9.8)
poster_text = Text(text="RAVEN", scale=1.5, position=(-0.23, 0.1), color=color.white, parent=poster)

# --- ПАСХАЛКА: ПЛАКАТ С БОБРОМ І ПИЩАЩИМ НОСОМ ---
beaver_poster = Entity(model='quad', color=color.Color(0.4, 0.25, 0.15, 1), scale=(3, 4), x=4, y=1, z=9.8)
beaver_text = Text(text="БОБЕР", scale=1.5, position=(-0.23, 0.3), color=color.white, parent=beaver_poster)
beaver_nose = Entity(model='sphere', color=color.black, scale=(0.3, 0.3, 0.3), x=4, y=0.6, z=9.6, collider='box')


def honk_beaver_nose():
    if not game_started or game_over or cameras_open: return
    print_info("ПІП!")
    try:
        winsound.Beep(1000, 150)
    except:
        pass


beaver_nose.on_click = honk_beaver_nose

# Вентилятор та елементи захисту
vent_hole = Entity(model='cube', color=color.black, scale=(0.2, 3, 3), x=9.9, y=-3, z=2)
table = Entity(model='cube', color=color.Color(0.3, 0.2, 0.1, 1), scale=(8, 2, 4), x=0, y=-4, z=5)
monitor = Entity(model='cube', color=color.black, scale=(3, 2, 0.5), x=0, y=-2.5, z=4.5)
monitor_screen = Entity(model='cube', color=color.Color(0, 0.1, 0.2, 1), scale=(2.8, 1.8, 0.1), x=0, y=-2.5, z=4.4)

fan_base = Entity(model='cube', color=color.black, scale=(0.4, 0.8, 0.4), x=2.5, y=-3, z=4.5)
fan_blade = Entity(model='cube', color=color.dark_gray, scale=(1.2, 0.2, 0.1), x=2.5, y=-2.2, z=4.3)

left_door = Entity(model='cube', color=color.light_gray, scale=(1, 8, 4), x=-9.5, y=7, z=0)
vent_gate = Entity(model='cube', color=color.light_gray, scale=(0.5, 3, 3), x=9.5, y=5, z=2)

# --- ІНТЕРФЕЙС ТА ПЛАНШЕТ КАМЕР ---
ui_office = Entity(parent=camera.ui, enabled=False)
power_text = Text(parent=ui_office, text="", position=(-0.8, 0.45), scale=2)
time_text = Text(parent=ui_office, text="", position=(0.6, 0.45), scale=2)

btn_door = Button(parent=ui_office, text="Двері Ліві", color=color.azure, scale=(0.2, 0.06), position=(-0.6, -0.4))
btn_vent = Button(parent=ui_office, text="Вентиляція", color=color.azure, scale=(0.2, 0.06), position=(-0.35, -0.4))
btn_tablet = Button(parent=ui_office, text="ПЛАНШЕТ", color=color.orange, scale=(0.25, 0.08), position=(0.5, -0.4))

ui_tablet = Entity(parent=camera.ui, enabled=False)
tablet_bg = Panel(parent=ui_tablet, color=color.Color(0, 0, 0, 0.9), scale=(1.3, 0.75), position=(0, 0.05))
cam_title = Text(parent=ui_tablet, text="", position=(-0.5, 0.35), scale=2.5, color=color.green)
cam_screen_text = Text(parent=ui_tablet, text="", position=(-0.5, 0.2), scale=1.8, color=color.white)

cam_buttons = {}
cam_positions = {"1A": (0.4, 0.2), "1B": (0.4, 0.0), "2A": (0.3, -0.2), "2B": (0.5, -0.2)}

# --- ГОЛОВНЕ МЕНЮ ГРИ ---
ui_menu = Entity(parent=camera.ui, enabled=True)
menu_bg = Panel(parent=ui_menu, color=color.black, scale=(2, 2))
menu_title = Text(parent=ui_menu, text="FIVE NIGHTS\nAT RAVEN'S", scale=4, position=(-0.5, 0.25), color=color.red)

btn_start = Button(parent=ui_menu, text="Нова гра", color=color.dark_gray, scale=(0.3, 0.07), position=(-0.4, -0.1))
btn_exit = Button(parent=ui_menu, text="Вихід", color=color.dark_gray, scale=(0.3, 0.07), position=(-0.4, -0.22))


def start_game():
    global game_started, session_id
    game_started = True
    session_id += 1  # Створюємо унікальний ID для цієї сесії гри
    ui_menu.enabled = False
    ui_office.enabled = True

    mouse.locked = False
    mouse.visible = True

    time_text.text = f"Час: {time_hour}:00 AM"
    invoke(advance_time, session_id, delay=25)


btn_start.on_click = start_game
btn_exit.on_click = application.quit

# --- НОВИЙ ЕКРАН GAME OVER (З КНОПКОЮ ПЕРЕЗАПУСКУ) ---
ui_game_over = Entity(parent=camera.ui, enabled=False)
game_over_bg = Panel(parent=ui_game_over, color=color.red, scale=(2, 2))
game_over_title = Text(parent=ui_game_over, text="☠ GAME OVER ☠", scale=5, origin=(0, 0), position=(0, 0.25),
                       color=color.black)
game_over_reason = Text(parent=ui_game_over, text="", scale=1.8, origin=(0, 0), position=(0, 0.05), color=color.white)
btn_retry = Button(parent=ui_game_over, text="Грати знову", color=color.dark_gray, scale=(0.3, 0.07),
                   position=(0, -0.2))


def restart_game():
    global game_over, game_started, power, time_hour, doors_closed, vent_closed, cameras_open, current_cam, animatronics, session_id

    ui_game_over.enabled = False  # Ховаємо екран смерті

    # Скидаємо всі параметри гри
    game_over = False
    game_started = True
    session_id += 1  # Оновлюємо ID сесії, щоб старі таймери вимкнулися
    power = 100.0
    time_hour = 0
    doors_closed = False
    vent_closed = False
    cameras_open = False
    current_cam = "1A"

    animatronics["Raven"] = "1A"
    animatronics["Bonzo"] = "1A"
    animatronics["Technician"] = "1B"

    # Повертаємо 3D об'єкти на початкові місця
    left_door.y = 7
    left_door.color = color.light_gray
    vent_gate.y = 5
    vent_gate.color = color.light_gray

    camera.rotation_x = 0
    camera.rotation_y = 0
    camera.x = 0
    camera.y = 0

    # Вмикаємо офіс назад
    ui_office.enabled = True
    ui_tablet.enabled = False

    mouse.locked = False
    mouse.visible = True

    time_text.text = f"Час: {time_hour}:00 AM"
    invoke(advance_time, session_id, delay=25)


btn_retry.on_click = restart_game


# --- ЛОГІКА СИСТЕМ ОФІСУ ---
def toggle_door():
    global doors_closed
    if game_over or cameras_open or not game_started: return
    doors_closed = not doors_closed
    left_door.y = -1 if doors_closed else 7
    left_door.color = color.red if doors_closed else color.light_gray
    print_info("Ліві двері " + ("ЗАЧИНЕНО" if doors_closed else "ВІДЧИНЕНО"))


def toggle_vent():
    global vent_closed
    if game_over or cameras_open or not game_started: return
    vent_closed = not vent_closed
    vent_gate.y = -3 if vent_closed else 5
    vent_gate.color = color.red if vent_closed else color.light_gray
    print_info("Вентиляцію " + ("ЗАЧИНЕНО" if vent_closed else "ВІДЧИНЕНО"))


def toggle_tablet():
    global cameras_open
    if game_over or not game_started: return
    cameras_open = not cameras_open
    ui_tablet.enabled = cameras_open
    if cameras_open:
        update_camera_screen()
        print_info("Планшет активовано")


def change_cam(cam_name):
    global current_cam
    current_cam = cam_name
    update_camera_screen()


def update_camera_screen():
    cam_title.text = f"КАМЕРА {current_cam}"
    present = [name for name, loc in animatronics.items() if loc == current_cam]

    if current_cam == "1A":
        desc = "СЦЕНА: Головний майданчик.\n"
        desc += f"Присутні: {', '.join(present) if present else 'ПОРУШЕННЯ СИСТЕМИ! ПОРОЖНЬО!'}"
    elif current_cam == "1B":
        desc = "ГОЛОВНИЙ ЗАЛ: Місце відпочинку.\n"
        desc += f"Присутні: {', '.join(present) if present else 'Нікого немає.'}"
    elif current_cam == "2A":
        desc = "ЛІВИЙ КОРИДОР: Веде прямо до твоїх дверей!\n"
        desc += f"СТАТУС: "
        desc += f"{'УВАГА! ХТОСЬ БІЛЯ ДВЕРЕЙ!' if present else 'Чисто.'}"
    elif current_cam == "2B":
        desc = "ВЕНТИЛЯЦІЙНА ШАХТА: Справа від офісу.\n"
        desc += f"{'ЖУТКИЙ СКРЕЖІТ! ВІН ТУТ!' if present else 'Тихо.'}"

    cam_screen_text.text = desc


def print_info(msg):
    info_label.text = msg
    invoke(setattr, info_label, 'text', '', delay=2)


btn_door.on_click = toggle_door
btn_vent.on_click = toggle_vent
btn_tablet.on_click = toggle_tablet

for name, pos in cam_positions.items():
    b = Button(parent=ui_tablet, text=name, scale=(0.08, 0.06), position=pos, color=color.dark_gray)
    b.on_click = Func(change_cam, name)
    cam_buttons[name] = b


# --- ІГРОВИЙ ЦИКЛ ОНОВЛЕННЯ ---
def update():
    global power, game_over, game_started

    if not game_started:
        return

    if game_over:
        if jumpscare_active:
            camera.x = random.uniform(-0.15, 0.15)
            camera.y = random.uniform(-0.15, 0.15)
        return

    # Обертання вентилятора
    fan_blade.rotation_z += time.dt * 600

    # Менеджмент енергії
    drain = time.dt * 0.1
    if doors_closed: drain += time.dt * 0.5
    if vent_closed: drain += time.dt * 0.4
    if cameras_open: drain += time.dt * 0.3

    power -= drain
    power_text.text = f"Енергія: {max(0, int(power))}%"

    if power <= 0:
        trigger_jumpscare("Енергія вимкнулась. Тень Рейвена завітала в гості...")

    # Плавний огляд офісу за допомогою миші
    if not cameras_open:
        target_rot_y = mouse.x * 120
        target_rot_x = -mouse.y * 35

        target_rot_y = clamp(target_rot_y, -55, 55)
        target_rot_x = clamp(target_rot_x, -20, 20)

        camera.rotation_y = lerp(camera.rotation_y, target_rot_y, time.dt * 5)
        camera.rotation_x = lerp(camera.rotation_x, target_rot_x, time.dt * 5)

    # Шанс переміщення роботів
    if random.randint(1, 1000) == 1:
        move_animatronics()


# --- ЛОГІКА ШТУЧНОГО ІНТЕЛЕКТУ ---
def move_animatronics():
    if game_over or not game_started: return

    for bot in ["Raven", "Bonzo"]:
        pos = animatronics[bot]
        if pos == "1A" and random.random() > 0.5:
            animatronics[bot] = "1B"
        elif pos == "1B" and random.random() > 0.5:
            animatronics[bot] = "2A"
            print_info("[!] Чути важкі кроки зліва...")
        elif pos == "2A":
            invoke(check_door_attack, bot, session_id, delay=4)

    if animatronics["Technician"] == "1B" and random.random() > 0.4:
        animatronics["Technician"] = "2B"
        print_info("[!] Справа у вентиляції щось шурхотить...")
    elif animatronics["Technician"] == "2B":
        invoke(check_vent_attack, session_id, delay=4)

    if cameras_open:
        update_camera_screen()


def check_door_attack(bot, s_id):
    if game_over or s_id != session_id: return
    if animatronics[bot] == "2A":
        if not doors_closed:
            trigger_jumpscare(f"{bot} увірвався через ліві двері!")
        else:
            print_info("[!] Сильний удар у двері! Аніматроник відступив.")
            animatronics[bot] = "1A"


def check_vent_attack(s_id):
    if game_over or s_id != session_id: return
    if animatronics["Technician"] == "2B":
        if not vent_closed:
            trigger_jumpscare("Технік вистрибнув з вентиляції!")
        else:
            print_info("[!] Скрегіт об залізну решітку вентиляції. Технік відійшов.")
            animatronics["Technician"] = "1B"


# --- СИСТЕМА СКРИМЕРА ---
def play_screech_sound():
    try:
        for _ in range(3):
            for freq in range(1500, 400, -90):
                winsound.Beep(freq, 15)
            for freq in range(400, 1200, 80):
                winsound.Beep(freq, 12)
    except:
        pass


def trigger_jumpscare(reason):
    global game_over, jumpscare_active
    game_over = True
    jumpscare_active = True
    ui_tablet.enabled = False
    ui_office.enabled = False

    camera.rotation_x = 0
    camera.rotation_y = 0

    global monster_head
    monster_head = Entity(model='cube', color=color.Color(0.08, 0.08, 0.08, 1), scale=(4, 4, 1), z=1.5, y=0)
    Entity(parent=monster_head, model='sphere', color=color.red, scale=(0.25, 0.25, 0.25), x=-0.6, y=0.5, z=-0.6)
    Entity(parent=monster_head, model='sphere', color=color.red, scale=(0.25, 0.25, 0.25), x=0.6, y=0.5, z=-0.6)
    Entity(parent=monster_head, model='cube', color=color.light_gray, scale=(1.8, 0.3, 0.2), x=0, y=-0.6, z=-0.6)

    threading.Thread(target=play_screech_sound, daemon=True).start()
    invoke(show_final_game_over, reason, delay=1.5)


def show_final_game_over(reason):
    global jumpscare_active
    jumpscare_active = False
    camera.x = 0
    camera.y = 0
    destroy(monster_head)

    # Передаємо причину смерті у контейнер і показуємо екран Game Over
    game_over_reason.text = reason
    ui_game_over.enabled = True

    # Повертаємо курсор для взаємодії з кнопкою перезапуску
    mouse.locked = False
    mouse.visible = True


# --- ІГРОВИЙ ТАЙМЕР ЧАСУ ---
def advance_time(s_id):
    global time_hour, game_over
    if game_over or not game_started or s_id != session_id: return
    time_hour += 1
    time_text.text = f"Час: {time_hour}:00 AM"

    if time_hour >= 6:
        game_over = True
        ui_tablet.enabled = False
        ui_office.enabled = False

        Panel(color=color.black, scale=(2, 2))
        Text(
            text="6:00 AM\n\nЗМІНУ ПЕРЕЖИТО...\nАле це ще не кінець.",
            scale=3.5,
            origin=(0, 0),
            color=color.green
        )
    else:
        invoke(advance_time, s_id, delay=25)


app.run()