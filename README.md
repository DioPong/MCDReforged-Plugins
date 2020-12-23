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

> Users' data is stored in ~/config/home.json


## Plugin - Location

- Function : Set your current location to teleport. Supported dimensions: `the end`  `overworld`  `nether`
- pget URL : https://github.com/DioPong/MCDReforged-Plugins/main/Plugins/location.py

| Syntax | Description |
| -------- | -------- |
| loc new [position] [remark] | Record your current location. Remark is optional, the same as [position] by default. MCDR admin permission is required. |
| loc rm [position] | Remove existed record point. MCDR admin permission is required. |
| loc list | List all record point. |
| loc [position] | Directly transport to Target-Record-Point. |

> Users' data is stored in ~/config/home.json