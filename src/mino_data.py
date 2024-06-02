import random

class MinoData:
    SIZE = 50

    T_MINO = [[0,0,1,1],[0,1,1,2],[0,2,1,3],[1,1,2,2]]

    MINOS_DICT = {
        1 : T_MINO
    }

    @classmethod
    def get_random_mino(cls):
        RANDOM_MINOS_NUM = random.randint(1, 1)
        return cls.MINOS_DICT[RANDOM_MINOS_NUM]
