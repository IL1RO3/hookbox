from time import perf_counter
from datetime import timedelta

class RequestDurationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = perf_counter()
        response = self.get_response(request)
        duration_ms = (perf_counter() - start) * 1000
        response["X-Request-Duration"] = f"{duration_ms:.2f} ms"

        if hasattr(request, "request_log"):
            request.request_log.request_duration = timedelta(
                milliseconds=duration_ms
            )
            request.request_log.save(
                update_fields=["request_duration"]
            )

        return response 
