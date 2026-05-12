import threading

# Thread-local storage for request
_thread_locals = threading.local()


def get_current_request():
    """Get the current request object."""
    return getattr(_thread_locals, 'request', None)


def get_current_user():
    """Get the current user from the request."""
    request = get_current_request()
    if request:
        return getattr(request, 'user', None)
    return None


class RequestMiddleware:
    """Middleware to store the current request in thread-local storage."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        _thread_locals.request = request
        try:
            response = self.get_response(request)
        finally:
            # Clean up thread-local storage
            _thread_locals.request = None
        return response
