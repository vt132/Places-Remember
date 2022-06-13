from django.shortcuts import render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from requests import request

from memories import models

class MemoriesListView(ListView):
    model = models.Memories
    template_name = "memories_list.html"
    context_object_name = 'mem_list'
    
    def get_queryset(self):
        queryset = super(MemoriesListView, self).get_queryset()
        return queryset.filter(user = self.request.user)

    def get_context_data(self):
        uid = self.request.user.social_auth.get(provider='facebook').uid
        queryset = models.Memories.objects.all()
        queryset = queryset.filter(user = self.request.user)
        context = {
            'qs':queryset,
            'uid':uid,
        }
        return context
   

class MemoriesDetailView(DetailView):
    model = models.Memories

class MemoriesCreateView(SuccessMessageMixin,CreateView):
    model = models.Memories
    fields =['name', 'position', 'desc']
    template_name = "memories_create.html"
    success_message = 'Memories create successfully'
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.save()
        return super(MemoriesCreateView, self).form_valid(form)
    def get_success_url(self):
        return reverse('list_view')
        

class MemoriesUpdateView(SuccessMessageMixin, UpdateView):
    model = models.Memories
    fields =['name', 'position', 'desc']
    success_message = 'Memories update successfully'


class MemoriesDeleteView(SuccessMessageMixin, DeleteView):
    model = models.Memories
    success_url = reverse_lazy('list_mem')

def default_map(request):
    # TODO: move this token to Django settings from an environment variable
    # found in the Mapbox account settings and getting started instructions
    # see https://www.mapbox.com/account/ under the "Access tokens" section
    mapbox_access_token = 'pk.eyJ1IjoidnRoMTMyIiwiYSI6ImNrcXhhMDV4YTA5cGgyb21yNzI2dnU0dHkifQ.dPa7Yjpa9pM3ddEimTXy3w'
    return render(request, 'memcreate.html', 
                  { 'mapbox_access_token': mapbox_access_token })