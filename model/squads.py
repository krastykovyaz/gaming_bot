

class Way(object):
    """ Путь отряда """
    def __init__(self, total, traveled):
        self.total = total  # какой путь нужно пройти
        self.traveled = traveled  # сколько уже прошел
        self.left = total - traveled  # сколько осталось


class Squad(object):
    """
    Состояние отрядов. Передается в игровом стейте
    """
    def __init__(self, squad):
        self.id = squad["Id"]  # идентификатор отряда
        self.from_id = squad["FromId"]  # откуда вышел
        self.to_id = squad["ToId"]  # куда идет
        self.player_color = squad["PlayerColor"]  # кому принадлежит
        self.creeps_count = squad["CreepsCount"]  # сколько крипов в отряде
        self.speed = squad["Speed"]  # скорость передвижения
        self.way = Way(squad["Way"]["Total"], squad["Way"]["Traveled"])  # путь отряда
        self.buff = squad["BuffMask"]  # побитовая маска - каждый байт - крип, в каждом байте бит соответствует бафу
        # - берсерк 0, чума 1, убийство червяком -2


class CreepParameters(object):
    """
    Класс предоставляющий праматеры крипов по умолчанию, которые передаются в игровых параметрах при
    инициализации игры
    """
    def __init__(self, params):
        # скорость в единицах расстояния карты
        self.speed = params["Speed"]
        # время между шеренгами в тиках
        self.wave_delay = params["WaveDelay"]
        # максимальное количество крипов в шеренге
        self.max_wave_creeps_count = params["MaxWaveCreepsCount"]
        # интервал между крипами в шеренге
        self.creep_in_wave_distance = params["CreepInWaveDistance"]
