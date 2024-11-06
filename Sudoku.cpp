#include <iostream>
#include <vector>
#include <stack>
#include <string>

using namespace std;

class Sudoku
{
private:
    vector<vector<int>> m_board;
public:
    Sudoku(vector<vector<int>> board)
    {
        m_board = board;
    }
    void printBoard()
    {
        string buffer = "+ - + - + - + - + - + - + - + - + - +";
        cout<<buffer<<endl;
        for(int i=0; i<9; i++)
        {
            for(int j=0; j<9; j++)
            {
                cout<<"| "<<m_board[i][j]<<" ";
            }
            cout<<"|"<<endl<<buffer<<endl;
        }
    }
    bool isValid(const int& row,const int& col,const int& num)
    {
        for(int i=0; i<9; i++)
        {
            if(m_board[row][i] == num)
                return false;
        }
        for(int i=0; i<9; i++)
        {
            if(m_board[i][col] == num)
                return false;
        }


        int start_row = 3 * (row / 3);
        int start_col = 3 * (col / 3);
        for(int i=start_row; i<start_row+3; i++)
        {
            for(int j=start_col; j<start_col+3; j++)
            {
                if( m_board[i][j] == num)
                    return false;
            }
        }
        return true;
    }

    pair<int, int> find_empty()
    {
        pair<int, int> pos(9,9);    //回傳(9,9)=>None
        for(int i=0; i<9; i++)
        {
            for(int j=0; j<9; j++)
            {
                if(m_board[i][j] == 0)
                {
                    pos = pair<int,int>(i,j);
                    return pos;
                }
            }
        }
        return pos;
    }
    bool backTracking()
    {
        stack<vector<int>> states;
        pair<int, int> empty = find_empty();
        //沒有空白
        if(empty == pair<int, int>(9,9))
            return true;
        int row = empty.first;
        int col = empty.second;
        int num = 1;
        while(1)
        {
            while(num<=9)
            {
                if(isValid(row,col,num))
                {
                    m_board[row][col] = num;
                    states.push({row,col,num});
                    empty = find_empty();
                    if(empty == pair<int, int>(9,9))
                        return true;
                    row = empty.first;
                    col = empty.second;
                    num = 1;
                    break;
                }
                num++;
            }
            if(num>9)
            {
                if(states.empty())
                {
                    return false;
                }
                vector<int> pre_state = states.top();
                states.pop();
                m_board[pre_state[0]][pre_state[1]] = 0;
                row = pre_state[0];
                col = pre_state[1];
                num = pre_state[2] + 1;
            }
        }
    }
};


int main()
{
    vector<vector<int>> board = {
        {0, 0, 0, 8, 0, 6, 0, 0, 0},
        {0, 0, 0, 0, 2, 0, 0, 7, 0},
        {0, 0, 9, 4, 0, 0, 5, 0, 0},
        {4, 0, 0, 0, 0, 0, 3, 0, 6},
        {3, 0, 0, 0, 0, 0, 0, 0, 0},
        {2, 6, 0, 0, 0, 1, 7, 0, 0},
        {9, 3, 5, 0, 1, 0, 0, 4, 0},
        {0, 0, 0, 5, 0, 8, 2, 0, 0},
        {0, 0, 0, 0, 0, 3, 0, 1, 0},
    };
    Sudoku game(board);
    game.printBoard();
    cout<<"<===================================>"<<endl;
    game.backTracking();
    game.printBoard();
    return 0;
}