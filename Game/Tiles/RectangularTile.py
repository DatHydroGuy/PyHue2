from Game.Tiles import Tile


class RectangularTile(Tile):
    def __init__(self, grid_position, draw_position, size, game):
        super(RectangularTile, self).__init__(grid_position, draw_position, size, game)
