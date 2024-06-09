import tkinter
import time
from tetris import Mino, Field
from mino_data import MinoData

def main():
    root = tkinter.Tk()
    root.title(u"Py-Tetris")

    #画面サイズ
    SIZE = 30
    
    #テトリスは10x20マスのゲーム 
    canvas = tkinter.Canvas(root, width=12 * SIZE, height=22 * SIZE)
    canvas.pack()

    #盤面作成
    test_field = Field()
    #print(test_field.field)
    #print(test_field.field_canvas_dict)

    #テトリミノの生成
    test_mino = Mino(test_field.field_canvas_dict)
    root.bind("<KeyPress>", test_mino.key_event)
    
    def draw_tetris():
        canvas.delete("all")
        test_field.draw_field(canvas, SIZE)
        test_mino.draw_mino(canvas, SIZE)
        print(test_mino.is_set)
        if test_mino.is_set:
            test_field.update_field_by_mino(test_mino)
            test_field.check_bottom_row()
            #print(test_field.field)
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
