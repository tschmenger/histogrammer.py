#!/usr/bin/env python
# -*- coding: utf-8 -*-
# AUTHOR: Torsten Schmenger
import sys
import re
#import logging ### use this in a try: exception: setup, write: logging.exception("message") under except:
#from pprint import pprint as pp
nums = re.compile(r"[+-]?\d+(?:\.\d+)?")
whitespace_killer=re.compile(r"\s+")
# importing Statistics module
import statistics

################################################################################################################################################
#### Default Variables

binsize = 10
colinterested = ""
filus = ""
gram = "="
separator = "\t"
header = ""
################################################################################################################################################
#### Defining OPTIONS
def HELP():
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "© by Torsten Schmenger, 2021"
	print "This script will take a numeric column of a given file and plot a histogram in the command line."
	print "Equal sized Groups will be formed according to the highest value of the given column divided by the number of bins."
	print "After assigning counts into each group the script will normalize the values from 0 to 1."
	print "The histogram is then plotted using = for each 0.005 of the normalized value."
	print "How to use:"
	print "/.histogrammer.py -c NUM -f FILEPATH [OPTIONS] -h -g SYMBOL -s SEPARATOR -b SIZE -k VALUE"
	print "		-c	NUM defines the target column"
	print "		-f	FILEPATH determines the target file"
	print "		-h	prints this help text"
	print "		-s	SEPARATOR sets the field-delimiter in the target file, default is \"\t\" (tab)"
	print "		-g	SYMBOL can either be \"#\" or = or '0' or 'o' or '.' to plot the histogram, default is ="
	print "		-b	SIZE sets the number of bins, default is 10"
	print "		-k	VALUE can be y/1 or n/0, default is n/0. Prints the column header specified with -c. Specify after -c and -f!"
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "\n"


def COLUMN(number):
	colinterested = whitespace_killer.sub("",sys.argv[number+1])
	return colinterested

def BIN(number):
	binsize = int(whitespace_killer.sub("",sys.argv[number+1]))
	try:
		binsize + 1
		return binsize
	except:
		binsize = 10
		return binsize

def OPENER(number):
	filus = whitespace_killer.sub("",sys.argv[number+1])
	return filus	

def SYMBOLER(number):
	gram = whitespace_killer.sub("",sys.argv[number+1])
	if "#" in gram:
		return gram
	elif "=" in gram:
		return gram
	elif "0" in gram:
		return gram
	elif "o" in gram:
		return gram
	elif "." in gram:
		return gram
	else:
		gram = "="
		return gram

def DELIM(number):
	separator = whitespace_killer.sub("",sys.argv[number+1])
	return separator

def HEAD(number):
	head_checker = whitespace_killer.sub("",sys.argv[number+1]) 
	if "y" or "1" in head_checker:
		try:
			f = open(filus)
			header = f.readline().split(separator)[int(colinterested)-1]
			f.close()
		except:
			header = "Header: Error. Check header options."
	elif "n" or "0" in head_checker:
		header = ""
	else:
		pass
	return header
		

################################################################################################################################################
print "\n"

if len(sys.argv) == 3:
	print "Error. Not enough input parameters detected."
	print "\n"
	HELP()
	sys.exit()
elif len(sys.argv) == 1:
	HELP()
	sys.exit()
else:
	pass

for i in range(0,len(sys.argv)):
	item = sys.argv[i]
	if "-h" in item:
		HELP()
		sys.exit()
	elif "-c" in item:
		colinterested = COLUMN(i)
		print "Detected Input: Column of Interest is",colinterested
	elif "-b" in item:
		binsize = BIN(i)
		print "Detected Input: Changed the Number of Bins from 10 to",binsize
	elif "-f" in item:
		filus = OPENER(i)
		print "Detected Input: Target file is",filus
	elif "-g" in item:
		gram = SYMBOLER(i)
		print "Detected Input: Plotting Symbol is",gram
	elif "-s" in item:
		separator = SYMBOLER(i)
		print "Detected Input: Field Delimiter is",separator
	elif "-k" in item:
		header = HEAD(i)
	else:
		pass


### First, getting an overview of the data and determining the different bin groupings
storage = []
grouper = {}
indexer = []
errors = []
with open(filus,"r") as infile:
	for line in infile:
		poi = line.split(separator)[int(colinterested)-1].replace(" ","").replace("\n","")
		try:
			storage.append(float(poi))
		except:
			errors.append(poi)
			pass
try:
	maximum = format(max(storage), '.4f')
	minimum = format(min(storage), '.4f')
	if float(minimum)< 0.0:
		difference = float(maximum) + abs(float(minimum))
	else:
		difference = float(maximum)
except:
	#logging.exception("message")
	print "Error: There were no numeric values in column",colinterested
	print "\n"
	sys.exit()

if len(storage) < len(errors):
	print "There were more STRING characters than numeric values in column",colinterested
	print "Please reconsider your choice."
	print "An example of STRING characters that were found is:"
	try:
		print errors[:10]
	except:
		print errors[:5]
	print "\n"
	sys.exit()

thresholds = [minimum]
binner = difference/binsize
### this will define the different upper and lower limits for each of the bins
for i in range(1,binsize+1):
	cutoff = i * binner + float(minimum)
	thresholds.append(cutoff)

	### preparing a way to store counts
for x in range(0,len(thresholds)-1):
	partner_one = format(float(thresholds[x]), '.4f')
	partner_two = format(float(thresholds[x+1]), '.4f')
	stringler = str(partner_one)+" to "+str(partner_two)
	indexer.append(stringler)
	if grouper.has_key(stringler)==False:
		grouper[stringler]=0

### now we assign values to grouper
with open(filus,"r") as infile:
	for line in infile:
		poi = line.split(separator)[int(colinterested)-1].replace(" ","").replace("\n","")
		try:
			for group in grouper:
				first = group.split(" to ")[0]
				second = group.split(" to ")[1]
				if float(first) <= float(poi) <= float(second):
					grouper[group]+=1			
		except:
			pass

	summa = 0.0
	for categ in grouper:
		summa += grouper[categ]
	for categ in grouper:
		old = float(grouper[categ])
		new = round(old/summa,4)
		grouper[categ]=[new]


### now we have to transform the numeric values in grouper into something more visible, for instance "####" for each 0.05 
for categ in grouper:
	oldval = grouper[categ][0]
	intermediate = int(round(float(oldval)/0.005))
	grouper[categ].append(intermediate*gram)

print "\n"
print "\t","\t","\t","\t",header
print "Bin Groups","\t","rel. value","\t","Histogram"
for item in indexer:
	print item,"\t",grouper[item][0],"\t","|",grouper[item][1]
print "\n"
print "Statistics"
print "Mean=",round(sum(storage)/len(storage),2)
print "STDEV=",round(statistics.stdev(storage),2)
print "\n"



