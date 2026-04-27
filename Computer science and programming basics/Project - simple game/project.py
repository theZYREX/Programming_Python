import random

# Персонаж
class Character:
    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
        self.attack = 0
        self.defense = 0
        self.health = 100
        self.inventory = ["Аптечка"]
        self.crystals_collected = 0

        if specialization == "Солдат" or specialization == '1':
            self.attack = 5
            self.defense = 2
        elif specialization == "Танк" or specialization == '2':
            self.attack = 3
            self.defense = 5
        elif specialization == "Ассасин" or specialization == '3':
            self.attack = 4
            self.defense = 4
        elif specialization == "Случайный" or specialization == '4':
            self.randomize_stats()
        else:
            print("Некорректная специализация!")

    def randomize_stats(self):
        total_points = 8
        while True:
            self.attack = random.randint(0, total_points)
            remaining_points = total_points - self.attack

            if remaining_points <= 0:
                break

            self.defense = remaining_points

            if self.attack + self.defense == total_points:
                break

    def show_stats(self):
        return f"Атака: {self.attack}, Защита: {self.defense}, Здоровье: {self.health}"

    def show_inventory(self):
        if not self.inventory:
            return "Инвентарь пуст."
        return "Инвентарь: " + ", ".join(self.inventory)

    def redistribute_points(self):
        print("Текущие характеристики:")
        print(self.show_stats())

        while True:
            try:
                new_attack = int(input("Введите новые очки Атаки (0-10): "))
                new_defense = int(input("Введите новые очки Защиты (0-10): "))

                total_points = new_attack + new_defense

                if total_points > 8:
                    print("Сумма всех очков не должна превышать 8. Попробуйте снова.")
                else:
                    self.attack = new_attack
                    self.defense = new_defense
                    print("Характеристики успешно обновлены!")
                    break

            except ValueError:
                print("Пожалуйста, введите целые числа.")


# Враги
class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def is_alive(self):
        return self.health > 0


# Враги с уникальными характеристиками
class EnemyType1(Enemy):
    def __init__(self):
        super().__init__(name="Местный Хищник", health=5, attack=5, defense=2)


class EnemyType2(Enemy):
    def __init__(self):
        super().__init__(name="Ядовитый паук", health=10, attack=7, defense=3)


class EnemyType3(Enemy):
    def __init__(self):
        super().__init__(name="Биолюминесцентное Существо", health=15, attack=9, defense=4)



# Функция боя
def battle(player, enemy):
    print(f"\nВы встретили врага: {enemy.name}!")


    while player.health > 0 and enemy.is_alive():
        action = input("\nВыберите действие:\n1. Атака\n2. Использовать аптечку\n3. Уклонение\n4. Сбежать\n> ")

        if action == "1":
            damage_dealt = max(0, player.attack - enemy.defense)
            enemy.health -= damage_dealt
            print(f"Вы атаковали {enemy.name} и нанесли {damage_dealt} урона! Осталось здоровья врага: {enemy.health}")

        elif action == "2":
            if "Аптечка" in player.inventory:
                player.inventory.remove("Аптечка")
                player.health += 30
                print("Вы использовали аптечку и восстановили здоровье на 30 единиц.")
            else:
                print("У вас нет аптечек!")

        elif action == "3":
            if random.random() < 0.7:
                print(f"Вы успешно уклонились от атаки!")
                continue

        elif action == "4":
            print("Вы решили сбежать из боя!")
            print(f"Ваше здоровье осталось на уровне: {player.health}")
            return

        # Ход врага
        if enemy.is_alive():
            damage_taken = max(0, enemy.attack - player.defense)
            player.health -= damage_taken
            print(f"{enemy.name} атакует вас и наносит {damage_taken} урона! Ваше здоровье: {player.health}")

    if not enemy.is_alive():
        print(f"Вы победили {enemy.name}!")

        player.attack += 1
        player.defense += 1

        print(f"Ваши характеристики увеличились!\nАтака: {player.attack}, Защита: {player.defense}")

    else:
        print("Вы погибли в бою!")


# Основная игра
def main():
    print("Вы — капитан экспедиции на планету Нова-7. Ваша миссия: добыть образцы кристалла и доставить их на Землю.\nВы успешно приземлились на планету.")

    name = input("Введите своё имя: ")
    specialization = input("Выберите специализацию \n1.Солдат\n2.Танк\n3.Ассасин\n4.Случайный\nчисло или название> ").strip()

    player = Character(name, specialization)

    print(f"Ваши характеристики:\n{player.show_stats()}")

    change_stats = input("Вы желаете изменить характеристики персонажа? (да/нет): ").strip().lower()

    if change_stats == 'да':
        player.redistribute_points()

    print('\nДобро пожаловать - NOVA 7')
    while True:
        print("\nЧто делать дальше?")

        action = input(
            "1. Просмотреть характеристики и инвентарь.\n2. Исследовать ближайшую местность.\n3. Отправиться и исследовать кратер.\n4. Исследовать заброшенную станцию\n> ")

        if action == "1":
            print(f"Ваши характеристики:\n{player.show_stats()}")
            print(player.show_inventory())

        elif action == "2":
            if random.random() < 0.8:
                enemy_type_choice = random.choice([EnemyType1(), EnemyType2(), EnemyType3()])
                battle(player, enemy_type_choice)
            else:
                print("Вы исследуете местность и находите кристаллы!")
                player.crystals_collected += 1
                player.inventory.append("Кристалл")
                print("Вы собрали образец кристалла.")

        elif action == "3":
            if random.random() < 0.6:
                enemy_type_choice = random.choice([EnemyType1(), EnemyType2(), EnemyType3()])
                battle(player, enemy_type_choice)
            else:
                print("Вы исследуете местность и находите кристаллы!")
                player.crystals_collected += 1
                player.inventory.append("Кристалл")
                print("Вы собрали образец кристалла.")

        elif action == "4":
            print("Вы отправились на заброшенную станцию.")
            player.inventory.append("Аптечка")
            print("Вы нашли аптечку!")

            next_action = input("Что вы хотите сделать дальше?\n1. Покинуть станцию\n2. Исследовать дальше\n> ")

            if next_action == "1":
                print("Вы покинули заброшенную станцию.")

            elif next_action == "2":
                if random.random() < 0.7:
                    enemy_type_choice = random.choice([EnemyType1(), EnemyType2(), EnemyType3()])
                    battle(player, enemy_type_choice)
                else:
                    print("Вы исследуете станцию и находите кристаллы!")
                    player.crystals_collected += 1
                    player.inventory.append("Кристалл")
                    print("Вы собрали образец кристалла.")

        else:
            print("Некорректный ввод. Попробуйте снова.")

        if player.crystals_collected >= 3:
            print(f"\nМиссия завершена! Вы успешно добыли {player.crystals_collected} образца кристалла.\nПоздравляем с прохождением игры!")
            break


if __name__ == "__main__":
    main()

