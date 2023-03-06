# coding=utf-8
import requests
import json
import os

global content_dict


def Check():
	# 读取 标题匹配规则
	global content_dict
	with open('matching rules.txt', encoding='utf-8') as file_obj:
		rules = file_obj.read()
		searchKeyWords = '+'.join(rules.split(' '))

	code = 1
	# code == 0 表示获取数据成功
	while not code == 0:
		url = 'https://api.bilibili.com/x/web-interface/wbi/search/type?__refresh__=true&_extra=&context=&page=1&page_size=50&order=pubdate&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword={}&qv_id=ynSAaNRU2PCYdvqzakmyrRVgjteo2SJi&ad_resource=5654&source_tag=3&category_id=&search_type=video&tids=30&dynamic_offset=0&w_rid=8d037edd7872dfd06eb04fb4284883db&wts=1674118836'.format(
			searchKeyWords)
		r = requests.get(url)
		content = r.content.decode('utf-8')  # <class 'str'>
		content_dict = json.loads(content)  # <class 'dict'>
		code = content_dict['code']
	# print(content_dict)
	# print(code)

	result = ''
	for video in content_dict['data']['result']:
		result += video['title'].replace("<em class=\"keyword\">","").replace("</em>","").replace("&amp;","&") + '\n'
		result += ' 作者：' + str(video['author']) + '  '
		result += ' 链接：' + str(video['arcurl']) + '\r\n'

	# 生成本次查询文件
	with open("new.txt", "w", encoding='utf-8') as file:
		file.write(result)

	# 第一次使用不存在 old.txt 需要进行生成
	if not os.path.isfile('old.txt'):
		with open("old.txt", "w", encoding='utf-8') as file:
			file.write(result)

	# 开始读取两个文件
	file_1 = open(r'./new.txt', 'r', encoding='utf8')
	file_2 = open(r'./old.txt', 'r', encoding='utf8')
	# 按行分割文件,返回的是列表
	a = file_1.read().splitlines()
	b = file_2.read().splitlines()
	# 差异对比
	# dif = set(a) - set(b) # 注意：使用 set 去重会导致 标题 作者 链接 这三者无序，影响推送
	dif = [x for x in a if x not in b]

	# 读取 sendkey
	with open('sendkey.txt', encoding='utf-8') as file_obj:
		sendkey = file_obj.read()
		sendkey = sendkey.rstrip()

	if dif and sendkey:
		# 需要使用 ''.join(dif) 使其不输出'这个符号，否则推送时候会出错
		full = '有一首新的原创曲：' + ''.join(dif)
		print(full)
		serverChanUrl = "https://sctapi.ftqq.com/" + str(sendkey) + ".send?title=" + ''.join(dif) + "&desp=" + str(full)
		requests.get(serverChanUrl)

	# 关闭文件
	file_1.close()
	file_2.close()

	# 修改文件，删去 old.txt ，将 new.txt 重命名为 old.txt
	if os.path.isfile('old.txt'):
		os.remove('./old.txt')
	if os.path.isfile('new.txt'):
		os.rename('./new.txt', './old.txt')


if __name__ == '__main__':
	Check()
