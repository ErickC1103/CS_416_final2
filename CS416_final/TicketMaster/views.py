from contextlib import nullcontext

from django.shortcuts import render,redirect
import requests
from django.contrib import messages
from datetime import datetime
from .models import Viewer



def find_best_image(images):
    if not images:
        return None
    best_image = images[0]
    for image in images:
        if ('ratio' in image and 'fallback' in image and 'width' in image):
         if image['ratio'] == "16_9" and not image['fallback'] and image['width'] >= 1024:
             best_image = image
             break


    return best_image
def index(request):

    if request.method == "POST":
        genre = request.POST['genre']
        city = request.POST['city']

        if not genre or not city:
            messages.info(request, 'Both number of users and gender are required fields.')
            return redirect('index')
        events = get_events(genre, city)
        if events is None:
            messages.info(request, 'Could not find an event, please try another search.')
            return redirect('index')

        else:
            #print(events)
            if request.user.is_authenticated:
                Viewer.objects.create(viewer=request.user, searches=genre + " " + city)
            event_total = events['_embedded']['events']
            event_list = []
            for event in event_total:
                title = event['name']
                eventid = event['id']

                if 'images' in event:
                    image_url = find_best_image(event['images'])['url']
                else:
                    image_url = None

                venue = event['_embedded']['venues'][0]['name']

                city = event['_embedded']['venues'][0]['city']['name']

                state = event['_embedded']['venues'][0]['state']['name']

                address = event['_embedded']['venues'][0]['address']['line1']

                ticket_link = event['url']


                event_starting_info = event['dates']['start']

                if 'localDate' in event_starting_info:
                    raw_date = event_starting_info['localDate']
                    event_date = datetime.strptime(raw_date[:10], '%Y-%m-%d')
                    event_date = datetime.strftime(event_date, '%a %b %d %Y')
                else:
                    raw_date = None
                    event_date = None
                if 'localTime' in event_starting_info:
                    raw_time = event_starting_info['localTime']
                    event_time = datetime.strptime(raw_time[:5], '%H:%M')
                    event_time = datetime.strftime(event_time, '%#I:%M%p')
                else:
                    raw_time = None
                    event_time = None
                #end of for




                #print(title)
                event_details = {
                    'title': title,
                    'id': eventid,
                    'image': image_url,
                    'venue': venue,
                    'city': city,
                    'state': state,
                    'address': address,
                    'ticket_link': ticket_link,
                    'event_date': event_date,
                    'event_time': event_time,
                }
                print(event_details)
                event_list.append(event_details)
            context = {'events': event_list}
            return render(request,'ticket-master/index.html',context)
    return render(request,'ticket-master/index.html')








def get_events(genre, city):
    try:
        url = 'https://app.ticketmaster.com/discovery/v2/events.json?countryCode=US&apikey=7s7IqRGZ56syvGLtkL5x5TeJv0HynG5n'
        parameters = {
            'classificationName': genre,
            'city': city,
            'sort': 'date,asc'
        }
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()
        if data['page']['totalElements'] == 0:
            return None
        return data
    except requests.exceptions.RequestException as e:
        print('Error in getting events')
        return None









