import sys
import time
import serial
import serial.tools.list_ports

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
    ' ': ' '
}

MELODIES = {
    'march': [[100, 100], [100, 100], [100, 100], [300, 300]] * 2,
    'waltz': [[300, 150], [100, 150], [100, 300]] * 2,
    'sos': [[150, 150], [150, 150], [150, 450], [450, 150], [450, 150], [450, 450], [150, 150], [150, 150], [150, 150]]
}

MORSE_SPEEDS = {1: 300, 2: 200, 3: 150, 4: 100, 5: 60}


class ArduinoDriver:
    def __init__(self):
        self.conn = None

    def list_ports(self):
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports if 'usb' in port.device or 'acm' in port.device.lower()]

    def connect(self, port_name):
        try:
            self.conn = serial.Serial(port_name, 9600, timeout=5)
            response = self.conn.readline().decode('utf-8').strip()
            if response == "READY":
                return True, f"Устройство на порту {port_name} готово."
            else:
                return False, f"Ошибка: устройство ответило '{response}', ожидался 'READY'."
        except serial.SerialException as e:
            return False, f"Не удалось подключиться к порту {port_name}: {e}"

    def disconnect(self):
        if self.conn and self.conn.is_open:
            self.conn.close()
            print("Порт закрыт.")

    def send_command(self, cmd):
        if not self.conn or not self.conn.is_open:
            return "ERROR:NO_CONNECTION"

        try:
            self.conn.write(f"{cmd}\n".encode('utf-8'))
            response = self.conn.readline().decode('utf-8').strip()
            return response
        except serial.SerialException as e:
            return f"ERROR:COMMUNICATION_ERROR: {e}"


def show_help():
    print("\nДоступные команды:")
    print("  help                     - Показать эту справку")
    print("  status                   - Получить текущее состояние светодиода")
    print("  led on/off               - Включить/выключить светодиод")
    print("  led blink <n> <ms>       - Мигнуть N раз с интервалом в ms")
    print("  led fade <duration_ms>   - Плавная пульсация длительностью ms")
    print("  melody list              - Список доступных мелодий")
    print("  melody <name>            - Воспроизвести световую мелодию (march, waltz, sos)")
    print("  morse <text>             - Передать текст азбукой Морзе")
    print("  morse speed <1-5>        - Установить скорость Морзе (1=медленно, 5=быстро)")
    print("  rock <n>                 - Отбить ритм 'We Will Rock You' N раз")
    print("  exit                     - Завершить работу\n")


def handle_morse(driver, text, speed_ms):
    print(f"Передаю: {text.upper()}")
    morse_text = ""
    for char in text.upper():
        if char in MORSE_CODE:
            code = MORSE_CODE[char]
            morse_text += code + " "
            for symbol in code:
                if symbol == '.':
                    driver.send_command(f"BLINK {speed_ms} {speed_ms}")
                elif symbol == '-':
                    driver.send_command(f"BLINK {speed_ms * 3} {speed_ms}")
            time.sleep(speed_ms * 3 / 1000)
        elif char == ' ':
            morse_text += "  "
            time.sleep(speed_ms * 7 / 1000)
    print(morse_text)
    print("OK")


def handle_fade(driver, duration):
    steps = 20
    step_delay = duration / (2 * steps)

    print(f"Выполняю пульсацию длительностью {duration} мс...")
    for i in range(1, steps + 1):
        on_ms = int(i * (step_delay / steps))
        off_ms = int(step_delay - on_ms)
        driver.send_command(f"BLINK {max(1, on_ms)} {max(0, off_ms)}")
    for i in range(steps, 0, -1):
        on_ms = int(i * (step_delay / steps))
        off_ms = int(step_delay - on_ms)
        driver.send_command(f"BLINK {max(1, on_ms)} {max(0, off_ms)}")
    print("OK")


def main():
    driver = ArduinoDriver()
    morse_speed_level = 3

    ports = driver.list_ports()
    if not ports:
        print("Arduino не найдена. Проверьте подключение и драйверы.")
        sys.exit(1)

    print("Найдены следующие порты:")
    for i, port in enumerate(ports):
        print(f"  [{i + 1}] {port}")

    try:
        choice = int(input("Выберите номер порта: ")) - 1
        if not 0 <= choice < len(ports):
            raise ValueError
        port_to_connect = ports[choice]
    except (ValueError, IndexError):
        print("Неверный выбор.")
        sys.exit(1)

    success, message = driver.connect(port_to_connect)
    print(message)
    if not success:
        sys.exit(1)

    show_help()

    try:
        while True:
            cmd_line = input("> ").strip().lower().split()
            if not cmd_line:
                continue

            command = cmd_line[0]

            if command == "exit":
                break
            elif command == "help":
                show_help()
            elif command == "status":
                print(f"Состояние: {driver.send_command('STATUS')}")
            elif command == "led":
                if len(cmd_line) > 1:
                    if cmd_line[1] == "on":
                        print(driver.send_command("LED_ON"))
                    elif cmd_line[1] == "off":
                        print(driver.send_command("LED_OFF"))
                    elif cmd_line[1] == "blink" and len(cmd_line) == 4:
                        n, ms = int(cmd_line[2]), int(cmd_line[3])
                        print(f"Мигаю {n} раз с интервалом {ms} мс...")
                        for _ in range(n):
                            driver.send_command(f"BLINK {ms} {ms}")
                        print("OK")
                    elif cmd_line[1] == "fade" and len(cmd_line) == 3:
                        handle_fade(driver, int(cmd_line[2]))
                    else:
                        print("Ошибка: неверные параметры для 'led'. См. 'help'.")
                else:
                    print("Ошибка: неверные параметры для 'led'. См. 'help'.")
            elif command == "melody":
                if len(cmd_line) > 1:
                    if cmd_line[1] == "list":
                        print("Доступные мелодии:", ", ".join(MELODIES.keys()))
                    elif cmd_line[1] in MELODIES:
                        print(f"Воспроизвожу: {cmd_line[1]}...")
                        for on, off in MELODIES[cmd_line[1]]:
                            driver.send_command(f"BLINK {on} {off}")
                        print("OK")
                    else:
                        print("Ошибка: неизвестная мелодия.")
                else:
                    print("Ошибка: не указана мелодия. См. 'help'.")
            elif command == "morse":
                if len(cmd_line) > 1:
                    if cmd_line[1] == "speed" and len(cmd_line) == 3:
                        try:
                            level = int(cmd_line[2])
                            if level in MORSE_SPEEDS:
                                morse_speed_level = level
                                print(f"Скорость Морзе установлена на уровень {level}.")
                            else:
                                print("Ошибка: уровень скорости должен быть от 1 до 5.")
                        except ValueError:
                            print("Ошибка: неверный уровень скорости.")
                    else:
                        text = " ".join(cmd_line[1:])
                        handle_morse(driver, text, MORSE_SPEEDS[morse_speed_level])
                else:
                    print("Ошибка: не указан текст для передачи. См. 'help'.")
            elif command == "rock":
                if len(cmd_line) == 2:
                    try:
                        repetitions = int(cmd_line[1])
                        if repetitions <= 0:
                            print("Ошибка: количество повторений должно быть больше нуля.")
                            continue
                        print(f"Отбиваю ритм 'We Will Rock You' {repetitions} раз...")
                        for i in range(repetitions):
                            driver.send_command("BLINK 100 150")
                            driver.send_command("BLINK 100 150")
                            driver.send_command("BLINK 150 400")
                            print(f"  Такт {i + 1}/{repetitions} выполнен.")
                        print("OK")
                    except ValueError:
                        print("Ошибка: количество повторений должно быть числом.")
                else:
                    print("Ошибка: не указано количество повторений. Пример: rock 5")
            else:
                print("Неизвестная команда. Введите 'help' для справки.")

    except KeyboardInterrupt:
        print("\nЗавершение работы по запросу пользователя.")
    finally:
        driver.disconnect()


if __name__ == "__main__":
    main()
