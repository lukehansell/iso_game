from tile import TILE_TYPE

level = {
  "tiles": [
    [ TILE_TYPE.GRASS ] * 10,
    [ TILE_TYPE.GRASS ] * 10,
    [ TILE_TYPE.GRASS ] * 10,
    [ TILE_TYPE.GRASS ] * 10,
    [ TILE_TYPE.GRASS ] * 10,
    [ TILE_TYPE.GRASS ] * 10,
    [ TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.SAND ],
    [ TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.SAND, TILE_TYPE.SAND],
    [ TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.SAND, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.GRASS, TILE_TYPE.SAND, TILE_TYPE.SAND, TILE_TYPE.SAND],
    [ TILE_TYPE.GRASS, TILE_TYPE.SAND, TILE_TYPE.SAND, TILE_TYPE.SAND, TILE_TYPE.SAND, TILE_TYPE.GRASS, TILE_TYPE.SAND, TILE_TYPE.SAND, TILE_TYPE.SAND, TILE_TYPE.WATER],
  ]
}