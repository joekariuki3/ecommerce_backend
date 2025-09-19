from django.http import HttpResponse

def landing_page(request):
    return HttpResponse("""
        <h1>Welcome to E-commerce API</h1>
        <p>View the <a href='/swagger/'>Swagger Documentation</a> or <a href='/redoc/'>Redoc Documentation</a>.</p>
    """)