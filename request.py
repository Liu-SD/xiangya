import requests
import json

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
			"med_time": "10:00",
			"med_name": "苯扎贝特片",
			"med_dosage": "2片",
			"med_mode": "口服"
		}, {
			"med_time": "10:00",
			"med_name": "复方铝酸铋",
			"med_dosage": "1片",
			"med_mode": "口服"
		}],
	}

# # json方法一
# res = requests.post('http://localhost:5000/api/json2pdf', json=json_data) 


# json 方法二
## headers中添加上content-type这个参数，指定为json格式
headers = {'Content-Type': 'application/json'}

## post的时候，将data字典形式的参数用json包转换成json格式。
response = requests.post(url='http://localhost:5000/api/json2pdf', headers=headers, data=json.dumps(json_data))

if response.ok:
    print(response.json())