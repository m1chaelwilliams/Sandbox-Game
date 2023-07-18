base_recipes = [
    {'output':'wood_planks','quantity':4,'recipe':{'wood':1}},
    {'output':'stick','quantity':4,'recipe':{'wood_planks':1}},
    {'output':'wood_slab','quantity':2,'recipe':{'wood_planks':1}},
    {'output':'wood_stairs','quantity':4,'recipe':{'wood_planks':6}},
    {'output':'wood_platform','quantity':2,'recipe':{'wood_planks':1}},
    {'output':'crafting_table','quantity':1,'recipe':{'wood_planks':4}},
    
]
table_recipes = [
    *base_recipes,
    {'output':'chest','quantity':1,'recipe':{'wood_planks':8}},
    {'output':'wood_wall','quantity':16,'recipe':{'wood_planks':4}},
    {'output':'furnace','quantity':1,'recipe':{'stone':8}},
    {'output':'door','quantity':1,'recipe':{'wood_planks':4}},
    {'output':'wood_pickaxe','quantity':1,'recipe':{'stick':2, 'wood_planks':3}},
    {'output':'stone_pickaxe','quantity':1,'recipe':{'stick':2, 'stone':3}},
    {'output':'iron_pickaxe','quantity':1,'recipe':{'stick':2, 'iron':3}},
    {'output':'diamond_pickaxe','quantity':1,'recipe':{'stick':2, 'diamond':3}},
]
