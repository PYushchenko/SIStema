from django.conf.urls import url
from . import views
from .staff import views as staff_views

urlpatterns = [
    url(r'^exam/$', views.exam, name='exam'),
    url(r'^exam/solution/(?P<solution_id>\d+)/', views.solution, name='solution'),
    url(r'^exam/submit/(?P<task_id>\d+)/', views.submit, name='submit'),
    url(r'^exam/upgrade/$', views.upgrade, name='upgrade'),


    # Staff urls
    url(r'^enrolling/$', staff_views.enrolling, name='enrolling'),
    url(r'^enrolling/(?P<user_id>\d+)/$', staff_views.enrolling_user, name='enrolling_user'),
    url(r'^enrolling/(?P<user_id>\d+)/questionnaire/(?P<questionnaire_name>[^/]+)/$', staff_views.user_questionnaire, name='user_questionnaire'),
    url(r'^enrolling/(?P<user_id>\d+)/topics/$', staff_views.user_topics, name='user_topics'),
    url(r'^enrolling/(?P<user_id>\d+)/change_group/$', staff_views.change_group, name='change_group'),

    url(r'^check/$', staff_views.check, name='check'),
    url(r'^check/(?P<group_name>[^/]+)/$', staff_views.check_group, name='check_group'),
    url(r'^solution/(?P<solution_id>\d+)/$', staff_views.solution, name='user_solution'),

    url(r'^results/$', staff_views.results, name='results'),

    url(r'^initial/reset/$', staff_views.initial_reset, name='initial.reset'),
    url(r'^initial/auto_reject/$', staff_views.initial_auto_reject, name='initial.auto_reject'),
    url(r'^initial/checking_groups/$', staff_views.initial_checking_groups, name='initial.checking_groups'),
    ]
