from enum import Enum


class BuildingType(Enum):
    """ Типы башен """
    Tower = 1  # обычная башня
    Forge = 2  # кузница


class Building(object):
    """
    Состояние башен. Передается в игровом стейте
    """
    def __init__(self, building, parameters):
        self.id = building["Id"]  # идентификатор башни
        self.type = BuildingType(building["Type"])  # тип башни 1 - башня, 2 - кузница
        self.creeps_count = building["CreepsCount"]  # текущее количество крипов
        self.player_color = building["PlayerColor"]  # принадлежность игроку
        self.creep_creation_time = building["CreepCreationTime"]  # сколько тиков создается крип
        self.buff_mask = building["BuffMask"]  # побитовая маска i-й бит growl-1, plague-2, exchange-3, invision-4
        self.DefenseBonus = building["DefenseBonus"]  # текущая защита
        # уровень от 0 до 3 определяет текущие значения башни, нужно их подтягивать откуда-то и как-то - из параметров
        self.level = parameters.get_tower_level(building["Level"])  # текущий уровень башни

    def add_defence(self, defence_bonus):
        self.DefenseBonus += defence_bonus


class TowerLevelParameters(object):
    """
    Класс предоставляющий праматеры башен по уровням, которые передаются в игровых параметрах при
    инициализации игры
    """
    def __init__(self, id, params):
        # номер уровня
        self.id = id
        # цена перехода
        self.update_coast = params["UpdateCoast"]
        # бонус защиты в абсолютном значении + 1
        self.defense_bonus = params["DefenseBonus"]
        # время в тиках за котрое создается 1 крип
        self.creep_creation_time = params["CreepCreationTime"]
        # начальное дефолтное занчение количества крипов для игрока
        self.default_player_count = params["DefaultPlayerCount"]
        # начальное дефолтное занчение количества крипов для нейтрального
        self.default_neutral_count = params["DefaultNeutralCount"]
        # максимальное количество крипов для игрока после которого останавливается рост
        self.player_max_count = params["PlayerMaxCount"]
        # максимальное количество крипов для нейтрального игрока после которого останавливается рост
        self.neutral_max_count = params["NeutralMaxCount"]


class ForgeParameters(object):
    """
    Класс предоставляющий праматеры кузницы, которые передаются в игровых параметрах при
    инициализации игры
    """
    def __init__(self, params):
        # дает бонус к защите башен
        self.defence_bonus = params["DefenseBonus"]
        # начальное дефолтное занчение количества крипов для игрока
        self.default_player_count = params["DefaultPlayerCount"]
        # начальное дефолтное занчение количества крипов для нейтрального
        self.default_neutral_count = params["DefaultNeutralCount"]
        # максимальное количество крипов для игрока после которого останавливается рост
        self.player_max_count = params["PlayerMaxCount"]
        # максимальное количество крипов для нейтрального игрока после которого останавливается рост
        self.neutral_max_count = params["NeutralMaxCount"]