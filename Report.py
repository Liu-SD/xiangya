# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:07:49 2019

@author: LINFANLI

Editt On 2021
@author: JunJie

"""

# import os
#import numpy as np
# import pandas as pd
# import datetime
import templates as templates
import codecs
import sys
import uuid
import collections
import qrcode
import base64
import datetime
from io import BytesIO
import json
# from app import ip, port
# from get_pyecharts import get_pyecharts_geo, get_pyecharts_line, get_pyecharts_heatmap
# from get_aqi import cal_pm25_iaqi,cal_pm10_iaqi,cal_co_iaqi,cal_no2_iaqi,cal_so2_iaqi
# import re
# import pdfkit


# 获取当前的工作路径
#print(os.getcwd())
# 重置工作路径
# os.chdir(r'E:\Pycharm-Projects\AirQualityReport')
# E:\Pycharm-Projects\AirQualityReport
# print(os.getcwd())
# path = '/home/junjie/Code/xiangya/project'
# path = "/home/pdluser/Workspace/junjie/xiangya"
path = sys.path[0]


def sort_key(old_dict, reverse=False):
    """对字典按key排序, 默认升序, 不修改原先字典"""
    # 先获得排序后的key列表
    keys = sorted(old_dict.keys(), reverse=reverse)
    # 创建一个新的空字典
    new_dict = collections.OrderedDict()
    # 遍历 key 列表
    for key in keys:
        new_dict[key] = old_dict[key]
    return new_dict

# 转换为二维码，然后转换为base64
def url_to_qrcode(res_path):
    img = qrcode.make(data=res_path)
    output_buffer = BytesIO()
    img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str.decode("utf-8")

def time_to_timestamp(t, t_getup, t_breakfast, t_lunch, t_supper, t_sleep):
    if t < t_breakfast:
        ts = "早餐前"
    elif t == t_breakfast:
        ts = "早餐时"
    elif t < t_lunch - datetime.timedelta(hours=1):
        ts = "早餐后"
    elif t < t_lunch:
        ts = "中餐前"
    elif t == t_lunch:
        ts = "中餐时"
    elif t < t_supper - datetime.timedelta(hours=1):
        ts = "中餐后"
    elif t < t_supper:
        ts = "晚餐前"
    elif t == t_supper:
        ts = "晚餐时"
    elif t < t_sleep - datetime.timedelta(hours=0.5):
        ts = "晚餐后"
    else:
        ts = "睡前"
    return ts

def json2pdf(json_data, ip, port):
    li_html = ""
    t_getup = datetime.datetime.strptime(str(json_data['t_getup']), "%H")
    t_breakfast = datetime.datetime.strptime(str(json_data['t_breakfast']), "%H")
    t_lunch = datetime.datetime.strptime(str(json_data['t_lunch']), "%H")
    t_supper = datetime.datetime.strptime(str(json_data['t_supper']), "%H")
    t_sleep = datetime.datetime.strptime(str(json_data['t_sleep']), "%H")
    dic = collections.OrderedDict()
    dic_count = collections.OrderedDict()
    # 利用map合并同一时间点的药品并计数
    for med_item in json_data['med_list']:
        index = med_item['med_time']
        index = datetime.datetime.strptime(index, "%H:%M")
        ts = time_to_timestamp(index, t_getup, t_breakfast, t_lunch, t_supper, t_sleep)
        index = index.strftime("%H:%M")

        if index not in dic:
            dic[index] = ([], ts)
            dic_count[index] = 0
            # dic[index] = dic[index] + "<br>"
            # dic[index] = dic[index] + " ;  "
            # dic[index] = dic[index] + "<br>" +  med_item['med_name'] + " " + med_item['med_dosage'] + " " +med_item['med_mode']
        dic[index][0].append((med_item['med_name'], med_item['med_spec']+'/'+med_item['med_unit'], med_item['med_dosage']+med_item['med_unit'], med_item['med_mode']))
        dic_count[index] += 1

    dic = sort_key(dic)

    sum_t = 1
    threshold = 27
    li_html_append = ""
    # 判断条目的数量，超过一定内容，就划分为两部分
    for k,(v, ts) in dic.items():
        # print(dic_count[k])

        if sum_t <= threshold:
            li_html = li_html + templates.template('li.html').render(time= k, info = v, timestamp= ts)
        else:
            li_html_append = li_html_append + templates.template('li.html').render(time= k, info = v, timestamp= ts)
        sum_t += dic_count[k] + 2

    sum_t -= 2
    append_html = ""
    # if sum_t > threshold:
    if li_html_append != "":
        append_html = templates.template('append_li.html').render(append_html = li_html_append)

    educations = []
    if 'user_edu' in json_data and json_data['user_edu'] != "":
        educations.append(('患者教育', json_data['user_edu'].replace("\r", "").strip("\n").replace("\n", "<br>")))
    if 'disease_edu' in json_data and json_data['disease_edu'] != "":
        educations.append(('疾病教育', json_data['disease_edu'].replace("\r", "").strip("\n").replace("\n", "<br>")))
    if 'med_forbid' in json_data and json_data['med_forbid'] != "":
        educations.append(('禁忌', json_data['med_forbid'].replace("\r", "").strip("\n").replace("\n", "<br>")))
    if 'med_caution' in json_data and json_data['med_caution'] != "":
        educations.append(('注意事项', json_data['med_caution'].replace("\r", "").strip("\n").replace("\n", "<br>")))
    if 'med_food' in json_data and json_data['med_food'] != "":
        educations.append(('食物相互作用', json_data['med_food'].replace("\r", "").strip("\n").replace("\n", "<br>")))
    if 'med_disease' in json_data and json_data['med_disease'] != "":
        educations.append(('疾病相互作用', json_data['med_disease'].replace("\r", "").strip("\n").replace("\n", "<br>")))


    file_name = '%s.pdf' %  str(uuid.uuid4())
    # file_name = "out.pdf"
    res_path = path + "/pdfs/" + file_name

    res_download_path = ip + ":" + str(port) + "/pdfs/" + file_name
    img_base64_data = url_to_qrcode(res_download_path)

    # 整个输出模版渲染
    res = templates.template('test.html').render(
        li_html = li_html,
        append_html = append_html,
        hospital = json_data['hospital'],
        clinic_id = json_data['clinic_id'],
        section = json_data['section'],
        date = json_data['date'],
        time = json_data['time'],
        name = json_data['name'],
        gender = json_data['gender'],
        birthday = json_data['birthday'],
        age = json_data['age'],
        diagnosis = json_data['diagnosis'],
        educations = educations,
        img_base64_data = img_base64_data)

    # 保存渲染后的html
    outputfile = path + "/test.html"
    with codecs.open(outputfile, 'w+b', encoding='utf8') as file:
        file.write(res)
    # pdfkit.from_string(res,path + '/out.pdf')

    from weasyprint import HTML
    HTML(string=res).write_pdf(res_path, stylesheets=[path + "/templates/style.css",path+"/templates/layui/css/layui.css"], presentational_hints=True)
    # HTML(filename=outputfile).write_pdf(path + '/out1.pdf')
    return res_download_path



if __name__ == "__main__":
    ip = "106.12.125.175"
    port = 12333
    with open('report.json') as f:
        json_data = json.load(f)

    print(json2pdf(json_data, ip , port))
    pass
