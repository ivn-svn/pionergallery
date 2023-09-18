from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from pioner_gallery.mediaplanner import views as mediaplannerviews

urlpatterns = [
    path('media_planner/', mediaplannerviews.media_planner, name='media_planner'),
    path('event/<int:event_id>/', mediaplannerviews.event_detail, name='event_detail'),
    path('calendar/', mediaplannerviews.calendar_view, name='calendar_view'),
    path('calendar_horizontal/', mediaplannerviews.calendar_horizontal, name='calendar_horizontal'),
    path('calendar_vertical/', mediaplannerviews.calendar_vertical, name='calendar_vertical'),
    path('calendar_data/', mediaplannerviews.calendar_data, name='calendar_data'),
    path('delete_event/<int:event_id>/', mediaplannerviews.delete_event, name='delete_event'),
    path('edit_event/<int:event_id>/', mediaplannerviews.edit_event, name='edit_event'),
    path('map/', mediaplannerviews.map, name='map'),
    # path('edit_marker/<int:marker_id>/', mediaplannerviews.edit_marker, name='edit_marker'),
    # path('delete_marker/<int:marker_id>/', mediaplannerviews.delete_marker, name='delete_marker'),
    path('add_marker/', mediaplannerviews.add_marker, name='add_marker'),
    path('social_graph/', mediaplannerviews.social_graph, name='social_graph'),
]
