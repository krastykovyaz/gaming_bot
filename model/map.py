from math import *
import json


class Map(object):
    """ Класс предоставляяющий вспомогательные методы работы с картой """
    def __init__(self, game):
        self.map = json.loads(game["ResponseGameParametersArgs"]["Map"])
        self.links = self.map["Links"]
        # Вычисляем и добавляем расстояние между башнями
        for link in self.links:
            link["Distance"] = self.__towers_distance(link["From"], link["To"])

    def towers_distance(self, from_id, to_id):
        """ Возвращает расстояние между башнями """
        if from_id > to_id:
            temp_id = from_id
            from_id = to_id
            to_id = temp_id

        for link in self.links:
            if link["From"] == from_id and link["To"] == to_id:
                return link["Distance"]

    def points_distance(self, point1, point2):
        """ Вычиляет расстояние между двумя точками """
        return sqrt((point1["x"] - point2["x"]) ** 2 + (point1["y"] - point2["y"]) ** 2)

    def __towers_distance(self, from_id, to_id):
        """ Вычисляет расстояние между двумя башнями """
        if from_id == to_id:
            return 0

        # массив точек в векторе
        waypoints = self.__get_waypoints(from_id, to_id)

        if waypoints is None:
            return 0

        result = 0

        for i in range(0, len(waypoints) - 1):
            result += self.points_distance(waypoints[i], waypoints[i + 1])

        return result

    def __get_waypoints(self, from_id, to_id):
        """ Извлекает массив точек маршрута между двумя башнями """
        if from_id > to_id:
            temp_id = from_id
            from_id = to_id
            to_id = temp_id

        for link in self.links:
            if link["From"] == from_id and link["To"] == to_id:
                return link["Vectors"]

    def get_squad_center_position(self, squad):
        """ Вычисляет координаты центра отряда """
        from_id = squad.from_id
        to_id = squad.to_id
        part_of_path = squad.way.traveled / squad.way.total

        waypoints = self.__get_waypoints(from_id, to_id)
        distance = self.towers_distance(from_id, to_id)
        absolute_part = distance * part_of_path

        distance = 0
        if from_id > to_id:
            waypoints.reverse()

        for i in range(0, len(waypoints)-1):
            part_of_path = self.points_distance(waypoints[i], waypoints[i + 1])
            distance += part_of_path
            if distance >= absolute_part:
                current_path = absolute_part - (distance - part_of_path)
                current_part = current_path / part_of_path

                res = {"x": waypoints[i]["x"] + (waypoints[i + 1]["x"] - waypoints[i]["x"]) * current_part,
                       "y": waypoints[i]["y"] + (waypoints[i + 1]["y"] - waypoints[i]["y"]) * current_part}

                return res

        return {"x": 0, "y": 0}

    def get_nearest_towers(self, from_id, towers):
        """ Сортирует массив towers по расстояние до from_id """
        distances = []
        for tower in towers:
            distances.append({
                "tower": tower,
                "distance": self.towers_distance(from_id, tower.id)
            })
        distances.sort(key=lambda b: b["distance"])
        result = []
        for item in distances:
            result.append(item["tower"])
        return result

    def get_tower_location(self, tower_id):
        """ Возвращает location башни """
        for link in self.links:
            if link["From"] == tower_id:
                return {
                    "x": link["Vectors"][0]["x"],
                    "y": link["Vectors"][0]["y"]
                }


