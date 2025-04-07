from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('',views.Authentication, name = 'Authentication'),
    path('Admin_page',views.view_results, name='Admin_page'),
    path('Voting_page/<ind>',views.voting_procedures, name='Voting_page'),
    path('Vote/<index>', views.Vote, name='Vote'),
    path('Vote/counter/<id>,<index>',views.counter,name='counter'),
    path('Thanks',views.thanks, name='Thanks'),
    path('add_user/', views.add_user, name='add_user'),
    path('uc/', views.upload_file, name='upload_file'),
    path('ap/', views.add_position, name='add_position'),
    path('ac/', views.add_candidate, name='add_candidate'),
    path('export_csv/', views.export_csv, name='export_csv'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),


]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)