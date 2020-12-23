from os import rename, remove, path, getcwd
from time import sleep
import re
from utils.rtext import *

# >>>>> Special Commands for DTS <<<<<

PREFFIX = "sr"

HELP_MESSAGE = '''
§6------ SpecificRoutine Center ------§r
§d 快捷自定义指令插件§r§5【说明】(可以首字母替换)§r
§6--------------------------------§r
'''.strip()

operations = '''
§7{0}§r 显示帮助信息
§7{0} day/night§r 切换白天/夜晚
§7{0} clean/r§r 切换晴天/雨天
§7{0} peace§r 机器人开启伪和平
'''.strip().format(PREFFIX)


def command_run(message, text, command):
    return RText(message).set_hover_text(text).set_click_event(RAction.run_command, command)


def print_message(server, info, msg, tell=True):
    if info.is_player:
        server.reply(info, msg)


def print_help_messages(server, info):
    if info.is_player:
        server.reply(info, HELP_MESSAGE)
        text = f"§7{PREFFIX} 显示帮助信息§r\n" \
               f"§7{PREFFIX} " + RText('peace', color=RColor.yellow).h(f'假人开启伪和平§r').c(RAction.run_command, f'{PREFFIX} peace\n') + "§7 伪和平§r\n" \
               f"§7{PREFFIX} " + RText('clear', color=RColor.yellow).h(f'晴天§r').c(RAction.run_command, f'{PREFFIX} clear') + ' | ' + RText('rain', color=RColor.yellow).h(f'雨天§r').c(RAction.run_command, f'{PREFFIX} rain') + "§7 切换晴天/雨天§r\n" + \
               f"§7{PREFFIX} " + RText('day', color=RColor.yellow).h(f'白天§r').c(RAction.run_command, f'{PREFFIX} day') + ' | ' + RText('night', color=RColor.yellow).h(f'夜晚§r').c(RAction.run_command, f'{PREFFIX} night') + "§7 切换白天/夜晚§r\n" 
        print_message(
            server, info,
            text + "§6--------------------------------§r"
        )


def load_command(server, info, commands):
    command = commands[0]

    # Set timer --------------------------------------------------------
    if command in ["d", "day"]:
        server.execute('time set 3000')

    elif command in ["n", "night"]:
        server.execute('time set 13000')

    # Set Weather ------------------------------------------------------
    elif command in ["c", "clear"]:
        server.execute('weather clear')

    elif command in ["r", "rain"]:
        server.execute('weather rain')

    # Load peace -------------------------------------------------------
    elif command in ["peace", "p"]:
        server.execute(f'execute in minecraft:the_end run player bot spawn at 51 112 155')
        sleep(0.5)
        server.execute(f'player peace kill')
        sleep(0.5)
        server.say("§6>> 伪和平开启 <<§r")

    # Misc -------------------------------------------------------------
    elif command == "clean":
        server.reply(info, "\n"*20)

    # Sensitive permissions --------------------------------------------
    # restart
    elif command == "restart":
        # admin and owner
        if server.get_permission_level(info) >= 3:
            server.restart()

    elif command == "head":
        if len(commands) == 2:
            if server.get_permission_level(info) >= 3:
                head = "minecraft:player_head{SkullOwner:" + commands[1] + "}"
                server.execute(f"give {info.player} {head}")
            else:
                server.reply(info, "§d［权限不足］§r")

    # plugin manager
    elif command in ["plg", "plugin"]:
        if len(commands) == 3:
            operation = commands[1]
            if operation in ["remove", "removeconfirm", "restore"]:
                if server.get_permission_level(info) == 4:
                    plugin_name = commands[2]
                    plugin_full_name = path.join(getcwd(), f"plugins/{plugin_name}")

                    server.reply(info, f"§7[*]You are trying to remove plg{plugin_name}")

                    if operation == "remove":
                        try:
                            rename(plugin_full_name, plugin_full_name + '.bak')
                            server.say(f"§a[+] Plugin {plugin_name} remove succeed§r")
                        except FileNotFoundError:
                            server.say(f"§c[+] Plugin {plugin_name} remove failed§r")
                    elif operation == "removeconfirm":
                        try:
                            remove(plugin_full_name) if path.exists(plugin_full_name) else remove(
                                plugin_full_name + '.bak')
                            server.say(f"§a[+] Plugin {plugin_name} delete succeed§r")
                        except FileNotFoundError:
                            server.say(f"§c[+] Plugin {plugin_name} delete failed§r")
                    elif operation == "restore":
                        try:
                            rename(plugin_full_name + '.bak', plugin_full_name)
                            server.say(f"§a[+] Plugin {plugin_name} restore succeed§r")
                        except FileNotFoundError:
                            server.say(f"§c[+] Plugin {plugin_name} restore failed§r")
    else:
        server.reply(info, '§d【命令错误】§r')


def on_info(server, info):
    # specify server_background and user
    cm = info.content
    if cm == PREFFIX:
        print_help_messages(server, info)

    elif cm.startswith(PREFFIX) and info.is_player:
        command_splited = cm.replace(PREFFIX, '').split()
        load_command(server, info, commands=command_splited)
    else:
        return False

def on_load(server, old):
    server.add_help_message("sc", "简易指令")
