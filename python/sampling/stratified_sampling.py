#!/usr/bin/env python
import sys, re, os, math
import numpy as np
sample_file = sys.argv[1].strip()
sample_number = int(sys.argv[2].strip())
samples = dict()
samples_prob = dict()
samples_count = dict()
samples_all_size = 0.0
bucket_count = dict()
for line in open(sample_file):
	p = re.split('\t', line.strip())
	if len(p) != 2: continue
	k = p[0].strip()
	v = int( p[1].strip() )
	b = round(math.log(v)/math.log(2),0)
	b = re.sub('\.0', '', str(b))
	if not b in bucket_count: bucket_count[b]=0
	bucket_count[b] += 1
	if not b in samples: 
		samples[b] = list()
		samples_prob[b] = list()
	samples[b].append(k)
	samples_prob[b].append(v)
	if not k in samples_count: samples_count[k] = v
	else: samples_count[k] += v
	samples_all_size += v

samples_size = dict()
last_remain = 0
for k,v in sorted(bucket_count.iteritems(),key=lambda(k,v):(v,k)):
	sumval = 0.0
	for c in samples_prob[k]:
		sumval += c
	samples_size[k] = round( (sumval/samples_all_size) * sample_number, 0) + last_remain
	if samples_size[k] > v:
		last_remain = samples_size[k] - v
		samples_size[k] = v
	else: last_remain = 0
	for i in range(0,len(samples_prob[k])):
		samples_prob[k][i] /= sumval

sample_set = dict()
for k,v in samples_size.iteritems():
	sample_number = v
	remain_number = v
	while True:
		sel_number = sample_number
		if remain_number < sel_number: sel_number = remain_number
		sample_list = np.random.choice(samples[k], sel_number, p=samples_prob[k])
		new_sample_count = 0
		for item in sample_list:
			if item in sample_set: sample_set[item] += 1
			else: 
				new_sample_count += 1
				sample_set[item] = 1
		remain_number -= new_sample_count
		if remain_number == 0: 
			break
i = 1
for k,v in sorted(sample_set.iteritems(), key=lambda(k,v):(v,k), reverse=True):
	if i > int(sys.argv[2].strip()): break
	i += 1
	print '%s\t%s\t%s'%(k, samples_count[k], v)
