from django.contrib import admin
from HubNet.models import InterestTag, Event, Sensor, Participant, Record, Interaction, Marker

# Author: Thomas "Raste" Rouvinez
# Creation date: 2014.11.18
# Last modified: 2014.11.19

# --------------------------------------------------
# Interest Tags.
# --------------------------------------------------

class InterestTagInline(admin.TabularInline):
	model = Event.interestTags.through
	extra = 1

class InterestTagAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['description']}),
		(None, {'fields': ['color']}),
	]
	
	list_display = ('description', 'color')
	search_fields = ['description', 'color']
	
# --------------------------------------------------
# Participants.
# --------------------------------------------------

class ParticipantsInline(admin.TabularInline):
	model = Event.participants.through
	extra = 1
	
class ParticipantsAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['reference','tagId']}),
		(None, {'fields': ['firstName','lastName']}),
		(None, {'fields': ['sex']}),
		(None, {'fields': ['interestTag']}),
	]
	
	list_display = ('reference', 'firstName', 'lastName', 'tagId', 'interestTag')
	search_fields = ['reference', 'interestTag__description', 'tagId', 'firstName', 'lastName']
	
# --------------------------------------------------
# Sensors.
# --------------------------------------------------

class SensorsInline(admin.TabularInline):
	model = Event.sensors.through
	extra = 1

class SensorsAdmin(admin.ModelAdmin):
	fieldsets = [
		('Sensor Identification', {'fields': ['identifier', 'description']}),
		('Properties', {'fields': ['x', 'y', 'displayable']}),
	]
	
# --------------------------------------------------
# Marker.
# --------------------------------------------------

class MarkersInline(admin.TabularInline):
	model = Marker
	extra = 1

class MarkersAdmin(admin.ModelAdmin):
	fieldsets = [
		('Marker information', {'fields': ['timeStamp', 'label', 'event']})
	]
	
# --------------------------------------------------
# Record.
# --------------------------------------------------
def delete_all_records(modeladmin, request, queryset):
	Record.objects.all().delete()
	
class RecordAdmin(admin.ModelAdmin):
	list_display = ('event', 'timeStamp', 'tagId')
	search_fields = ['event__name', 'timeStamp', 'tagId']
	actions = [delete_all_records]

# --------------------------------------------------
# Interactions.
# --------------------------------------------------
def delete_all_interactions(modeladmin, request, queryset):
	Interaction.objects.all().delete()
	
class InteractionAdmin(admin.ModelAdmin):
	list_display = ('event', 'tagId1', 'tagId2')
	search_fields = ['event__name',  'tagId1', 'tagId2']
	actions = [delete_all_interactions]
# --------------------------------------------------
# Events.
# --------------------------------------------------
# Associate all of the participants to this event
def event_association(modeladmin, request, queryset):
	participants = Participant.objects.all()
	for part in participants:
		for ev in queryset:
			ev.participants.add(part)
event_association.short_description = 'Associate all participants to selected events'

# Associate all of the participants with a name to this event
def event_association_name(modeladmin, request, queryset):
	participants = Participant.objects.exclude(firstName__isnull = True).exclude(lastName__isnull = True)
	for part in participants:
		for ev in queryset:
			ev.participants.add(part)
event_association_name.short_description = 'Associate all participants with a name to selected events'

class EventAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['name']}),
		(None, {'fields': ['startDate', 'stopDate']}),
	]

	inlines = [InterestTagInline, SensorsInline, MarkersInline, ParticipantsInline]
	list_display = ('name','__id__', 'startDate')
	search_fields = ['name', 'startDate']
	actions = [event_association, event_association_name]
	
admin.site.register(Event, EventAdmin)
admin.site.register(InterestTag, InterestTagAdmin)
admin.site.register(Participant, ParticipantsAdmin)
admin.site.register(Sensor, SensorsAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Marker, MarkersAdmin)