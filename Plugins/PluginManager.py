import requests
import json
import os

PLUGIN_PREFFIX = '!!plugin'
PLUGIN_CONF = 'config/plugins.json'
# ENABLE_PERMISSION = None  # None, 4:owner, 3:admin: 2:user, 1:guest


HELP_MESSAGE = '''
§6--------------------------§r
§6 Plugin Manager 201224§r
§6--------------------------§r
§2- addconf§r
§2- download§r
§2- list§r
§2- removefile§r
§2- removeconf§r
§6--------------------------§r
'''.strip()


def run(server, info, commands):
    operation = commands[0]
    if operation == 'addconf':
        if len(commands) == 3:
            plugin = commands[1]
            url = commands[2]
            try: 
                data = json.load(open(PLUGIN_CONF))
                data.update({plugin: url})
                open(PLUGIN_CONF, 'w', encoding='utf8').write(json.dumps(data))
                server.reply(info, f"§2[+] Add plugin {plugin} to config succeed§r")
            except IOError or FileNotFoundError:
                server.reply(info, "§4[-] Faild to load config§r")
    elif operation == 'download':
        plugin = commands[1]
        data = json.load(open(PLUGIN_CONF))
        if data.get(plugin):
            plg_content = requests.get(data[plugin]).text
            with open(f"plugins/{plugin}.py", 'w', encoding='utf8') as f:
                f.write(plg_content)
            server.refresh_changed_plugins()
            server.reply(info, f"§2[+] Download {plugin} succeed§r")
        else:
            server.reply(info, f"§4Plugin {plugin} Not Found!§r")
    elif operation == "list":
        data = json.load(open(PLUGIN_CONF))
        if data:
            for item in data:
                server.reply(info, f"§4> Name: {item}\n{data[item]}§r")
        else:
            server.reply(info, "§7[ ..... ]§r")
    elif operation == "removefile":
        plugin = commands[1]
        try:
            os.remove(f"plugins/{plugin}")
            server.refresh_changed_plugins()
            server.reply(info, f"§2[+] Remove {plugin} succeed§r")
        except FileNotFoundError:
            server.reply(info, "§4[-] No Such Plugin§r")
    elif operation == "removeconf":
        plugin = commands[1]
        data = json.load(open(PLUGIN_CONF))
        if data.get(plugin):
            del data[plugin]
            open(PLUGIN_CONF, 'w', encoding='utf8').write(json.dumps(data))
        else:
            server.reply(info, "§4[-] No Such Config§r")
    elif operation == 'rename':
        src, dst = commands[1], commands[2]
        try:
            if not os.path.exists(dst):
                os.rename(f"plugins/{src}", f"plugins/{dst}")
                server.refresh_changed_plugins()
                server.reply(info, f"§2[+] Rename {src} to {dst} succeed§r")
            else:
                server.reply(info, f"§4[-] Plugin {dst} already existed§r")
        except FileNotFoundError:
            server.reply(info, "§4[-] No Such Plugin§r")
    else:
        server.reply(info, "§4[-] Command Not Found§r")


def on_info(server, info):
    pre_command = info.content
    if pre_command == PLUGIN_PREFFIX and info.is_player:
        server.reply(info, HELP_MESSAGE)

    elif pre_command.startswith(PLUGIN_PREFFIX) and info.is_player:
        if server.get_permission_level(info) >= 3:
            commands = pre_command.replace(PLUGIN_PREFFIX, '').split()
            run(server, info, commands)
        else:
            server.reply(info, "§2[=] 权限不足§r")
        

def on_load(server, old):
    if not os.path.exists(PLUGIN_CONF):
        with open(PLUGIN_CONF, 'w') as f:
            f.write("{}")
    server.add_help_message("!!plugin", "自定义更新插件")
