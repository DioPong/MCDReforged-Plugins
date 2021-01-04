import json
import os

HOME_PREFFIX = 'home'
HOME_CONF = 'config/home.json'

HELP_MESSAGE = '''
§6--------------------------§r
§6 Home 201223§r
§6--------------------------§r
§7help§r §2- 帮助§r 
§7sethome§r §2- 设置家§r 
§6--------------------------§r
'''.strip()


def print_help_messages(server, info):
    if info.is_player:
        server.reply(info, HELP_MESSAGE)


def loading(server, info, command):
    if command == 'set':
        pos_data = str(server.rcon_query(f'data get entity {info.player} Pos')).split('[')[1][:-1].split(", ")
        dim = server.rcon_query(f"data get entity {info.player} Dimension").split('"')[1]
        pos_x = round(float(pos_data[0][0:-1]))
        pos_y = round(float(pos_data[1][0:-1]))
        pos_z = round(float(pos_data[2][0:-1]))
        try:
            
            data = json.load(open(HOME_CONF))
            name = info.player
            flag = False
            if data.get(name):
                flag = True
                
            
            data.update({info.player: {"dimension": dim, "position": f"{pos_x} {pos_y} {pos_z}"}})
            open(HOME_CONF, 'w', encoding='utf8').write(json.dumps(data))
            if flag: 
                server.reply(info, '§6[+] 更新成功§r') 
            else: 
                server.reply(info, '§6[+] 添加成功§r')
            
        except FileNotFoundError or IOError:
            server.reply('§6[+] 添加失败§r') 

    elif command == "help":
        print_help_messages(server, info)


def tp(server, info):
    data = json.load(open(HOME_CONF))[info.player]
    server.execute(f"execute in {data['dimension']} run teleport {info.player} {data['position']}")


def on_info(server, info):
    pre_command = info.content
    if pre_command == HOME_PREFFIX and info.is_player:
        tp(server, info)
    elif pre_command.startswith(HOME_PREFFIX) and info.is_player:
        loading(server, info, pre_command.replace(HOME_PREFFIX, '').strip())


def on_load(server, old):
    if not os.path.exists(HOME_CONF):
        with open(HOME_CONF, 'w') as f:
            f.write("{}")
    server.add_help_message(HOME_PREFFIX, "My House")
