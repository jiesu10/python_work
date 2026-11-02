import os
import datetime
import json
from html import escape

DATA_FILE = "todo_data.txt"

class TodoItem:
    """待办任务类"""
    def __init__(self, title: str, priority: str, deadline: str, finished: str = "未完成"):
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.finished = finished

    def to_line(self):
        return json.dumps(
            [self.title, self.priority, self.deadline, self.finished],
            ensure_ascii=False,
        )

    @staticmethod
    def from_line(line: str):
        line = line.strip()
        if not line:
            return None
        try:
            parts = json.loads(line)
        except json.JSONDecodeError:
            # Keep reading records written by older versions of this app.
            parts = line.split("|")
        if (
            not isinstance(parts, list)
            or len(parts) != 4
            or not all(isinstance(value, str) for value in parts)
        ):
            return None
        try:
            parts[2] = datetime.datetime.strptime(parts[2], "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            # Preserve legacy records with invalid dates instead of dropping them.
            pass
        return TodoItem(parts[0], parts[1], parts[2], parts[3])


class TodoManager:
    def __init__(self):
        self.todo_list = []
        self.load_from_file()

    def load_from_file(self):
        self.todo_list.clear()
        if not os.path.exists(DATA_FILE):
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f.readlines():
                item = TodoItem.from_line(line)
                if item:
                    self.todo_list.append(item)

    def save_to_file(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for item in self.todo_list:
                f.write(item.to_line() + "\n")

    def add_task(self, title, priority, deadline):
        new_task = TodoItem(title, priority, deadline, "未完成")
        self.todo_list.append(new_task)
        self.save_to_file()

    def show_all(self):
        if len(self.todo_list) == 0:
            print("📭 当前任务清单为空！")
            return
        print("\n=======全部任务清单=======")
        for idx, task in enumerate(self.todo_list):
            print(f"[{idx+1}] {task.title:15} | {task.priority:4} | {task.deadline} | {task.finished}")

    def mark_done(self, idx):
        real_idx = idx - 1
        if 0 <= real_idx < len(self.todo_list):
            self.todo_list[real_idx].finished = "完成"
            self.save_to_file()
            print(f"✅ 任务{idx}标记为【完成】")
        else:
            print("❌编号不存在！")

    def delete_task(self, idx):
        real_idx = idx -1
        if not (0 <= real_idx < len(self.todo_list)):
            print("❌编号不存在！")
            return
        confirm = input(f"⚠️确认删除任务{idx}?(y/n):")
        if confirm.lower() == "y":
            del self.todo_list[real_idx]
            self.save_to_file()
            print(f"🗑️任务{idx}已删除")
        else:
            print("取消删除")

    def edit_task(self, idx, title=None, priority=None, deadline=None):
        real_idx = idx - 1
        if not (0 <= real_idx < len(self.todo_list)):
            print("❌编号不存在！")
            return
        if title is not None and not title.strip():
            print("❌标题不能为空！")
            return
        if priority is not None and priority not in ("高", "中", "低"):
            print("❌优先级只能是：高、中、低！")
            return
        if deadline is not None:
            try:
                deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("❌日期格式错误！")
                return
        if title is None and priority is None and deadline is None:
            print("没有需要修改的内容。")
            return

        task = self.todo_list[real_idx]
        if title is not None:
            task.title = title.strip()
        if priority is not None:
            task.priority = priority
        if deadline is not None:
            task.deadline = deadline
        self.save_to_file()
        print(f"✅任务{idx}已更新。")

    def show_finished(self):
        finished = [t for t in self.todo_list if t.finished == "完成"]
        if len(finished) == 0:
            print("没有已完成任务")
            return
        print("\n====已完成任务====")
        for i,t in enumerate(finished):
            print(f"{i+1}. {t.title} | {t.priority} | {t.deadline} | {t.finished}")

    def sort_by_deadline(self):
        sorted_tasks = sorted(self.todo_list, key=lambda x:x.deadline)
        print("\n====按截止日期排序任务====")
        for idx,t in enumerate(sorted_tasks):
            print(f"{idx+1}. {t.title:15} | {t.priority:4} | {t.deadline} | {t.finished}")

    def get_stat(self):
        total = len(self.todo_list)
        done = sum(1 for t in self.todo_list if t.finished == "完成")
        undone = total - done
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        overdue = sum(1 for t in self.todo_list if t.finished=="未完成" and t.deadline < today_str)
        rate = (done / total *100) if total>0 else 0
        return {"total":total,"done":done,"undone":undone,"overdue":overdue,"rate":rate}

    def print_stat(self):
        s = self.get_stat()
        print("\n========任务统计报告========")
        print(f"任务总数：{s['total']}")
        print(f"✅已完成：{s['done']}")
        print(f"⏳未完成：{s['undone']}")
        print(f"⚠️已逾期：{s['overdue']}")
        print(f"📊完成率：{s['rate']:.2f} %")

    def export_html(self):
        now_str = datetime.date.today().strftime("%Y-%m-%d")
        filename = f"report_{now_str}.html"
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        stat = self.get_stat()
        html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>待办任务报告 ''' + now_str + '''</title>
<style>
table {border-collapse:collapse;width:95%;margin:10px auto;}
th,td {border:1px solid #666;padding:8px;text-align:center;}
.overdue {background-color:#ffaaaa;}
</style>
</head>
<body>
<h2 align="center">待办清单报告 ''' + now_str + '''</h2>
<div align="center">
<p>总任务:''' + str(stat["total"]) + '''｜已完成:''' + str(stat["done"]) + '''｜未完成:''' + str(stat["undone"]) + '''｜逾期:''' + str(stat["overdue"]) + '''｜完成率:''' + f'{stat["rate"]:.2f}' + '''%</p >
</div>
<table>
<tr><th>序号</th><th>标题</th><th>优先级</th><th>截止日期</th><th>状态</th></tr>'''
        for idx,t in enumerate(self.todo_list):
            cls = 'overdue' if (t.finished=="未完成" and t.deadline < today_str) else ''
            html += (
                f'<tr class="{cls}"><td>{idx+1}</td>'
                f'<td>{escape(t.title)}</td><td>{escape(t.priority)}</td>'
                f'<td>{escape(t.deadline)}</td><td>{escape(t.finished)}</td></tr>'
            )
        html += '''</table>
</body>
</html>'''
        with open(filename,"w",encoding="utf-8") as f:
            f.write(html)
        print(f"📄HTML报告导出成功 → {filename}")

    def draw_chart(self):
        try:
            import cv2
            import numpy as np
        except ImportError:
            print("❌图表功能需要 OpenCV 和 NumPy，请运行：python -m pip install -r requirements.txt")
            return

        high = sum(1 for t in self.todo_list if t.priority=="高")
        mid = sum(1 for t in self.todo_list if t.priority=="中")
        low = sum(1 for t in self.todo_list if t.priority=="低")
        h,w = 480,640
        img = np.full((h,w,3),255,np.uint8)
        bar_width =120
        gap = 80
        base_y = 400
        max_bar_h =250
        data = [high,mid,low]
        colors = [(0,0,255),(0,180,0),(255,140,0)]
        labels = ["高优先级","中优先级","低优先级"]
        max_val = max(data) if max(data) !=0 else 1
        for i,val in enumerate(data):
            x1 = gap + i*(bar_width+gap)
            x2 = x1 + bar_width
            bar_h = int(val/max_val * max_bar_h)
            y1 = base_y - bar_h
            y2 = base_y
            cv2.rectangle(img,(x1,y1),(x2,y2),colors[i],-1)
            cv2.putText(img,f"{val}",(x1+40,y1-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),2)
            cv2.putText(img,labels[i],(x1+10,base_y+35),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,0),2)
        cv2.putText(img,"任务优先级统计图",(180,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)
        cv2.imwrite("chart.png",img)
        print("📊统计图已保存 chart.png")


def input_deadline(allow_empty=False):
    while True:
        prompt = "请输入截止日期(YYYY-MM-DD)（回车保留原日期）：" if allow_empty else "请输入截止日期(YYYY-MM-DD):"
        s = input(prompt).strip()
        if allow_empty and not s:
            return None
        try:
            parsed = datetime.datetime.strptime(s, "%Y-%m-%d")
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            print("❌日期格式错误！例子：2026-10-20")


def main():
    mgr = TodoManager()
    while True:
        print("\n========📒我的待办清单========")
        print("1 添加任务")
        print("2 查看全部任务")
        print("3 标记任务完成")
        print("4 删除任务")
        print("5 修改任务")
        print("6 查看已完成任务")
        print("7 按截止日期排序")
        print("8 任务统计")
        print("9 导出HTML报告")
        print("10 生成优先级统计图")
        print("0 退出程序")
        sel = input("请输入功能编号：").strip()
        if sel == "1":
            title = input("输入任务标题：").strip()
            if not title:
                print("标题不能为空！")
                continue
            while True:
                prio = input("输入优先级(高/中/低):").strip()
                if prio in ("高","中","低"):
                    break
                print("只能输入：高、中、低！")
            dl = input_deadline()
            mgr.add_task(title,prio,dl)
            print("✅任务添加成功！")
        elif sel == "2":
            mgr.show_all()
        elif sel == "3":
            mgr.show_all()
            try:
                num = int(input("输入要标记完成的任务编号："))
                mgr.mark_done(num)
            except ValueError:
                print("❌请输入数字！")
        elif sel == "4":
            mgr.show_all()
            try:
                num = int(input("输入要删除的任务编号："))
                mgr.delete_task(num)
            except ValueError:
                print("❌请输入数字！")
        elif sel == "5":
            mgr.show_all()
            try:
                num = int(input("输入要修改的任务编号："))
            except ValueError:
                print("❌请输入数字！")
                continue
            title = input("输入新标题（回车保留）：").strip()
            while True:
                prio = input("输入新优先级(高/中/低，回车保留)：").strip()
                if not prio or prio in ("高", "中", "低"):
                    break
                print("只能输入：高、中、低！")
            deadline = input_deadline(allow_empty=True)
            mgr.edit_task(num, title or None, prio or None, deadline)
        elif sel == "6":
            mgr.show_finished()
        elif sel == "7":
            mgr.sort_by_deadline()
        elif sel == "8":
            mgr.print_stat()
        elif sel == "9":
            mgr.export_html()
        elif sel == "10":
            mgr.draw_chart()
        elif sel == "0":
            mgr.save_to_file()
            print("👋程序退出，数据已保存。")
            break
        else:
            print("❌无效编号，请输入0-10")


if __name__ == "__main__":
    main()
