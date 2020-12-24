# MCDReforged-Plugins

A repository for plugins, based on [MCDReforged](https://github.com/Fallen-Breath/MCDReforged)

## Plugin - Home

- Function : `Set home and teleport to your home.`
- pget URL : https://github.com/DioPong/MCDReforged-Plugins/main/Plugins/home.py

| Syntax       | Description                                    |
| ------------ | ---------------------------------------------- |
| home         | Go back to you home                            |
| home sethome | Get your current location as your home.        |
| home help    | Print help messages, help you use this plugin. |

> Users' data is stored in ~/config/home.json. it will be generated when the plugin is loaded if not exists.


## Plugin - Location

- Function : Set your current location to teleport. Supported dimensions: `the end`  `overworld`  `nether`
- pget URL : https://github.com/DioPong/MCDReforged-Plugins/main/Plugins/location.py

| Syntax | Description |
| -------- | -------- |
| loc new [position] [remark] | Record your current location. Remark is optional, the same as [position] by default. MCDR admin permission is required. |
| loc rm [position] | Remove existed record point. MCDR admin permission is required. |
| loc list | List all record point. |
| loc [position] | Directly transport to Target-Record-Point. |

> Users' data is stored in ~/config/home.json. it will be generated when the plugin is loaded if not exists.

## PluginManager

- Function : Manager your plugin from remote host.
- pget URL : https://github.com/DioPong/MCDReforged-Plugins/main/Plugins/PluginManager.py

| Syntax                                         | Description                    |
| ---------------------------------------------- | ------------------------------ |
|!!plugin|Print help message|
| !!plugin addconf [alias/plg name] [remote url] | Add new plugin to config file. |
|!!plugin removeconf|Remove specify plugin from config.|
|!!plugin removefile|Remove Plugin.|
|!!plugin list|Print all existed URLs in config file.|
|!!plugin download|Read config file and download specify plugin|

> Here is a how-to-use-example :
>```Minecraft
> !!plugin add home https://raw.githubusercontent.com/DioPong/MCDReforged-Plugins/main/Plugins/home.py
> !!plugin download home
>```

> The plugin PluginManager itself is in the blocklist, you are supposed to no operation this plugins itself.
>
> Plugin's data is stored in ~/config/PluginManager.json, it will be generated when the plugin is loaded if not exists.

> MCDR permission >= `admin` required

## SpecificRoutine

This plugin is only for [DDServer](https://minecraft.diopong.top/). It's very cheated, you should use it.

I push it to Github only for managing it easily from remote via PluginManager mentioned above.

| Syntax     | Description                                                 |
| ---------- | ------------------------------------------------------------ |
| sr p/peace | Spawn carpet bot to specify location to launch the **Chunk** in the nether. |
|sr day|execute time set 3000|
|sr n/night|execute time set 13000|
|sr c/clear|execute weather clear|
|sr r/rain|execute weather rain|
|sr head [player]|get [player]'s head|
|sr restart|Simply restart the server|

> `sr head [player]` | `[sr restart]` : Require MCDR permission >= `admin`.