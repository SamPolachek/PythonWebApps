from django.views.generic import TemplateView

# Create your views here.
class PhotoView(TemplateView):
    template_name = 'photo.html'
    