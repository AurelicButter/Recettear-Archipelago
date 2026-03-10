from .world import RecettearWorld as RecettearWorld
from worlds.LauncherComponents import Component, components, launch_subprocess

def launch_client() -> None:
    from .client import main
    launch_subprocess(main, name="Recettear Client")

def add_client_to_launcher() -> None:
    components.append(Component("Recettear Client", func=launch_client))

add_client_to_launcher()