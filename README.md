# Recettear: An Item Shop's Archipelago

An [Archipelago](https://archipelago.gg) implementation for [Recettear: An Item Shop's Tale](https://store.steampowered.com/app/70400/Recettear_An_Item_Shops_Tale/).

## Installation

Recettear Archipelago is provided as an all-in-one APWorld/Client. Install the APWorld as normally done for custom worlds. Then launch the `Recettear: An Item Shop's Client` in the AP Launcher.

## Player Setup

Requirements:
- Windows OS
- Archipelago 0.6.7+
- A legal copy of [Recettear: An Item Shop's Tale](https://store.steampowered.com/app/70400/Recettear_An_Item_Shops_Tale/) through Steam (on latest version)

To setup and connect to the multiworld:

1. Install the client with the instructions from [Installation](#installation)
2. Start Recettear: An Item Shop's Tale 
3. Load into a game file (either a new game or save file)
4. Start the AP client, Recettear: An Item Shop's Tale Client from the AP launcher
5. Provide AP connection details
6. If successfully, the client should print out `Ready! Connected to both Recettear and Archipelago.`

## Support 

Found a bug? Or having trouble with something? You can either open an issue here on this GitHub repository [here](https://github.com/AurelicButter/Recettear-Archipelago/issues/new) or ask in the [Recettear thread](https://discord.com/channels/731205301247803413/1434321415921860768) on the Archipelago server.

## Development Setup

To setup Recettear Archipelago for development, do the following:

1. Clone the [Archipelago](https://github.com/ArchipelagoMW/Archipelago) repository and follow AP's official guide on [Running From Source](https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/running%20from%20source.md)
2. In the local repo, checkout the latest version tag (ie: 0.6.7)
3. Clone Recettear Archipelago as a subrepo in the `worlds` directory. (See below for example)

```
Archipelago (https://github.com/ArchipelagoMW/Archipelago)
    -> worlds
        -> recettear (https://github.com/AurelicButter/Recettear-Archipelago)
            -> __init__.py
            -> ...
```

4. Run Archipelago. The world and client will be installed automatically. To update changes, simply restart the Archipelago process.

## Credits

A special thanks to these initial articles and posts for documenting Recettear. Without them, it's very likely this would not exist.
- [(Wikia) Recettear Wiki](https://recettear.fandom.com/wiki/Recettear_Wiki) 
- [(Steam) Recettear HexEdit for HACKERS](https://steamcommunity.com/sharedfiles/filedetails/?id=677693042)
- [(Cheat Engine) Recettear 1.108 Steam](https://fearlessrevolution.com/viewtopic.php?t=803)

In addition, these repositories helped determine the route to take as well as provide some inner working details on how Recettear functions.
- [(GitHub) Recemoddar](https://github.com/ribeena/Recemoddar)
- [(GitHub) Recettear Repacker](https://github.com/UnrealPowerz/recettear-repacker)
