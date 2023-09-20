from django.shortcuts import render
from pioner_gallery.mediaplanner.models import Event
from pioner_gallery.mediaplanner.forms import EventForm
from django.urls import reverse
from django.http import JsonResponse
from .models import Event
from django.shortcuts import redirect, get_object_or_404
import os
import folium
from folium import plugins
import rioxarray as rxr
import earthpy as et
import earthpy.spatial as es
from .models import Marker
from django.views.decorators.csrf import csrf_exempt

from .. import settings


def map(request):
    # Import data from EarthPy
    data = et.data.get_data('colorado-flood')

    # Set working directory to earth-analytics
    os.chdir(os.path.join(et.io.HOME, 'earth-analytics', 'data'))

    # Create a map using the Map() function and the coordinates for Boulder, CO
    m = folium.Map(location=[45, 13])

    # Add static marker to the map


    # Add static marker to the map
    # icon = folium.CustomIcon(
    #     icon_image='https://www.toledoblade.com/image/2013/09/13/1140x_a10-7_cTC/Colorado-Flooding-11.jpg',
    #     icon_size=(50, 50))
    # static_marker = folium.Marker(location=[40.0150, -105.2705], icon=icon)
    # static_marker.add_to(m)

    # Add dynamic markers from the database to the map
    all_markers = Marker.objects.all()
    for marker in all_markers:
        if marker.image and marker.image.url:
            icon_url = request.build_absolute_uri(marker.image.url)  # Build the full URL using request object
        else:
            icon_url = 'https://www.toledoblade.com/image/2013/09/13/1140x_a10-7_cTC/Colorado-Flooding-11.jpg'
        custom_icon = folium.CustomIcon(icon_image=icon_url, icon_size=(150, 150))

        mkr = folium.Marker(location=[marker.latitude, marker.longitude], icon=custom_icon)
        mkr.add_to(m)

    # Convert the map to HTML string after adding all elements
    map_html = m._repr_html_()

    return render(request, 'pioner_gallery\map.html', {'map': map_html})


@csrf_exempt
def add_marker(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        image = request.FILES.get('image')

        # Assuming category is optional for now
        marker = Marker(latitude=latitude, longitude=longitude, image=image)
        marker.save()

        return JsonResponse({'status': 'success', 'marker_id': marker.id})

def social_graph(request):

    return render(request, 'pioner_gallery/socialgraph.html')
def media_planner(request):
    events = Event.objects.all()
    for event in events:
        event.shareable_link = request.build_absolute_uri(reverse('event_detail', args=[event.id]))
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            form = EventForm()  # Reset the form
        else:
            print("Form is not valid")
            print(form.errors)

    return render(request, 'pioner_gallery/media_planner.html', {'events': events, 'form': form})


def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('media_planner')
    else:
        form = EventForm(instance=event)
    return render(request, 'pioner_gallery/media_planner.html', {'form': form, 'edit_mode': True})


def delete_event(request, event_id):
    if request.method == 'POST':  # Ensure that it's a POST request
        event = get_object_or_404(Event, pk=event_id)  # Get the event or 404 if not found
        event.delete()
        return redirect('media_planner')  # Redirect back to the main media planner view after deletion


def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'pioner_gallery/event_details.html', {'event': event})


def events_list(request):
    events = Event.objects.all()
    for event in events:
        event.shareable_link = request.build_absolute_uri(reverse('event_detail', args=[event.id]))
    return render(request, 'pioner_gallery/events_list.html', {'events': events})


def calendar_view(request):
    return render(request, 'pioner_gallery/calendar.html')


def calendar_horizontal(request):
    return render(request, 'pioner_gallery/calendar_horizontal.html')


def calendar_vertical(request):
    return render(request, 'pioner_gallery/calendar_vertical.html')


def calendar_data(request):
    events = Event.objects.all()
    event_list = [event.to_json() for event in events]
    return JsonResponse(event_list, safe=False)
