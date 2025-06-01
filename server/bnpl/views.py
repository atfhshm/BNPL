from django.http import HttpRequest, JsonResponse


def root(request: HttpRequest) -> JsonResponse:
    site_url: str = request.get_host()
    info = {
        'name': 'BNPL',
        'version': '1.0.0',
        'description': 'BNPL API',
        'urls': {
            'admin': f'{site_url}/admin/',
            'silk': f'{site_url}/silk/',
            'api': f'{site_url}/api/v1/',
            'swagger': f'{site_url}/api/v1/swagger/',
            'redoc': f'{site_url}/api/v1/redoc/',
        },
    }
    return JsonResponse({'message': 'Hello, World!', 'info': info})
