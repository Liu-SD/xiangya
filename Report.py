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
from io import BytesIO
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

def json2pdf(json_data):
	li_html = ""
	dic = collections.OrderedDict()
	for med_item in json_data['med_list']:
		index = med_item['med_time']
		if(dic.get(index) != None):
			dic[index] = dic[index] + "<br>"
			dic[index] = dic[index] + med_item['med_name'] + " " + med_item['med_dosage'] + " " + med_item['med_mode']
		else:
			dic[index] = med_item['med_name'] + " " + med_item['med_dosage'] + " " + med_item['med_mode']

	dic = sort_key(dic)
	for k,v in dic.items():
		li_html = li_html + templates.template('li.html').render(time= k, info = v)

	file_name = '%s.pdf' %  str(uuid.uuid4())
	# file_name = "out.pdf"
	res_path = path + "/pdfs/" + file_name

	img_base64_data = url_to_qrcode(res_path)

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
		time_mech = json_data.get('time_mech', ""), 
		med_forbid = json_data.get('med_forbid', ""), 
		med_caution = json_data.get('med_caution', ""),
		img_base64_data = img_base64_data)

	# 保存渲染后的html
	# outputfile = path + "/test.html"
	# with codecs.open(outputfile, 'w+b', encoding='utf8') as file:
	#     file.write(res)
	# pdfkit.from_string(res,path + '/out.pdf')

	from weasyprint import HTML
	HTML(string=res).write_pdf(res_path, stylesheets=[path + "/templates/style.css",path+"/templates/layui/css/layui.css"], presentational_hints=True)
	# HTML(filename=outputfile).write_pdf(path + '/out1.pdf')
	return res_path
	


if __name__ == "__main__":
	json_data ={
		"code": 200,
		"msg": "访问成功",
		"hospital": "中南大学湘雅医院",
		"clinic_id": "0008374568",
		"section": "心血管内科",
		"date": "2020-8-11",
		"time": "15:44",
		"name": "张广杰",
		"gender": "男",
		"birthday": "1982-2-7",
		"age": "38岁",
		"diagnosis": "200个字符以内，高脂血症,IGT,高尿酸血症",
		"doctor": "余国龙",
		"user_edu": "口服给药的一般方法为吞服，通过水来保护和润滑食道，促进药物的吸收和排泄。但是有些药物为了加速药效、加快溶解吸收或者减少刺激或副作用，会采取一些特殊的给药方式，如嚼服、含服、舌下含服和泡腾等",
		"disease_edu": "餐中服用或餐后服用可缓解药物引起的胃肠反应",
		"time_mech": "服用时间需要注意……",
		"med_forbid": "不能与……同服，否则……",
		"med_caution": "在……时间内不得超过……",
		"med_list": [{
			"med_time": "18:00",
			"med_name": "苯扎贝特片",
			"med_dosage": "2片",
			"med_mode": "口服"
		}, {
			"med_time": "09:00",
			"med_name": "苯扎贝特片",
			"med_dosage": "2片",
			"med_mode": "口服"
		}, {
			"med_time": "13:00",
			"med_name": "苯片",
			"med_dosage": "2片",
			"med_mode": "口服"
		}],
	}

	print(json2pdf(json_data))
	pass