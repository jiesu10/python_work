from math import isfinite


class Robot:
    def __init__(self, robot_id, name, robot_type, battery, status):
        self.robot_id = robot_id
        self.name = name
        self.robot_type = robot_type
        # 受保护属性 封装
        self.battery = battery
        self._status = status

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not isfinite(value)
            or not 0 <= value <= 100
        ):
            raise ValueError("电量必须是0到100之间的有限数值")
        self._battery = value

    def show_info(self):
        """展示机器人全部信息"""
        print(f"\n【机器人ID:{self.robot_id}】 名称:{self.name}")
        print(f"设备类型:{self.robot_type},电量:{self.battery}%,状态:{self._status}")

    def work(self):
        """机器人工作，消耗电量"""
        if self._status != "工作中":
            print(f"{self.name} 当前不在工作状态，无法启动工作！")
            return
        if self.battery < 10:
            print(f"{self.name}电量过低，不能继续工作，请充电！")
            return
        self.battery -= 10
        print(f"{self.name}正在执行普通任务，消耗10%电量，剩余电量{self.battery}%")

    def charge(self):
        """充电，电量上限100"""
        add = 30
        self.battery = min(100, self.battery + add)
        print(f"{self.name}完成充电，+{add}%，当前电量{self.battery}%")

    def change_status(self, new_status):
        """修改运行状态"""
        self._status = new_status
        print(f"{self.name}状态变更为：{self._status}")


# 子类巡逻机器人，继承Robot
class PatrolRobot(Robot):
    def __init__(self, robot_id, name, robot_type, battery, status, patrol_area):
        super().__init__(robot_id, name, robot_type, battery, status)
        self.patrol_area = patrol_area  # 新增属性：巡逻区域

    # 重写work方法（多态）
    def work(self):
        if self._status != "工作中":
            print(f"{self.name}不在工作状态，无法巡逻！")
            return
        if self.battery < 20:
            print(f"{self.name}电量不足，巡逻任务需要更多电量，请充电！")
            return
        self.battery -= 20
        print(f"【巡逻机器人】{self.name}正在区域 {self.patrol_area} 巡逻，消耗20%电量，剩余{self.battery}%")

    def show_info(self):
        super().show_info()
        print(f"专属巡逻区域：{self.patrol_area}")


def main():
    """主程序演示，创建多个对象放入列表"""
    robot_list = []
    r1 = Robot(1, "机械臂A", "工业操作机器人", 80, "待机")
    r2 = PatrolRobot(2, "巡逻一号", "安防巡逻机器人", 90, "待机", "一楼实验大厅")
    r3 = Robot(3, "搬运B", "物料搬运机器人", 15, "工作中")

    robot_list.append(r1)
    robot_list.append(r2)
    robot_list.append(r3)

    print("========全部机器人信息========")
    for bot in robot_list:
        bot.show_info()

    print("\n========启动工作演示========")
    r1.change_status("工作中")
    r1.work()

    r2.change_status("工作中")
    r2.work()

    r3.work()
    r3.charge()


if __name__ == "__main__":
    main()
