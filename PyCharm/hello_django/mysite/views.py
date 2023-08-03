from django.http.response import HttpResponse
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import QueryDict

from .views_auth import logged_in_or_basicauth


class HomeView(TemplateView):
    template_name = 'home.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("HomeView.get()...")
        params = self.get_params(request.GET)
        for k, v in params.items():
            print(k, ':', v)
        kwargs.update(params)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("HomeView.post()...")
        params = self.get_params(request.POST)
        for k, v in params.items():
            print(k, ':', v)
        kwargs.update(params)
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        print("HomeView.put()...")
        putParams = QueryDict(request.body)
        params = self.get_params(putParams)
        for k, v in params.items():
            print(k, ':', v)
        kwargs.update(params)
        return super().get(request, *args, **kwargs)

    def get_params(self, query):
        language = query.get('language', 'RUBY')
        framework = query.get('framework', 'RAILS')
        name = query.get('name', '홍길동')
        email = query.get('email', 'hong@gmail.com')
        url = query.get('url', 'http://google.co.kr')
        return {
            'language': language,
            'framework': framework,
            'name': name,
            'email': email,
            'url': url,
        }


@logged_in_or_basicauth(realm='ksh')
def auth_view(request):
    print("auth_view()...")
    return HttpResponse("This is Basic Auth Success Response.")


# def cookie_view(request):
#     print("cookie_view()...")
#     request.session.set_test_cookie()
#     return HttpResponse('This is set_test_cookie() Response.')


@csrf_exempt
def cookie_view_post(request):
    print("cookie_view_post()...")
    print("request.COOKIES:", request.COOKIES)
    print("request.session:", request.session.items())
    print("request.headers:", request.headers)

    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse(f"OK. Cookie received: {request.COOKIES}")
        else:
            return HttpResponse("NOK. Please enable Cookie and try again.")

    request.session.set_test_cookie()
    return HttpResponse("Django have set sessionid cookie.")
