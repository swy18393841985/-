import sys
import random
from itertools import chain
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class Buttonkeyboard:
    Up = 0
    Down = 1
    Left = 2
    Right = 3


class MyLabel(QLabel):
    def __init__(self, text=None):
        super().__init__()
        # 颜色字典
        self.color = {"2": "#FFF5EE", "4": "#EED5B7", "8": "#D2B48C", "16": "#CD853F", "32": "#CD6839", "64": "#8B4726",
                      "128": "#A52A2A", "256": "#B22222", "512": "#8B3626", "1024": "#8B2500", "2048": "#8B0000",
                      "4096": "#8B0000", "8192": "#696969", "16384": "#363636", "32768": "#1C1C1C"}
        self.setFixedSize(80, 80)
        self.setFont(QFont(QFont("Arial Black", 15, QFont.Bold)))
        self.setAlignment(Qt.AlignCenter)
        # 设置边框
        if text != "0":
            self.setText(text)
            color = "background-color:%s;border-width: 1px;border-style: solid; border-color: gray;" % self.color.get(
                text, "#bbb5b0")
            self.setStyleSheet(color)
        else:
            # 设置颜色和
            self.setStyleSheet(
                "background-color:#bbb5b0;color:black;border-width: 1px;border-style: solid; border-color: gray;")


class Main(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化界面
        self.reset()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("2048")
        self.setFixedSize(338, 400)
        # 分数栏
        self.label = QLabel("分数: %s" % str(self.grade))
        self.label.setFont(QFont("Berlin Sans FB", 20, QFont.Bold))

        self.grid = QGridLayout(self)
        # 设置间距为0
        self.grid.setSpacing(0)
        self.grid.addWidget(self.label, 0, 0, 1, 4, alignment=Qt.AlignCenter)
        self.addblock()
        self.show()

    # 用 block 来填充界面
    def addblock(self):
        self.label.setText("分数: %s" % str(self.grade))
        for i in range(1, 5):
            for j in range(0, 4):
                self.grid.addWidget(MyLabel(str(self.block[i - 1][j])), i, j)

    # 生成最开始的界面
    def gameStart(self):
        for i in range(0, 2):
            self.block[random.randint(0, 3)][random.randint(0, 3)] = self.random[random.randint(0, 1)]

    # 胜利在数字块中出现2048
    def is_win(self):
        if max(list(chain(*self.block))) == "2048":
            return True

    def reset(self):
        self.random = ["2", "4"]
        self.grade = 0
        # 初始化界面
        self.block = [["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"], ["0", "0", "0", "0"]]
        self.gameStart()

    def keyPressEvent(self, QKeyEvent):
        # 向上移动
        if QKeyEvent.key() == Qt.Key_Up:
            # 向上那么我们只需让其实现行列转换就可以变为左移
            self.block = self.transpose(self.block)
            self.show_block()
            # 再将其复原
            self.block = self.transpose(self.block)
            self.addblock()

        # 向下移动
        if QKeyEvent.key() == Qt.Key_Down:
            self.block = self.transpose(self.block)
            self.block = self.revers_block(self.block)
            self.show_block()
            self.block = self.revers_block(self.block)
            self.block = self.transpose(self.block)
            self.addblock()

        # 向左移动
        if QKeyEvent.key() == Qt.Key_Left:
            self.show_block()

            self.addblock()
        # 向右移动
        if QKeyEvent.key() == Qt.Key_Right:
            '''
            现反转矩阵然后向左移动、在反转回来
            '''
            # 反转
            self.block = self.revers_block(self.block)

            self.show_block()

            self.block = self.revers_block(self.block)
            # 重新填充界面
            self.addblock()

    """
    程序的主要算法

    """

    # 调用移动和随机出现模块
    def show_block(self):
        # 如果胜利
        if self.is_win():
            result = QMessageBox.question(self, '恭喜你胜利了', \
                                          '重新开始', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                self.reset()
        elif self.move_possible():
            for row in self.block:
                self.move(row)
            self.random_block()

        # 行数都没有可以合并的而且找不到空白的块
        elif not self.gameOver():
            result = QMessageBox.question(self, '很遗憾', \
                                          '重新开始', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                self.reset()

    # 判断所有的行列是否有可以消除的
    def gameOver(self):
        # 判断行和列有没有可以合并的
        for i in range(0, 4):
            for j in range(0, 3):
                # self.block[i][j] == self.block[i][j+1] 判断行  or 后边判断列 这里直接包含了空白
                if self.block[i][j] == self.block[i][j + 1] or self.block[j][i] == self.block[j + 1][i]:
                    return True
        if not self.find_blank():
            return False

    # 判断是否有移动的可能
    def move_possible(self):
        # 只要有一行可移动就可以移动
        for row in self.block:
            for i in range(len(row) - 1):
                # 前边有空白
                if row[i] == "0" and row[i + 1] != "0":
                    return True
                # 没有空白可以合并
                if row[i] != "0" and row[i] == row[i + 1]:
                    return True
        return False

    # 移动
    def move(self, row):
        '''
        如果说我们可以将二位列表进行转动，那么是不是可以实现所有的移动都是向某一个方向进行的
        我们以向左为例
        '''
        # 记录有数字的下标
        subscript = []
        col_num = 0
        for col_value in row:
            if col_value != "0":
                subscript.append(col_num)
            col_num += 1

        # 如果这一行存在不为0的数字
        if len(subscript) > 0:
            b = 0
            while b < len(row):
                # len(subscript) 表示这一行有值的个数
                if b < len(subscript):
                    # 让值替换  原来的列表从左到右的值，直到所有值替换完成
                    row[b] = row[subscript[b]]
                # 如果有值得替换完则让其他的用0来替换实现移动效果
                else:
                    row[b] = "0"
                # 合并 只有所有的都没有合并的时候才返回False
                self.merge_black(row, b)
                # 如果有合并
                b += 1

    # 合并
    def merge_black(self, row, col_num):
        if col_num > 0 and row[col_num] == row[col_num - 1] and row[col_num] != "0":
            row[col_num - 1] = str(int(row[col_num]) + int(row[col_num - 1]))
            self.grade += 2
            row[col_num] = "0"
            new_num = 0
            old_row_num = 0
            # 记录下不是"0"的数字的位置
            while new_num < len(row):
                if row[new_num] != "0":
                    # 从列表最左边开始替换
                    row[old_row_num] = row[new_num]
                    old_row_num += 1
                new_num += 1
            # 将剩下的都变为"0"
            while old_row_num < len(row):
                row[old_row_num] = "0"
                old_row_num += 1

    # 随机出现块
    def random_block(self):
        def choice(lis):
            # 随机选 可以选两个或者一个 更多的是2 少数为4
            num = random.randint(0, len(lis) - 1)
            if random.randint(0, 100) > 89:
                self.block[lis[num][0]][lis[num][1]] = "4"
            else:
                self.block[lis[num][0]][lis[num][1]] = "2"

        lis = self.find_blank()
        choice(lis)

    # 寻找空白
    def find_blank(self):
        # 空白块下标位置
        blank_postion = []
        row_num = 0
        for row in self.block:
            col_num = 0
            for col in row:
                if col == "0":
                    blank_postion.append((row_num, col_num))
                col_num += 1
            row_num += 1
        return blank_postion

    # 矩阵(二位列表)转置
    def transpose(self, field):
        return [list(row) for row in zip(*field)]

    # 矩阵逆转让每一行实现倒序
    def revers_block(self, field):
        return [row[::-1] for row in field]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())