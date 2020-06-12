"""
调度模块：
1.定时去调用获取模块从各大网站爬取代理
2.定时去调用检测模块检测代理可用性
3.调用展示模块，获取最新的代理，无需定时执行，只需要开启即可
"""
from multiprocessing import Process
from api import app
from getter import Getter
from tester import Tester
import time


# 定义检测和获取模块循环时间为20秒
GETTER_CYCLE = 20
TESTER_CYCLE = 20

# 定义模块开启开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True


class Scheduler(object):
    """定义调度器"""
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """定时20秒检测代理"""
        tester = Tester()
        while True:
            """无限循环检测"""
            print("测试器开始运行")
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """定时20秒获取代理"""
        getter = Getter()
        while True:
            print("开始抓取代理")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """开启API,无需循环，不像其他两个模块定期更新数据库的东西"""
        app.run()

    def run(self):
        print("代理池开始运行")
        # 三个模块调用三个进程运行
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester())
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter())
            getter_process.start()
        if API_ENABLED:
            api_process = Process(target=self.schedule_api())
            api_process.start()

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.run()