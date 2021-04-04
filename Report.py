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
import time
from io import BytesIO
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

def json2pdf(json_data, ip, port):
	li_html = ""
	dic = collections.OrderedDict()
	for med_item in json_data['med_list']:
		index = med_item['med_time']
		index = time.strptime(index , "%H:%M")
		index = time.strftime("%H:%M", index)
		
		if(dic.get(index) != None):
			# dic[index] = dic[index] + "<br>"
			dic[index] = dic[index] + " ;  "
			dic[index] = dic[index] + med_item['med_name'] + " " + med_item['med_dosage'] + " " + med_item['med_mode']
		else:
			dic[index] = med_item['med_name'] + " " + med_item['med_dosage'] + " " + med_item['med_mode']

	dic = sort_key(dic)
	for k,v in dic.items():
		li_html = li_html + templates.template('li.html').render(time= k, info = v)

	file_name = '%s.pdf' %  str(uuid.uuid4())
	# file_name = "out.pdf"
	res_path = path + "/pdfs/" + file_name

	res_download_path = ip + ":" + str(port) + "/pdfs/" + file_name
	img_base64_data = url_to_qrcode(res_download_path)

	res = templates.template('test.html').render(
		li_html = li_html, 
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
		# 处理用药注意事项中可能没有内容的情况
		user_edu = json_data.get('user_edu', ""), 
		disease_edu = json_data.get('disease_edu', ""), 
		# time_mech = json_data.get('time_mech', ""), 
		med_forbid = json_data.get('med_forbid', ""), 
		med_caution = json_data.get('med_caution', ""),
		med_food = json_data.get('med_food', ""), 
		med_disease = json_data.get('med_disease', ""), 
		img_base64_data = img_base64_data)

	# 保存渲染后的html
	# outputfile = path + "/test.html"
	# with codecs.open(outputfile, 'w+b', encoding='utf8') as file:
	#     file.write(res)
	# pdfkit.from_string(res,path + '/out.pdf')

	from weasyprint import HTML
	HTML(string=res).write_pdf(res_path, stylesheets=[path + "/templates/style.css",path+"/templates/layui/css/layui.css"], presentational_hints=True)
	# HTML(filename=outputfile).write_pdf(path + '/out1.pdf')
	return res_download_path
	


if __name__ == "__main__":
	ip = "106.12.125.175" 
	port = 12333

	json_data ={
	"code": "200",
	"msg": "Test Msg",
	"hospital": "中南大学湘雅医院",
	"clinic_id": "0009131453",
	"section": "神经内科",
	"date": "020-08-11",
	"time": "15:33",
	"name": "杨菊香",
	"gender": "女",
	"birthday": "1961-07-25",
	"age": "59岁",
	"diagnosis": "帕金森氏病?",
	"doctor": "王俊峙",
	"user_edu": "用药咨询建议患者报告精神病行为、抑郁症或自杀意念的症状[3] [1] [2]。因为该药可能导致嗜睡和突然的睡眠，警告患者直到药物疗效发挥完全，避免开车或其他需要精神警",
	"disease_edu": "用于治疗帕金森病、症状性帕金森综合症（脑炎后、动脉硬化性或中毒性），但不包括药物引起的帕金森综合症。\n\r\n\r\n",
	"med_forbid": "本品禁用于已知对左旋多巴、苄丝肼或其赋型剂过敏的患者。禁止将本品与非选择性单胺氧化酶抑制剂合用，但选择性单胺氧化酶 B 抑制剂（如司来吉兰和雷沙吉兰）和选择性单胺氧化酶 A 抑制剂（如吗氯贝胺）则不在禁止合用之列。合用单胺氧化酶 A 与单胺氧化酶 B 抑制剂相当于非选择性单胺氧化酶抑制剂，因而不应与本品联合应用。",
	"med_caution": "本品若与拟交感神经药物（如肾上腺素，去甲肾上腺素，异丙肾上腺素，安非他命等）同时使用，可能会增强这类药物作用，故不推荐与拟交感神经药物的联合用药。如果必须联合用药，必须密切监视心血管系统，且拟交感神经药物的剂量需要减少。\n其他抗帕金森药物可与本品联合用药。",
	"med_food": "如正在接受其他抗帕金森药物的治疗（如抗胆碱能类或金刚烷胺），在本品初始治疗时应持续用药。但随着本品逐渐起效，其他药物的剂量可能需要减少或逐渐停用。\n",
	"med_disease": "曾患有冠状动脉疾病、心肌梗塞、心律失常或心力衰竭的患者使用本品时应格外注意。",
	"med_list": [
		{
		"med_time": "8:00",
		"med_name": "多巴丝肼片",
		"med_dosage": "0.25g",
		"med_mode": "口服"
		},
		{
		"med_time": "13:00",
		"med_name": "多巴丝肼片",
		"med_dosage": "0.25g",
		"med_mode": "口服"
		},
		{
		"med_time": "19:00",
		"med_name": "多巴丝肼片",
		"med_dosage": "0.25g",
		"med_mode": "口服"
		},
		{
		"med_time": "7:00",
		"med_name": "盐酸普拉克索片",
		"med_dosage": "0.125mg",
		"med_mode": "口服"
		},
		{
		"med_time": "12:00",
		"med_name": "盐酸普拉克索片",
		"med_dosage": "0.125mg",
		"med_mode": "口服"
		},
		{
		"med_time": "19:00",
		"med_name": "盐酸普拉克索片",
		"med_dosage": "0.125mg",
		"med_mode": "口服"
		},
		{
		"med_time": "7:00",
		"med_name": "恩他卡朋片",
		"med_dosage": "0.2g",
		"med_mode": "口服"
		},
		{
		"med_time": "11:00",
		"med_name": "恩他卡朋片",
		"med_dosage": "0.2g",
		"med_mode": "口服"
		},
		{
		"med_time": "17:00",
		"med_name": "恩他卡朋片",
		"med_dosage": "0.2g",
		"med_mode": "口服"
		},
		{
		"med_time": "7:00",
		"med_name": "苯扎贝特片",
		"med_dosage": "0.2g",
		"med_mode": "口服"
		},
		{
		"med_time": "8:00",
		"med_name": "血脂康胶囊",
		"med_dosage": "0.6g",
		"med_mode": "口服"
		},
		{
		"med_time": "19:00",
		"med_name": "血脂康胶囊",
		"med_dosage": "0.6g",
		"med_mode": "口服"
		},
		{
		"med_time": "7:00",
		"med_name": "非布司他片",
		"med_dosage": "40.0mg",
		"med_mode": "口服"
		}
	]
	}

	print(json2pdf(json_data, ip , port))
	pass