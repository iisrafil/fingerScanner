from django.shortcuts import redirect;
from django.http import HttpResponse;

def authenticated_already(view_func):
    def wrapper_func(req, *args, **kwargs):
        if req.user.is_authenticated:
            return redirect("home");
        return view_func(req, *args, **kwargs);
    return wrapper_func;

def allowed_users(roles: set={}):
    def decorator(view_func):
        def wrapper_func(req, *args, **kwargs):
            grp = {x.name for x in req.user.groups.all()};
            # print(grp);
            if not (bool(roles.intersection(grp)) ^ bool(grp)):
                return view_func(req, *args, **kwargs);
            else: return HttpResponse("""
                <h1>access denied</h1>
                <a href="/front/">home</a>
            """)
        return wrapper_func;
    return decorator;