import json
import os

import sentry_sdk
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


def profile(request, username):
    # User.DoesNotExist for anyone who is not in the db -> 500 -> Sentry
    user = User.objects.get(username=username)
    return JsonResponse({"user": user.username})


@csrf_exempt
def trigger(request):
    """Used by the playground dashboard: same crash, but tagged with a run id."""
    body = json.loads(request.body or "{}")
    run = body.get("run", "manual")
    with sentry_sdk.new_scope() as scope:
        client = None
        if body.get("dsn"):
            # dashboard "Use my DSN": this event goes to the visitor's project
            client = sentry_sdk.Client(dsn=body["dsn"], environment="playground", release=os.environ.get("RELEASE"))
            scope.set_client(client)
        scope.set_tag("run_id", run)
        if body.get("fresh", True):
            scope.fingerprint = ["{{ default }}", run]
        try:
            profile(request, f"ghost-{run}")
        except User.DoesNotExist as exc:
            event_id = sentry_sdk.capture_exception(exc)
        if client:
            client.flush(5)
            client.close()
    sentry_sdk.flush(5)
    return JsonResponse({"event_id": event_id})


urlpatterns = [
    path("profile/<str:username>/", profile),
    path("trigger", trigger),
]
