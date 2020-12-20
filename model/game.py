import ssl
import asyncio
import websockets
import time
from .message import *


class Game:
    bot_ready = True

    def __init__(self, process, websocket_url, user_id, bot_id, game_id):
        self.process = process
        if not game_id:
            self.game_id = 0
        else:
            self.game_id = game_id
        self.user_id = user_id
        self.bot_id = bot_id
        self.lobby_changed = 0
        self.ssl_context = ssl.SSLContext()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.run(websocket_url, user_id, bot_id, game_id))

    async def run(self, websocket_url, user_id, bot_id, game_id):
        async with websockets.connect(websocket_url, ssl=self.ssl_context) as websocket:
            msg = RequestGame(user_id, bot_id, game_id)
            print("OUT >>> Request Game")
            await websocket.send(msg.send_message())
            await self.handler(websocket)

    async def handler(self, websocket):
        async for message in websocket:
            input_msg = Message(message)

            if input_msg.game_id == 0:
                input_msg.msg_type = 0

            if self.game_id != 0 and self.game_id != input_msg.game_id:
                input_msg.msg_type = 0

            if input_msg.msg_type == 18:
                print("IN <<< Game parameters")

                self.game_id = input_msg.game_id
                self.game_server = input_msg.json["ResponseGameParametersArgs"]["GameServer"]
                self.game_parameters = input_msg

                output_msg = PlayerConnect(self.game_server, self.game_id, self.bot_id)
                print("OUT >>> Bot connect")
                await websocket.send(output_msg.send_message())
                time.sleep(0.1)

                # Определение героя бота
                hero_type = self.game_parameters.json["ResponseGameParametersArgs"]["HeroType"]
                output_msg = PlayerChangeHero(self.game_server, self.game_id, self.bot_id, hero_type)
                print("OUT >>> Bot choose hero")
                await websocket.send(output_msg.send_message())
                time.sleep(0.1)

                # Выбор цвета игрока
                team_players = self.game_parameters.json["ResponseGameParametersArgs"]["TeamPlayers"]

                player_color = None

                for team in team_players:
                    if "PlayerId" in team:
                        if team["PlayerId"] == self.bot_id:
                            player_color = team["PlayerColor"]
                            break

                if not player_color:
                    for team in team_players:
                        if "PlayerId" not in team:
                            player_color = team["PlayerColor"]
                            break

                    output_msg = PlayerChangeColor(self.game_server, self.game_id, self.bot_id, player_color)
                    print("OUT >>> Bot choose color")
                    await websocket.send(output_msg.send_message())
                    time.sleep(0.1)

                # # Передача боту параметров игры
                self.game_parameters.json["HeroType"] = hero_type
                self.game_parameters.json["PlayerColor"] = player_color
                # msg_bytes = '{}\n'.format(input_msg.to_string()).encode()
                # self.process.stdin.write(msg_bytes)
                # self.process.stdin.flush()

            if input_msg.msg_type == 24:
                print("IN <<< Lobby changed")
                self.lobby_changed += 1
                if self.lobby_changed > 2:
                    print(">>> GAME READY <<<")

            if input_msg.msg_type == 10:
                print("IN <<< All players connected")

                output_msg = PlayerPrepared(self.game_server, self.game_id, self.bot_id)
                print("OUT >>> Bot prepared")
                await websocket.send(output_msg.send_message())

                # Передача боту параметров игры
                self.game_parameters.json["Teams"] = input_msg.json["AllPlayersConnectedArgs"]["Teams"]
                msg_bytes = '{}\n'.format(self.game_parameters.to_string()).encode()
                self.process.stdin.write(msg_bytes)
                self.process.stdin.flush()


            if input_msg.msg_type == 12:
                print("IN <<< All players prepared")

                output_msg = PlayerReady(self.game_server, self.game_id, self.bot_id)
                print("OUT >>> Bot ready")
                await websocket.send(output_msg.send_message())

            if input_msg.msg_type == 14:
                print("IN <<< All players ready")

            if input_msg.msg_type == 2:
                print("IN <<< Game started")

            if input_msg.msg_type == 4:
                if self.bot_ready:
                    print("IN <<< Game tick: " + str(input_msg.json["GameStateArgs"]["Tick"]))

                    # Если бот готов - отправляем ему стэйт
                    self.bot_ready = False

                    msg_bytes = '{}\n'.format(json.dumps(input_msg.json["GameStateArgs"], ensure_ascii=False)).encode()
                    self.process.stdin.write(msg_bytes)
                    self.process.stdin.flush()

                    # Заупскаем асинхронное ожидание команды
                    self.loop.create_task(self.get_command(websocket))

            if input_msg.msg_type == 6:
                print("IN <<< Game over")
                self.process.kill()
                await websocket.close()

            if input_msg.msg_type == 5:
                print("IN <<< Game cancel")
                self.process.kill()
                await websocket.close()

            if input_msg.msg_type == 9:
                print("IN <<< Player disconnected")

    async def get_command(self, websocket):
        while not self.bot_ready:
            command = self.process.stdout.readline().decode('utf-8').strip()
            if command == "end":
                self.bot_ready = True
            elif command:
                print("OUT >>> Send command: " + command)
                msg = GameActions(self.game_server, self.game_id, json.loads(command))
                await websocket.send(msg.send_message())


