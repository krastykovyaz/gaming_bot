import json
import gzip
import base64


class Message(object):
    json = {}

    def __init__(self, msg_base64):
        msg_gzip = base64.b64decode(msg_base64)
        msg_bytes = gzip.decompress(msg_gzip)
        msg_string = msg_bytes.decode()
        self.json = json.loads(msg_string)
        self.msg_type = self.json["MsgType"]
        if "GameId" in self.json:
            self.game_id = self.json["GameId"]
        else:
            self.game_id = 0

    def send_message(self):
        msg_string = json.dumps(self.json, ensure_ascii=False)
        msg_gzip = gzip.compress(msg_string.encode())
        msg_base64 = base64.b64encode(msg_gzip)
        return msg_base64

    def to_string(self):
        return json.dumps(self.json, ensure_ascii=False)


class RequestGame(Message):
    json = {
        "MsgType": 17,
        "RequestGameParametersArgs": {
            "BotId": ""
        }
    }

    def __init__(self, user_id, bot_id, game_id):
        if user_id:
            self.json["RequestGameParametersArgs"]["UserId"] = user_id
        if bot_id:
            self.json["RequestGameParametersArgs"]["BotId"] = bot_id
        if game_id:
            self.json["RequestGameParametersArgs"]["GameId"] = game_id


class PlayerConnect(Message):
    json = {
        "MsgType": 8,
        "GameId": "",
        "Subscribers": [],
        "PlayerConnectArgs": {
                "PlayerId": ""
            }
    }

    def __init__(self, game_server, game_id, bot_id):
        self.json["Subscribers"].append(game_server)
        self.json["GameId"] = game_id
        self.json["PlayerConnectArgs"]["PlayerId"] = bot_id


class PlayerChangeHero(Message):
    json = {
        "MsgType": 22,
        "GameId": "",
        "Subscribers": [],
        "PlayerChangeHeroTypeArgs": {
            "PlayerId": "",
            "HeroType": 0
        }
    }

    def __init__(self, game_server, game_id, bot_id, hero_type):
        self.json["Subscribers"].append(game_server)
        self.json["GameId"] = game_id
        self.json["PlayerChangeHeroTypeArgs"]["PlayerId"] = bot_id
        self.json["PlayerChangeHeroTypeArgs"]["HeroType"] = hero_type


class PlayerChangeColor(Message):
    json = {
        "MsgType": 23,
        "GameId": "",
        "Subscribers": [],
        "PlayerChangeColorArgs": {
            "PlayerId": "",
            "PlayerColor": 2
        }
    }

    def __init__(self, game_server, game_id, bot_id, player_color):
        self.json["Subscribers"].append(game_server)
        self.json["GameId"] = game_id
        self.json["PlayerChangeColorArgs"]["PlayerId"] = bot_id
        self.json["PlayerChangeColorArgs"]["PlayerColor"] = player_color


class PlayerPrepared(Message):
    json = {
        "MsgType": 11,
        "GameId": "",
        "Subscribers": [],
        "PlayerPreparedArgs": {
            "PlayerId": ""
        }
    }

    def __init__(self, game_server, game_id, bot_id):
        self.json["Subscribers"].append(game_server)
        self.json["GameId"] = game_id
        self.json["PlayerPreparedArgs"]["PlayerId"] = bot_id


class PlayerReady(Message):
    json = {
        "MsgType": 13,
        "GameId": "",
        "Subscribers": [],
        "PlayerReadyArgs": {
            "PlayerId": ""
        }
    }

    def __init__(self, game_server, game_id, bot_id):
        self.json["Subscribers"].append(game_server)
        self.json["GameId"] = game_id
        self.json["PlayerReadyArgs"]["PlayerId"] = bot_id


class GameActions(Message):
    json = {
        "MsgType": 3,
        "GameId": "",
        "Subscribers": [],
        "GameActionsArgs": {
            "Action": {}
        }
    }

    def __init__(self, game_server, game_id, action):
        self.json["Subscribers"].append(game_server)
        self.json["GameId"] = game_id
        self.json["GameActionsArgs"]["Action"] = action
