from model.abilites import *


class Cooldown(object):
    """ Фриз на применение абилок """
    def __init__(self, cooldown):
        self.ability = AbilityType(cooldown["Ability"])  # тип абилки
        self.player_color = cooldown["PlayerColor"]  # кто применил
        self.ticks_to_cooldown_end = cooldown["TicksToCooldownEnd"]  # сколько тиков осталось до повторного применения
