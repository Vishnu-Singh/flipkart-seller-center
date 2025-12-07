from django.urls import path
from .views import (
    DocumentationHomeView, SetupGuideView, APIDocumentationView,
    ChangelogView, QuickStartView, APIReferenceView, TroubleshootingView
)

app_name = 'documentation'

urlpatterns = [
    path('', DocumentationHomeView.as_view(), name='home'),
    path('setup/', SetupGuideView.as_view(), name='setup'),
    path('quick-start/', QuickStartView.as_view(), name='quick_start'),
    path('api/<str:app_name>/', APIDocumentationView.as_view(), name='api_docs'),
    path('api-reference/', APIReferenceView.as_view(), name='api_reference'),
    path('changelog/', ChangelogView.as_view(), name='changelog'),
    path('troubleshooting/', TroubleshootingView.as_view(), name='troubleshooting'),
]
