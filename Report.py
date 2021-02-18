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
path = "/home/pdluser/Workspace/junjie/xiangya"


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
	"med_listlist": [{
		"med_time": "09:00",
		"med_name": "苯扎贝特片",
		"med_dosage": "2片",
		"med_mode": "口服"
	}, {
		"med_time": "09:00",
		"med_name": "苯扎贝特片",
		"med_dosage": "2片",
		"med_mode": "口服"
	}],
}

diagnosis = "200个字符以内，高脂血症,IGT,高尿酸血症"

med_time = "09:00"
med_name = "苯扎贝特片"
med_dosage = "2片"
med_mode = "口服"
li_html = templates.template('li.html').render(time= med_time, info = med_name + " " + med_dosage + " " + med_mode)
li1_html = templates.template('li.html').render(time= med_time, info = med_name + " " + med_dosage + " " + med_mode)

res = templates.template('test.html').render(diagnosis=diagnosis, li_html = li_html + li1_html)

# outputfile = path + "/test.html"
# with codecs.open(outputfile, 'w+b', encoding='utf8') as file:
#     file.write(res)

# pdfkit.from_string(res,path + '/out.pdf')
from weasyprint import HTML
HTML(string=res).write_pdf(path + '/out.pdf', stylesheets=[path + "/templates/style.css",path+"/templates/layui/css/layui.css"])
# HTML(filename=outputfile).write_pdf(path + '/out1.pdf')