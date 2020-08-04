# os.path.realpath(__file__) 获取当前执行脚本的绝对路径
# os.path.dirname(path) 去掉当前执行脚本的文件名，返回文件的目录
from os.path import realpath, dirname
import json


def get_config(filename):
    # 组建json文件的路径
    path = dirname(realpath(__file__)) + '/configs/' + filename + '.json'
    with open(path, 'r', encoding='utf-8') as f:
        # 将json文件转成字典
        return json.loads(f.read())