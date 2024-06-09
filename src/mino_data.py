import random

class MinoData:
    @staticmethod
    def get_random_mino():
        T_MINO = [[1,1,2,2],[1,2,2,3],[1,3,2,4],[2,2,3,3]]
        I_MINO = [[1,1,2,2],[1,2,2,3],[1,3,2,4],[1,4,2,5]]
        

        MINOS_DICT = {
            2 : T_MINO,
            3 : I_MINO,
        }

        COLOR_DICT = {
            2 : "red",
            3 : "green",
        }

        RANDOM_MINOS_NUM = random.randint(3, 3)

        mino_data = MINOS_DICT[RANDOM_MINOS_NUM]
        mino_color = COLOR_DICT[RANDOM_MINOS_NUM]

        return mino_data, mino_color, RANDOM_MINOS_NUM
