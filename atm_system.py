import sys
import random
from math import isfinite
from datetime import datetime


def show_menu():
    """打印主菜单"""
    print("\n========欢迎来到银行ATM========")
    print("1.查询余额")
    print("2.存款")
    print("3.取款")
    print("4.退出系统")
    print("==============================")


def query_balance(balance):
    """
    查询余额
    :param balance: 当前账户余额
    :return: 无
    """
    print(f"\n【余额查询】您当前账户余额：{balance} 元")


def save_money(balance):
    """
    存款功能
    :param balance: 当前余额
    :return: 更新后的余额
    """
    while True:
        try:
            money = float(input("\n请输入存款金额："))
            if not isfinite(money) or money <= 0:
                print("输入错误！存款金额必须是大于0的有限数字，请重新输入！")
                continue
            new_balance = balance + money
            # 生成6位流水号
            serial = random.randint(100000, 999999)
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"存款成功！本次存入：{money}元")
            print(f"交易流水号：{serial}，交易时间：{now_time}")
            print(f"更新后账户余额：{new_balance} 元")
            return new_balance
        except ValueError:
            print("输入不是合法数字，请重新输入！")


def draw_money(balance):
    """
    取款功能
    :param balance: 当前余额
    :return: 更新后余额
    """
    while True:
        try:
            money = float(input("\n请输入取款金额："))
            if not isfinite(money) or money <= 0:
                print("取款金额必须是大于0的有限数字！")
                continue
            if money > balance:
                print(f"余额不足！当前余额 {balance} 元，无法取出 {money} 元")
                return balance
            new_balance = balance - money
            serial = random.randint(100000, 999999)
            now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"取款成功！本次取出：{money}元")
            print(f"交易流水号：{serial}，交易时间：{now_time}")
            print(f"更新后账户余额：{new_balance} 元")
            return new_balance
        except ValueError:
            print("输入不是合法数字，请重新输入！")


def main():
    """ATM主程序循环"""
    balance = 5000  # 初始余额5000元
    while True:
        show_menu()
        op = input("请输入功能选择(1-4):")
        if op == "1":
            query_balance(balance)
        elif op == "2":
            balance = save_money(balance)
        elif op == "3":
            balance = draw_money(balance)
        elif op == "4":
            print("\n感谢使用ATM系统，再见！")
            sys.exit(0)
        else:
            print("输入有误，请输入1~4之间数字！")


if __name__ == "__main__":
    main()
