import tkinter
import time
from tetris import Mino, Field
from mino_data import MinoData

def main():
    root = tkinter.Tk()
    root.title(u"Py-Tetris")

    #画面サイズ
    SIZE = 30
    
    #テトリスは10x20マスのゲームだが壁の部分を考慮し12x22でキャンバスを作成
    canvas = tkinter.Canvas(root, width=12 * SIZE, height=22 * SIZE)
    canvas.pack()

    #盤面作成
    test_field = Field()

    #テトリミノの生成
    test_mino = Mino(test_field.field_canvas_dict)
    root.bind("<KeyPress>", test_mino.key_event)
    
    def draw_tetris():
        #ゲームオーバーの場合はキャンバスを削除し再帰を抜ける..
        if test_field.is_game_over():
            canvas.delete("all")
            return
        
        canvas.delete("all")
        test_field.draw_field(canvas, SIZE)
        test_mino.draw_mino(canvas, SIZE)

        if test_mino.is_set:
            test_field.update_field_by_mino(test_mino)
            test_field.check_delete_target_row()
            #ミノのインスタンスを初期化しミノを再生成
            test_mino.__init__(test_field.field_canvas_dict)
            
        canvas.after(50, draw_tetris)
    
    def auto_down():
        test_mino.move_down_mino()
        canvas.after(1000, auto_down)

    draw_tetris()
    auto_down()

    root.mainloop()
    
if __name__ == "__main__":
    main()
