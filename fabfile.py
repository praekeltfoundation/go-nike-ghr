from fabric.api import cd, sudo, env

DEPLOY_USER = 'jmbo'
env.path = '/var/praekelt/ghr/'

def restart():
    sudo('/etc/init.d/nginx restart')
    sudo('supervisorctl reload')


def deploy():
    with cd(env.path):
        sudo('git pull', user=DEPLOY_USER)
        sudo('ve/bin/python manage.py syncdb --migrate --noinput',
             user=DEPLOY_USER)
        sudo('ve/bin/python manage.py collectstatic --noinput',
             user=DEPLOY_USER)


def install_packages(force=False):
    with cd(env.path):
        sudo('ve/bin/pip install %s -r requirements.pip' % (
             '--upgrade' if force else '',), user=DEPLOY_USER)
