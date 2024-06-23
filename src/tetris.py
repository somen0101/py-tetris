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
        #横12マスx縦22マスを生成する
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
    
    
    def update_field_by_mino(self, mino_obj):
        """
        NOTE:
        この関数では移動不可能な場所を書き換える事(1->1)を考慮しない
        """
        fc_dict = self.field_canvas_dict
        for canvas_dict in fc_dict.values():
            for mino_block in mino_obj.mino:
                block_tuple = tuple(mino_block)
                if block_tuple in canvas_dict:
                    canvas_dict[block_tuple] = mino_obj.mino_num
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
    
    #全ての行を確認し削除対象の行(埋まっている行)を削除
    def check_delete_target_row(self):
        del_row_index_list = []
        for r_i, row in enumerate(self.field):
            if r_i == 21:
                continue
            if 0 not in row:
                del_row_index_list.append(r_i)

        #削除対象の行がなければ早めに抜ける
        if len(del_row_index_list) == 0:
            return
        
        top_row = [1 if x == 0 or x == 11 else 0 for x in range(0, 12)]
        for r_i in del_row_index_list:
            #削除対象の行を消し、一番上に新しい行を生成
            del self.field[r_i]
            self.field.insert(0, top_row)
        self.field_canvas_dict = self.__convert_field_array_to_canvas_dict(self.field)

    def is_game_over(self):
        for block in self.field[0]:
            if block != 0 and block != 1:
                self.game_over = True
                return True
        return False 
            
    

#テトリミノ
class Mino:
    def __init__(self, field_canvas_dict):
        mino_data, mino_color, mino_num, mino_center_block_index = MinoData.get_random_mino()
        self.mino = mino_data
        self.color = mino_color
        self.mino_num = mino_num
        self.center_block_index = mino_center_block_index
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
        if key == "Up":
            self.rotate_mino()
    
    def move_down_mino(self):
        if self.is_set:
            return
        if self.__can_down_move():
            for block in self.mino:
                block[1] += 1
                block[3] += 1
        else:
            #最下行まで来たら固定する
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
    
    def rotate_mino(self):
        if self.is_set:
            return
        if self.__can_rotate():
            #回転中心軸のブロック
            center_block = self.mino[self.center_block_index]
            rotate_center_x = center_block[0]
            rotate_center_y = center_block[1]
            for b_i, block in enumerate(self.mino):
                if b_i != self.center_block_index:
                    before_x = block[0]
                    before_y = block[1]
                    block[0] = -before_y + rotate_center_x + rotate_center_y
                    block[1] = before_x - rotate_center_x + rotate_center_y
                    block[2] = block[0] + 1
                    block[3] = block[1] + 1
    
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
    
    #回転可能の判定
    def __can_rotate(self):
        #回転中心軸のブロック
        center_block = self.mino[self.center_block_index]
        rotate_center_x = center_block[0]
        rotate_center_y = center_block[1]
        for canvas_dict in self.field_canvas_dict.values():
            for b_i, block in enumerate(self.mino):
                if b_i != self.center_block_index:
                    before_x = block[0]
                    before_y = block[1]
                    x_1 = -before_y + rotate_center_x + rotate_center_y
                    y_1 = before_x - rotate_center_x + rotate_center_y
                    x_2 = x_1 + 1
                    y_2 = y_1 + 1
                    block_tuple = (x_1, y_1, x_2, y_2)
                    if canvas_dict.get(block_tuple) and canvas_dict.get(block_tuple) != 0:
                        return False
        return True
