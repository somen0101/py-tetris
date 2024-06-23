import random
from field_data import FieldData

class MinoData:
    @staticmethod
    def get_random_mino():
        T_MINO = [[1,1,2,2],[1,2,2,3],[1,3,2,4],[2,2,3,3]]
        I_MINO = [[1,0,2,1],[1,1,2,2],[1,2,2,3],[1,3,2,4]]
        O_MINO = [[1,1,2,2],[1,2,2,3],[2,1,3,2],[2,2,3,3]]
        L_MINO = [[1,2,2,3],[2,2,3,3],[3,2,4,3],[3,1,4,2]]
        J_MINO = [[1,1,2,2],[1,2,2,3],[2,2,3,3],[3,2,4,3]]
        Z_MINO = [[1,1,2,2],[2,1,3,2],[2,2,3,3],[3,2,4,3]]
        S_MINO = [[1,2,2,3],[2,2,3,3],[2,1,3,2],[3,1,4,2]]

        MINOS_DICT = {
            2 : T_MINO,
            3 : I_MINO,
            4 : O_MINO,
            5 : L_MINO,
            6 : J_MINO,
            7 : Z_MINO,
            8 : S_MINO,       
        }

        COLOR_DICT = FieldData.COLOR_DICT

        #回転時の中心ブロック
        CENTER_BLOCK_INDEX_DICT = {
            2:2,
            3:2,
            4:2,
            5:2,
            6:2,
            7:2,
            8:2,
        }

        RANDOM_MINOS_NUM = random.randint(2, 8)

        mino_data = MINOS_DICT[RANDOM_MINOS_NUM]
        mino_color = COLOR_DICT[RANDOM_MINOS_NUM]
        mino_center_block_index = CENTER_BLOCK_INDEX_DICT[RANDOM_MINOS_NUM]

        return mino_data, mino_color, RANDOM_MINOS_NUM, mino_center_block_index
