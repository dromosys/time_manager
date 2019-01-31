import pytz

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

class TimezoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        
        #if 'django_timezone' not in request.session:
        #    print("middlware.django_timezone not set")  
        #else :
        #    print("middlware.get_timezone", request.session['django_timezone'])    
        
        tzname = request.session.get('django_timezone')
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()