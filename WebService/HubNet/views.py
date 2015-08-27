from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from HubNet.models import Record, Event, Sensor, InterestTag, Participant, Marker, Interaction
from django.db.models import Q
from django.template import RequestContext, loader
from django_tables2 import RequestConfig
from collections import Counter
from django.utils.html import mark_safe
from operator import itemgetter

import django_tables2 as tables2
import django_filters

import itertools
import time
import datetime
import json
import yaml
import logging
import os

G_eventID = 0;

# Load homepage
def home(request):
	# Load events list
	events = list(Event.objects.all().order_by('-startDate').values_list('id','name', 'startDate'))
	res = []
	for e in events:
		temp = {}
		temp["id"] = e[0]
		temp["name"] = e[1]
		temp["date"] = datetime.datetime.strftime(e[2], '%d %b %Y')
		res.append(temp)
	template = loader.get_template('flatpages/home.html')
	return HttpResponse(template.render(RequestContext(request,{'events': res})))
	
# ---------------------------------------------------------------------------------------------------
# Server information methods.
# ---------------------------------------------------------------------------------------------------
# Get the version of the webservice.
def version(request):
	return HttpResponse("v2.0")
	
# Get the time of the webservice.
def wstime(request, diff):
	if 'callback' in request.REQUEST:
		# Send a JSONP response.
		data = '%s({\'timeStamp\' : \'%s\'});' % (request.REQUEST['callback'], (datetime.datetime.now() - datetime.timedelta(seconds=int(diff))).replace(microsecond=0))
		return HttpResponse(data, "text/javascript")

	return HttpResponse(str((datetime.datetime.now() - datetime.timedelta(seconds=int(diff))).replace(microsecond=0)))
	
# Get configuration of tables
def get_tables(request, eventID):
	if request.method == 'GET':	
		i_eventID = int(str(unicode(eventID)))
		tablesObj = Sensor.objects.filter(event__pk=i_eventID).order_by('identifier')
		i = 0
		tables = []
		for t in tablesObj:
			tables.append([tablesObj.values_list('identifier', flat=True)[i], tablesObj.values_list('description', flat=True)[i], tablesObj.values_list('x', flat=True)[i], tablesObj.values_list('y', flat=True)[i]]);
			i += 1
		flatList = list(itertools.chain.from_iterable(tables))
	return HttpResponse(':&:'.join(map(str,flatList)));
	
# Get participants and their informations
def get_participants(request, eventID):
	if request.method == 'GET':	
		i_eventID = int(str(unicode(eventID)))
		partObj = Participant.objects.filter(event__pk=i_eventID).order_by('reference')
		interObj = InterestTag.objects
		i = 0
		parts = []
		for t in partObj:
			#parts = interObj.values_list('id', flat=True);
			pubkey = partObj.values_list('interestTag_id', flat=True)[i]
			parts.append([str(idk) for idk in partObj.values_list('tagId','firstName', 'lastName')[i]])
			parts.append([str(interObj.filter(id=pubkey).values_list('color', flat=True)[0]),
						  str(1)]); #score
			i += 1
		flatList = list(itertools.chain.from_iterable(parts))
	return HttpResponse(':&:'.join(map(str,flatList)));

# Get interest tags and their informations
def get_interests(request, eventID):
	if request.method == 'GET':	
		i_eventID = int(str(unicode(eventID)))
		interObj = InterestTag.objects.order_by('description').filter(event__pk = i_eventID)
		inter = []
		i = 0
		for t in interObj:
			inter.append([str(interObj.values_list('description')[i][0]), str(interObj.values_list('color', flat = True)[i])])
			i += 1
		flatList = list(itertools.chain.from_iterable(inter))
	return HttpResponse(':&:'.join(map(str,flatList)));
	
# Get interest tags and their informations
def get_interestTags(request):
	if request.method == 'GET':	
		interObj = InterestTag.objects.order_by('description')
		inter = []
		i = 0
		for t in interObj:
			inter.append([str(interObj.values_list('pk')[i][0]),str(interObj.values_list('description')[i][0])])
			i += 1
		flatList = list(itertools.chain.from_iterable(inter))
	return HttpResponse(':&:'.join(map(str,flatList)));
	
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
			i_tagID = data["tagID"]

			# Convert time stamps correctly.
			c_timestamp = datetime.datetime.strptime(str(i_timeStamp), "%Y-%m-%d %H:%M:%S")
			# Acquire relations in database.
			e = Event.objects.get(pk=i_eventID)
			s = Sensor.objects.get(identifier=i_sensorID)
			
			bulk1 = []
			# Write the records.
			for tagID in i_tagID:
				bulk1.append(Record(event=e, sensor=s, timeStamp=c_timestamp, tagId=tagID))
			Record.objects.bulk_create(bulk1)
			
			# Create list of couples based on participants interactions
			couples = list(itertools.combinations(i_tagID,2))
			
			bulk_list1 = [Interaction(event = e, sensor = s, tagId1 = c[0], tagId2 = c[1]) for c in couples]

			Interaction.objects.bulk_create(bulk_list1)	
				
		except Exception as inst:
			print(inst)
			logging.debug('record failed')
			return HttpResponse('FAILED')
			
	return HttpResponse("OK")

	
# ---------------------------------------------------------------------------------------------------
# Gamification method.
# ---------------------------------------------------------------------------------------------------
def get_scores1(request, eventID):
	if request.method == 'GET':
		i_eventID = int(str(unicode(eventID)))
		parts = Participant.objects.filter(event__pk=i_eventID).values_list('tagId','interestTag')
		ret = []
		for i, part in enumerate(parts):
			try:
				totalInt = Interaction.objects.filter(Q(tagId1 = part[0]) | Q(tagId2 = part[0])).count()
			except:
				totalInt = 0
			# Othergroups: number of interactions with participants from other groups
			try:
				sameGroup = Participant.objects.filter(event__pk=i_eventID).filter(interestTag = part[1]).values_list('tagId',flat=True)
				otherGroups = (totalInt-Interaction.objects.filter(Q(tagId1__in = sameGroup)).filter(Q(tagId2__in = sameGroup)).filter(Q(tagId1 = part[0]) | Q(tagId2 = part[0])).count())/2
			except:
				otherGroups = 0
				
			# Score: number of interactions with other participants (participants of the same group 1 point, other groups 1.5 points)
			score = totalInt+otherGroups #(totalInt+(totalInt-internalInt)/2)
			
			if(score!=0):
				ret.append([part[0],score])
		# Sort list by score
		ret = sorted(ret, key=itemgetter(1), reverse = True)
		retValue = list(itertools.chain.from_iterable(ret))
	return HttpResponse(':&:'.join(map(str,retValue)));	
	
# ---------------------------------------------------------------------------------------------------
# Live interaction methods.
# ---------------------------------------------------------------------------------------------------

# Class to create tables
class ParticipantTable(tables2.Table):
	finder = tables2.LinkColumn('find_part', verbose_name='Position', empty_values=(), orderable = False)
	fdg = tables2.LinkColumn('fdg_part', verbose_name='Interactions with groups', empty_values=(), orderable = False)
	
	def render_finder(self, value, record):
		global G_eventID
		return mark_safe('''<a href=%s>%s</a>''' % ('../find/'+str(record.tagId)+'/'+str(G_eventID), 'Show >>'))
	
	def render_fdg(self, value, record):
		global G_eventID
		return mark_safe('''<a href=%s>%s</a>''' % ('../fdgraph/'+str(G_eventID)+'/'+str(record.tagId), 'Show >>'))
	
	class Meta:
		model = Participant
		# fields to display
		fields = ('firstName', 'lastName', 'interestTag')
		# add class="table" to <table> tag
		attrs = {'class':'table table-full'}
		
# Class to create filters
class ParticipantFilter(django_filters.FilterSet):
	firstName = django_filters.Filter(lookup_type='icontains')
	lastName = django_filters.Filter(lookup_type='icontains')
	
	class Meta:
		model = Participant
		fields = ['firstName', 'lastName', 'interestTag']
				
# Search participants
def search_participants(request, eventID):
	i_eventID = int(str(unicode(eventID)))
	global G_eventID
	G_eventID = i_eventID
	
	queryset = Participant.objects.filter(event__pk = i_eventID)
	f = ParticipantFilter(request.GET, queryset=queryset)
	table = ParticipantTable(f.qs)
	RequestConfig(request, paginate={"per_page": 25, "page": 1}).configure(table)
	return render(request, 'live_interaction/search.html', {'table': table, 'filter': f, 'event': i_eventID})

# Show participant in the room
def find_participants(request, partId, eventID):
	i_eventID = int(str(unicode(eventID)))
	try:
		last_rec = Record.objects.order_by('-timeStamp').filter(tagId = partId).values_list('sensor_id', 'event_id', 'timeStamp')[0]
		recTime = last_rec[2]
		tablesObj = Sensor.objects.filter(event__pk=eventID).filter(displayable = True).order_by('identifier').values_list('id','x','y','description')
		# Create json
		tables = []
		timeDiff = abs(datetime.datetime.now()-recTime).seconds
		print("Timediff:"+str(timeDiff))
		if timeDiff<10:
			for t in tablesObj:
				c = "black"
				if t[0] == last_rec[0]: #and timeDiff<10:
					c = "red"
				tables.append('{"x":'+str(t[1])+', "y":'+str(t[2])+', "color":"'+c+'", "text":"'+str(t[3])+'"}');
				res = '{"tables":['+','.join(tables)+']}'
			template = loader.get_template('live_interaction/find.html')
			return HttpResponse(template.render(RequestContext(request,{'results' :res, 'event': i_eventID})))
		else:
			template = loader.get_template('live_interaction/not_found.html')
	except Exception as inst:
		print(inst)
		template = loader.get_template('live_interaction/not_found.html')
	return HttpResponse(template.render(RequestContext(request,{'event': i_eventID})))


# ---------------------------------------------------------------------------------------------------
# Live visualization methods.
# ---------------------------------------------------------------------------------------------------
# Output force directed graph for user with other groups.
def forceGraph(request, eventID, partID):
	if request.method == 'GET':	
		# Get the required data & setup.
		i_eventID = int(str(unicode(eventID)))	
		
		# Database requests
		part = Participant.objects.filter(event__pk = i_eventID).filter(tagId = partID)
		interests = InterestTag.objects.filter(event__pk = i_eventID)
		
		# Create nodes (and a dictionary for links)
		linkDic = {}
		dic = []
		temp_nodes = []
		
		name = str(part[0].firstName)+" "+str(part[0].lastName)
		
		dic.append(name)
		linkDic[name] = 0
		temp_nodes.append('{"name": "'+name+'", "color": "black"}')
		
		for i,obj in enumerate(interests):
			dic.append(str(obj.description))
			linkDic[str(obj.description)]=i+1;
			temp_nodes.append('{"name": "'+str(obj.description)+'", "color": "#'+str(obj.color)+'"}')
		
		# Links between nodes
		temp_links = []
		print(part[0].tagId)
		for i,inter in enumerate(interests):
			tagsInInter = Participant.objects.filter(event__pk = i_eventID).filter(interestTag = inter).values('tagId')
			try:
				x = Interaction.objects.filter(event__pk = i_eventID).filter(Q(tagId1 = part[0].tagId) | Q(tagId2 = part[0].tagId)).filter(Q(tagId1__in = tagsInInter) | Q(tagId2__in = tagsInInter)).count()
			except:
				x = 0
			if x>=1:
				print(x)
				temp_links.append('{"source":'+str(0)+', "target":'+str(i+1)+', "value":'+str(x)+'}')
		
		results = '{"nodes": ['+','.join(temp_nodes)+'], "links":['+ ','.join(temp_links)+ ']}'
		
	template = loader.get_template('visualization/force_graph_indiv.html')
	return HttpResponse(template.render(RequestContext(request,{'results' :results, 'event': i_eventID})))	
	
# Show leaderboard with points
def leaderboard(request, eventID):
	try:
		if request.method == 'GET':
			i_eventID = int(str(unicode(eventID)))
			parts = Participant.objects.filter(event__pk=i_eventID).values_list('tagId','firstName', 'lastName', 'interestTag')
			ret = []
			# Interactions: number of interactions with other participants (participants of the same group 1 point, other groups 1.5 points)
			for i, part in enumerate(parts):
				try:
					interactions = Interaction.objects.filter(Q(tagId1 = part[0]) | Q(tagId2 = part[0])).count()
				except:
					interactions = 0
				# Othergroups: number of interactions with participants from other groups
				try:
					sameGroup = Participant.objects.filter(event__pk=i_eventID).filter(interestTag = part[3]).values_list('tagId',flat=True)
					otherGroups = (interactions-Interaction.objects.filter(Q(tagId1__in = sameGroup)).filter(Q(tagId2__in = sameGroup)).filter(Q(tagId1 = part[0]) | Q(tagId2 = part[0])).count())/2
				except:
					otherGroups = 0
				
				if(interactions!=0):
					if(otherGroups!=0):
						ret.append([str(part[1])+' '+str(part[2]), interactions, otherGroups])
			# Sort list by score
			ret.sort(key=lambda obj: obj[1]+obj[2], reverse = True)
			
			results = []
			
			for i in ret:
				results.append('{ "key" : "'+ str(i[0])+'", "pop1" : '+str(i[1])+', "pop2" :'+str(i[2])+'}')
		template = loader.get_template('visualization/leaderboard.html')
		return HttpResponse(template.render(RequestContext(request,{'max' : ret[0][1]+ret[0][2] ,'results' :'['+','.join(results)+']', 'event': i_eventID})))
	except:
		return HttpResponse("Leaderboard still empty, register some values before!")
# ---------------------------------------------------------------------------------------------------
# Statistics methods.
# ---------------------------------------------------------------------------------------------------
# Output statistics for force directed graph.
def output_forceGraph(request, eventID):
	if request.method == 'GET':	
		# Get the required data & setup.
		i_eventID = int(str(unicode(eventID)))	
		
		# Database requests
		recParts = Record.objects.filter(event__pk=i_eventID).values('tagId')
		tagList = Participant.objects.filter(event__pk=i_eventID).filter(tagId__in = recParts).order_by('tagId')
		participantCount = tagList.count()
		
		interactions = Interaction.objects.filter(event__pk = i_eventID)
		
		# Create nodes (and a dictionary for links)
		linkDic = {}
		dic = []
		temp_nodes = []

		for i,obj in enumerate(tagList):
			dic.append(str(obj.tagId))
			linkDic[str(obj.tagId)] = i
			temp_nodes.append('{"name": "'+str(obj.firstName)+' '+str(obj.lastName)+'", "color": "#'+str((obj.interestTag.color))+'"}')
				
		# Results as json
		temp_links = []
		for i in range(participantCount):
			for j in range(i+1, participantCount):
				x = interactions.filter(tagId1 = dic[i]).filter(tagId2 = dic[j]).count()
				if x>=10:
					temp_links.append('{"source":'+str(i)+', "target":'+str(j)+', "value":'+str(x)+'}')
		
		results = '{"nodes": ['+','.join(temp_nodes)+'], "links":['+ ','.join(temp_links)+ ']}'
		
	template = loader.get_template('analytics/force_graph.html')
	return HttpResponse(template.render(RequestContext(request,{'results' :results, 'event': i_eventID})))
	
def output_paths(request, eventID):
	i_eventID = int(str(unicode(eventID)))

	tablesObj = Sensor.objects.filter(event__pk = i_eventID).filter(displayable = True).order_by('identifier').values('id','x','y','description')
	tablesDic = {}
	
	tables = []
	
	for i,table in enumerate(tablesObj):
		tablesDic[table['id']] = i;
		tables.append('{"x":'+str(table['x'])+',"y":'+str(table['y'])+'}')
		
	recs = Record.objects.filter(event__pk = i_eventID)
	parts = Participant.objects.filter(event__pk= i_eventID).filter(Q(tagId__in = recs.values('tagId')))
	paths = []
	for part in parts:
		allRecs = recs.filter(tagId = part.tagId).order_by('timeStamp').values_list('sensor', flat=True)
		cleanRecs = [x[0] for x in itertools.groupby(allRecs)]
		for first, second in itertools.izip(cleanRecs, cleanRecs[1:]):
			paths.append(tuple(sorted([first,second])))
	
	paths = Counter(paths).most_common()
	
	pathsJSON = []
	#Create JSON
	for path in paths:
		pathsJSON.append('{"source":'+str(tablesDic[path[0][0]])+', "target":'+str(tablesDic[path[0][1]])+', "value":'+str(path[1])+'}')
	
	results = '{"tables": ['+','.join(tables)+'], "paths":['+','.join(pathsJSON)+']}'
	
	template = loader.get_template('analytics/paths.html')
	return HttpResponse(template.render(RequestContext(request,{'results' :results, 'event': i_eventID})))
	
def get_all(request):
	start_time = time.time()
	res = Record.objects.all().count()
	tit = time.time()-start_time
	size = res
	return HttpResponse(str(size)+" elements in "+ str(tit)+" seconds")
	
def write_test(request):
	res = ""
	for x in range(1,21):
		temp = 0
		for y in range(1,1000):
			i_timeStamp = "2015-08-15 13:33:32"
			i_tagID = ["AAAAAAAAAAAAAAAAAAAA" for _ in range(x)]

			# Convert time stamps correctly.
			c_timestamp = datetime.datetime.strptime(str(i_timeStamp), "%Y-%m-%d %H:%M:%S")
			# Acquire relations in database.
			e = Event.objects.get(pk=13)
			s = Sensor.objects.get(identifier=1)
			
			start_time = time.time()
			bulk_list = []
			# Write the records.
			for tagID in i_tagID:
				bulk_list.append(Record(event=e,sensor=s,timeStamp=c_timestamp, tagId = tagID))
			
			Record.objects.bulk_create(bulk_list)
			
			# Create list of couples based on participants interactions
			couples = list(itertools.combinations(i_tagID,2))
			
			bulk_list1 = [Interaction(event = e, sensor = s, tagId1 = c[0], tagId2 = c[1]) for c in couples]

			Interaction.objects.bulk_create(bulk_list1)	
			
			tit = time.time()-start_time
			temp += tit
		res += str(temp/1000)+os.linesep
	print(res)
	return HttpResponse(res)