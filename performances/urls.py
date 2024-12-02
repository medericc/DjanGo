from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('seasons/', views.seasons, name='seasons'),
    path('highlights/', views.highlights, name='highlights'),
    path('match/add/', views.match_form, name='add_match'),
    path('match/edit/<int:match_id>/', views.match_form, name='edit_match'),
    path('highlight/add/', views.highlight_form, name='add_highlight'),
    path('highlight/edit/<int:highlight_id>/', views.highlight_form, name='edit_highlight'),
    path('season/add/', views.season_form, name='add_season'),
    path('export/csv/', views.export_matches_csv, name='export_csv'),
path('export/pdf/', views.export_matches_pdf, name='export_pdf'),

    path('season/edit/<int:season_id>/', views.season_form, name='edit_season'),
]
