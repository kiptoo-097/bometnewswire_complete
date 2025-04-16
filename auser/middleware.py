class CrawlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        crawlers = [
            'facebookexternalhit/1.1',
            'facebookexternalhit/1.0',
            'Facebot',
            'Twitterbot',
        ]
        
        if any(crawler in user_agent for crawler in crawlers):
            request._dont_enforce_csrf_checks = True
            if request.method == 'HEAD':
                from django.http import HttpResponse
                return HttpResponse()
        
        return self.get_response(request)