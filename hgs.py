import sys
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt


DNAfull=[
[5, -4, -4, -4, -4, 1, 1,-4, -4, 1, -4, -1, -1, -1, -2],
[-4, 5, -4, -4, -4, 1, -4, 1, 1, -4, -1, -4, -1, -1, -2],
[-4, -4, 5, -4, 1, -4, 1, -4, 1, -4, -1, -1, -4, -1, -2],
[ -4, -4, -4, 5, 1, -4, -4, 1, -4, 1, -1, -1, -1, -4, -2],
[-4, -4, 1, 1, -1, -4, -2, -2, -2, -2, -1, -1, -3, -3, -1],
[1, 1, -4, -4, -4, -1, -2, -2, -2, -2, -3, -3, -1, -1, -1],
[1, -4, 1, -4, -2, -2, -1, -4, -2, -2, -3, -1, -3, -1, -1],
[-4, 1, -4, 1, -2, -2, -4, -1, -2, -2, -1, -3, -1, -3, -1],
[-4, 1, 1, -4, -2, -2, -2, -2, -1, -4, -1, -3, -3, -1, -1],
[ 1, -4, -4,  1, -2, -2, -2, -2, -4, -1, -3, -1, -1, -3, -1],
[-4, -1, -1, -1, -1, -3, -3, -1, -1, -3, -1, -2, -2, -2, -1],
[-1, -4, -1, -1, -1, -3, -1, -3, -3, -1, -2, -1, -2, -2, -1],
[-1, -1, -4, -1, -3, -1, -3, -1, -3, -1, -2, -2, -1, -2, -1],
[-1, -1, -1, -4, -3, -1, -1, -3, -1, -3, -2, -2, -2, -1, -1],
[-2, -2, -2, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
]



blosum = DNAfull

pam= DNAfull

S = -11
E = -1
MIN = -float("inf")
amino = ['A', 'T', 'G', 'C', 'S', 'W', 'R', 'Y', 'K', 'M', 'B', 'V', 'H', 'D', 'N']

def _match(s, t, i, j, matrix):
    index1 = amino.index(t[i-1])
    index2 = amino.index(s[j-1])
    return matrix[index1][index2]

def _init_x(i, j):
    if i > 0 and j == 0:
        return MIN
    else:
        if j > 0:
            return S + E * j
        else:
            return 0

def _init_y(i, j):
    if j > 0 and i == 0:
        return MIN
    else:
        if i > 0:
            return S + E * i
        else:
            return 0

def _init_m(i, j):
    if j == 0 and i == 0:
        return 0
    else:
        if j == 0 or i == 0:
            return S + E * (i+j)
        else:
            return 0


def distance_matrix(s, t, matrix):
    dim_i = len(t) + 1
    dim_j = len(s) + 1

    # Initialize matrices with zeros
    X = [[0] * dim_j for _ in range(dim_i)]
    Y = [[0] * dim_j for _ in range(dim_i)]
    M = [[0] * dim_j for _ in range(dim_i)]

    # Fill the first row and column based on the initialization functions
    for i in range(1, dim_i):
        X[i][0] = _init_x(i, 0)
        Y[i][0] = _init_y(i, 0)
        M[i][0] = _init_m(i, 0)

    for j in range(1, dim_j):
        X[0][j] = _init_x(0, j)
        Y[0][j] = _init_y(0, j)
        M[0][j] = _init_m(0, j)

    # Fill the matrices based on the recurrence relations
    for i in range(1, dim_i):
        for j in range(1, dim_j):
            X[i][j] = max(S + E + M[i][j - 1], E + X[i][j - 1])
            Y[i][j] = max(S + E + M[i - 1][j], E + Y[i - 1][j])
            M[i][j] = max(_match(s, t, i, j, matrix) + M[i - 1][j - 1], X[i][j], Y[i][j])

    return X, Y, M


def backtrace(s, t, X, Y, M, matrix):
    sequ1 = []
    sequ2 = []
    i = len(t)
    j = len(s)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and M[i][j] == M[i-1][j-1] + _match(s, t, i, j, matrix):
            sequ1.append(s[j-1])
            sequ2.append(t[i-1])
            i -= 1
            j -= 1
        elif i > 0 and M[i][j] == Y[i][j]:
            sequ1.append('_')
            sequ2.append(t[i-1])
            i -= 1
        elif j > 0 and M[i][j] == X[i][j]:
            sequ1.append(s[j-1])
            sequ2.append('_')
            j -= 1

    sequ1.reverse()
    sequ2.reverse()

    sequ1r = ' '.join(sequ1)
    sequ2r = ' '.join(sequ2)

    return sequ1r, sequ2r

class SequenceAlignmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sequence Alignment 8008121162')
        layout = QVBoxLayout()

        self.long_seq_label = QLabel('Long Sequence:')
        self.long_seq_input = QLineEdit()
        layout.addWidget(self.long_seq_label)
        layout.addWidget(self.long_seq_input)

        self.short_seq_label = QLabel('Short Sequence:')
        self.short_seq_input = QLineEdit()
        layout.addWidget(self.short_seq_label)
        layout.addWidget(self.short_seq_input)

        self.blosum_nw_button = QPushButton('DNAfull NW Align')
        self.blosum_nw_button.clicked.connect(lambda: self.align_sequences(use_blosum=True, use_sw=False))
        layout.addWidget(self.blosum_nw_button)



        # self.pam_nw_button = QPushButton('PAM250 NW Align')
        # self.pam_nw_button.clicked.connect(lambda: self.align_sequences(use_blosum=False, use_sw=False))
        # layout.addWidget(self.pam_nw_button)



        self.result_label = QLabel('Alignment Score:')
        layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def align_sequences(self, use_blosum=True, use_sw=False):
        start_time = time.time()  # 记录开始时间

        long_seq = self.long_seq_input.text().upper()
        short_seq = self.short_seq_input.text().upper()

        if not long_seq or not short_seq:
            self.result_text.setPlainText('请输入两条序列。')
            return

        for char in long_seq + short_seq:
            if char not in amino:
                self.result_text.setPlainText('序列中存在无效字符。')
                return

        if use_blosum:
            matrix_name = "DNAfull"
            matrix = blosum
        else:
            matrix_name = "DNAfull"
            matrix = pam

        method = "Needleman-Wunsch"
        X, Y, M = distance_matrix(long_seq, short_seq, matrix)
        str1, str2 = backtrace(long_seq, short_seq, X, Y, M,matrix)
        score = M[len(short_seq)][len(long_seq)]

        end_time = time.time()  # 记录结束时间
        elapsed_time = end_time - start_time  # 计算耗时
        result = f"Matrix Used: {matrix_name}\nAlignment Method: {method}\nAlignment Score: {score}\n{str1}\n{str2}\nTime Elapsed: {elapsed_time} seconds"
        self.result_text.setPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SequenceAlignmentApp()
    window.show()
    sys.exit(app.exec_())