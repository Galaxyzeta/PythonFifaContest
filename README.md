# PythonFifaContest
这是HDU Python竞赛关于Fifa数据集的数据挖掘与web展示项目。
技术：
- 后端：django
- 前端：html+css+js+bootstrap+chart.js(待用)

## 简介
1. 在 AllPlayer 页面展示所有的球员简略信息，带分页。
2. 在 BestPlayer 页面选择10人职业，查询最佳选择后，前端canvas绘制球员在足球场的位置。

## Todo
1. 在前端添加 Analysis 页面，调用后端给出的数据生成图表进行展示。
2. 增加更多的后端分析函数，以备前端使用。
3. 某个图存在球半径过大问题 晚些改

##  Changelog

- 加入了消息提示
- 部分分析页面
- 加入散点图
- 增加selectbox可选项
- 加入饼图

## 用法
1. 安装django pandas numpy
2. cd BackEnd ==> python mange.py runserver 开启服务器
3. https://localhost:8000/app/xxxx 得到后台查询结果，具体查询url请看 BackEnd/MainApp/urls.py