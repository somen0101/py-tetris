from mino_data import MinoData 

class Mino:
    def __init__(self):
        self.mino = MinoData.get_random_mino()
    
    def move_down_mino(self):
        for block in self.mino:
            block[1] += 1
            block[3] += 1

    def move_right_mino(self): 
        for block in self.mino:
            block[0] += 1
            block[2] += 1
    
    def move_left_mino(self): 
        for block in self.mino:
            block[0] -= 1
            block[2] -= 1
    
    #ミノの描画
    def draw_mino(self, canvas, SIZE):
        block_1 = canvas.create_rectangle(self.mino[0][0] * SIZE, self.mino[0][1] * SIZE, self.mino[0][2] * SIZE,self.mino[0][3] * SIZE)
        block_2 = canvas.create_rectangle(self.mino[1][0] * SIZE, self.mino[1][1] * SIZE, self.mino[1][2] * SIZE,self.mino[1][3] * SIZE)
        block_3 = canvas.create_rectangle(self.mino[2][0] * SIZE, self.mino[2][1] * SIZE, self.mino[2][2] * SIZE,self.mino[2][3] * SIZE)
        block_4 = canvas.create_rectangle(self.mino[3][0] * SIZE, self.mino[3][1] * SIZE, self.mino[3][2] * SIZE,self.mino[3][3] * SIZE)
        return block_1, block_2, block_3, block_4
    
    #これ以上右に動かせるかの判定
    def can_right_move(self):
        for block in self.mino:
            if block[0] == 5 or block[2] == 5:
                return False
        return True
    
    #これ以上左に動かせるかの判定
    def can_left_move(self):
        for block in self.mino:
            if block[0] == 0 or block[2] == 0:
                return False
        return True

#盤面
class Field:
    def __init__(self):
        self.field = self.generate_field()
    
    #盤面初期生成
    @staticmethod
    def generate_field():
        #横12マスx縦21マス
        field_array = []
        for y in range(0, 21):
            temp = []
            for x in range(0, 12):
                if y == 20 or (x == 0 or x == 11):
                    temp.append(1)
                else:
                    temp.append(0)            
            field_array.append(temp)
        return field_array
    
    #一列揃ったら一番下を削除する
    def delete_line():
        return
