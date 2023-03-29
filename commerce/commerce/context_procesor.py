from django.contrib.auth.decorators import login_required

def global_context(request):
    watchlist=request.user.watchlist.all().count()
    return {"follow_number":watchlist}
