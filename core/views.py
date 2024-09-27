from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import *
from .football import get_football_fixtures
from .tennis import get_tennis_fixtures, get_ATP_list
from .formula1 import get_F1_race_details, get_F1_driver_standings, get_F1_last_race_results
from .lol import get_LoL_fixtures
import traceback
from django.views import View
from django.views.generic import TemplateView
import json

# football view
class FootballView(View):
    template_name = 'football.html'
    form_class = ClubForm

    def get(self, request):
        form = self.form_class
        # display the clubs saved in the session
        session_list = request.session.get('session_list_football')
        if session_list == None:
            context = {
                "form":form
            }
        else:
            all_fixtures, session_list = get_football_fixtures(None, session_list)

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
                    all_fixtures, session_list = get_football_fixtures(club_name, request.session.get('session_list_football'))
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
    form_class = PlayerForm

    def get(self, request):
        form = self.form_class
        atp_list = get_ATP_list()
        # display the players saved in the session
        session_list = request.session.get('session_list_tennis')
        if session_list == None:
            context = {
                "form":form,
                "atp_list": json.dumps(atp_list)
            }
        else:
            all_fixtures, session_list = get_tennis_fixtures(None, session_list)
            context = {
                "form": form,
                "all_fixtures" : all_fixtures[::-1], #reverse order so the last searched club is displayed first
                "atp_list": json.dumps(atp_list)
            }

        return render(request, self.template_name, context)
    
    def post(self, request):
        atp_list = get_ATP_list()
        action = request.POST.get('action')
        if action == 'get_fixtures':
            form = self.form_class(request.POST)
            if form.is_valid():
                player_name = form.cleaned_data['player_name']
                try:
                    #  get all fixtures, and the IDs list to update the session data
                    all_fixtures, session_list = get_tennis_fixtures(player_name, request.session.get('session_list_tennis'))
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
        context['next_race_details'] = get_F1_race_details()
        context['last_race_results'] = get_F1_last_race_results()
        context['driver_standings'] = get_F1_driver_standings()
        return context

# league of legends view
class LeagueOfLegendsView(View):
    template_name = 'lol.html'
    form_class = LolClubForm

    def get(self, request):
        form = self.form_class
        # display the clubs saved in the session
        session_list = request.session.get('session_list_lol')
        if session_list == None:
            context = {
                "form":form
            }
        else:
            all_fixtures, session_list = get_LoL_fixtures(None, session_list)

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
                    all_fixtures, session_list = get_LoL_fixtures(club_name, request.session.get('session_list_lol'))
                    request.session['session_list_lol'] = session_list
                    context = {
                        "form": form,
                        "all_fixtures" : all_fixtures[::-1] #reverse order so the last searched club is displayed first
                    }
                    return render(request, self.template_name, context)
                except Exception as e:
                    print(traceback.format_exc())
                    messages.error(request, 'Fixtures could not be retrieved, please check spelling.')
                    return redirect('lol')

            # if not valid, refresh page
            return redirect('lol')
        
        # clear the session data, and return an empty form
        elif action == 'clear_results':
            try:
                del request.session["session_list_lol"]
            except KeyError:
                pass
            return redirect('lol')

# valorant view
class ValorantView(View):
    template_name = 'valorant.html'
    def get(self, request):
        context = {}
        return render(request, self.template_name, context)