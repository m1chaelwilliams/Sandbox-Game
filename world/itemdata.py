from sprites.tile import *

class Item:
    def __init__(self, name: str = "default", quantity: int = 0) -> None:
        self.name = name
        self.quantity = quantity
        self.target_group = None
    def use(self, *args, **kwargs):
        pass
    def pickup(self, amount = 1):
        self.quantity += amount
    def drop(self, amount = 1) -> int:
        amt = amount
        self.quantity -= amount
        if self.quantity < 0:
            amt -= abs(self.quantity)
            self.quantity = 0
        return amt
    def empty(self):
        self.name = "default"
        self.quantity = 0
    def __str__(self) -> str:
        return f'Name: {self.name}, Quantity: {self.quantity}'

class BlockItem(Item):
    def __init__(self, name: str, quantity: int = 1) -> None:
        super().__init__(name, quantity)
    def use(self, image, position, groups, chunk, *args, **kwargs):
        self.quantity -= 1
        if self.quantity < 0:
            self.quantity = 0
        else:
            block = items[self.name].use_type(groups, image, position, name=self.name, hardness=items[self.name].hardness, durability=items[self.name].durability)
            chunk.add_block(block)
        if self.quantity == 0:
            self.name = "default"
class SpecialBlockItem(Item):
    def __init__(self, name: str = "default", quantity: int = 0, target_group="block_group") -> None:
        super().__init__(name, quantity)
        self.target_group = target_group
    def use(self, image, position, groups, chunk, *args, **kwargs):
        self.quantity -= 1
        if self.quantity < 0:
            self.quantity = 0
        else:
            block = items[self.name].use_type(groups, image, position, name=self.name, hardness=items[self.name].hardness, durability=items[self.name].durability)
            chunk.add_block(block)
        if self.quantity == 0:
            self.name = "default"
class DirectionalBlockItem(Item):
    def __init__(self, name: str = "default", quantity: int = 0) -> None:
        super().__init__(name, quantity)
    def use(self, image, position, groups, chunk, flipped: bool = False):
        self.quantity -= 1
        if self.quantity < 0:
            self.quantity = 0
        else:
            block = items[self.name].use_type(groups, image, position, name=self.name, flipped = flipped, hardness=items[self.name].hardness, durability=items[self.name].durability)
            chunk.add_block(block)
        if self.quantity == 0:
            self.name = "default"

        
class ItemData:
    def __init__(self, name: str, type: Item, groups = ['sprites', 'block_group'], use_type: Tile = Tile, type_str: str = "block", durability: int = 20, hardness: int = 1, strength: int = 1) -> None:
        self.name = name
        self.type = type
        self.type_str = type_str
        self.groups = groups
        self.use_type = use_type
        self.durability = durability
        self.hardness = hardness
        self.strength = strength

items = {
    'grass':ItemData('grass', BlockItem),
    'dirt':ItemData('dirt', BlockItem),
    'stone':ItemData('stone', BlockItem, hardness=2, durability=40),
    'wood':ItemData('wood', BlockItem, durability=30),
    'coal':ItemData('coal', BlockItem, hardness=2, durability=40),
    'iron':ItemData('iron', BlockItem, hardness=3, durability=50),
    'diamond':ItemData('diamond', BlockItem, hardness=4, durability=70),
    'leaves':ItemData('leaves', BlockItem),
    'chest':ItemData('chest', SpecialBlockItem, groups=['item_group', 'block_group', 'chest_group'], use_type=StorageBlock),
    'crafting_table':ItemData('crafting_table', BlockItem, groups=['sprites', 'platform_group']),
    'wood_planks':ItemData('wood_planks', BlockItem),
    'wood_slab':ItemData('wood_slab', BlockItem),
    'wood_stairs':ItemData('wood_stairs', DirectionalBlockItem),
    'grass_wall':ItemData('grass_wall', BlockItem, ['wall_group', 'block_group'], use_type=WallBlock, type_str="wall"),
    'stone_wall':ItemData('stone_wall', BlockItem, ['wall_group', 'block_group'], use_type=WallBlock, type_str="wall"),
    'dirt_wall':ItemData('dirt_wall', BlockItem, ['wall_group', 'block_group'], use_type=WallBlock, type_str="wall"),
    'wood_wall':ItemData('wood_wall', BlockItem, ['wall_group', 'block_group'], use_type=WallBlock, type_str="wall"),
    'door':ItemData('door', SpecialBlockItem, ['item_group', 'block_group'], use_type=DoorBlock),
    'wood_platform':ItemData(name='wood_platform', type=BlockItem, groups=['platform_group', 'sprites'], type_str="platform"),
    'wood_pickaxe':ItemData(name='wood_pickaxe', type=Item, strength=2),
    'stone_pickaxe':ItemData(name='stone_pickaxe', type=Item, strength=3),
    'iron_pickaxe':ItemData(name='iron_pickaxe', type=Item, strength=4),
    'diamond_pickaxe':ItemData(name='diamond_pickaxe', type=Item, strength=5),
    'furnace':ItemData(name='furnace', type=BlockItem, groups=['sprites', 'platform_group'], use_type=FurnaceBlock, durability=50),
    'stick':ItemData(name='stick', type=Item, groups=['sprites']),
    'default':ItemData('default', Item),
}