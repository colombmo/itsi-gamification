from django.conf.urls import patterns, url
from HubNet import views

urlpatterns = patterns('',

	# Home page
	url(r'home', views.home, name = 'home'),
	
	# ---------------------------------------------------------------------------------------------------
	# Server information methods.
	# ---------------------------------------------------------------------------------------------------
	# General view, returns the version.
    url(r'version', views.version, name='Version'),
	
	# General view, returns the version.
    url(r'time/(?P<diff>\d+)', views.wstime, name='Time'),
	
	# General view, returns the tables configuration.
    url(r'getTables/(?P<eventID>\d+)', views.get_tables, name='Tables'),
	
	# General view, returns the participants' informations.
    url(r'getParticipants/(?P<eventID>\d+)', views.get_participants, name='Participants'),
	
	# General view, returns the interest tags' informations.
    url(r'getInterests/(?P<eventID>\d+)', views.get_interests, name='Interests'),
	
	# General view, returns the interest tags' informations.
    url(r'getInterestTags', views.get_interestTags, name='InterestTags'),
	
	# ---------------------------------------------------------------------------------------------------
	# Inputs methods.
	# ---------------------------------------------------------------------------------------------------
	
	# Inputs record data view, returns success value.
    url(r'irec/$', views.input_record, name='Input Record'),
	
	# Inputs a new time marker.
    url(r'mrkr/(?P<eventID>\d+)/(?P<label>.+).*', views.input_marker, name='Input Marker'),
	
	# ---------------------------------------------------------------------------------------------------
	# Gamification method.
	# ---------------------------------------------------------------------------------------------------
	
	# Compute scores for each participant
	url(r'getScores1/(?P<eventID>\d+)', views.get_scores1, name ='getScores1'),
	
	# ---------------------------------------------------------------------------------------------------
	# Live interaction methods.
	# ---------------------------------------------------------------------------------------------------
	
	# Search participants
	url(r'participants/(?P<eventID>\d+)', views.search_participants, name='participants'),
	
	#Show participant in the room
	url(r'find/(?P<partId>.+)/(?P<eventID>\d+)', views.find_participants, name='find_part'),
	
	# ---------------------------------------------------------------------------------------------------
	# Live visualization methods.
	# ---------------------------------------------------------------------------------------------------
	# Output force directed graph for user with other groups.
    url(r'leaderboard/(?P<eventID>\d+)', views.leaderboard, name='leaderboard'),
	
	# Output force directed graph for user with other groups.
    url(r'fdgraph/(?P<eventID>\d+)/(?P<partID>.+)', views.forceGraph, name='forceGraph'),
	
	# ---------------------------------------------------------------------------------------------------
	# Statistics methods.
	# ---------------------------------------------------------------------------------------------------
	# Outputs statistics for force directed graphs.
    url(r'fdg/(?P<eventID>\d+).*', views.output_forceGraph, name='fdg'),
	
	# Outputs paths taken by users
	url(r'paths/(?P<eventID>\d+).*', views.output_paths, name='paths'),
	
	# ---------------------------------------------------------------------------------------------------
	# Efficiency tests.
	# ---------------------------------------------------------------------------------------------------	
	# Test reading speed
	url(r'get_all/', views.get_all, name='read'),
	
	# Test writing speed
	url(r'write_test/', views.write_test, name='write'),	
)