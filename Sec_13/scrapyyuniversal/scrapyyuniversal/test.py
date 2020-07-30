from lxml.html import etree

text = """
<div class="bd defList" id="rank-defList">
		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569844.html" target="_blank">智能AI产业步入“深水区”</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:37</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569823.html" target="_blank">“三评”改革：激活新动能 让科技评价回归科学</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:23</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569809.html" target="_blank">国家知识产权局：我国每万人口发明专利拥有量达到14.3件</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:20</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569798.html" target="_blank">用智能制造点燃“经济炼钢”引擎 促进经济发展</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:13</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569792.html" target="_blank">“DNA元件百科全书”：超百万人类与小鼠体内调控基因的候选功能性元件</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:10</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569785.html" target="_blank">“ITER”：让“人造太阳”开启未来光明之路</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:02</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569764.html" target="_blank">数字化转型加速 线上线下融合引领消费新业态</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 10:00</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569758.html" target="_blank">科技部发布《通知》：全面加强科研作风学风建设 压实科研诚信主体责任</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:56</span> <span class="tag"></span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		
      <div class="wntjItem item_defaultView clearfix">
        <div class="item_img"><a href="http://tech.china.com/article/20200730/20200730569740.html" target="_blank"><img src="http://techchina.nancai.net/2020/0730/20200730094850106.jpg" alt="“鲲龙”入海：海上救援的“多面手”  "></a></div>
        <div class="item_con">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569740.html" target="_blank">“鲲龙”入海：海上救援的“多面手”  </a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:46</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		
      <div class="wntjItem item_defaultView clearfix">
        <div class="item_img"><a href="http://tech.china.com/article/20200730/20200730569735.html" target="_blank"><img src="http://techchina.nancai.net/2020/0730/20200730094417578.jpg" alt="“地月合影”惊艳亮相 火星环绕器还有哪些独特之处？"></a></div>
        <div class="item_con">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569735.html" target="_blank">“地月合影”惊艳亮相 火星环绕器还有哪些独特之处？</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:42</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569728.html" target="_blank">“太空表演家” 火星环绕器是怎样炼成的</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:38</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569725.html" target="_blank">搭建数字化“高速公路” 构建商用市场“内循环”生态</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:35</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569721.html" target="_blank">国内首个叶面积指数自动观测网络成功建成 已获1200万条数据</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:32</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569716.html" target="_blank">南极冰穹A，被称之为“观星宝地”</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 09:27</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		
      <div class="wntjItem item_defaultView clearfix">
        <div class="item_img"><a href="http://tech.china.com/article/20200730/20200730569709.html" target="_blank"><img src="http://techchina.nancai.net/2020/0730/20200730092359485.jpg" alt="国产大飞机“三剑客”  蓝天竞翱翔"></a></div>
        <div class="item_con">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569709.html" target="_blank">国产大飞机“三剑客”  蓝天竞翱翔</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 08:59</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569687.html" target="_blank">工业和信息化部： 加强APP侵犯用户权益专项整治 依法处置</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 08:35</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200730/20200730569686.html" target="_blank">市值大战：折射芯片业“暗战难休”</a></h3>
            <div class="item_foot"> <span class="time">2020-07-30 08:31</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729569450.html" target="_blank">中关村5G大赛正式启动：面向全球征集5G创新应用项目</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 16:32</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729569411.html" target="_blank">“了不起的中国AI”系列视频引发热议 百度大脑引领中国AI发展硕果累累</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 16:15</span> <span class="tag">人民网</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		
      <div class="wntjItem item_defaultView clearfix">
        <div class="item_img"><a href="http://tech.china.com/article/20200729/20200729569300.html" target="_blank"><img src="http://techchina.nancai.net/2020/0729/20200729024849356.png" alt="百度AI一举拿下4项中国专利政府最高奖  人工智能领域数量第一"></a></div>
        <div class="item_con">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729569300.html" target="_blank">百度AI一举拿下4项中国专利政府最高奖  人工智能领域数量第一</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 14:47</span> <span class="tag">中国网科学</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729569017.html" target="_blank">我国地面数字电视覆盖网已全面建成  无线模拟电视将退出历史舞台</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 10:48</span> <span class="tag">中国网科学</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729568995.html" target="_blank">AI面部识别技术 破解动物行为研究难题</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 10:27</span> <span class="tag">中国网科学</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729568969.html" target="_blank">深度融入新科技 未来交通场景多样化</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 10:13</span> <span class="tag">中国网科学</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729568943.html" target="_blank">“宽带短波多媒体通信系统”项目通过科技成果评价</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 10:11</span> <span class="tag">中国网科学</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>		<div class="wntjItem item_defaultView clearfix">
        <div class="item_con" style="margin-left: 0px;">
          <div class="item-con-inner">
            <h3 class="tit"><a href="http://tech.china.com/article/20200729/20200729568915.html" target="_blank">云端沟通新场景涌现 打破“孤岛”成为企业迫切需求</a></h3>
            <div class="item_foot"> <span class="time">2020-07-29 09:55</span> <span class="tag">中国网科学</span> </div>
          </div>
        </div>
        <div class="item_num"><i class="s-nub"></i></div>
      </div>	<div class="pages">
	<ul>
		<a class="a1">8704条</a> <a href="http://tech.china.com/articles/index.html" class="a1">上一页</a> <span>1</span> <a href="http://tech.china.com/articles/index_2.html">2</a> <a href="http://tech.china.com/articles/index_3.html">3</a> <a href="http://tech.china.com/articles/index_4.html">4</a> <a href="http://tech.china.com/articles/index_5.html">5</a> <a href="http://tech.china.com/articles/index_6.html">6</a> <a href="http://tech.china.com/articles/index_7.html">7</a> <a href="http://tech.china.com/articles/index_8.html">8</a> <a href="http://tech.china.com/articles/index_9.html">9</a> <a href="http://tech.china.com/articles/index_10.html">10</a> ..<a href="http://tech.china.com/articles/index_349.html">349</a> <a href="http://tech.china.com/articles/index_2.html" class="a1">下一页</a>	</ul>
	</div>
				
    </div>
"""

html = etree.HTML(text, etree.HTMLParser())
print(html.xpath('//div[@id="rank-defList"]//h3[@class="tit"]'))
