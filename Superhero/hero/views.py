from pathlib import Path
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from csv import reader

from .models import Superhero
from .models import Article

class HeroListView(ListView):
    template_name = 'hero/list.html'
    model = Superhero


class HeroDetailView(DetailView):
    template_name = 'hero/detail.html'
    model = Superhero


class HeroCreateView(LoginRequiredMixin, CreateView):
    template_name = "hero/add.html"
    model = Superhero
    fields = '__all__'


class HeroUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "hero/edit.html"
    model = Superhero
    fields = '__all__'


class HeroDeleteView(LoginRequiredMixin, DeleteView):
    model = Superhero
    template_name = 'hero/delete.html'
    success_url = reverse_lazy('hero_list')

class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = "article_add.html"
    model = Article
    fields = '__all__'

    def form_valid(self, form):
        form.instance.hero = self.request.user
        return super().form_valid(form)
    
class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "article_edit.html"
    model = Article
    fields = '__all__'

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class UserHomeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_anonymous:
            return '/article/'
        return f'/hero/{get_me(self.request.user).pk}'

    def get_me(user):
        return Article.objects.get_or_create(user=user)[0]
    
class ArticleListView(ListView):
    template_name = "article/list.html"
    model = Article
    context_object_name = "articles"

class ArticleDetailView(DetailView):
    template_name = "article/detail.html"
    model = Article
    context_object_name = "article"

class ArticleUpdateView(UpdateView):
    template_name = "article/edit.html"
    model = Article
    fields = "__all__"


class ArticleDeleteView(DeleteView):
    model = Article
    template_name = "article/delete.html"
    success_url = reverse_lazy("article_list")

class CardView(TemplateView):
    template_name = 'card.html'

    def get_context_data(self, **kwargs):
        title = Superhero
        body = Article
        return dict(title=title, body=body, color='bg-primary', width='col')
    
class CardsView(TemplateView):
    template_name = 'cards.html'

    def get_context_data(self, **kwargs):
        return dict(cards=cards_data())
    
class DocumentView(TemplateView):
    template_name = 'document.html'

    def get_context_data(self, **kwargs):
        document = self.kwargs.get('doc')
        path = Path('Documents')/document
        markdown_text = markdown(path.read_text())
        return dict(text=markdown_text)
    
class TableView(TemplateView):
    template_name = 'table.html'

    def get_context_data(self, **kwargs):
        table = reader(open('Documents/lessons.csv'))
        return dict(title='Lessons Schedule',
                    table=table)
    
class PageView(TemplateView):
    def get_template_names(self):
        page = self.kwargs.get('page', 'index')
        return f'{page}.html'
    
class TabsView(TemplateView):
    template_name = 'tabs.html'

    def get_context_data(self, **kwargs):
        return dict(title='Tab View', tabs=tabs_data())

    def tabs_data():
        def options(i, tab, selected):
            data = tab
            if selected:
                data.update(dict(name=f'tab{i}', active='active', 
                    show='show', selected='true'))
            else:
                data.update(dict(name=f'tab{i}', active='', 
                    show='', selected='false'))
            return data

        def set_options(tabs):
            return [options(i, tab, i == 0) for i, tab in enumerate(tabs)]

        panels = [
                card_data(title="Tab 1", body='panel 1'),
                card_data(title="Tab 2", body='panel 2'),
                card_data(title="Tab 3", body='panel 3'),
            ]
        return set_options(panels)
    
class AccordionView(TemplateView):
    template_name = 'accordion.html'

    def get_context_data(self, **kwargs):
        return dict(accordion=accordion_data())
    
    def accordion_data():
        def create_card(i):
            return f'<h2>Lessons (week {i})</h2><p>...</p>'
        def card_content(i, active):
            card = card_data(f'Week {i+1}', create_card(i+1))
            if i == active:
                card.update(dict(id=i, collapsed='', show='show', aria='true'))
            else:
                card.update(dict(id=i, collapsed='collapsed', show='', aria='false'))
            return card
        return [card_content(i, 11) for i in range(12)]
    
class SuperView(TemplateView):
    template_name = 'super.html'

    def get_context_data(self, **kwargs):
        return dict(table=create_table())