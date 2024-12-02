from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import csv

from .models import Season, Highlight, Match
from .forms import MatchForm, HighlightForm, SeasonForm


# Page des saisons : statistiques cumulées
def seasons(request):
    seasons = Season.objects.all()
    data = []

    for season in seasons:
        total_points = sum(match.points for match in season.matches.all())
        total_assists = sum(match.assists for match in season.matches.all())
        total_rebounds = sum(match.rebounds for match in season.matches.all())
        total_steals = sum(match.steals for match in season.matches.all())
        total_blocks = sum(match.blocks for match in season.matches.all())
        total_turnovers = sum(match.turnovers for match in season.matches.all())
        avg_points = total_points / season.matches.count() if season.matches.count() > 0 else 0

        data.append({
            "season": season,
            "total_points": total_points,
            "total_assists": total_assists,
            "total_rebounds": total_rebounds,
            "total_steals": total_steals,
            "total_blocks": total_blocks,
            "total_turnovers": total_turnovers,
            "avg_points": avg_points,
        })

    return render(request, 'seasons.html', {"data": data})


# Export des matchs en PDF
def export_matches_pdf(request):
    matches = Match.objects.all()
    html_string = render_to_string('matches_pdf.html', {'matches': matches})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="matches.pdf"'
    response.write(html.write_pdf())
    return response


# Export des matchs en CSV
def export_matches_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="matches.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Adversaire', 'Points', 'Assists', 'Rebounds', 'Steals', 'Blocks', 'Turnovers'])

    matches = Match.objects.all()
    for match in matches:
        writer.writerow([match.date, match.opponent, match.points, match.assists, match.rebounds, match.steals, match.blocks, match.turnovers])

    return response


# Page des moments forts (highlights)
def highlights(request):
    highlights = Highlight.objects.all()
    return render(request, 'highlights.html', {"highlights": highlights})


# Formulaire pour créer ou éditer un match
def match_form(request, match_id=None):
    match = get_object_or_404(Match, id=match_id) if match_id else None

    if request.method == 'POST':
        form = MatchForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MatchForm(instance=match)

    return render(request, 'match_form.html', {'form': form})


# Formulaire pour créer ou éditer un moment fort
def highlight_form(request, highlight_id=None):
    highlight = get_object_or_404(Highlight, id=highlight_id) if highlight_id else None

    if request.method == 'POST':
        form = HighlightForm(request.POST, request.FILES, instance=highlight)
        if form.is_valid():
            form.save()
            return redirect('highlights')
    else:
        form = HighlightForm(instance=highlight)

    return render(request, 'highlight_form.html', {'form': form})


# Formulaire pour créer ou éditer une saison
def season_form(request, season_id=None):
    season = get_object_or_404(Season, id=season_id) if season_id else None

    if request.method == 'POST':
        form = SeasonForm(request.POST, instance=season)
        if form.is_valid():
            form.save()
            return redirect('seasons')
    else:
        form = SeasonForm(instance=season)

    return render(request, 'season_form.html', {'form': form})


# Dashboard des performances avec filtres
def dashboard(request):
    matches = Match.objects.all()

    # Filtres
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    opponent = request.GET.get('opponent')
    min_points = request.GET.get('min_points')
    max_points = request.GET.get('max_points')

    if date_from:
        matches = matches.filter(date__gte=date_from)
    if date_to:
        matches = matches.filter(date__lte=date_to)
    if opponent:
        matches = matches.filter(opponent__icontains=opponent)
    if min_points:
        matches = matches.filter(points__gte=min_points)
    if max_points:
        matches = matches.filter(points__lte=max_points)

    return render(request, 'dashboard.html', {'matches': matches})
