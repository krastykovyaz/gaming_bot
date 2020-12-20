from model.abilites import AbilityParameters, GameEventParameters
from model.buildings import TowerLevelParameters, ForgeParameters
from model.squads import CreepParameters
import json


class Parameters(object):
    """ Класс предоставляющий доступ к параметрам игры """
    def __init__(self, game):
        parameters = json.loads(game["ResponseGameParametersArgs"]["Parameters"])
        # максимальная продолжительность игры в тиках
        self.duration = parameters["Duration"]
        # защита башен по умолчанию
        self.default_defence_parameters = parameters["DefaultDefenseParameter"]
        # уровни башен
        self.tower_levels = []
        for tower in parameters["Towers"]:
            self.tower_levels.append(TowerLevelParameters(int(tower), parameters["Towers"][tower]))
        # параметры кузницы
        self.forge = ForgeParameters(parameters["Forges"])
        # параметры крипов
        self.creep = CreepParameters(parameters["Creeps"])
        # параметры абилок
        self.abilities = []
        for ability in parameters["AbilitiesParameters"]["abilities"]:
            self.abilities.append(AbilityParameters(ability))
        # параметры глобавльных игровых событий
        self.game_events = []
        for game_event in parameters["GameEventsParameters"]:
            self.game_events.append(GameEventParameters(game_event))

    def get_tower_level(self, level):
        """ Возвращает параметры уровня башни level """
        for tower_level in self.tower_levels:
            if tower_level.id == level:
                return tower_level

    def get_ability_parameters(self, ability):
        """ Возвращает параметры уровня башни level """
        for item in self.abilities:
            if item.ability == ability:
                return item
