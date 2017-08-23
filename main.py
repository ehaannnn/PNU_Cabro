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
	for sr in glob.glob(name+"*.json"):
		f = open(sr,"r")
		data = json.loads(f.read())
		f.close()
		yield data,name

def show_correlation_num_comments_and_socre():
	f = open(os.getcwd()+"\\data\\all_data.json","r")
	data = json.loads(f.read())
	f.close()
	#for data,sr in data:
	x = []
	y = []
	for item in data['children']:
		x.append(item['num_comment'])
		y.append(item['ups']-item['downs'])
	slope, intercept, r, p, std = stats.linregress(x,y)
	ry = polyval([slope, intercept], x)

	print stats.pearsonr(x,y)

	print(slope, intercept, r, p, std)
		#print(ry)
	plot(x,y, 'k.')
	plot(x,ry, 'r.-')
	title("all data")
	pylab.xlabel('num_comments')
	pylab.ylabel('score')
	#legend(['original', 'regression'])

	show()
#show_correlation_num_comments_and_socre()


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
	all_words = re.findall("[0-9a-z]+", message)
	return all_words

def count_most_common_word():
	trivial_words = ['a','the','is','are','in','to','for','and','of','with','i','on','your','from','this','it','that',\
						'what\'s','my','you','at','up','about','he','she','why','don\'t','years','take','can','but',\
						'me','as','s','was','by','be','when','never','had','have','too','his','him','her','get','now',\
						'us','says','make','were','always','am','well','being','will','do','did','all','how','if','after','before',\
						'what','new','an','not','has','made','i\'m','want','til','really','u','two','one','doesn\'t','since']
	f = open(os.getcwd()+"\\data\\all_data.json","r")
	data = json.loads(f.read())
	f.close()

	words = []
	for item in data['children']:
		words += tokenizer(item['title'])

	from collections import Counter
	f = open("word_cloud.csv","w")
	for word,count in Counter(words).items():
		#print word, count
		if count<=10:
			continue
		if word in trivial_words:
			continue
		f.write(word+","+str(count)+"\n")
	f.close()

#count_most_common_word()


'''				
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
'''

def integrate_subreddit():
	os.chdir(os.getcwd()+"\data")
	all_data = json.loads('{"root":"all", "children":[]}')
	for kind in subreddit:
		for data,sr in load_data(kind):
			#print sr
			for item in data['data']['children']:
				all_data["children"].append({"downs":item['data']['downs']
				,"ups":item['data']['ups']
				,"title":item['data']['title']
				,"created":item['data']['created']
				,"subreddit":item['data']['subreddit']
				,"url":item['data']['url']
				,"num_comment":item['data']['num_comments']})
	f = open("all_data.json","w")
	json.dump(all_data,f)
	f.close()

#integrate_subreddit()

def correlation_title_ups():
	f=open("all_data.json","r")
	data = json.loads(f.read())
	f.close()

	items = sorted(data['children'], key=lambda x:x['ups'])

	words = []
	for it,item in enumerate(items):
		if it==100:
			break
		words += tokenizer(item['title'])
	
	f = open("correlation_title_ups.txt","w")
	common_word = Counter(words).most_common(len(Counter(words)))
	for word, count in common_word:
		f.write(word + " : " + str(count) + "\n")
	f.close()




def top_20(comments, score):
	f=open("all_data.json","r")
	data = json.loads(f.read())
	f.close()

	data['children'] = sorted(data['children'], key=lambda x:x['ups']*score+x['num_comment']*comments)
	f = open("top_20.json","w")
	json.dump(data,f)
	f.close()

if len(sys.argv)!=1:
	top_20(str(sys.argv[1]),str(sys.argv[2]))




#correlation_title_ups()
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



def sort_word_cloud():
	import csv
	f = open("word_cloud.csv","r")
	reader = csv.reader(f, delimiter=",")

	sortedlist = sorted(reader,key=lambda row: int(row[1]), reverse=True)
	f.close()

	return sortedlist

def anova_test():
	sensitive_words = ['trump','sex','scaramucci','russia','arpaio',\
				'donald','obamacare','president','north','korea','russian','china',\
				'transgender','crisis','criminal','dunkirk','killed','killing','maduro','sheriff',\
				'duterte','shooting','drugs','drug','dead','fuck','f**k','pussy','death','fucking','f***ing',\
				'mccain','gay','tillerson','slayer','motherfucker','trumpgret','suck']

	f = open(os.getcwd()+"\\data\\all_data.json","r")
	data = json.loads(f.read())
	f.close()

	x_ups = []	#collect sensitive_words score
	x_downs = []
	x_score = []

	y_ups = []	#collect non_sensitive_words score
	y_downs = []
	y_score = []
	#f=open("test.txt","w")
	for item in data['children']:
		words = tokenizer(item['title'])
		check = False
		for word in words:
			if word in sensitive_words:	
				check = True
				break
		if check == False:
			y_ups.append(item['ups'])
			y_downs.append(item['downs'])
			y_score.append(item['ups']-item['downs'])
			#if item['ups'] > 5000:
			#	print str(item['title'])
		else:
			x_ups.append(item['ups'])
			x_downs.append(item['downs'])
			x_score.append(item['ups']-item['downs'])
			#f.write(item['title']+"\n")
	
	print len(x_ups), len(y_ups)
	print np.mean(x_ups), np.mean(y_ups)

	print stats.ttest_ind(x_ups,y_ups)
	#print stats.ttest_ind(x_downs,y_downs)
	#print stats.ttest_ind(x_score,y_score)
	#f.close()
#anova_test()