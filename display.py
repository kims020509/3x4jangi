from tkinter import *
import BOARD

class Display:
    def __init__(self):
        self.log = '로그 기록'
        self.md = Tk()
        self.md.title("12 장기")
        self.md.geometry("320x240+200+200")
        self.md_log = Label(self.md, text= self.log, width= 20, height= 7, anchor= 'n')
        self.md_command = [Label(self.md, text= "다음 수 : "), Entry(self.md), Button(self.md, text= "입력", command= self.command_button_click)]
        
    def start(self):
        self.md_log.grid(columnspan= 3, padx= 10, pady= 10)
        for i in range(3): self.md_command[i].grid(row= 1, column= i, padx=5)
        self.md.mainloop()

    def command_button_click(self):
        self.log += '\n' + self.md_command[1].get()
        print(self.log)
        self.md_log.config(text = self.log)
        self.md_command[1].delete(0)
        
    
if __name__ == '__main__':
    Test = Display()
    Test.start()
