# -*- coding: utf-8 -*-
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2
import json
import matplotlib.pyplot as plt
from scipy import stats, polyval
from pylab import plot, title, show, legend
import pylab
import numpy as np
import os
import glob


subreddit = ['news','popular','politics','funny','movies']

def get_data():	#get data from reddit server
	for sr in subreddit:
		baseUrl = "https://www.reddit.com/r/"+sr+"/.json?sort=top&limit=100"
		query = ""
		req = urllib2.Request(baseUrl, headers={'User-Agent': 'Mozilla/5.0'})
		#f = urllib.urlopen(baseUrl)
		items = json.loads(urllib2.urlopen(req).read())
		#f.close()
		yield items,sr,"0"
		#print data['kind']
		while items['data']['after'] != None:
			after = items['data']['after']
			req = urllib2.Request(baseUrl+"&after="+items['data']['after'], headers={'User-Agent': 'Mozilla/5.0'})
			#f = urllib.urlopen(baseUrl)
			items = json.loads(urllib2.urlopen(req).read())
			yield items,sr,after
		
		
def save_data():
	for data,sr,after in get_data():
		with open(sr+"_"+after+".json","w") as f:
			json.dump(data,f)

#save_data()

def load_data(name):
	os.chdir(os.getcwd()+"\data")
	for sr in glob.glob(name+"*.json"):
		f = open(sr,"r")
		data = json.loads(f.read())
		f.close()
		yield data,name

def show_correlation_num_comments_and_socre():
	for data,sr in load_data():
		x = []
		y = []
		for item in data['data']['children']:
			x.append(item['data']['num_comments'])
			y.append(item['data']['score'])

		slope, intercept, r, p, std = stats.linregress(x,y)
		ry = polyval([slope, intercept], x)

		#print(slope, intercept, r, p, std)
		#print(ry)
		plot(x,y, 'k.')
		plot(x,ry, 'r.-')
		title(sr)
		pylab.xlabel('num_comments')
		pylab.ylabel('score')
		#legend(['original', 'regression'])

		show()

from collections import defaultdict,Counter
import operator
def most_popular_subreddit():
	subreddit = defaultdict(int)
	total = 0
	for data,sr in load_data("popular"):
		for item in data['data']['children']:
			subreddit[item['data']['subreddit']] += 1
			total += 1

	sorted_sr = sorted(subreddit.items(), key=operator.itemgetter(1))

	f = open("popular_subreddit.txt","w")
	for sr,value in sorted_sr[-30:]:
		f.write(sr + " " +str(value/total)+"\n")
	f.close()
	print total
#most_popular_subreddit()

import re
def tokenizer(message):
	message = message.lower()
	all_words = re.findall("[0-9a-z']+", message)
	return all_words

def count_most_common_word():
	for data,sr in load_data("politics"):
		for item in data['data']['children']:
			if item['data']['selftext'] != None:
				all_words = tokenizer(item['data']['selftext'])
				f = open(sr+"_most_common_words.txt","a")
				f.write(item['data']['title'] + " , ups : " + str(item['data']['ups']) + " , downs : "+\
					str(item['data']['downs']) + " : , score : "+ str(item['data']['score']) + "\n")
				for word, count in Counter(all_words).most_common(10):
					f.write(word+" : "+str(count) + "\n")
				f.close()


import spiral
x,y = spiral.get_spiral_pointer()
#import sys
#sys.path.append(os.getcwd()+"\data")
f = open(os.getcwd()+"\data\\news_0.json","r")
data = json.loads(f.read())
f.close()
for it,item in enumerate(data['data']['children']):
	if it==20:
		break
	item['data']['point_x'] = x[it]
	item['data']['point_y'] = y[it]
f = open("news0_test.json","w")
json.dump(data,f)
f.close()

#count_most_common_word()


#this is for analyzing data
'''
f = m = n = pop = pol = size = 0
fc = mc = nc = popc = polc = totalc = 0
for data, sr in load_data():
	if sr[0]=='f':
		f += len(data['data']['children'])
		for item in data['data']['children']:
			fc += item['data']['num_comments']
		size += len(data['data']['children'])
	elif  sr[0]=='m':
		m += len(data['data']['children'])
		for item in data['data']['children']:
			mc += item['data']['num_comments']
		size += len(data['data']['children'])
	elif sr[0] == 'n':
		n += len(data['data']['children'])
		for item in data['data']['children']:
			nc += item['data']['num_comments']
		size += len(data['data']['children'])
	elif sr[0:3] == 'pop':
		pop += len(data['data']['children'])
		for item in data['data']['children']:
			popc += item['data']['num_comments']
		size += len(data['data']['children'])
	elif sr[0:3] == 'pol':
		pol += len(data['data']['children'])
		for item in data['data']['children']:
			polc += item['data']['num_comments']
		size += len(data['data']['children'])

	totalc += fc + mc + nc + popc+polc
print "funny : ", f
print "movies : ", m
print "news : ", n
print "popular : ", pop
print "politics : ", pol
print "total: ", size

print "num_comments funny : ", fc
print "num_comments movies : ", mc
print "num_comments news : ", nc
print "num_comments popular : ", popc
print "num_comments politics : ", polc
print "num_comments total: ", totalc

print "average num_comments funny : ", fc/f
print "average num_comments movies : ", mc/m
print "average num_comments news : ", nc/n
print "average num_comments popular : ", popc/pop
print "average num_comments politics : ", polc/pol
print "average num_comments total: ", totalc/size
'''