import requests
from bs4 import BeautifulSoup

base = "https://www.dongqiudi.com"
qualified_nation = ['喀麦隆', '塞内加尔', '突尼斯', '阿尔及利亚', '摩洛哥', '尼日利亚',   # 一档
                    '埃及', '加纳', '科特迪瓦', '马里', '布基纳法索', '几内亚',          # 二档
                    '佛得角', '加蓬', '毛里塔尼亚', '津巴布韦', '几内亚比绍', '塞拉利昂',  # 三档
                    '马拉维', '苏丹', '赤道几内亚', '科摩罗', '埃塞俄比亚', '冈比亚']     # 四档

def getOriHtmlText(url,code='utf-8'):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
        }
        r=requests.get(url,timeout=30,headers=headers)
        r.raise_for_status()
        r.encoding=code
        return r.text
    except:
        return "There are some errors when get the original html!"

# 获取每个俱乐部的球员信息
def get_club_data(url):
    html = getOriHtmlText(url)
    soup = BeautifulSoup(html,'html.parser')
    team_member = soup.findAll('script')
    team_member = sorted(team_member, key = lambda x : len(x), reverse=True)[0].string  # 成员信息存储在最长的script标签中
    
    beg = team_member.find('teamMemberData')
    end = team_member.find('relatedNewsList') - 1

    team_member_data = team_member[beg+len("teamMemberData")+1:end]  # 截取队内成员*类*json数据
    # print(team_member_data)
    team_member_list = team_member_data.split("},{age")  # 将队内成员数据逐个分开存入列表中，每人的数据是Str类型
    player_dict = {}  # 创建存放球员信息字典
    for item in team_member_list:
        person_name = item[item.find('person_name:'): item.find(',scheme')]  # 获取该成员中文姓名
        person_id = item[item.find('person_id:'): item.find(',person_logo')]  # 获取该成员id

        player_dict[person_name[13:-1]] = []
        player_dict[person_name[13:-1]].append(person_id[11:-1])  # 对应信息存入字典中{'name': [info...]}

    # print(player_id_dict)
    player_list = soup.body.find_all(class_="analysis-list-item")  # 获取页面中显示成员表格的条目信息（为区分教练和队员）
    for player in player_list:
        title = player.find('span', class_='item1').text
        if title == '教练':  # 判断该行成员的身份是否为教练
            coach_name = player.find('span', class_='item3').text  # 获取教练姓名
            # print(coach_name)
            # print('coach_id:', player_id_dict[coach_name])
            del player_dict[coach_name]  # 删除字典中教练的信息（只统计球员）
        else:  # 教练在前，球员在后
            break
    
    african_player = []
    for key,value in player_dict.items():
        player_id = value[0]
        player_html = getOriHtmlText(base + "/player/" + player_id + ".html")  # 请求访问球员个人详细信息
        soup = BeautifulSoup(player_html,'html.parser')
        player_nation = soup.body.find('div', class_='detail-info').find_all('li')[1].text[6:]
        player_dict[key].append(player_nation)
        if player_nation in qualified_nation:
            african_player.append(key)

    print(player_dict)
    return player_dict, african_player

# 爬虫入口
def get_data(url):
    html = getOriHtmlText(url)
    soup = BeautifulSoup(html,'html.parser')
    team = soup.findAll('script')
    team = sorted(team, key = lambda x : len(x), reverse=True)[0].string  # 成员信息存储在最长的script标签中
    beg = team.find('rounds:')
    end = team.find('desc', beg) - 1
    team_str = team[beg:end]
    team_list = team_str.split("{goals_against")  # 将球队信息逐个分开存入列表中
    del team_list[0]
    club_data = {}
    for item in team_list:
        team_name = item[item.find('team_name:'):item.find('}')][11:-1] # 获取球队名
        team_id = item[item.find('team_id:'):item.find(',team_logo')][9:-1]  # 获取该成员id
        print(team_name+ ', ' + team_id)
        club_data[team_name] = {}
        player_dict, african_player = get_club_data(base + "/team/"+team_id+".html")
        club_data[team_name]['players'] = player_dict
        club_data[team_name]['african_player'] = african_player
        print(team_name+' 数据爬取完毕！')

    print(club_data)


if __name__ == "__main__":
    print("---------------------------------------------------------------------------------------------------")
    print("---------------------------------------------------------------------------------------------------")
    get_data(base + '/data/1')  # 传参的url为英超数据页


