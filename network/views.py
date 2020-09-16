from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("(Network) Homepage.")

def story_index(request):
    return HttpResponse("Story Homepage.")
