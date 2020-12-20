from model.abilites import AbilityType
from enum import Enum
import json


class HeroType(Enum):
    """ Типв героев """
    Nobody = 0         # Не определен
    Warrior = 1        # Воин
    BlackSmith = 2     # Рунный кузнец
    Mag = 3            # Маг


class Hero(object):
    """
    Общий класс для всех героев. Содержит общий набор возможностей
    """
    hero_type = HeroType.Nobody
    player_color = 0

    def __init__(self, game_parameters):
        """
        Извлекает из параметров игры основные характеристики героя
        team_id - идентификатор команды для командной игры
        player_color - цвет команды игрока
        """
        # Проверка соответствия типа героя
        if game_parameters["HeroType"] != self.hero_type.value:
            raise Exception('Hero type in game parameters init hero type')

        self.player_color = game_parameters["PlayerColor"]

    def move(self, source_tower_id, target_tower_id, part):
        """
        Передвижение войск
        source_tower_id - идентификатор исходной башни
        target_tower_id - идентификатор целевой башни
        part - направляемая часть войск [0,1]
        """
        action = {
            "FromId": source_tower_id,
            "ToId": target_tower_id,
            "Part": part,
            "PlayerColor": self.player_color,
            "Type": 1
        }
        return json.dumps(action, ensure_ascii=False)

    def speed_up(self, location):
        """
        Ускорение союзных войск
        location - координата точки применения
        """
        action = {
            "X": location["x"],
            "Y": location["y"],
            "FirstTowerId": 0,
            "SecondTowerId": 0,
            "AbilityId": AbilityType.Speed_up.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)

    def upgrade_tower(self, tower_id):
        """
        Увеличивает уровень своей башни
        tower_id - идентификатор целевой башни
        """
        action = {
            "TowerId": tower_id,
            "PlayerColor": self.player_color,
            "Type": 4
        }
        return json.dumps(action, ensure_ascii=False)


class Mag(Hero):
    """
    Возможности героя Маг
    """
    hero_type = HeroType.Mag

    def plague(self, enemy_tower_id):
        """
        Чума. Применяется на башню противника и убивает в нем войска
        enemy_tower_id - идентификатор целевой башни противника
        """
        action = {
            "X": 0,
            "Y": 0,
            "FirstTowerId": enemy_tower_id,
            "SecondTowerId": 0,
            "AbilityId": AbilityType.Plague.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)

    def exchange(self, enemy_tower_id, my_tower_id):
        """
        Обмен. Меняет башни местами и усредняет количество войск
        enemy_tower_id - идентификатор целевой башни противника
        my_tower_id - идентификатор вашей башни
        """
        action = {
            "X": 0,
            "Y": 0,
            "FirstTowerId": enemy_tower_id,
            "SecondTowerId": my_tower_id,
            "AbilityId": AbilityType.Build_exchange.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)


class Warrior(Hero):
    """
    Возможности героя Воин
    """
    hero_type = HeroType.Warrior

    def berserk(self, location):
        """
        Берсерк. Усиливает движущиеся войска в заданной области
        location - координаты x, y
        """
        action = {
            "X": location["x"],
            "Y": location["y"],
            "FirstTowerId": 0,
            "SecondTowerId": 0,
            "AbilityId": AbilityType.Berserk.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)

    def growl(self, enemy_tower_id):
        """
        Рык. Распугивает соперника в башне. При применении войска соперника разбегаются по другим своим башням. Если других башен нет, останутся сидеть в этой башне
        enemy_tower_id - идентификатор целевой башни противника
        """
        action = {
            "X": 0,
            "Y": 0,
            "FirstTowerId": enemy_tower_id,
            "SecondTowerId": 0,
            "AbilityId": AbilityType.Growl.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)


class BlackSmith(Hero):
    """
    Возможности героя Кузнец
    """
    hero_type = HeroType.BlackSmith

    def area_damage(self, location):
        """
        Урон по площади. Не действует на берсерков. Начинает дейстовать через секунду.
        location - координаты x, y
        """
        action = {
            "X": location["x"],
            "Y": location["y"],
            "FirstTowerId": 0,
            "SecondTowerId": 0,
            "AbilityId": AbilityType.Area_damage.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)

    def armor(self, my_tower_id):
        """
        Защита своей башни (или союзника)
        my_tower_id - идентификатор целевой башни
        """
        action = {
            "X": 0,
            "Y": 0,
            "FirstTowerId": my_tower_id,
            "SecondTowerId": 0,
            "AbilityId": AbilityType.Armor.value,
            "PlayerColor": self.player_color,
            "Type": 2
        }
        return json.dumps(action, ensure_ascii=False)
