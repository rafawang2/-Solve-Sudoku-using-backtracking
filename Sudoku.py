from collections import deque

class Sudoku:
    def __init__(self, board):
        self.board = board

    def print_board(self): 
        for row in self.board:
            for num in row:
                if num == 0:
                    print(' ',end=' ')
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
     
    #回朔法(stack方法)
    def backtrack(self):
        stack = []
        empty = self.find_empty()
        
        #沒有空白，代表已完成
        if not empty:
            return True
        
        row, col = empty
        num = 1
        while True:
            #嘗試填數字
            while num <= 9:
                if self.is_valid(row, col, num):
                    
                    #填上當前數字並把當前狀態推入stack
                    self.board[row][col] = num
                    stack.append((row, col, num))
                    
                    #找下一個空格
                    empty = self.find_empty()
                    if not empty:
                        #完成數獨
                        return True
                    
                    row, col = empty
                    #下一個空格再從1重新開始填
                    num = 1
                    break
                #num數到9，還有空白但已經沒得填 => num += 1 -> 10，回朔回上一部 
                num += 1
            
            #回溯
            if num > 9:
                if not stack:
                    #無解
                    return False
                
                #回溯到上一個狀態
                #從stack取出上一步的狀態
                prev_row, prev_col, prev_num = stack.pop()
                #將上一步恢復為0
                self.board[prev_row][prev_col] = 0
                #更新當前位置為上一步的位置
                row, col = prev_row, prev_col
                #嘗試填入上一步數字的下一個數字(以免又填入相同的數字)
                num = prev_num + 1
    def DFS(self):
        empty = self.find_empty()
        if not empty:
            return True  # 解決成功

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.board[row][col] = num

                if self.DFS():  # 遞歸
                    return True

                # 回溯
                self.board[row][col] = 0
        
        return False  # 解決失敗
    
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

game = Sudoku(board=board1)
game.print_board()
game.DFS()
game.print_board()