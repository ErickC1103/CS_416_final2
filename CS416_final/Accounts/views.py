from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout

from .forms import TicketForm
from .models import Event, WishlistItem
import requests




# Create your views here.

def index(request):#head to the main webpage
    return render(request,"ticket-master/index.html")
#view for registering accounts
def register_view(request):
    # This function renders the registration form page and creates a new user based on the form data
    if request.method == 'POST':
        # We use Django's UserCreationForm to create a new user.
        form = UserCreationForm(request.POST)

        # Check whether it's valid (for example checking password matching
        if form.is_valid():
            form.save()
            # Redirect the user to login page after successful registration
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'ticket-master/accounts/register.html', {'form': form})



#view for logging in
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        #checks for password and username match
        if form.is_valid():
            # Get the user info from the form data and log in the user
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'ticket-master/accounts/login.html', {'form': form})

#view for logging user out, would first make a confirmation page just in case
def logout_view(request):
    if(request.method == 'POST'):
        logout(request)
        return redirect('index')
    return render(request, 'ticket-master/accounts/logout.html')


#For crud use in wish lists

# obtain the event from json through the event id
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

#view that would obtain an event based on the event ID
def get_event_from_json(event_id):
    url = f'https://app.ticketmaster.com/discovery/v2/events/{event_id}.json?apikey=7s7IqRGZ56syvGLtkL5x5TeJv0HynG5n'
    #print(url)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    event = response.json()# event has json data
    eventid = event['id'] # event id

    image = find_best_image(event['images'])
    image_url = image['url'] if image else None # would find the best image possible
    #details dropped here
    event_details = {
        'id': eventid,
        'title': event['name'],
        'venue': event['_embedded']['venues'][0]['name'],
        'event_date': event['dates']['start'].get('localDate'),
        'status': event['dates']['status']['code'],
        'image' : image_url,
        'ticket_url': event['url'],
        'time': event['dates']['start'].get('localTime'),

    }
    print(event_details)
    return event_details





@login_required
def add_to_wishlist(request, event_id):
    # fetch event details from json
    event_data = get_event_from_json(event_id)
    if not event_data:
        # event not found in json
        return redirect('index')

    # save event in model if it doesn't exist yet, update the model in case
    event, created = Event.objects.update_or_create(
        id=event_data['id'],
        defaults={
            'title': event_data['title'],
            'date': event_data['event_date'],
            'time': event_data['time'],
            'ticket_url': event_data['ticket_url'],
            'location': event_data['venue'],
            'status': event_data.get('status', 'available'),
            'image_url': event_data['image'],
        }
    )

    # save wishlist item
    WishlistItem.objects.get_or_create(
        user=request.user,
        event=event
    )
    #head to the wishlist
    return redirect('wishlist')

#view for the wish list
@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('event') #obtain wishlist items
    return render(request, 'ticket-master/accounts/wishlist.html', {'items': items})
#view for removing the wish list
@login_required
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, user=request.user)#would make a 404 error if not found
    if(request.method == "POST"):
        item.delete()#deletes item from wishlist
        #head to wishlist
        return redirect('wishlist')

    return render(request, 'ticket-master/accounts/remove_item.html', {'item': item})


#view for updating ticket amount
@login_required
def update_tickets(request, item_id):
    wishlist_item = get_object_or_404(WishlistItem, id=item_id, user=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            return redirect('wishlist')
    else:
        form = TicketForm(instance=wishlist_item)

    return render(request, 'ticket-master/accounts/update_tickets.html', {'form': form, 'item': wishlist_item})


