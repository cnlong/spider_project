import time
import json
import requests
import matplotlib.pyplot as plt
import numpy as np


class FeiyanData(object):
    """全国新冠肺炎数据并展示"""
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_={time}'.format(time=int(time.time()*1000))

    def get_data(self):
        """爬取数据"""
        # 获取页面返回的JSON数据的data部分
        response = requests.get(url=self.url).json()['data']
        # 将JSON格式数据转换为Python字典方便提取
        data = json.loads(response)
        # 获取省份信息
        # data['areaTree']得到是一个包含所有信息的列表，列表中有一个字典元素
        # data['areaTree'][0]获取列表中的字典
        # data['areaTree'][0]['children']获取字典中children键对应的值
        num_area = data['areaTree'][0]['children']
        # 解析所有确诊数据
        all_data = {}
        for area in num_area:
            all_data[area['name']] = area['total']['confirm']
        return all_data

    def plot_mapping(self):
        """绘制柱状图"""
        # 正常显示中文标签
        plt.rcParams['font.sans-serif'] = ['SimHei']
        # 正常显示负号
        plt.rcParams['axes.unicode_minus'] = False
        all_data = self.get_data()
        # 获取数据，便于画柱状图的XY轴
        names = all_data.keys()
        nums = all_data.values()

        # 创建长11英寸，宽7英寸的画布
        plt.figure(figsize=[11,7])
        # 在画布中创建柱状图
        # names为x轴数据，nums为Y轴数据，柱形图宽0.8，颜色为子夜
        plt.bar(names, nums, width=0.8, color='purple')
        # 设置X轴Y轴图像的标题
        plt.xlabel("地区", fontproperties='SimHei', size=15)
        plt.ylabel("人数", fontproperties='SimHei', size=12, rotation=90)
        plt.title("全国疫情确诊图", fontproperties='SimHei', size=16)
        # 将省份名称分布到X轴上
        plt.xticks(list(names), fontproperties='SimHei', rotation=-60, size=10)

        # 在每个柱状图上显示数字
        for a, b in zip(list(names), list(nums)):
            # a代表X轴位置
            # b代表Y轴位置
            # b代表添加的显示的文字
            # verticalalignment水平对齐的方式
            # horizontalalignment垂直对齐的方式
            plt.text(a, b, b, verticalalignment='bottom', horizontalalignment='center', size=6)
        # 显示柱状图
        plt.show()
        # 保存为图片
        plt.savefig('feiyan_data.jpg')


    def main(self):
        self.plot_mapping()


if __name__ == '__main__':
    feiyan_data = FeiyanData()
    feiyan_data.main()
