import re


from tilecloud import Tile, TileStore


class LogTileStore(TileStore):
    """Generates all tile coordinates matching the specified layout from file"""

    def __init__(self, tile_layout, file=None, **kwargs):
        TileStore.__init__(self, **kwargs)
        self.tile_layout = tile_layout
        self.file = file

    def get_one(self, tile):
        tile.data = None
        return tile

    def list(self):
        # FIXME warn that this consumes file
        filename_re = re.compile(self.tile_layout.pattern)
        for line in self.file:
            match = filename_re.search(line)
            if match:
                yield Tile(self.tile_layout.tilecoord(match.group()), line=line)

    def put_one(self, tile):
        self.file.write(self.tile_layout.filename(tile.tilecoord) + '\n')
        return tile
