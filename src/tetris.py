from mino_data import MinoData 
from field_data import FieldData

#盤面
class Field:
    def __init__(self):
        self.field = self.__generate_field()
        self.field_canvas_dict = self.__convert_field_array_to_canvas_dict(self.field)
        self.game_over = False
    
    #盤面初期生成
    @staticmethod
    def __generate_field():
        #横12マスx縦22マス
        field_array = []
        for y in range(0, 22):
            row = []
            for x in range(0, 12):
                if y == 21 or (x == 0 or x == 11):
                    row.append(1)
                else:
                    row.append(0)            
            field_array.append(row)
        return field_array
    
    @staticmethod
    def __convert_field_array_to_canvas_dict(field_array):
        canvas_dict = {}
        for r_index, row in enumerate(field_array):
            row_dict = {}
            for b_index, block in enumerate(row):
                block_tuple = (b_index, r_index, b_index + 1, r_index + 1)
                row_dict[block_tuple] = block
            canvas_dict["row_" + str(r_index)] = row_dict               
        return canvas_dict
    
    @staticmethod
    def __convert_canvas_dict_to_field_array(canvas_dict):
        field_array = [] 
        for _, block_dict in canvas_dict.items():
            row_array = []
            for _ , block_value in block_dict.items():
                row_array.append(block_value)
            field_array.append(row_array)
        return field_array
    
    
    def update_field_by_mino(self, mino_cls):
        """
        この関数では移動不可能な場所を書き換える事(1->1)を考慮しない
        """
        fc_dict = self.field_canvas_dict
        for canvas_dict in fc_dict.values():
            for mino_block in mino_cls.mino:
                block_tuple = tuple(mino_block)
                if block_tuple in canvas_dict:
                    canvas_dict[block_tuple] = mino_cls.mino_num
        field_array = self.__convert_canvas_dict_to_field_array(fc_dict)
        self.field_canvas_dict = fc_dict
        self.field = field_array
        return True
    
    #盤面の描画
    def draw_field(self, canvas, SIZE):
        COLOR_DICT = FieldData.COLOR_DICT
        for block_dict in self.field_canvas_dict.values():
            for block_tuple, block_value in block_dict.items():
                if block_value != 0:
                    canvas.create_rectangle(block_tuple[0] * SIZE, 
                                        block_tuple[1] * SIZE, 
                                        block_tuple[2] * SIZE, 
                                        block_tuple[3] * SIZE, fill=COLOR_DICT[block_value])
                else:
                    canvas.create_rectangle(block_tuple[0] * SIZE, 
                                        block_tuple[1] * SIZE, 
                                        block_tuple[2] * SIZE, 
                                        block_tuple[3] * SIZE)
                    
    
    #一番下の行を確認し埋まっていたら削除
    def check_bottom_row(self):
        del_row_index_list = []
        for r_i, row in enumerate(self.field):
            if r_i == 21:
                continue
            if 0 not in row:
                del_row_index_list.append(r_i)

        #削除対象の行がなければ抜ける
        if len(del_row_index_list) == 0:
            return
        
        top_row = [1 if x == 0 or x == 11 else 0 for x in range(0, 12)]
        for r_i in del_row_index_list:
            #の行を消し、一番上に新しい行を生成
            del self.field[r_i]
            self.field.insert(0, top_row)
        self.field_canvas_dict = self.__convert_field_array_to_canvas_dict(self.field)
            
    

#テトリミノ
class Mino:
    def __init__(self, field_canvas_dict):
        mino_data, mino_color, mino_num = MinoData.get_random_mino()
        self.mino = mino_data
        self.color = mino_color
        self.mino_num = mino_num
        self.is_set = False
        self.field_canvas_dict = field_canvas_dict

    #ミノの描画
    def draw_mino(self, canvas, SIZE):
        for block in self.mino:
            canvas.create_rectangle(block[0] * SIZE, 
                                    block[1] * SIZE, 
                                    block[2] * SIZE, 
                                    block[3] * SIZE,
                                    fill = self.color)
    
    def key_event(self, event):
        key = event.keysym
        if key == "Down":
            self.move_down_mino()
        if key == "Left":
            self.move_left_mino()
        if key == "Right":
            self.move_right_mino()
    
    def move_down_mino(self):
        if self.__can_down_move():
            for block in self.mino:
                block[1] += 1
                block[3] += 1
        else:
            #最下行まで来たら盤面にミノの座標返す
            self.is_set = True

    def move_right_mino(self): 
        if self.is_set:
            return
        if self.__can_right_move():
            for block in self.mino:
                block[0] += 1
                block[2] += 1
    
    def move_left_mino(self): 
        if self.is_set:
            return
        if self.__can_left_move():
            for block in self.mino:
                block[0] -= 1
                block[2] -= 1
    
    #これ以上右に動かせるかの判定
    def __can_right_move(self):
        for canvas_dict in self.field_canvas_dict.values():
            for block in self.mino:
                block_tuple = (block[0]+ 1, block[1], block[2]+ 1, block[3])
                if canvas_dict.get(block_tuple) and canvas_dict.get(block_tuple) != 0:
                    return False 
        return True
    
    #これ以上左に動かせるかの判定
    def __can_left_move(self):
        for canvas_dict in self.field_canvas_dict.values():
            for block in self.mino:
                block_tuple = (block[0]- 1, block[1], block[2]- 1, block[3])
                if canvas_dict.get(block_tuple) and canvas_dict.get(block_tuple) != 0:
                    return False
        return True
    
    #これ以上下に動かせるかの判定
    def __can_down_move(self):
        for canvas_dict in self.field_canvas_dict.values():
            for block in self.mino:
                block_tuple = (block[0], block[1]+ 1, block[2], block[3]+ 1)
                if canvas_dict.get(block_tuple) and canvas_dict.get(block_tuple) != 0:
                    return False
        return True
    
    #一番下の行まで来たら固定する。
    def set_mino_to_field(self):
        self.is_set = True
        #self.mino = 
        return
