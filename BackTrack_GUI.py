from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QSlider, QPushButton
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys, os

class GameWindow(QMainWindow):
    def __init__(self,board):
        super(GameWindow, self).__init__()
        self.setGeometry(500, 200, 950, 650)
        self.setWindowTitle('Sudoku Solver Visualization')
        self.gap = 50
        self.BoardStart_pos = (60, 60)
        self.board = board
        self.current_cell = None
        
        # 初始化回溯狀態
        self.stack = []
        self.current_pos = None
        self.current_num = 1
        
        self.Board_1 = [
        [0, 0, 0, 8, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 7, 0],
        [0, 0, 9, 4, 0, 0, 5, 0, 0],
        [4, 0, 0, 0, 0, 0, 3, 0, 6],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 6, 0, 0, 0, 1, 7, 0, 0],
        [9, 3, 5, 0, 1, 0, 0, 4, 0],
        [0, 0, 0, 5, 0, 8, 2, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 1, 0],
        ]
        
        # 添加控制按鈕
        self.setup_controls()
        
        # 設置定時器
        self.timer = QTimer()
        self.timer.timeout.connect(self.backtrack)
    
    def print_board(self): 
        for row in self.board:
            for num in row:
                if num == 0:
                    print('▢',end=' ')
                else:
                    print(num,end=' ')
            print()
    
    def is_valid(self, row, col, num):
        #檢查行與列
        for i in range(9):
            if self.board[row][i] == num:
                return False
        for i in range(9):
            if self.board[i][col] == num:
                return False

        # 檢查3x3
        start_row = 3 * (row // 3)
        start_col = 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == num:
                    return False
        return True
        
    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    #直接回傳第一個找到的空白
                    return (row, col)
        #如果找不到空位，返回None
        return None
     
    def backtrack(self):
        self.update()
        if self.current_pos is None:
            empty = self.find_empty()
            if not empty:
                self.timer.stop()
                self.start_button.setText('Completed')
                return True
            self.current_pos = empty
            self.current_num = 1
            self.current_cell = empty
            self.update()
            return False

        row, col = self.current_pos

        # 嘗試填入數字
        while self.current_num <= 9:
            if self.is_valid(row, col, self.current_num):
                # 填入數字
                self.board[row][col] = self.current_num
                self.stack.append((row, col, self.current_num))
                
                # 找下一個空格
                empty = self.find_empty()
                if not empty:
                    self.timer.stop()
                    self.start_button.setText('Completed')
                    return True
                
                # 更新當前位置
                self.current_pos = empty
                self.current_num = 1
                self.current_cell = empty
                self.update()
                return False
            
            self.current_num += 1

        # 如果當前位置試完1-9都不行，需要回溯
        if self.current_num > 9:
            if not self.stack:
                self.timer.stop()
                self.start_button.setText('No Solution')
                return False
            
            # 回溯到上一個狀態
            prev_row, prev_col, prev_num = self.stack.pop()
            self.board[prev_row][prev_col] = 0
            self.current_pos = (prev_row, prev_col)
            self.current_num = prev_num + 1
            self.current_cell = (prev_row, prev_col)
            self.update()
            return False
    
    def setup_controls(self):
        # 開始按鈕
        self.start_button = QPushButton('Start', self)
        self.start_button.setGeometry(600, 100, 100, 30)
        self.start_button.clicked.connect(self.start_solving)
        
        # 速度滑塊
        self.speed_slider = QSlider(Qt.Horizontal, self)
        self.speed_slider.setGeometry(600, 150, 200, 30)
        self.speed_slider.setMinimum(1)
        self.speed_slider.setMaximum(1000)
        self.speed_slider.setValue(100)
        self.speed_slider.valueChanged.connect(self.update_speed)
        
    def start_solving(self):
        if not self.timer.isActive():
            self.timer.start(self.speed_slider.value())
            self.start_button.setText('Stop')
        else:
            self.timer.stop()
            self.start_button.setText('Start')
    
    def update_speed(self):
        if self.timer.isActive():
            self.timer.setInterval(self.speed_slider.value())
    
    def paintEvent(self, event):
        painter = QPainter(self)
        self.draw_board(painter)
    
    def draw_board(self, painter):
        Dots_pen = QPen(QColor('#000000'), 1)
        thick_pen = QPen(QColor('#000000'), 3)
        
        # 畫格線
        length = self.gap * 9
        for i in range(10):
            if i % 3 == 0:
                painter.setPen(thick_pen)
            else:
                painter.setPen(Dots_pen)
            
            y = self.BoardStart_pos[1] + i * self.gap
            painter.drawLine(self.BoardStart_pos[0], y, 
                           self.BoardStart_pos[0] + length, y)
            
            x = self.BoardStart_pos[0] + i * self.gap
            painter.drawLine(x, self.BoardStart_pos[1], 
                           x, self.BoardStart_pos[1] + length)

        # 畫數字和高亮當前格子
        x = self.BoardStart_pos[0] + (self.gap)//4 - self.gap
        y = self.BoardStart_pos[1] + (self.gap-20)//2 + 20
        for i in range(9):
            for j in range(9):           
                # 繪製高亮背景
                x += self.gap
                if self.current_cell and self.current_cell == (i, j):
                    painter.fillRect(self.BoardStart_pos[0]+self.gap*j, self.BoardStart_pos[1]+self.gap*i, self.gap, self.gap, 
                                  QColor(255, 255, 0, 100))
                # 繪製數字
                number = self.board[i][j]
                if number != 0:
                    painter.setFont(QFont('Arial', 20))  # 設置字體和大小
                    # 計算每個數字的中心位置，讓數字在格子內居中
                    painter.drawText(x, y, str(number))  # 指定位置 (x, y) 和文字內容
            y += self.gap
            x = self.BoardStart_pos[0] + (self.gap)//4 - self.gap

def window():
    board1 = [
        [0, 0, 0, 8, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 7, 0],
        [0, 0, 9, 4, 0, 0, 5, 0, 0],
        [4, 0, 0, 0, 0, 0, 3, 0, 6],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 6, 0, 0, 0, 1, 7, 0, 0],
        [9, 3, 5, 0, 1, 0, 0, 4, 0],
        [0, 0, 0, 5, 0, 8, 2, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 1, 0],
    ]
    
    board2 =[
        [0,0,2,0,0,0,0,8,4],
        [0,0,1,6,0,0,0,0,7],
        [5,4,9,8,2,7,0,1,3],
        [0,1,5,0,0,0,3,7,8],
        [7,0,3,0,0,5,4,0,9],
        [9,2,0,0,0,0,5,0,0],
        [1,5,0,4,0,0,0,0,2],
        [0,0,0,7,0,3,0,9,6],
        [0,0,6,0,1,0,0,0,5]
    ]
    
    app = QApplication(sys.argv)
    win = GameWindow(board=board1)
    win.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    window()
    