## 懂球帝数据爬取

英超数据来源：https://www.dongqiudi.com/data/1

点击进入球队信息页面（例阿森纳）：https://www.dongqiudi.com/team/50000513.html

在英超数据页面源代码中找阿森纳页面的标识ID：50000513
在JS中找到每个球队的数据，下面为一个球队的数据，其中我们需要的是team_name:"阿森纳"和team_id:"50000513"。

```bash
{goals_against:b,goals_pro:b,last_rank:b,matches_draw:b,matches_lost:b,matches_total:b,matches_won:b,points:b,rank:dk,scheme:"dongqiudi:\u002F\u002Fv1\u002Fdata\u002Fteam\u002F50000513",team_id:"50000513",team_logo:"https:\u002F\u002Fimg1.dongqiudi.com\u002Ffastdfs5\u002FM00\u002F04\u002FC8\u002FrB8BO15q_yaAdgetAABZZa53gBI322.png",team_name:"阿森纳"}
```

注意到比如第一个属性goals_against:b，​b是该JS函数传入的变量，​数据里写变量名导致这条数据没法直接去做json解析，于是选择通过简单的字符串搜索的方法去寻找我们需要的信息。



##### 爬虫流程如下：

1. 从英超数据页中爬取球队ID
2. 通过球队ID请求球队数据页。
3. 从球队数据页中爬取球员名字和球员ID，过滤掉职称为教练的球队成员。
4. 通过球员ID请求球员数据页。
5. 从球员数据页中爬取球员数据信息。



##### 待解决问题：

- 网页版数据没有客户端全，可尝试Fiddler做代理监听手机访问APP流量。

