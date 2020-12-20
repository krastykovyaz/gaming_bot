from enum import Enum


class AbilityType(Enum):
    """ Типы абилок применяемых в игре """
    Speed_up = 0            # ускорение
    Vision = 1              # видеть количество войск в башнях (для игроков)
    Berserk = 2             # усиление войск (Warrior)
    Growl = 3               # крик (Warrior)
    Area_damage = 4         # урон по площади (BlackSmith)
    Plague = 5              # чума (Mag)
    Build_exchange = 6      # обмен башен с усреднением (Mag)
    Armor = 7               # защита башни (BlackSmith)
    Tremors = 8             # червь (общая)
    Fair_wind = 9           # усорение всех войск (общая)


class AbilityInputType(Enum):
    """ Способы применения абилок """
    CommonAbility = 0       # общая абилка
    AreaAbility = 1         # площадная абилка
    OneTowerAbility = 2     # применяется к одной башне
    TwoTowerAbility = 3     # применяется к двум башням


class Ability(object):
    """
    Примененные абилки. Передаются в игровом стейте
    """
    def __init__(self, ability):
        self.ability = AbilityType(ability["Ability"])  # тип абилки
        if "TargetTowerId" in ability:
            self.target_tower_id = ability["TargetTowerId"]  # башня к которой применена (для input type 2  )
        if "FirstTargetTowerId" in ability:
            self.first_target_tower_id = ability["FirstTargetTowerId"]  # башня к которой применена (для input type 3)
        if "SecondTargetTowerId" in ability:
            self.second_target_tower_id = ability["SecondTargetTowerId"]  # башня к которой применена (для input type 3)
        if "X" in ability:
            self.x = ability["X"]  # координаты (для абилок с input type 1)
        if "Y" in ability:
            self.y = ability["Y"]  # координаты (для абилок с type 1)
        self.ability_input_type = AbilityInputType(ability["AbilityInputType"])  # способ применения
        self.player_color = ability["OwnerColor"]  # кто применил
        self.initial_tick = ability["InitialTick"]  # в какой тик создана
        self.start_tick = ability["StartTick"]  # когда начала действовать
        self.end_tick = ability["EndTick"]  # когда закончит действовать


class AbilityParameters(object):
    """
    Класс предоставляющий праматеры абилок по умолчанию, которые передаются в игровых параметрах при
    инициализации игры
    """
    def __init__(self, params):
        # тип абилки
        self.ability = AbilityType(params["Id"])
        # тип действия 0 - общие, 1 - площадные, 2 - на 1 башню, 3 - на 2 башни
        self.input_type = AbilityInputType(params["InputType"])
        # сколько длится в тиках
        self.duration = params["Duration"]
        # через сколько будет доступна снова
        self.cooldown = params["Cooldown"]
        # время для иницилизации обилки
        self.cast_time = params["CastTime"]
        # для площадных не равен нулю
        self.radius = params["Radius"]
        # кастомные параметры абилки
        self.ability_data = params["AbilityData"]


class GameEventParameters(object):
    """
    Класс предоставляющий праматеры глобальных событий игры, которые передаются в игровых параметрах при
    инициализации игры
    """
    def __init__(self, params):
        # с какого тика начинается
        self.StartTick = params["StartTick"]
        # через сколько повторяется
        self.LoopInterval = params["LoopInterval"]
        # повторяется или нет
        self.LoopMode = params["LoopMode"]
        # 0 - на игрока, 1 - на всех
        self.UseMode = params["UseMode"]
        # тип абилки
        self.Ability = AbilityType(params["Ability"])
        # начальный цвет цели
        self.TargetColor = params["TargetColor"]
