使用requests库和正则表达式来抓取猫眼电影TOP100的相关内容

1.目标：提取猫眼电影TOP100的电影名称、时间、评分等信息
提取的URL为https://maoyan.com/board/4

2.准备工作，安装相关的库

3.提取分析
https://maoyan.com/board/4为首页信息，前10的电影信息
https://maoyan.com/board/4?offset=10，为第11到第20的电影信息
依次类推
https://maoyan.com/board/4?offset=90，为第91到第100的电影信息

其中offset代表一种偏移量，如果偏移量为n，则显示的电影序号为n+1到n+10的电影信息。
因此只需分开请求10次，分别设置offset即可获取不同的电影信息页面