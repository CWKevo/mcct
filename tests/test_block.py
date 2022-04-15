import mcct.minecraft.blocks as blocks



def test_chest():
    chest = blocks.ChestBlock(waterlogged=True, facing='west')
    chest.NBT.Lock = 'secret key'

    print(chest)



if __name__ == '__main__':
    test_chest()
