# !/user/bin/env python
# -*- coding:utf-8 -*-

import requests, re, time, ssl, urllib
from urllib import parse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import urllib3

urllib3.disable_warnings() #不显示警告信息
ssl._create_default_https_context = ssl._create_unverified_context
req = requests.Session()

# 获取RAIL_DEVICEID写在登录之前get_rail_deviceid()函数
# req.cookies['RAIL_DEVICEID'] = 'ng8GWpVBAs1dnOxtsAEnQ1EyfbEuCIGetci8OLRrXAtY_grSokW5WZb10aDdNS_Je4KbKlgf3fPtO4cZJGCox4ORGXGZ8Fhcq6TDWW1iuLlaU2kLccvL22V_HBd49idoCqL0dJEbfl3Plhhno73VZqQY5aKeAHHJ'


class Leftquery(object):
    '''余票查询'''

    def __init__(self):
        self.station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        self.headers = {
            'Host': 'kyfw.12306.cn',
            'If-Modified-Since': '0',
            'Pragma': 'no-cache',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def station_name(self, station):
        '''获取车站简拼'''
        html = requests.get(self.station_url, verify=False).text
        result = html.split('@')[1:]
        dict = {}
        for i in result:
            key = str(i.split('|')[1])
            value = str(i.split('|')[2])
            dict[key] = value
        return dict[station]

    def query(self, from_station, to_station, date):
        '''余票查询'''
        fromstation = self.station_name(from_station)
        tostation = self.station_name(to_station)
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            date, fromstation, tostation)
        # 学生票查询: url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=0X00'.format(date, fromstation, tostation)
        try:
            html = requests.get(url, headers=self.headers, verify=False).json()
            result = html['data']['result']
            if result == []:
                print('很抱歉,没有查到符合当前条件的列车!')
                exit()
            else:
                print(date + from_station + '-' + to_station + '查询成功!')
                # 打印出所有车次信息
                num = 1  # 用于给车次编号,方便选择要购买的车次
                for i in result:
                    info = i.split('|')
                    if info[0] != '' and info[0] != 'null':
                        print(str(num) + '.' + info[3] + '车次还有余票:')
                        print('出发时间:' + info[8] + ' 到达时间:' + info[9] + ' 历时多久:' + info[10] + ' ', end='')
                        seat = {21: '高级软卧', 23: '软卧', 26: '无座', 28: '硬卧', 29: '硬座', 30: '二等座', 31: '一等座', 32: '商务座',
                                33: '动卧'}
                        from_station_no = info[16]
                        to_station_no = info[17]
                        for j in seat.keys():
                            if info[j] != '无' and info[j] != '':
                                if info[j] == '有':
                                    print(seat[j] + ':有票 ', end='')
                                else:
                                    print(seat[j] + ':有' + info[j] + '张票 ', end='')
                        print('\n')
                    elif info[1] == '预订':
                        print(str(num) + '.' + info[3] + '车次暂时没有余票')
                    elif info[1] == '列车停运':
                        print(str(num) + '.' + info[3] + '车次列车停运')
                    elif info[1] == '23:00-06:00系统维护时间':
                        print(str(num) + '.' + info[3] + '23:00-06:00系统维护时间')
                    else:
                        print(str(num) + '.' + info[3] + '车次列车运行图调整,暂停发售')
                    num += 1
            return result
        except:
            print('查询信息有误!请重新输入!')
            exit()


class Login(object):

    '''登录模块'''

    def __init__(self):
        self.username = username
        self.password = password
        self.url_pic = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.15905700266966694'
        self.url_check = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.url_login = 'https://kyfw.12306.cn/passport/web/login'
        # self.url_rail_deviceid = 'https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=LViaqcvRbo&hashCode=RONh1-EomRApoVf1W9XrJYsBeCduvqTrQis5xPyHS_o&FMQw=1&q4f3=zh-CN&VySQ=FGExA0W53bSl7MR7lAZtO9-whgi60qgC&VPIf=1&custID=133&VEek=unknown&dzuS=29.0%20r0&yD16=0&EOQP=f57fa883099df9e46e7ee35d22644d2b&lEnu=3232235621&jp76=7047dfdd1d9629c1fb64ef50f95be7ab&hAqN=Win32&platform=WEB&ks0Q=6f0fab7b40ee4a476b4b3ade06fe9065&TeRS=1080x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/63.0.3239.132%20Safari/537.36&E3gR=fd7a8adb89dd5bf3a55038ad1adc5d35&timestamp='
        self.headers = {
            # 'Accept': 'application/json, text/javascript, */*; q=0.01',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-CN,zh;q=0.9',
            'Host': 'kyfw.12306.cn',
            # 'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }
    def get_rail_deviceid(self):
        #获取rail_deviceid
        global req
        html = requests.get('https://kyfw.12306.cn/otn/HttpZF/GetJS', headers=self.headers).text
        algID = re.search(r'algID\\x3d(.*?)\\x', html).group(1)
        # print('algID:' + algID)
        url_rail_deviceid = 'https://kyfw.12306.cn/otn/HttpZF/logdevice?algID={}&hashCode=g31sieVa_C2qFYjQo2GgvOscy68BGA2Bg86hZT3aWm8&FMQw=1&q4f3=zh-CN&VySQ=FGEdmmK0Wj7y9zUpl_D3rF9LHy5L5269&VPIf=1&custID=133&VEek=unknown&dzuS=29.0%20r0&yD16=0&EOQP=f57fa883099df9e46e7ee35d22644d2b&lEnu=3232235621&jp76=7047dfdd1d9629c1fb64ef50f95be7ab&hAqN=Win32&platform=WEB&ks0Q=6f0fab7b40ee4a476b4b3ade06fe9065&TeRS=1080x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/63.0.3239.132%20Safari/537.36&E3gR=fd7a8adb89dd5bf3a55038ad1adc5d35&timestamp='.format(algID)
        html_rail_deviceid = req.get(self.url_rail_deviceid+ str(int(time.time()*1000)),headers=self.headers).text
        rail_deviceid = re.search(r'"dfp":"(.*?)"', html_rail_deviceid).group(1)
        req.cookies['RAIL_DEVICEID'] = rail_deviceid

    def showimg(self):
        '''显示验证码图片'''
        global req
        html_pic = req.get(self.url_pic, headers=self.headers).content
        open('pic.jpg', 'wb').write(html_pic)
        img = mpimg.imread('pic.jpg')
        plt.imshow(img)
        plt.axis('off')
        plt.show()

    def captcha(self, answer_num):
        '''填写验证码'''
        answer_sp = answer_num.split(',')
        answer_list = []
        an = {'1': (31, 35), '2': (116, 46), '3': (191, 24), '4': (243, 50), '5': (22, 114), '6': (117, 94),
              '7': (167, 120), '8': (251, 105)}
        for i in answer_sp:
            for j in an.keys():
                if i == j:
                    answer_list.append(an[j][0])
                    answer_list.append(',')
                    answer_list.append(an[j][1])
                    answer_list.append(',')
        s = ''
        for i in answer_list:
            s += str(i)
        answer = s[:-1]
        # 验证验证码
        form_check = {
            'answer': answer,
            'login_site': 'E',
            'rand': 'sjrand',
            '_': str(int(time.time() * 1000))
        }
        global req
        html_check = req.get(self.url_check, params=form_check, headers=self.headers).json()
        print(html_check)
        if html_check['result_code'] == '4':
            print('验证码校验成功!')
        else:
            print('验证码校验失败!')
            exit()

    def login(self, answer_num):
        #登录账号
        answer_sp = answer_num.split(',')
        answer_list = []
        an = {'1': (31, 35), '2': (116, 46), '3': (191, 24), '4': (243, 50), '5': (22, 114), '6': (117, 94),
              '7': (167, 120), '8': (251, 105)}
        for i in answer_sp:
            for j in an.keys():
                if i == j:
                    answer_list.append(an[j][0])
                    answer_list.append(',')
                    answer_list.append(an[j][1])
                    answer_list.append(',')
        s = ''
        for i in answer_list:
            s += str(i)
        answer = s[:-1]
        form_login = {
            'username': self.username,
            'password': self.password,
            'appid': 'otn',
            'answer': answer
        }
        print(form_login)
        global req
        # self.headers['Content-Length'] = str(len(urllib.parse.urlencode(form_login)))
        # 20190416更新-必须cookie加上RAIL_DEVICEID(https://kyfw.12306.cn/otn/HttpZF/logdevice这个借口返回的,写成定值即可,2030年过期)
        # 要不然会登录失败,返回"网络可能存在问题，请您重试一下！",会跳转到https://www.12306.cn/mormhweb/logFiles/error.html
        # req.cookies['RAIL_DEVICEID'] = 'g9qXFFIFQ4jPKuxX6YTC38yc0xdYE2QfbPKdtS8HpYXgY9yKKaQGR2eOG-Kx67d6Hp-keCyhUqjc7pokitcskwj5X9i72soSkvlc4qFQ2hf-abUpuwvcHjww4n_kxYXe9tFbCAV_1VFtCQS64hAyI0ycCQgLbQDW'
        html_login = req.post(self.url_login, data=form_login, headers=self.headers).json()
        print(html_login)
        # print(html_login['headers']['Content-Length'])
        if html_login['result_code'] == 0:
            print('恭喜您,登录成功!')
        else:
            print('账号密码错误,登录失败!')
            exit()

def select():
    '''查票函数'''
    # 用户输入购票信息:
    from_station = input('请输入您要购票的出发地(例:北京):')
    # from_station = '北京'
    to_station = input('请输入您要购票的目的地(例:上海):')
    # to_station = '上海'
    date = input('请输入您要购票的乘车日期(例:2019-03-06):')
    # date = '2019-05-15'
    # 余票查询
    query = Leftquery()
    result = query.query(from_station, to_station, date)

def ver_code():
    login = Login()
    #login.get_rail_deviceid()
    login.showimg()
    # 填写验证码
    print('  =============================================================== ')
    print('   根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置 ')
    print('     --------------------------------------')
    print('            1  |  2  |  3  |  4 ')
    print('     --------------------------------------')
    print('            5  |  6  |  7  |  8 ')
    print('     --------------------------------------- ')
    print(' =============================================================== ')
    answer_num = input('请填入验证码(序号为1~8,中间以逗号隔开,例:1,2):')
    login.captcha(answer_num)
    #login.login(answer_num)


if __name__ == '__main__':
    print('*' * 30 + '12306购票' + '*' * 30)
    '''global username, password
    username=input("请输入用户名:")
    password=input("请输入密码:")
    ver_code()'''
    select()
