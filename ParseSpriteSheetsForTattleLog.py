import xml.etree.ElementTree as ET
import os
from PIL import Image

#TODO: add way to specify multiple output for enemies that are duplicates
#Ex: koopa bros, jungle/forest/normal fuzzies, etc.

#sprite ids that wont have any data output for them
sprite_id_exception_list = [
    1, 2, 3, 4, 5, 6, 7, 9, 10,
    11, 12, 13, 14, 15, 17, 18,
    19, 20, 21, 22, 23, 24, 25,
    26, 27, 28, 29, 30, 31, 32,
    0x5B, 0x5C, 0x5D, 0x5E, 0x5F,
    0x60, 0x61, 0x64, 0x65, 0x75,
    0x77,
]

variants_goomba_bros = {
    "name": "GoombaBros",
    "id": "62", #is hex
    "pal_variants": {
        "GoombaBroRed": "Palette_00",
        "GoombaBroBlue": "Palette_01",
    }
}

variants_goomba = {
    "name": "Goomba",
    "id": "26", #is hex
    "pal_variants": {
        "Goomba": "Palette_00",
        "Gloomba": "Palette_04",
        "HyperGoomba": "Palette_02",
    }
}

variants_spiked_goomba = {
    "name": "SpikedGoomba",
    "id": "27", #is hex
    "pal_variants": {
        "SpikedGoomba": "Palette_00",
        "SpikedGloomba": "Palette_01",
    }
}

variants_paragoomba = {
    "name": "Paragoomba",
    "id": "28", #is hex
    "pal_variants": {
        "Paragoomba": "Palette_00",
        "Paragloomba": "Palette_03",
        "HyperParagoomba": "Palette_02",
    }
}

variants_koopa_troopa = {
    "name": "KoopaTroopa",
    "id": "29", #is hex
    "pal_variants": {
        "KoopaTroopa": "Palette_01",
        "DarkKoopa": "Palette_00",
    }
}

variants_paratroopa = {
    "name": "ParaTroopa",
    "id": "2A", #is hex
    "pal_variants": {
        "ParaTroopa": "Palette_01",
        "DarkParaTroopa": "Palette_00",
    }
}

variants_koopa_bros = {
    "name": "KoopaBros",
    "id": "66", #is hex
    "pal_variants": {
        "KoopaBrosBlack": "Palette_00",
        "KoopaBrosRed": "Palette_01",
        "KoopaBrosYellow": "Palette_02",
        "KoopaBrosGreen": "Palette_03",
    }
}

variants_fuzzy = {
    "name": "Fuzzy",
    "id": "2B", #is hex
    "pal_variants": {
        "Fuzzy": "Palette_00",
        "ForestFuzzy": "Palette_01",
        "JungleFuzzy": "Palette_03",
    }
}

variants_bullet_bill = {
    "name": "BulletBill",
    "id": "2D", #is hex
    "pal_variants": {
        "BulletBill": "Palette_00",
        "BombshellBill": "Palette_01",
    }
}

variants_bill_blaster = {
    "name": "BillBlaster",
    "id": "2E", #is hex
    "pal_variants": {
        "BillBlaster": "Palette_00",
        "BombshellBillBlaster": "Palette_01",
    }
}

variants_monty_mole = {
    "name": "MontyMole",
    "id": "2F", #is hex
    "pal_variants": {
        "MontyMole": "Palette_00",
        "MontyMoleCh6_": "Palette_01",
    }
}

variants_cleft = {
    "name": "Cleft",
    "id": "30", #is hex
    "pal_variants": {
        "Cleft": "Palette_00",
        "HyperCleft": "Palette_01",
    }
}

variants_pokey = {
    "name": "Pokey",
    "id": "31", #is hex
    "pal_variants": {
        "Pokey": "Palette_00",
        "PoisonPokey": "Palette_01",
    }
}

variants_swooper = {
    "name": "Swooper",
    "id": "34", #is hex
    "pal_variants": {
        "Swooper": "Palette_00",
        "Swoopula": "Palette_01",
    }
}

variants_putrid_piranha = {
    "name": "PutridPiranha",
    "id": "36", #is hex
    "pal_variants": {
        "PutridPiranha": "Palette_00",
        "FrostPiranha": "Palette_01",
    }
}

variants_clubba = {
    "name": "WorldClubba",
    "id": "39", #is hex
    "pal_variants": {
        "WorldClubba": "Palette_00",
        "WorldWhiteClubba": "Palette_01",
    }
}

variants_shy_guy = {
    "name": "ShyGuy",
    "id": "3B", #is hex
    "pal_variants": {
        "ShyGuy": "Palette_00",
        "AntiGuy": "Palette_05",
    }
}

variants_dayzee = {
    "name": "Dayzee",
    "id": "3B", #is hex
    "pal_variants": {
        "CrazeeDayzee": "Palette_00",
        "AmayzDayzee": "Palette_01",
    }
}

variants_bubble = {
    "name": "Bubble",
    "id": "3B", #is hex
    "pal_variants": {
        "Bubble": "Palette_00",
        "Ember": "Palette_01",
    }    
}

variants_list = [
    variants_goomba, variants_spiked_goomba, variants_paragoomba, variants_goomba_bros,
    variants_koopa_troopa,  variants_paratroopa, variants_koopa_bros,
    variants_fuzzy, variants_bullet_bill, variants_bill_blaster,
    variants_pokey, variants_monty_mole, variants_cleft,
    variants_clubba, variants_swooper, variants_putrid_piranha,
    variants_shy_guy, variants_dayzee, variants_bubble
]


def get_image_size(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except IOError:
        print("Unable to open image file:", image_path)
        return None, None

def GetEnemyInfoFromPath(sprite_table_xml, sprite_folder_path):
    actorIndex = sprite_folder_path.split("/")[-1]

    # Parse the SpriteTable XML file
    tree = ET.parse(sprite_table_xml)
    root = tree.getroot()

    # Find the NpcSprites element
    npc_sprites = root.find('NpcSprites')

    if npc_sprites is not None:
        # Iterate through the Sprite elements under NpcSprites
        for sprite in npc_sprites.findall('Sprite'):
            sprite_id = sprite.get('src')
            if actorIndex == sprite_id:
                name = sprite.get('name')
                name = name.replace(' ', '')
                #print(f"actorIndex {actorIndex}, sprite_id {sprite_id}")
                #print(f"Sprite id {sprite_id} found with name {name}")
                return name, sprite_id

    return None, None  # Return None if no matching Sprite is found

def GetEnemyNameAndSpriteID(path_to_sprite_folder):
    path_to_ActorTypes_xml = "battle/ActorTypes.xml"
    if not os.path.exists(path_to_ActorTypes_xml):
        print(f"{path_to_ActorTypes_xml} not found!")
        exit()

    path_to_sprite_table_xml = "sprite/SpriteTable.xml"
    if not os.path.exists(path_to_sprite_table_xml):
        print(f"{path_to_sprite_table_xml} not found!")
        exit()

    #print(f"Paths: {path_to_sprite_table_xml}, {path_to_sprite_folder}")
    desc, sprite_id = GetEnemyInfoFromPath(path_to_sprite_table_xml, path_to_sprite_folder)
    if desc is None:
        print("Error, enemy not found")
    else:
        return desc, sprite_id

# Load the XML file
def main():
    i = 1
    for i in range(i, 0xED): #0xED
        if i in sprite_id_exception_list:
            continue
        if i > 0x82 and i < 0xEA:
            continue
        path_to_sprite_folder = f"sprite/npc/src/{i:02X}"
        path_to_sprite_xml = path_to_sprite_folder + "/SpriteSheet.xml"

        desc, sprite_id = GetEnemyNameAndSpriteID(path_to_sprite_folder)

        tree = ET.parse(path_to_sprite_xml)
        root = tree.getroot()

        # Find the AnimationList element
        animation_list = root.find('AnimationList')

        # Find all Animation elements
        animations = animation_list.findall('Animation')

        # Check if there are any animations
        if animations:
            # Get the first animation
            animation = animations[0]
        else:
            print("No animations found.")
            exit()

        # Iterate through the Component elements under the selected Animation
        total_str = ""
        total_components = 0
        curAnimIndexStr = ""
        raster_id_list = []
        component_position_list = []
        cur_command_list = []
        for component in animation.findall('Component'):
            name = component.get('name')
            xyz = component.get('xyz')
            x, y, z = map(int, xyz.split(','))
            if y != 0:
                y *= -1  # Flip the sign on y if it's not 0
            
            # Iterate through the Command elements within the Component
            commands = component.findall('Command')
            curAnimIndex = 0
            loop_count = 0
            #print(f"Currently parsing {name}")
            #print(f"-  Commands length: {len(commands)}")
            for command in commands:
                val = command.get('val')
                val_int = int(val, 16)
                cur_command_list.append(val_int)
                val_raster_index = val_int & 0x00FF
                #print(f"-  Loop count is currently {loop_count} and val_int is {hex(val_int)}")
                if val_int & 0x3000 == 0x3000:
                    loop_count += 1
                    continue
                if val_int & 0x1F00 == 0x1F00:
                    loop_count += 1
                    continue                    
                if val_int & 0x1000:
                    #print(f"-  val_int was valid! is {val_int}")
                    curAnimIndex = val_raster_index
                    curAnimIndexStr = "{:02X}".format(val_raster_index)
                    raster_id_list.append(val_raster_index)
                    component_position_list.append(x)
                    component_position_list.append(y)
                    total_components += 1
                    #print(f"val_raster_index is {hex(val_raster_index)}")
                    break
                else:
                    #print(f"-  {hex(val_int)} Was neither")
                    loop_count += 1
        variant_total = 0
        for variant in variants_list:
            if desc == variant["name"]:
                variant_total = len(variant["pal_variants"])
                j_loop_count = 0
                for j in variant["pal_variants"]:
                    cur_item = variant["pal_variants"][j]  # Accessing the value directly using the key 'j'
                    str1 = ""
                    for i in range(total_components):
                        str1 += f"#export:Data ${j}{i}Raster {{ ~RasterFile:CI-4:../{path_to_sprite_folder}/Raster_{raster_id_list[i]:02X}.png }}\n"
                        str1 += f"#export:Data ${j}{i}Palette {{ ~PaletteFile:CI-4:../{path_to_sprite_folder}/{cur_item}.png }}\n"
                    str2 = f"#export:Data ${j}Data {{\n"
                    str2 += f"    {total_components} %number of components\n"
                    str2 += f"    %raster ptr    %palette ptr    %xpos    %ypos   %width  %height\n"
                    for i in range(total_components):
                        width, height = get_image_size(f"{path_to_sprite_folder}/Raster_{raster_id_list[i]:02X}.png")
                        str2 += f"    ${j}{i}Raster  ${j}{i}Palette    {component_position_list[i * 2]}`s    {component_position_list[i * 2 + 1]}`s   {width}`s  {height}`s\n"
                    str2 += "}"
                    print(f"{str1}{str2}")
                    j_loop_count += 1
                break


        if variant_total != 0:
            continue

        str1 = ""
        for i in range(total_components):
            str1 += f"#export:Data ${desc}{i}Raster {{ ~RasterFile:CI-4:../{path_to_sprite_folder}/Raster_{raster_id_list[i]:02X}.png }}\n"
            str1 += f"#export:Data ${desc}{i}Palette {{ ~PaletteFile:CI-4:../{path_to_sprite_folder}/Raster_{raster_id_list[i]:02X}.png }}\n"
        str2 = f"#export:Data ${desc}Data {{\n"
        str2 += f"    {total_components} %number of components\n"
        str2 += f"    %raster ptr    %palette ptr    %xpos    %ypos   %width  %height\n"
        for i in range(total_components):
            width, height = get_image_size(f"{path_to_sprite_folder}/Raster_{raster_id_list[i]:02X}.png")
            str2 += f"    ${desc}{i}Raster  ${desc}{i}Palette    {component_position_list[i * 2]}`s    {component_position_list[i * 2 + 1]}`s   {width}`s  {height}`s\n"
        str2 += "}"

        print(f"{str1}{str2}")

if __name__ == "__main__":
    main()