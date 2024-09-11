from django.views.generic import TemplateView

class HulkView(TemplateView):
    template_name = 'hero.html'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Hulk',
            'body': 'Bruce Banner',
            'image': '/static/images/hulk.jpg'
        }
    
class IronManView(TemplateView):
    template_name = 'hero.html'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Iron Man',
            'body': 'Tony Stark',
            'image': '/static/images/iron_man.jpg'
        }
    
class BlackWidowView(TemplateView):
    template_name = 'hero.html'

    def get_context_data(self, **kwargs):
        return {
            'title': 'Black Widow',
            'body': 'Natasha Romanova',
            'image': '/static/images/black_widow.jpg'
        }
    
class IndexView(TemplateView):
    template_name = 'heroes.html'