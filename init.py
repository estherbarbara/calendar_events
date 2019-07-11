from flask import Flask, render_template, json, request, jsonify
from datetime import datetime
import os.path

#Class representation of an event
class Event:
    def __init__(self, start_hour, start_min, end_hour, end_min, width=288, color="blue"):
        self.start_hour = start_hour
        self.start_min = start_min
        self.end_hour = end_hour
        self.end_min = end_min
        self.width = width
        self.color = color

    def set_width(self, width):
    	self.width = width

    def set_color(self, color):
    	self.color = color

    def start_time(self):
    	h = self.start_hour
    	m = self.start_min
    	return ("0" if h < 10 else "") + str(h) + ":" + ("0" if m < 10 else "") + str(m)

    def end_time(self):
    	h = self.end_hour
    	m = self.end_min
    	return ("0" if h < 10 else "") + str(h) + ":" + ("0" if m < 10 else "") + str(m)

class Hour:
    def __init__(self, hour_str, events):
        self.hour_str = hour_str
        self.events = events

class Day:
    def __init__(self, events):
    	hours = []
    	i=0
    	while i<24 :
            hour_events = []
            for event in events :
                ev_start = event.start_hour + (event.start_min/100)
                ev_end = event.end_hour + (event.end_min/100)
                if ev_start >= i/2 and ev_end <= i/2 :
                    hour_events.append(event.color)
            hours.append( Hour( (("0" if i < 10 else "") + str(int(i)) + ":" + ( "30" if i-int(i)==0.5 else "00" ) ), hour_events) )
            i=i+0.5
        self.hours = hours
def count_collision_events(events, index):
    event = events[index]
    i = 0
    collision_counter = 1
    while i < len(events) :
        if i != index : #doesnt consider the event in question
        #put in float variables the hour and minutes to compare
            looped_hour_start = events[i].start_hour + (events[i].start_min/100)
            looped_hour_end = events[i].end_hour + (events[i].end_min/100)
            current_ev_start = event.start_hour + (event.start_min/100)
            current_ev_end = event.end_hour + (event.end_min/100)
            #looped event start after the event_x start and start before event_x ends
            #or looped event ends after the event_x start and ends before event_x ends
            if ( looped_hour_start > current_ev_start and looped_hour_start < current_ev_end ) or ( looped_hour_end > current_ev_start and looped_hour_end < current_ev_end ) : 
                collision_counter = collision_counter + 1
        i = i + 1
    return collision_counter


app = Flask(__name__)

@app.route('/calendar/', methods=['GET'])
def home():
    #Initial empty game
    events = []
    event = Event(9, 0, 15, 30)
    events.append(event)
    event = Event(9, 0, 14, 30)
    events.append(event)
    event = Event(9, 30, 11, 30)
    events.append(event)
    event = Event(11, 30, 12, 00)
    events.append(event)
    event = Event(14, 30, 15, 0)
    events.append(event)
    event = Event(15, 30, 16, 0)
    events.append(event)

    colors = ["blue", "green", "red", "navy", "purple", "pink"]
    index = 0
    while index < len(events) :
        event = events[index]
        coll = count_collision_events(events,index)
        event.set_width( event.width/coll )
        index = index + 1
        #event.set_color( colors[i] )

    #A calendar day
    day = Day(events)

    return render_template('main.html', day=day)
