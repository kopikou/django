from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from artists.models import Artist


# Create your views here.
#def show_artists(request):
    #artists = Artist.objects.all()

    #result = ""
    #for a in artists:
        #result += a.name + "<br>"

    #return HttpResponse(result)

class ShowArtistsView(TemplateView):
    template_name = "artists/show_artists.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()

        return context
    