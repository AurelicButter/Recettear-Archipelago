from test.bases import WorldTestBase
from ..world import RecettearWorld
from .. import globals

class RecettearTestBase(WorldTestBase):
    game = globals.game
    world: RecettearWorld