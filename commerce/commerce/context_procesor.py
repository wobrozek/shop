from django.contrib.auth.decorators import login_required

def global_context(request):
    try:
        watchlist=request.user.watchlist.all()
        return {"follow_number":len(watchlist)}
    except:
        return {"follow_number":0}
