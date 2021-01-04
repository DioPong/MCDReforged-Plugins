import os
import json

LOC_PREFFIX = 'loc'
LOC_CONF = 'config/location.json'

HELP_MESSAGE = '''
§6--------------------------§r
§6 Location Transport 201223§r
§6--------------------------§r
§2- 传送到目标地点§r §7NOP: name§r
§2- 列出所有传送点§r §7NOP: list§r 
§2- 增加指定传送点§r §7OP: add§r
§2- 删除所有传送点§r §7OP: rm§r
§6--------------------------§r
'''.strip()


def print_help_messages(server, info):
    if info.is_player:
        server.reply(info, HELP_MESSAGE)


def get_pos(server, info):
    if info.is_player:
        pos_data = str(server.rcon_query(f'data get entity {info.player} Pos')).split('[')[1][:-1].split(", ")
        dimension = server.rcon_query(f"data get entity {info.player} Dimension").split('"')[1]
        pos_x = round(float(pos_data[0][0:-1]))
        pos_y = round(float(pos_data[1][0:-1]))
        pos_z = round(float(pos_data[2][0:-1]))
        return [dimension, f"{pos_x} {pos_y} {pos_z}"]


def add_location(server, info, name, pos, alias):
    try:
        data = json.load(open(LOC_CONF))
        if data.get(name):
            server.reply(info, "§4[-] 已存在命名§r")
            return
        data.update({name: {"dimension": pos[0], "position": pos[1], "alias": alias}})
        open(LOC_CONF, 'w', encoding='utf8').write(json.dumps(data))
        server.reply(info, "§2[+] 增加成功")
    except IOError or FileNotFoundError:
        server.say("配置文件不存在！")


def rm_location(server, info, alias):
    try:
        data = json.load(open(LOC_CONF))
        if data.get(alias):
            del data[alias]
            open(LOC_CONF, 'w', encoding='utf8').write(json.dumps(data))
            server.reply(info, "§2[-] 删除成功§r")
    except IOError or FileNotFoundError:
        server.say("配置文件不存在！")


def list_location(server, info):
    data = json.load(open(LOC_CONF))
    if data:
        for item in data:
            server.reply(info, f"§c[+] {data[item]['alias']}§r§8 > {item}§r")
    else:
        server.reply(info, "§7[ ..... ]§r")


def transport(server, info, target):
    data = json.load(open(LOC_CONF))
    if data.get(target):
        server.execute(f"execute in {data[target]['dimension']} run teleport {info.player} {data[target]['position']}")


def run(server, info, commands):
    operation = commands[0]
    if operation == 'add':
        if server.get_permission_level(info) >= 3:
            name = commands[1]
            pos_info = get_pos(server, info)
            alias = commands[2] if len(commands) == 3 else name
            add_location(server, info, name, pos_info, alias)
        else:
            server.reply(info, "§3[*] 权限不足§r")
    elif operation == 'rm':
        if server.get_permission_level(info) >= 3:
            rm_location(server, info, commands[1])
        else:
            server.reply(info, "§4[*] 权限不足§r")
    elif operation == 'list':
        list_location(server, info)
    else:
        transport(server, info, operation)


def on_info(server, info):
    pre_command = info.content
    if pre_command == LOC_PREFFIX:
        print_help_messages(server, info)

    elif pre_command.startswith(LOC_PREFFIX) and info.is_player:
        commands = pre_command.replace(LOC_PREFFIX, '').split()
        run(server, info, commands)


def on_load(server, old):
    if not os.path.exists(LOC_CONF):
        with open(LOC_CONF, 'w') as f:
            f.write("{}")
    server.add_help_message("loc", "传送点管理")
