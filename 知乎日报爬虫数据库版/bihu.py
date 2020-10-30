import ahttp
from bs4 import BeautifulSoup
import pymysql.cursors

cc = 0

start_range = int(input("请输入开始序号："))
end_range = int(input("请输入结束序号："))
scanstep = int(input("请输入扫描步长："))
scanspeed = int(input("请输入扫描速度："))


# 连接数据库
connect = pymysql.Connect(
    host='localhost', port=3306, user='用户名', passwd='密码', db='bihu', charset='utf8'
)

# 获取游标
cursor = connect.cursor()

def addBihu():

    # 插入数据
    sql = "INSERT INTO bh(btitle,burl,bimg,btext,bcontent,bgo) VALUES ( '%s', '%s', '%s', '%s', '%s', '%s')"
    data = (
        htitle.text,
        str(q).replace("<AhttpResponse status[200] url=[", "").replace("]>", ""),
        img.attrs.get("src"),
        h2.text,
        hcontent,
        hgo
    )
    try:
        cursor.execute(sql % data)
    except:
        pass
    connect.commit()
    if cursor.rowcount > 0:
        print('━━●●━━━━━━━━━━━')
    else:
        print('失败:', cursor.rowcount, '条数据受影响')


def split_list_by_n(list_collection, n):
    """
    将集合均分，每份n个元素
    :param list_collection:
    :param n:
    :return:返回的结果为平分后的每份可迭代对象
    """
    for i in range(0, len(list_collection), n):
        yield list_collection[i: i + n]


# urls = [f"https://movie.douban.com/top250?start={c}" for c in range(0, 250)]
urls = [f"https://daily.zhihu.com/story/{c}" for c in range(start_range, end_range, scanstep)]
count = '预计提取: '+str(len(urls)) + ' 条数据'
print(count.replace("0000 ","万",1))
temp = split_list_by_n(urls, scanspeed)

for i in temp:
    reqs = [ahttp.get(url) for url in i]
    result = ahttp.run(reqs, order=True)
    for q in result:
        soup = BeautifulSoup(q.text, features='lxml')  # html.parser或者lxml，后者性能更好
        error = soup.select_one(
            '.ErrorPage-subtitle'
        )
        if error is None:
            title = soup.select_one('.DailyHeader-title')
            img = soup.select_one('.DailyHeader-image > img:nth-child(1)')
            # imgs = soup.select('.content-image')
            h2 = soup.select_one('.question-title')
            # author = soup.select_one('.ZhihuDaily-Author')
            content = soup.select_one('.content')
            go = soup.select_one('.view-more > a')
            if not title is None:
                htitle = title
                print('\r\n'+title.text)
            if not str(q) is None:
                print(str(q).replace("<AhttpResponse status[200] url=[", "").replace("]>", ""))
            if not img is None:
                print(img.attrs.get("src"))
            # for iimgs in imgs:
            #     print(iimgs.attrs.get("src"))
            if not h2 is None:
                print(h2.text)
            # print(author)
            if not content is None:
                hcontent = content
                print(content.text)
            if not go is None:
                hgo = go.attrs.get("href")
                print(go.attrs.get("href"))
            addBihu()
            cc += 1
        else:
            cc += 1
            cb = cc/len(urls) * 100
            print("\r{:^3.2f}%".format(cb),end = "")
cursor.close()
connect.close()
