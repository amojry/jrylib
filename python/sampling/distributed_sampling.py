#~/usr/bin/env python
import sys, re, os, math
import numpy as np
sample_file = sys.argv[1].strip()
sample_number = int(sys.argv[2].strip())
samples = list()
samples_prob = list()
samples_count = dict()
sumval = 0.0

for line in open(sample_file):
	p = re.split('\t', line.strip())
	if len(p) != 2: continue
	k = p[0].strip()
	v = int( p[1].strip() )
	samples.append(k)
	samples_prob.append(v)
	if not k in samples_count: samples_count[k] = v
	else: samples_count[k] += v
	sumval += v

for i in range(0, len(samples)):
	samples_prob[i] /= sumval

if sample_number > len(samples): sample_number = len(samples)
sample_set = dict()
remain_number = sample_number - len(sample_set)
while True:
	sel_number = sample_number
	if remain_number < sel_number: sel_number = remain_number
	sample_list = np.random.choice(samples, sel_number, p=samples_prob)
	for item in sample_list:
		if item in sample_set: sample_set[item] += 1
		else: sample_set[item] = 1
	remain_number = sample_number - len(sample_set)
	if remain_number == 0: 
		break
for k,v in sorted(sample_set.iteritems(), key=lambda(k,v):(v,k), reverse=True):
	print '%s\t%s\t%s'%(k, samples_count[k], v)
