from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from .football import getFootballFixtures
from .tennis import getTennisFixtures, getATPList
from .formula1 import getF1RaceDetails, getF1DriverStandings, getF1LastRaceResults
import traceback
from django.views import View
from django.views.generic import TemplateView
import json

# football view
class FootballView(View):
    template_name = 'football.html'
    form_class = clubForm

    def get(self, request):
        form = self.form_class
        # display the clubs saved in the session
        session_list = request.session.get('session_list_football')
        if session_list == None:
            context = {
                "form":form
            }
        else:
            all_fixtures, session_list = getFootballFixtures(None, session_list)

            context = {
                "form": form,
                "all_fixtures" : all_fixtures[::-1] #reverse order so the last searched club is displayed first
            }

        return render(request, self.template_name, context)
    
    def post(self, request):
        action = request.POST.get('action')
        # check for which button has been pressed
        if action == 'get_fixtures':
            form = self.form_class(request.POST)

            if form.is_valid():
                club_name = form.cleaned_data['club_name']
                try:
                    # get all fixtures, and the IDs list to update the session data
                    all_fixtures, session_list = getFootballFixtures(club_name, request.session.get('session_list_football'))
                    request.session['session_list_football'] = session_list
                    context = {
                        "form": form,
                        "all_fixtures" : all_fixtures[::-1] #reverse order so the last searched club is displayed first
                    }
                    return render(request, self.template_name, context)
                except Exception as e:
                    print(traceback.format_exc())
                    messages.error(request, 'Fixtures could not be retrieved, please check spelling.')
                    return redirect('football')

            # if not valid, refresh page
            return redirect('football')
        
        # clear the session data, and return an empty form
        elif action == 'clear_results':
            try:
                del request.session["session_list_football"]
            except KeyError:
                pass
            return redirect('football')
    
    # removes a fixtures table from the session
    def delete(self, request):
        data = json.loads(request.body)
        try:
            session_list = request.session["session_list_football"]
            list_size = len(session_list)
            # fixtures displayed in the template are reversed
            session_list.pop(list_size-data['table_no'])
            request.session.modified = True
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

# tennis view
class TennisView(View):
    template_name = 'tennis.html'
    form_class = playerForm

    def get(self, request):
        form = self.form_class
        atp_list = getATPList()
        # display the players saved in the session
        session_list = request.session.get('session_list_tennis')
        if session_list == None:
            context = {
                "form":form,
                "atp_list": json.dumps(atp_list)
            }
        else:
            all_fixtures, session_list = getTennisFixtures(None, session_list)
            context = {
                "form": form,
                "all_fixtures" : all_fixtures[::-1], #reverse order so the last searched club is displayed first
                "atp_list": json.dumps(atp_list)
            }

        return render(request, self.template_name, context)
    
    def post(self, request):
        atp_list = getATPList()
        action = request.POST.get('action')
        if action == 'get_fixtures':
            form = self.form_class(request.POST)
            if form.is_valid():
                player_name = form.cleaned_data['player_name']
                try:
                    #  get all fixtures, and the IDs list to update the session data
                    all_fixtures, session_list = getTennisFixtures(player_name, request.session.get('session_list_tennis'))
                    request.session['session_list_tennis'] = session_list
                    context = {
                        "form": form,
                        "all_fixtures" : all_fixtures[::-1], #reverse order so the last searched club is displayed first
                        "atp_list": json.dumps(atp_list)
                        
                    }
                    return render(request, self.template_name, context)
                
                except Exception as e:
                    print(traceback.format_exc())
                    messages.error(request, 'Fixtures could not be retrieved, please check spelling.')
                    return redirect('tennis')
                
            # if not valid, refresh page
            return redirect('tennis')
        
        # clear the session data, and return an empty form
        elif action == 'clear_results':
            try:
                del request.session["session_list_tennis"]
            except KeyError:
                pass
            return redirect('tennis')
            
    # removes a fixtures table from the session
    def delete(self, request):
        data = json.loads(request.body)
        try:
            session_list = request.session["session_list_tennis"]
            list_size = len(session_list)
            # fixtures displayed in the template are reversed
            session_list.pop(list_size-data['table_no'])
            request.session.modified = True
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=500)

# formula 1 view
class Formula1View(TemplateView):
    template_name = 'formula1.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next_race_details'] = getF1RaceDetails()
        context['starting_grid'] = 'grid'
        context['last_race_results'] = getF1LastRaceResults()
        context['driver_standings'] = getF1DriverStandings()
        return context

# league of legends view
class LeagueOfLegendsView(View):
    template_name = 'lol.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)

# valorant view
class ValorantView(View):
    template_name = 'valorant.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)