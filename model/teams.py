from model.hero import *


class PLayer(object):
    """ Класс с необходимой информацией об иргроках """
    def __init__(self, player_color, hero_type):
        self.player_color = player_color
        self.hero_type = hero_type


class Teams(object):
    """ Класс игровых команд """

    my_team = []  # массив игроков моей команды
    enemy_team = []  # массив игроков команд противников

    def __init__(self, game):
        self.teams = game["Teams"]

        if game["HeroType"] == HeroType.Mag.value:
            self.my_her = Mag(game)

        if game["HeroType"] == HeroType.Warrior.value:
            self.my_her = Warrior(game)

        if game["HeroType"] == HeroType.BlackSmith.value:
            self.my_her = BlackSmith(game)

        my_team_id = self.__get_team_id(self.my_her.player_color)

        for team in game["Teams"]:
            for player in team["Players"]:
                if team["TeamId"] == my_team_id:
                    self.my_team.append(PLayer(player["PlayerColor"], player["HeroType"]))
                else:
                    self.enemy_team.append(PLayer(player["PlayerColor"], player["HeroType"]))

    def my_team_players_color(self):
        """ Возвращает массив цветов игроков команды моего бота """
        result = []
        for player in self.my_team:
            result.append(player.player_color)
        return result

    def enemy_players_have_hero(self, hero_type):
        """ Возвращает True если в команде противника найден тип героя hero_type """
        for player in self.enemy_team:
            if player.hero_type == hero_type:
                return player

    def get_team_colors_by_color(self, player_color):
        """ Возвращает массив игроков команды игрока player_color """
        team_id = self.__get_team_id(player_color)
        result = []
        for team in self.teams:
            for player in team["Players"]:
                if team["TeamId"] == team_id:
                    result.append(player["PlayerColor"])
        return result

    def __get_team_id(self, player_color):
        """ Возвращает идентификатор команды бота игрока player_color """
        for team in self.teams:
            for player in team["Players"]:
                if player["PlayerColor"] == player_color:
                    return team["TeamId"]
