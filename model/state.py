from model.abilites import Ability, AbilityType
from model.buildings import Building, BuildingType
from model.squads import Squad
from model.cooldowns import Cooldown
import json


class State(object):
    """ Класс предоставляющий доступ к состоянию игры """

    def __init__(self, state, teams, parameters):
        self.state = json.loads(state)
        self.__player_color = teams.my_her.player_color
        self.__my_team_players_color = teams.my_team_players_color()

        # получаем список всех зданий
        self.buildings = []
        for building in self.state["State"]["buildingStates"]:
            self.buildings.append(Building(building, parameters))

        # получаем список всех отрядов
        self.squads = []
        for squad in self.state["State"]["squadStates"]:
            self.squads.append(Squad(squad))

        # получаем список всех примененных абилок
        self.abilities = []
        for ability in self.state["State"]["AbilityStates"]:
            self.abilities.append(Ability(ability))

        # получаем список всех фризов на применение абилок
        self.cooldowns = []
        for cooldown in self.state["State"]["CooldownState"]:
            self.cooldowns.append(Cooldown(cooldown))

        # глобальный бафф который происходит побитовая маска
        self.global_buffs_mask = self.state["State"]["GlobalBuffsMask"]

        # получаем список кузниц
        self.forges = list(filter(lambda x: x.type == BuildingType.Forge, self.buildings))

        # добавление бонуса защиты для башен игрока владеющего кузницей
        for forg in self.forges:
            team_colors = teams.get_team_colors_by_color(forg.player_color)
            if len(team_colors) > 0:
                for building in list(filter(lambda x: x.type != BuildingType.Forge
                                            and x.player_color in team_colors,
                                            self.buildings)):
                    building.add_defence(parameters.forge.defence_bonus)

    def my_buildings(self):
        """ Мои здания """
        return list(filter(lambda x:
                           x.type == BuildingType.Tower and
                           x.player_color == self.__player_color,
                           self.buildings))

    def enemy_buildings(self):
        """ Вражеские здания """
        return list(filter(lambda x:
                           x.player_color not in self.__my_team_players_color and
                           x.player_color != 0 and
                           x.type == BuildingType.Tower,
                           self.buildings))

    def neutral_buildings(self):
        """ Нейтральные здания """
        return list(filter(lambda x:
                           x.player_color == 0 and
                           x.type == BuildingType.Tower,
                           self.buildings))

    def forges_buildings(self):
        """ Кузницы """
        return list(filter(lambda x: x.type == BuildingType.Forge,
                           self.buildings))

    def my_squads(self):
        """ Мои отряды """
        return list(filter(lambda x:
                           x.player_color == self.__player_color,
                           self.squads))

    def enemy_squads(self):
        """ Вражеские отряды """
        return list(filter(lambda x:
                           x.player_color not in self.__my_team_players_color,
                           self.squads))

    def my_active_abilities(self):
        """ Мои возможности активные в текущем стейте """
        return list(filter(lambda x:
                           x.player_color == self.__player_color,
                           self.abilities))

    def enemy_active_abilities(self, ability=None):
        """ Активные абилки примененные врагом """
        if ability:
            return list(filter(lambda x:
                               x.player_color not in self.__my_team_players_color and
                               x.ability == ability,
                               self.abilities))
        else:
            return list(filter(lambda x:
                               x.player_color not in self.__my_team_players_color,
                               self.abilities))

    def ability_ready(self, ability):
        """ Готовность возможности к повторному применению """
        for cool_down in self.cooldowns:
            if cool_down.player_color == self.__player_color and cool_down.ability == ability:
                return False
        return True






