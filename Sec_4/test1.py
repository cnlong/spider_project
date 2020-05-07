from lxml.html import etree
text = """
<div>
<ul> 
<li class="item-0"><a href="link1.html">first item</a></li> 
<li class="item-1"><a href="link2.html">second item</a></li> 
<li class="item-inactive"><a href="link3.html">third item</a></li> 
<li class="item-1"><a href="link4.html">fourth item</a></li> 
<li class="item-0"><a href＝"link5.html">fifth item</a> 
</ul> 
</div>
"""
# 使用HTML类实例化一个XPath对象
html = etree.HTML(text)
# 调用实例对象的tostring方法，修正不完整的HTML文档
# 注意，输出结果是byte类型，需要转换
result = etree.tostring(html)
print(result.decode('utf-8'))