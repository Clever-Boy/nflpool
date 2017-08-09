from pyramid.config import Configurator
import nflpool.controllers.home_controller as home
import nflpool.controllers.account_controller as account
import nflpool.controllers.admin_controller as admin
import nflpool.controllers.standings_controller as standings
import nflpool.controllers.picks_controller as picks
from nflpool.data.dbsession import DbSessionFactory
import os
import nflpool
from nflpool.services.email_service import EmailService
from nflpool.services.email_service import EmailTemplateParser

dev_mode = False


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    init_mode(config)
    init_includes(config)
    init_routing(config)
    init_db(config)
    init_smtp_mail(config)
    init_email_templates(config)

    return config.make_wsgi_app()


def init_email_templates(_):
    EmailTemplateParser.global_init()


def init_smtp_mail(config):
    global dev_mode
    unset = 'YOUR_VALUE'

    settings = config.get_settings()
    smtp_username = settings.get('smtp_username')
    smtp_password = settings.get('smtp_password')
    smtp_server = settings.get('smtp_server')
    smtp_port = settings.get('smtp_port')

    local_dev_mode = dev_mode

    if smtp_username == unset:
        log = LogService.get_startup_log()
        log.warn("SMTP server values not set in config file. "
                 "Outbound email will not work.")
        local_dev_mode = True  # turn off email if the system has no server.

    EmailService.global_init(smtp_username, smtp_password, smtp_server, smtp_port, local_dev_mode)


def init_db(_):
    top_folder = os.path.dirname(nflpool.__file__)
    rel_folder = os.path.join('db', 'nflpooldb.sqlite')

    db_file = os.path.join(top_folder, rel_folder)
    DbSessionFactory.global_init(db_file)


def init_mode(config):
    global dev_mode
    settings = config.get_settings()
    dev_mode = settings.get('mode') == 'dev'
#    log = LogService.get_startup_log()
#    log.notice('Running in {} mode.'.format('dev' if dev_mode else 'prod'))


def init_routing(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_handler('root', '/', handler=home.HomeController, action='index')

    add_controller_routes(config, home.HomeController, 'home')
    add_controller_routes(config, account.AccountController, 'account')
    add_controller_routes(config, admin.AdminController, 'admin')
    add_controller_routes(config, standings.StandingsController, 'standings')
    add_controller_routes(config, picks.PicksController, 'picks')

    config.scan()


def add_controller_routes(config, ctrl, prefix):
    config.add_handler(prefix + 'ctrl_index', '/' + prefix, handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl_index/', '/' + prefix + '/', handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl', '/' + prefix + '/{action}', handler=ctrl)
    config.add_handler(prefix + 'ctrl/', '/' + prefix + '/{action}/', handler=ctrl)
    config.add_handler(prefix + 'ctrl_id', '/' + prefix + '/{action}/{season}', handler=ctrl)


def init_includes(config):
    config.include('pyramid_chameleon')
    config.include('pyramid_handlers')

