from django.conf.urls import url
from django.conf.urls import handler400, handler403, handler404, handler500

from server.views import migrate, requirements_install, restart_all_servers,\
    restart_all_api_servers, start_all_servers, stop_all_servers, start_all_api_servers,\
    stop_all_api_servers, get_facebook_tokens, process_codebase, setup_system,\
    backup, home


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^web/restart_all_servers/$', restart_all_servers, name='restart_all_servers'),
    url(r'^web/restart_all_api_servers/$', restart_all_api_servers, name='restart_all_api_servers'),
    url(r'^web/start_all_servers/$', start_all_servers, name='start_all_servers'),
    url(r'^web/stop_all_servers/$', stop_all_servers, name='stop_all_servers'),
    url(r'^web/start_all_api_servers/$', start_all_api_servers, name='start_all_api_servers'),
    url(r'^web/stop_all_api_servers/$', stop_all_api_servers, name='stop_all_api_servers'),
    url(r'migrate/^$', migrate, name='migrate'),
    url(r'^get_facebook_tokens/$', get_facebook_tokens, name='get_facebook_tokens'),
    url(r'^process_codebase/$', process_codebase, name='process_codebase'),
    url(r'^setup_system/$', setup_system, name='setup_system'),
    url(r'^backup/$', backup, name='backup'),
    url(r'^install_requirements/$', requirements_install, name='install_requirements'),
]

handler400 = 'server.views.bad_request'
handler403 = 'server.views.permission_denied'
handler404 = 'server.views.page_not_found'
handler500 = 'server.views.server_error'