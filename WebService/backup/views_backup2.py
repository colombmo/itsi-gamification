from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from HubNet.models import Record, Event, Sensor, InterestTag, Participant, Marker
from datetime import datetime
from django.template import RequestContext, loader

import numpy as np
import pandas as pd

import itertools
import sys
import time

import json
import yaml
import datetime
import logging
import urllib
import re

# ---------------------------------------------------------------------------------------------------
# Server information methods.
# ---------------------------------------------------------------------------------------------------

# Get the version of the webservice.
def version(request):
	return HttpResponse("v0.1A")
	
# Get the time of the webservice.
def wstime(request, diff):
	if 'callback' in request.REQUEST:
		# Send a JSONP response.
		data = '%s({\'timeStamp\' : \'%s\'});' % (request.REQUEST['callback'], (datetime.datetime.now() - datetime.timedelta(seconds=int(diff))).replace(microsecond=0))
		return HttpResponse(data, "text/javascript")

	return HttpResponse(str((datetime.datetime.now() - datetime.timedelta(seconds=int(diff))).replace(microsecond=0)))
	
# ---------------------------------------------------------------------------------------------------
# Inputs methods.
# ---------------------------------------------------------------------------------------------------

# Post a new marker.
@csrf_exempt
def input_marker(request, eventID, label):
	if request.method == 'POST':
		try:
			i_eventID = int(str(unicode(eventID)))
			i_label = str(unicode(label))
			c_timestamp = datetime.datetime.now()
			
			# Acquire relations in database.
			e = Event.objects.get(pk=i_eventID)
			
			# Add new marker.
			Marker.objects.create(label=i_label, timeStamp=c_timestamp, event=e)
			
		except:
			logging.debug('Posting marker failed')
			return HttpResponse('FAILED')

	return HttpResponse("OK")
	
# Post a new record for an event & sensor.
@csrf_exempt
def input_record(request):
	if request.method == 'POST':
		try:
			# Read data from the JSON payload.
			raw = yaml.load(request.body)
			str_data = str(raw).replace("'", '"')
			data = json.loads(str_data)

			i_eventID = data["eventID"]
			i_sensorID = data["sensorID"]
			i_timeStamp = data["timeStamp"]
			i_records = data["records"]

			# Convert time stamps correctly.
			c_timestamp = datetime.datetime.strptime(str(i_timeStamp), "%Y-%m-%d %H:%M:%S")
			# Acquire relations in database.
			e = Event.objects.get(pk=i_eventID)
			s = Sensor.objects.get(identifier=i_sensorID)

			# Write the records.
			for rec in i_records:
				Record.objects.create(event=e, sensor=s, timeStamp=c_timestamp, tagId=rec["tag"], rssi=rec["rssi"])
				
		except:
			logging.debug('record failed')
			return HttpResponse('FAILED')
			
	return HttpResponse("OK")
	
# ---------------------------------------------------------------------------------------------------
# Statistics methods.
# ---------------------------------------------------------------------------------------------------
	
# Get all the markers for a given event.
def output_statMarkers(request, eventID):
	if request.method == 'GET':	
		i_eventID = int(str(unicode(eventID)))
		
		# Get starting time of the event to compute the time difference.
		eventObject = Event.objects.filter(pk=i_eventID)
		eventTime = eventObject[0].startDate
	
		# Gather list of markers.
		markers = Marker.objects.filter(event__pk=i_eventID)
		count = Marker.objects.filter(event__pk=i_eventID).count()
		results = '['
		
		if(count > 0):
			for x in range(0, count):
				# Compute the time difference.
				diff = ((markers[x].timeStamp - eventTime).seconds) +1
			
				# Add the data to the json response.
				if(x != count -1):
					results += '{"time": ' + str(diff) + ', "label": "' + markers[x].label + '"}, '
				else:
					results += '{"time": ' + str(diff) + ', "label": "' + markers[x].label + '"}]'
		else:
			results = '[]'
			
		if 'callback' in request.REQUEST:
				# Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
		
	return HttpResponse(json.dumps(results), "application/json")
	
#Get all records
def output_all(request, eventID, sensorID):
	if request.method == 'GET':
		try:
			# Gather required data.
			i_eventID = int(str(unicode(eventID)))
			i_sensorID = int(str(unicode(sensorID)))
			
			eventTime = Event.objects.filter(pk=i_eventID)[0].startDate
			
			records = Record.objects.values_list('timeStamp', flat=True).filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).order_by('timeStamp')
			count = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).count()
			# Determine the number of minutes of the records.
			if(count > 1):
				# Crunch the data.	
				def get_sec(record):
					return record.seconds
				vget_sec = np.vectorize(get_sec)	# Vectorized function to get seconds component of time difference

				records_array = np.array(records)
				delta_time = vget_sec(records_array-records[0])	# Get time difference between each record and start time in seconds 
				
				statistics = np.bincount(delta_time).tolist()	# Get number of recordings at each second (in a list)
				
				# Format the values to json.
				results = '['
				
				minutes = (records[count-1] - records[0]).seconds +1
				minutesCount = 0
				startTime = records[0]
				eventTmpTime = eventTime
				timeDiffEventBegin = (startTime - eventTmpTime).seconds
				
				for z in range(0, timeDiffEventBegin):
					results += '{"time": ' + str(minutesCount) + ', "value": 0}, '
					minutesCount += 1
				
				for y in range(0, minutes):
					# Add the data to the json response.
					if(y != minutes -1):
						results += '{"time": ' + str(minutesCount) + ', "value": ' + str(statistics[y]) + '}, '
						minutesCount += 1
					else:
						results += '{"time": ' + str(minutesCount) + ', "value": ' + str(statistics[y]) + '}]'
			else:
				return HttpResponse('NONE')
		except:
			logging.debug('request record failed')
			return HttpResponse('FAILED')
	template = loader.get_template('visualization/scatter.html')
	return HttpResponse(template.render(RequestContext(request,{'results' :results})))
	#return HttpResponse(results)
		

# Get all records for a given event and sensor.
def output_statData(request, eventID, sensorID):
	if request.method == 'GET':	
		try:
			# Gather required data.
			i_eventID = int(str(unicode(eventID)))
			i_sensorID = int(str(unicode(sensorID)))
			
			eventObject = Event.objects.filter(pk=i_eventID)
			eventTime = eventObject[0].startDate
			
			records = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).order_by('timeStamp')
			count = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).count()
			
			# Determine the number of minutes of the records.
			if(count > 1):
				tdelta = records[count-1].timeStamp - records[0].timeStamp
				minutes = (tdelta.seconds) +1
				statistics = [0] * minutes
				
				# Crunch the data.
				for x in range(0, count):
					index = ((records[x].timeStamp - records[0].timeStamp).seconds)
					statistics[index] += 1;
					
				# Format the values to json.
				results = '['
				
				minutesCount = 0
				startTime = records[0].timeStamp
				eventTmpTime = eventTime
				timeDiffEventBegin = (startTime - eventTmpTime).seconds
				
				for z in range(0, timeDiffEventBegin):
					results += '{"time": ' + str(minutesCount) + ', "value": 0}, '
					minutesCount += 1
				
				for y in range(0, minutes):
					# Add the data to the json response.
					if(y != minutes -1):
						results += '{"time": ' + str(minutesCount) + ', "value": ' + str(statistics[y]) + '}, '
						minutesCount += 1
					else:
						results += '{"time": ' + str(minutesCount) + ', "value": ' + str(statistics[y]) + '}]'

				if 'callback' in request.REQUEST:
					# Send a JSONP response.
					data = '%s(%s);' % (request.REQUEST['callback'], results)
					return HttpResponse(data, "text/javascript")
					
			else:
				return HttpResponse('NONE')
		except:
			logging.debug('request record failed')
			return HttpResponse('FAILED')
			
	#return HttpResponse(json.dumps(results), "application/json")
	return HttpResponse(results)
	
# Output statistics per interest tag for a sensor.
def output_statData_perTag(request, eventID, sensorID):
	if request.method == 'GET':	
		#try:
		# Gather required data.
		i_eventID = int(str(unicode(eventID)))
		i_sensorID = int(str(unicode(sensorID)))
		
		eventObject = Event.objects.filter(pk=i_eventID)
		
		interestTags = InterestTag.objects.filter(event__pk=i_eventID).order_by('id')
		countInterestTags = InterestTag.objects.filter(event__pk=i_eventID).count()
		interestsDict = {}
		
		eventTime = eventObject[0].startDate
		
		records = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).order_by('timeStamp')
		count = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).count()		
		
		# Create interest tags hashmap.
		for tagsTmpCount in range(0, countInterestTags):
			interestsDict[interestTags[tagsTmpCount].id] = tagsTmpCount
		
		# Determine the number of minutes of the records.
		if(count > 1):
			tdelta = records[count-1].timeStamp - records[0].timeStamp
			minutes = (tdelta.seconds) +1
			statistics = np.zeros((countInterestTags, minutes))
			
			# Crunch the data.
			for x in range(0, count):
				index = ((records[x].timeStamp - records[0].timeStamp).seconds)
				
				if(Participant.objects.filter(tagId=str(records[x].tagId)).count() > 0):
					tag = interestsDict[Participant.objects.filter(tagId=str(records[x].tagId))[0].interestTag.id]
					statistics[tag][index] += 1;
				
			# Format the values to json.
			results = '['
			
			for t in range(0, countInterestTags):
				# Compute array per interest tag.
				array = '['
				minutesCount = 0
				startTime = records[0].timeStamp
				eventTmpTime = eventTime
				timeDiffEventBegin = (startTime - eventTmpTime).seconds
				
				for z in range(0, timeDiffEventBegin):
					array += '{"x": ' + str(minutesCount) + ', "y": 0}, '
					minutesCount += 1
				
				for y in range(0, minutes):
					# Add the data to the json response.
					if(y != minutes -1):
						array += '{"x": ' + str(minutesCount) + ', "y": ' + str(statistics[t][y]) + '}, '
						minutesCount += 1
					else:
						array += '{"x": ' + str(minutesCount) + ', "y": ' + str(statistics[t][y]) + '}]'
						
				# Prepare new interest tag.
				if(t != countInterestTags -1):
					results += '{"name": "' + str(interestTags[t].description + '", "values": ' + array + '}, ')
				else:
					results += '{"name": "' + str(interestTags[t].description + '", "values": ' + array + '}]')

			if 'callback' in request.REQUEST:
				# Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
				
		else:
			return HttpResponse('NONE')
		#except:
		#	logging.debug('request record failed')
		#	return HttpResponse('FAILED')
			
	#return HttpResponse(json.dumps(results), "application/json")
	return HttpResponse(results)
	
# Output statistics of tag percentage per table.
def output_statDataInterests(request, eventID, sensorID):
	if request.method == 'GET':	
		#try:
		# Gather required data.
		i_eventID = int(str(unicode(eventID)))
		i_sensorID = int(str(unicode(sensorID)))
		
		eventObject = Event.objects.filter(pk=i_eventID)
		
		interestTags = InterestTag.objects.filter(event__pk=i_eventID).order_by('id')
		countInterestTags = InterestTag.objects.filter(event__pk=i_eventID).count()
		interestsDict = {}
		
		# For special use between two markers.
		start = Marker.objects.filter(event__pk=i_eventID).filter(label='Buffet')[0].timeStamp
		stop = Marker.objects.filter(event__pk=i_eventID).filter(label='End')[0].timeStamp
		
		records = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).filter(timeStamp__range=[start, stop]).order_by('timeStamp')
		count = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).filter(timeStamp__range=[start, stop]).count()
		
		#records = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).order_by('timeStamp')
		#count = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID).count()		
		
		# Create interest tags hashmap.
		for tagsTmpCount in range(0, countInterestTags):
			interestsDict[interestTags[tagsTmpCount].id] = tagsTmpCount
		
		# Determine the number of seconds of the records.
		if(count > 1):
			tdelta = records[count-1].timeStamp - records[0].timeStamp
			minutes = (tdelta.seconds) +1
			statistics = np.zeros((countInterestTags, minutes))
			
			# Crunch the data.
			for x in range(0, count):
				index = ((records[x].timeStamp - records[0].timeStamp).seconds)
				
				if(Participant.objects.filter(tagId=str(records[x].tagId)).count() > 0):
					tag = interestsDict[Participant.objects.filter(tagId=str(records[x].tagId))[0].interestTag.id]
					statistics[tag][index] += 1
				
			# Sum all readings per interest tag.
			sums = [0] * countInterestTags
			
			for t in range(0, countInterestTags):
				for u in range(0, minutes-1):
					sums[t] += statistics[t][u]
			
			# Compute percentages.
			results = '[{"count": ' + str(count) + '}, '
			
			for w in range(0, countInterestTags):
				if(w != countInterestTags-1):
					results += '{' + str(interestTags[w].description) + ': ' + str(sums[w] / count) + '}, '
				else:
					results += '{' + str(interestTags[w].description) + ': ' + str(sums[w] / count) + '}]'

			if 'callback' in request.REQUEST:
				# Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
				
		else:
			return HttpResponse('NONE')
		#except:
		#	logging.debug('request record failed')
		#	return HttpResponse('FAILED')
			
	return HttpResponse(json.dumps(results), "application/json")
	
# Output statistics of tag percentage per table.
def output_statOverlap(request, eventID, sensorID1, sensorID2):
	if request.method == 'GET':	
		#try:
		# Gather required data.
		i_eventID = int(str(unicode(eventID)))
		i_sensorID1 = int(str(unicode(sensorID1)))
		i_sensorID2 = int(str(unicode(sensorID2)))
		
		eventObject = Event.objects.filter(pk=i_eventID)
		overlapHits = 0
		
		# Get all records from the first sensor.
		recordsS1 = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID1)
		recordsS1Count = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID1).count()
		
		# For each record of the first sensor, check if any overlap exists.
		for x in range(0, recordsS1Count):
			startTime = recordsS1[x].timeStamp
			
			potentialOverlaps = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID2).filter(timeStamp=startTime).count()
			
			if(potentialOverlaps > 0):
				tests = Record.objects.filter(event__pk=i_eventID).filter(sensor__identifier=i_sensorID2).filter(timeStamp=startTime)
				
				for y in range(0, potentialOverlaps):
					if(tests[y].tagId == recordsS1[x].tagId):
						overlapHits += 1
		
		# Format results.
		results = '[overlap: ' + str(overlapHits) + ', total: ' + str(recordsS1Count) + ']'
		
		if 'callback' in request.REQUEST:
			# Send a JSONP response.
			data = '%s(%s);' % (request.REQUEST['callback'], results)
			return HttpResponse(data, "text/javascript")
				
		#except:
		#	logging.debug('request record failed')
		#	return HttpResponse('FAILED')
			
	return HttpResponse(json.dumps(results), "application/json")

# Output statistics for force directed graph.
def output_forceGraph(request, eventID):
	if request.method == 'GET':
		# Get the required data & setup.
		i_eventID = int(str(unicode(eventID)))	
		startTime = Record.objects.filter(event__pk=3).order_by('timeStamp')[0].timeStamp
					
		# Database requests
		participantDict = Participant.objects.filter(event__pk=3)
		participantCount = participantDict.count()
		tagList = participantDict.values_list('tagId', flat=True)
		sensors = Sensor.objects.filter(event__pk=i_eventID).exclude(displayable=False)
		
		eventObject = Event.objects.filter(pk=i_eventID)
		timeEnd = eventObject[0].stopDate
		ev_duration = ((timeEnd - startTime).seconds) +1
		
		# Create nodes (and a dictionary for links)
		linkDic = {}
		temp_nodes = []
		for i,obj in enumerate(participantDict):
			linkDic[str(obj.tagId)] = i
			temp_nodes.append('{"name": "'+str(obj.tagId)+'", "group": '+str((obj.interestTag).pk)+'}')
		
		def get_timeStamp(record):
			return record.timeStamp
		vget_timeStamp = np.vectorize(get_timeStamp)
		
		all_td = np.array([datetime.timedelta(seconds = s) for s in range(ev_duration)])
		all_times = all_td+startTime
		ts_dict = {}
		for i,t in enumerate(all_times):
			ts_dict[str(t)]=i
		
		# Iterate through records for each sensor
		res = np.zeros((participantCount, participantCount), dtype = np.int)	# Interaction matrix (i,j), contains number of interactions between participant i and j
		for sen in sensors:
			# Get records and timestamps
			records = Record.objects.filter(event__pk=i_eventID).filter(sensor__pk= sen.pk).order_by('timeStamp')
			t1 = time.time()
			rec_ts = list(records.values_list('timeStamp', flat=True))
			rec_id = list(records.values_list('tagId', flat=True))
			print str(1000*(time.time()-t1))
			# Conversion to numpy array (~0.5 seconds/array)
			
			#rec = np.array(records)
			records_array = np.array([ts_dict[str(t)] for t in rec_ts],dtype = np.int)
			
			#records_array = vget_timeStamp(rec)
			# Get all indices of duplicated timestamps
			idx_sort = np.argsort(records_array)
			sorted_records_array = records_array[idx_sort]
			vals, idx_start, count = np.unique(sorted_records_array, return_counts=True, return_index=True)
			users_inter = np.split(idx_sort, idx_start[1:])
			users_inter = filter(lambda x: x.size > 1, users_inter)
			
			# Transform array ids in tagIds and create all interacting tag couples
			tempTags = [list(set([str(rec_id[i]) for i in id_list])) for id_list in users_inter]
			tag_couples = [x for l in tempTags for x in itertools.combinations(l,2)]
						
			# Prevent possible errors with unregistered tags
			idlst = []
			for el in tag_couples:
				try:
					idlst.append(tuple(sorted((linkDic[el[0]], linkDic[el[1]])))) # Translate tagId to id used for links
				except:
					pass
			#Populate interaction matrix
			already_checked = []
			for couple in idlst:
				if couple not in already_checked:
					already_checked.append(couple)
					res[couple[0]][couple[1]] += idlst.count(couple) # This puts number of interactions between two users in the matrix

		# Results as json
		temp_links = ['{"source":'+str(i)+', "target":'+str(j)+', "value":'+str(res[i][j])+'}' for i in range(participantCount) for j in range(i+1, participantCount) if res[i][j]!=0]
		results = '{"nodes": ['+','.join(temp_nodes)+'], "links":['+ ','.join(temp_links)+ ']}'

	template = loader.get_template('visualization/force_graph.html')
	return HttpResponse(template.render(RequestContext(request,{'results' :results})))
	
# Output statistics for force directed graph.
def output_statForceGraph(request, eventID):
	if request.method == 'GET':	
		#try:
			# Get the required data & setup.
			i_eventID = int(str(unicode(eventID)))
			eventObject = Event.objects.filter(pk=i_eventID)
			
			startTime = Record.objects.filter(event__pk=3).order_by('timeStamp')[0].timeStamp
			timeEnd = eventObject[0].stopDate
			seconds = ((timeEnd - startTime).seconds) +1
			
			# Get list and count of participant to initialize the matrix.
			participantDict = Participant.objects.filter(event__pk=3)
			participantList = []
			
			for obj in participantDict:
				participantList.append(str(obj.tagId))
			
			particitipantCount = Participant.objects.filter(event__pk=3).count()
			matrix = np.zeros((particitipantCount, particitipantCount))
			
			# Get number and references to the sensors.
			sensors = Sensor.objects.filter(event__pk=i_eventID).exclude(displayable=False)
			sensorsCount = Sensor.objects.filter(event__pk=i_eventID).exclude(displayable=False).count()
			
			# Iterate through the records.
			for second in range(0, seconds):
				# For each table, get the set of participants around it at the same time.
				for table in range(0, sensorsCount):
					records = Record.objects.filter(timeStamp=startTime).filter(sensor__identifier=sensors[table].identifier)
					
					# Create list of participants tagID at the table.
					indexes = []
					
					for x in range(0, len(records)-1):
						indexes.append(participantList.index(str(records[x].tagId)))
						
					# Increment by 1 all combinations of these participants in the matrix.
					
				
				print(indexes)
				# Increment the seconds by 1:
				startTime += datetime.timedelta(seconds=1)
		
			results = []
		
			if 'callback' in request.REQUEST:
				# Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
				
		#except:
		#	logging.debug('request record failed')
		#	return HttpResponse('FAILED')
			
	return HttpResponse(json.dumps(results), "application/json")

# ---------------------------------------------------------------------------------------------------
# Live visualization methods.
# ---------------------------------------------------------------------------------------------------
	
# Get updated live feed.
@csrf_exempt
def output_getLiveUpdate(request, eventID, timeStamp):
	if request.method == 'GET':
		try:
			i_eventID = int(str(unicode(eventID)))
			i_timeStamp = str(unicode(timeStamp))
			
			# Prepare request context.
			c_timestamp = datetime.datetime.strptime(i_timeStamp, "%Y-%m-%d %H:%M:%S")
			
			# Gather list of records.
			records = Record.objects.filter(event__pk=i_eventID).filter(timeStamp=c_timestamp).exclude(sensor__displayable=False)
			
			# Sort distinct results.
			distinctRecords = []
			seen = set()
		
			for rec in records:
				if rec.tagId not in seen:
					distinctRecords.append(rec)
					seen.add(rec.tagId)
		
			results = [ob.as_json() for ob in distinctRecords]
			print results
			
			if 'callback' in request.REQUEST:
                # Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
			
		except:
			logging.debug('request record failed')
			return HttpResponse('FAILED')
		
		return HttpResponse(json.dumps(results), "application/json")
		
# Get distinct live records.
def output_live_distinct(request, eventID):
	if request.method == 'GET':
		try:
			# Identify latest created record (closest to liveness).
			lastRecord = Record.objects.filter(event__pk=eventID).latest(field_name="timeStamp")
		
			# Get all records from most live timeStamp with distinct tagID.
			records = Record.objects.filter(timeStamp=lastRecord.timeStamp)
		
			distinctRecords = []
			seen = set()
		
			# Get distinct tagIDs.
			for rec in records:
				if rec.tagId not in seen:
					distinctRecords.append(rec)
					seen.add(rec.tagId)
		
			results = [ob.as_json() for ob in distinctRecords]
			
			if 'callback' in request.REQUEST:
                # Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
			
		except:
			logging.debug('request live distinct failed')
			return HttpResponse('{[]}', "application/json")
				
	return HttpResponse(json.dumps(results), "application/json")

		
# Get config file.
@csrf_exempt
def output_config(request, eventID):
	if request.method == 'GET':
		try:
			sensors = Sensor.objects.filter(event__pk = eventID).exclude(displayable=False)
			results = [ob.as_json() for ob in sensors]
			
			if 'callback' in request.REQUEST:
                # Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
				
		except:
			logging.debug('request config failed')
			return HttpResponse('FAILED')
			
		return HttpResponse(json.dumps(results), "application/json")
	
# Get All records for an event.
def output_all_records(request, eventID):
	if request.method == 'GET':
		try:
			records = Record.objects.filter(event__pk=eventID)
			results = [ob.as_json() for ob in records]
			
		except:
			logging.debug('request all records failed')
			return HttpResponse('FAILED')
				
	return HttpResponse(json.dumps(results), "application/json")
	
# Get All records for an event.
def output_all_interestTags(request, eventID):
	if request.method == 'GET':
		try:
			tags = InterestTag.objects.filter(event__pk=eventID)
			results = [ob.as_json() for ob in tags]
			
		except:
			logging.debug('request all interest tags failed')
			return HttpResponse('FAILED')
				
	return HttpResponse(json.dumps(results), "application/json")
	
# Get All records for an event.
def output_all_participants(request, eventID):
	if request.method == 'GET':
		try:
			participants = Participant.objects.filter(event__pk=eventID)
			results = [ob.as_json() for ob in participants]
			
			if 'callback' in request.REQUEST:
                # Send a JSONP response.
				data = '%s(%s);' % (request.REQUEST['callback'], results)
				return HttpResponse(data, "text/javascript")
			
		except:
			logging.debug('request all interest tags failed')
			return HttpResponse('FAILED')
				
	return HttpResponse(json.dumps(results), "application/json")