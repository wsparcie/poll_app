from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path('list/', views.polls_list, name='list'),
    path('add/', views.polls_add, name='add'),
    path('delete/<int:poll_id>/', views.polls_delete, name='delete_poll'),
    path('end/<int:poll_id>/', views.end_poll, name='end_poll'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),
    path('poll/<int:poll_id>/answers/', views.poll_answer, name='poll_answer'),
    path('poll/<int:poll_id>/generate-token/', views.generate_token, name='generate_token'),
    path('poll/<int:poll_id>/tokens/', views.poll_tokens, name='poll_tokens'),
]