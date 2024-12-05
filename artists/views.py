from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from artists.models import Artist

from django.shortcuts import render
from django.template import RequestContext
 
 


class ShowArtistsView(TemplateView):
    template_name = "artists/show_artists.html"

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['artists'] = Artist.objects.all()

        return context
    