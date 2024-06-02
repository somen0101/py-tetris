import tkinter
import time
from tetris import Mino, Field 

def main():
    root = tkinter.Tk()
    root.title(u"Py-Tetris")

    #画面サイズ
    SIZE = 50
    #盤面作成
    test_field = Field()
    
    def key_event(event):
        key = event.keysym
        if key == "Down":
            test_mino.move_down_mino()
        if key == "Left":
            test_mino.move_left_mino()
        if key == "Right":
            test_mino.move_right_mino()

    #テトリスは10x20マスのゲーム 
    canvas = tkinter.Canvas(root, width=11 * SIZE, height=21 * SIZE)
    canvas.pack()

    root.bind("<KeyPress>", key_event)
    test_mino = Mino()

    def draw_tetris():
        canvas.delete("all")
        test_mino.draw_mino(canvas, SIZE)
        root.after(50, draw_tetris)
    
    def auto_down():
        test_mino.move_down_mino()
        root.after(1500, auto_down)
    
    root.after(50, draw_tetris)
    root.after(1500, auto_down)

    root.mainloop()
    
if __name__ == "__main__":
    main()
