from functools import wraps
import traceback

from django.conf import settings

from jsonit.http import JSONResponse


JSONIT_TRACEBACK = getattr(settings, "JSONIT_TRACEBACK", False)


def catch_ajax_exceptions(func):
    """
    Catches exceptions which occur when using an AJAX request.

    These exceptions will be returned using a :class:`JSONResponse` rather than
    letting the exception propogate.
    """

    @wraps(func)
    def dec(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception, e:
            if request.is_ajax():
                if JSONIT_TRACEBACK:
                    return JSONResponse(
                        request, exception=traceback.format_exc())
                else:
                    return JSONResponse(request, exception=e)
            raise

    return dec
