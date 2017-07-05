from subprocess import Popen, TimeoutExpired

from django.shortcuts import render
from django.conf import settings

from .models import NetworkSite


def home(request):
    return render(request, 'server/home.html')

#TODO major fucntional mapping if decided to expand this project
#TODO security/ login if used not in local machine
#TODO async
#TODO outputs collection system
# TODO frop wsgiinstaller and integrate here


def process_output(proc):
    """
    Communicates with process.
    """
    try:
        outs, errs = proc.communicate(timeout=settings.COMMAND_TIMEOUT)
    except TimeoutExpired:
        proc.kill()
        outs, errs = proc.communicate()
    return outs, errs


def set_environments():
    """
    Sets required environment variables.
    """
    proc = Poepn("export LD_LIBRARY_PATH=/usr/local/anaconda/lib:$LD_LIBRARY_PATH")
    proc = Poepn("MYSQL_ROOT_PASSWORD={}".format(settings.MYSQL_ROOT_PASSSWORD))    
    return process_output(proc=proc)


def install_certbot():
    proc = Poepn("cd /usr/local/sbin")
    proc = Poepn("sudo wget https://dl.eff.org/certbot-auto")
    proc = Poepn("sudo chmod a+x /usr/local/sbin/certbot-auto")
    proc = Poepn("sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096")
    return process_output(proc=proc)


def install_python():
    proc = Poepn("sudo apt install gcc -y")
    proc = Poepn("wget https://repo.continuum.io/archive/Anaconda3-4.3.1-Linux-x86_64.sh -O /usr/local/anaconda.sh")
    proc = Poepn("bash /usr/local/anaconda.sh -b -p /usr/local/anaconda")
    proc = Poepn("rm /usr/local/anaconda.sh")
    proc = Poepn("echo 'export PATH=\"/usr/local/anaconda/bin:$PATH\"' >> ~/.bashrc")
    proc = Poepn("source ~/.bashrc")
    proc = Poepn("conda update --all -y")
    return process_output(proc=proc)


def install_image_manage,ent():
    proc = Popen("sudo apt install libpng-dev zlib1g-dev -y")
    proc = Popen("")
    proc = Popen("")
    proc = Popen("")


def cd_to_project(proj):
    """Goes to project fodler."""
    proc = Popen("cd {0}/{1}".format(proj.path, proj.folder_name))
    return process_output(proc=proc)


def activate_env(proj):
    """Activates environment."""
    proc = Popen("source /usr/local/anaconda/bin/activate {0}".format(proj.folder_name))
    return process_output(proc=proc)


def deactivate_env():
    """Deactivates environment."""
    proc = Popen("source /usr/local/anaconda/bin/deactivate")
    return process_output(proc=proc)


def stop_server(proj, api=""):
    """Stops server."""
    assert isinstance(api, str)

    proc = Popen("/sbin/stop {0}{1}".format(api, proj.folder_name))
    return process_output(proc=proc)
    

def start_server(proj, api=""):
    """Stops server."""
    assert isinstance(api, str)

    proc = Popen("/sbin/start {0}{1}".format(api, proj.folder_name))
    return process_output(proc=proc)


def migrate(request):
    set_environments()
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = cd_to_project(proj=proj)
        outputs, errs = activate_env(proj=proj)
        proc = Popen("/usr/local/anaconda/envs/{0}/bin/python manage.py makemigrations && \
            /usr/local/anaconda/envs/{0}/bin/python manage.py migrate".format(proj.folder_name))
        outputs, errs = process_output(proc=proc)
        outputs, errs = deactivate_env(proj=proj)
        
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def requirements_install(request):
    set_environments()
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = cd_to_project(proj=proj)
        outputs, errs = activate_env(proj=proj)
        proc = Popen("pip install --upgrade git+https://github.com/codelucas/newspaper")
        proc = Popen("python -m nltk.downloader all")
        proc = Popen("/usr/local/anaconda/envs/{0}/bin/pip install -r requirements.txt".format(proj.folder_name))
        outputs, errs = process_output(proc=proc)
        outputs, errs = deactivate_env(proj=proj)
    
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def restart_all_servers(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = stop_server(proj=proj)
        outputs, errs = start_server(proj=proj)
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def restart_all_api_servers(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = stop_server(proj=proj, api="a")
        outputs, errs = start_server(proj=proj, api="a")
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def start_all_servers(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = start_server(proj=proj)
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def start_all_api_servers(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = start_server(proj=proj, api="a")
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def stop_all_servers(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = stop_server(proj=proj)
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


def stop_all_api_servers(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = stop_server(proj=proj, api="a")
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })


#TODO this should be fully automated: 1. get key expiry, 2. run this, 3. write key to .env files, 
#probably betetr done on remote script
def get_facebook_tokens(request):
    outputs, errs = "", ""
    
    for proj in NetworkSite.objects.all():
        outputs, errs = cd_to_project(proj=proj)
        outputs, errs = activate_env(proj=proj)
        proc = Popen("/usr/local/anaconda/envs/{0}/bin/python /home/{0}/facebook_key_refresh.py".format(proj.folder_name))
        outputs, errs = process_output(proc=proc)
        outputs, errs = deactivate_env(proj=proj)
    return render(request, 'server/result.html', {'res': outs, 'errs': errs })



#TODO NOT USED ANYWHERE
def create_folder(proj, directory):
    """Creates directory within project directory."""
    proc = Popen("mkdir /home/{0}/{1}".format(proj.folder_name, directory))
    return process_output(proc=proc)


#TODO NOT USED ANYWHERE
def fix_permissions(proj):
    """Fixes permissions of project folder recursively."""
    proc = Popen("chown -R www-data:www-data  /home/{0}".format(proj.folder_name))
    return process_output(proc=proc)


#TODO NOT implemented
def process_codebase(request):
    """Gets new updated files from git to box/ and copies them for all network sites from box/."""
    pass


def update_system():
    """Update and upgrade system."""
    proc = Poepn("sudo apt update  -y")
    proc = Poepn("sudo apt upgrade  -y")
    proc = Poepn("sudo apt dist-upgrade  -y")
    return process_output(proc=proc)


def mysql_deps():
    proc = Poepn("sudo apt install libmysqlclient-dev expect mysql-server -y")
    sudo mysql_secure_installation

    
def install_elastic_search():
    """Install Elastic Search."""
    proc = Popen("sudo apt install -y default-jdk curl")
    proc = Poepn("curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.4.0.deb")
    proc = Poepn("sudo dpkg -i elasticsearch-5.4.0.deb")
    proc = Poepn("sudo update-rc.d elasticsearch defaults 95 10")
    proc = Poepn("sudo /etc/init.d/elasticsearch start")
    proc = Poepn("sudo cp /home/$PROJECT/monitrc /etc/monit/monitrc")


#TODO NOT implemented
def setup_system(request):
    """Set ups and prepares the bare metal server for QPreob."""
    update_system()


#TODO NOT implemented
def backup(request):
    """Back ups databases, crons and data."""
    pass


def page_not_found(request):
    return render(request, template_name='server/404.html', context=None, content_type=None, status=404, using=None)


def permission_denied(request):
    return render(request, template_name='server/403.html', context=None, content_type=None, status=403, using=None)


def server_error(request):
    return render(request, template_name='server/500.html', context=None, content_type=None, status=500, using=None)


def bad_request(request):
    return render(request, template_name='server/400.html', context=None, content_type=None, status=400, using=None)
