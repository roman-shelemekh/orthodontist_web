from .forms import SearchForm

def search_form(request):
    searchform = SearchForm(request.GET)
    return {'searchform': searchform}