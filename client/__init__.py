import asyncio
import traceback
from typing import Optional
import colorama
import Utils
from typing import Any
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, server_loop
from .. import globals
from .constants import ClientStatus
from pymem.exception import ProcessNotFound, ProcessError, PymemError, WinAPIError
import logging
from .MemoryManager import MemoryManager
from .RecettearProcess import RecettearProcess

debug_logger = logging.getLogger("RecettearDebug")

class RecettearCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_connection_status(self):
        """Check connection to Recettear"""
        if isinstance(self.ctx, RecettearContext):
            logger.info(f"Recettear status: {self.ctx.game_status}")

    def _cmd_resync(self):
        """Forces a resync to receive all items again from the beginning. Triggering this is not reversable."""
        self.ctx: RecettearContext

        self.ctx.memManager.reset_store()
        self.ctx.memManager.get_ap_store().last_check_received = -1
        asyncio.create_task(self.ctx.send_msgs([{ "cmd": "Sync" }]))

class RecettearContext(CommonContext):
    __ready: bool = False
    __held_item_ids: list[int] = []

    command_processor = RecettearCommandProcessor
    game = globals.game
    items_handling = 0b111
    memManager: MemoryManager | None = None
    game_process: RecettearProcess | None = None

    def __init__(self, server_address: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Initializes the context

        :param server_address: Address of the Archipelago server.
        :param password: Password for server authentication
        """
        super().__init__(server_address, password)

        self.game_status = ClientStatus.CONNECTION_INITIAL
        self.ap_connected = False
        self.fully_connected = False
        self.memManager = MemoryManager()

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server
        
        :param password_requested: Whether the server requires a password.
        """

        # Expand functionality to check for active game and slot before authentication.

        if password_requested and not self.password:
            await super(RecettearContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

        self.ap_connected = True
        self.set_client_status()
        
    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        await super().disconnect(allow_autoreconnect)
        self.set_client_status(disconnect=True)

    def update_storage_keys(self, item_updates: dict[str, int], operation="add"):
        """
        Updates the data storage keys with a given value

        :param item_updates: A key, value dictionary containing keys to update with the values to add
        :param operation: The operation to use on all provided item updates. Defaults to add
        """

        update_items = []
        for key, value in item_updates.items():
            update_items.append({ "key": key, "value": value, "operation": operation })

        if len(update_items) > 0:
            msg_set = []

            for pair in update_items:
                msg_set.append({
                    "cmd": "Set",
                    "key": pair["key"],
                    "want_reply": False,
                    "operations": [{ "operation": pair["operation"], "value": pair["value"]}]
                })

            asyncio.create_task(self.send_msgs(msg_set))

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: Command received from the server
        :param args: The arguements for the command
        """

        if cmd == "Connected":
            slot_data: dict = args.get("slot_data", {})
            gen_game_version: str = slot_data.get("game_version")
            
            if gen_game_version[:gen_game_version.rfind(".")] != globals.world_version[:globals.world_version.rfind(".")]:
                self.gui_error("Incompatible Client Version",
                    f"This slot was generated with RecettearAP version {gen_game_version} and " +
                    f"is only compatible with ~{gen_game_version[:gen_game_version.rfind(".")] + ".X"} versions. " +
                    f"This client's version is {globals.world_version} which is not allowed.")
                self.disconnect()
                return

            self.memManager.update_slot_data(slot_data)
            self.memManager.set_location_checks(self.checked_locations)
            
            self.set_notify("last_check_received")
        elif cmd == "ReceivedItems":
            if self.__ready is False:
                self.__held_item_ids.extend([item.item for item in args.get("items", [])])
            else:
                storage_updates = self.memManager.received_items([item.item for item in args.get("items", [])])
                self.update_storage_keys(storage_updates)            
        elif cmd == "Retrieved":
            if self.__ready is False:
                keys: dict[str, any] = args.get("keys")

                if "last_check_received" in keys:
                    last_check = keys.get("last_check_received")
                    if last_check not in (None, -1):
                        self.memManager.update_item_tracking(keys)
                    else:
                        self.update_storage_keys({ "last_check_received": -1 }, "replace")

                    storage_updates = self.memManager.ready_items(self.__held_item_ids)
                    self.update_storage_keys(storage_updates, "replace")
                    self.__held_item_ids.clear()
                    self.__ready = True

        super().on_package(cmd, args)

    def run_gui(self):
        from kvui import GameManager

        class RecettearManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = f"{globals.game.replace("Tale", "Archipelago")} Client"

        self.ui = RecettearManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def set_client_status(self, disconnect=False, process_lost=False) -> None: 
        self.fully_connected = False

        if disconnect:
            self.ap_connected = False
            self.game_status = ClientStatus.CONNECTION_DISCONNECTED
        elif process_lost:
            self.game_status = ClientStatus.CONNECTION_GAME_LOST
        elif self.ap_connected and self.game_process is not None:
            self.game_status = ClientStatus.CONNECTION_CONNECTED
            self.fully_connected = True
        elif self.ap_connected:
            self.game_status = ClientStatus.CONNECTION_AP_CONNECTION
        elif self.game_process is not None:
            self.game_status = ClientStatus.CONNECTION_GAME_CONNECTION
        else:
            self.game_status = ClientStatus.CONNECTION_GAME_LOST

        logger.info(self.game_status)

    def open_game_process(self) -> bool:
        try:
            self.game_process = RecettearProcess()
        except ProcessNotFound:
            self.game_status = ClientStatus.CONNECTION_GAME_REFUSED
            logger.info(self.game_status)
            return False
        except ProcessError as e:
            self.game_status = ClientStatus.CONNECTION_GAME_REFUSED            
            logger.info(f"Unexpected error connecting to Recettear: {e}")
            return False

        self.memManager.add_game_process(self.game_process)

        self.set_client_status()
        return True
        
    async def unhook_game_process(self):            
        if self.game_process is not None:
            self.game_process = self.game_process.close_process()

        self.memManager.remove_game_process()

        self.set_client_status(process_lost=True)

async def game_watcher(ctx: RecettearContext):
    sleep_time = 0.0
    while not ctx.exit_event.is_set():
        if sleep_time > 0.0:
            try:
                await asyncio.wait_for(ctx.watcher_event.wait(), sleep_time)
            except asyncio.TimeoutError:
                pass
            sleep_time = 0.0
            ctx.watcher_event.clear()

        try:
            if ctx.game_process is None:
                if not ctx.open_game_process():
                    logger.info("Connection to Recettear failed, attempting again in 5 seconds...")
                    sleep_time = 5
                else:
                    # Pass successful connection silently. Add 5 seconds to allow for AP connection.
                    sleep_time = 10
            elif not ctx.fully_connected:
                logger.info(ctx.game_status)
                logger.info("Retrying connection in 5 seconds...")
                sleep_time = 5
            else: # Client is fully connected to server & game. Begin processing game data and monitoring.
                location_ids = ctx.memManager.search_locations()
                ctx.locations_checked.update(location_ids)

                locations_checked = ctx.locations_checked.difference(ctx.checked_locations)
                if locations_checked:
                    await ctx.check_locations(locations_checked)

                sleep_time = 0.1
        except Exception as e:
            await ctx.unhook_game_process()

            if isinstance(e, (ProcessNotFound, ProcessError, PymemError, WinAPIError)):
                msg = "Connection to game lost, attempting re-connection in 5 seconds..."
                debug_logger.error(traceback.format_exc())
            else:
                msg = "Unexpected error occurred, attempting re-connection to game in 5 seconds..."
                logger.error(traceback.format_exc())
            logger.info(msg)
            await ctx.disconnect()
            sleep_time = 5
            continue

def main():
    Utils.init_logging("RecettearClient", exception_logger="ClientException")

    async def _main():
        ctx = RecettearContext()
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        game_watcher_task = asyncio.create_task(game_watcher(ctx), name="RecettearGameWatcher")

        await ctx.exit_event.wait()
        ctx.watcher_event.set()
        ctx.server_address = None

        try:
            await game_watcher_task
        except Exception as e:
            logger.exception(e)

        await ctx.shutdown()

    colorama.init()
    asyncio.run(_main())
    colorama.deinit()