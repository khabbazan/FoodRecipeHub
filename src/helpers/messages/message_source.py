# flake8: NOQA
from fastapi_babel.core import make_gettext as _

messages_dict = {
    ############################## user API ##############################
    "login_user": {
        "sync": _("user '{user}' login successfully"),
    },
    "failed_login_user": {
        "sync": _("user '{user}' login failed"),
    },
    "update_user": {
        "sync": _("user '{user}' update successfully"),
    },
    "failed_update_user": {
        "sync": _("user '{user}' update failed"),
    },
    "logout_user": {
        "sync": _("user '{user}' logout successfully"),
    },
    "failed_logout_user": {
        "sync": _("user '{user}' logout failed"),
    },
    "refresh_token": {
        "sync": _("refresh token for user '{user}' update successfully"),
    },
    "failed_refresh_token": {
        "sync": _("refresh token for user '{user}' update failed"),
    },
    ############################## recipe API ##############################
    "create_recipe": {
        "sync": _("recipe '{title}' for '{user}' create successfully"),
    },
    "failed_create_recipe": {
        "sync": _("recipe '{title}' for '{user}' create failed"),
    },
    "update_recipe": {
        "sync": _("recipe '{uuid}' updated by {user} successfully"),
    },
    "failed_update_recipe": {
        "sync": _("recipe '{uuid}' was not successfully updated by {user}"),
    },
    "delete_recipe": {
        "sync": _("recipe '{uuid}' deleted by {user} successfully"),
    },
    "failed_delete_recipe": {
        "sync": _("recipe '{uuid}' was not successfully deleted by {user}"),
    },
    ############################## relation API ##############################
    "follow_user": {
        "sync": _("user '{user}' follows '{following}' successfully"),
    },
    "failed_follow_user": {
        "sync": _("user '{user}' failed to follow '{following}'"),
    },
    "unfollow_user": {
        "sync": _("user '{user}' unfollow '{following}' successfully"),
    },
    "failed_unfollow_user": {
        "sync": _("user '{user}' failed to unfollow '{following}'"),
    },
}
