import time
import logging
import sys
from ldap3 import SEARCH_SCOPE_WHOLE_SUBTREE
from flask import current_app
from flask.ext.assets import ManageAssets
from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server
from newauth.app import create_app
from newauth.models import db, AuthContact, User, Group, GroupMembership, APIKey
from newauth.models.enums import GroupType
from newauth.plugins.sync.ldap import LDAPUser

app = create_app()

manager = Manager(app)
manager.add_command('assets', ManageAssets)
manager.add_command('db', MigrateCommand)

for plugin in app.loaded_plugins.itervalues():
    if hasattr(plugin, 'ExtraCommands'):
        manager.add_command(plugin.ExtraCommands_prefix, plugin.ExtraCommands)

@manager.command
def update_contacts():
    with app.app_context():
        app.debug = True
        AuthContact.update_contacts()


@manager.command
def make_admin(user):
    with app.app_context():
        u = User.query.filter_by(user_id=user).first()
        if not u:
            raise Exception('Could not find user {}.'.format(user))
        g = Group.query.filter_by(name=app.config['ADMIN_GROUP']).first()
        if not g:
            g = Group(name=app.config['ADMIN_GROUP'], description='The admin group.', type=GroupType.hidden.value)
        membership = GroupMembership(user=u, is_admin=True, can_ping=True)
        g.members.append(membership)
        db.session.add(g)
        db.session.commit()


@manager.command
def make_ping(user):
    with app.app_context():
        u = User.query.filter_by(user_id=user).first()
        if not u:
            raise Exception('Could not find user {}.'.format(user))
        g = Group.query.filter_by(name=app.config['PING_GROUP']).first()
        if not g:
            g = Group(name=app.config['PING_GROUP'], description='The ping group.', type=GroupType.hidden.value)
        membership = GroupMembership(user=u, is_admin=True, can_ping=True)
        g.members.append(membership)
        db.session.add(g)
        db.session.commit()


@manager.command
def update_users(user_id=None):
    with app.app_context():
        if user_id:
            user = User.query.filter_by(user_id=user_id).first()
            if not user:
                current_app.logger.warn('Could not find user #{}'.format(user_id))
                return
            user.update_keys()
            user.update_status()
            db.session.add(user)
            db.session.commit()
        else:
            users = User.query.filter_by().all()
            print('Found {} users.'.format(len(users)))
            count = len(users)
            i = 0
            for user in users:
                i += 1
                print('Updating {}'.format(user.user_id))
                print('{} %'.format((i / count) * 100))
                user.update_keys()
                user.update_status()
                db.session.add(user)
                db.session.commit()
                time.sleep(1)


if __name__ == '__main__':
    manager.run()
