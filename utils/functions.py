from django.http import HttpResponse

def make_response(status=200, content_type="text/plain", content=None):
    response = HttpResponse()
    response.status_code = status
    response['Content-Type'] = content_type
    response.content = content
    return response
