from .keycloak import *
from .config import *


def keycloak_setup():
    settings = get_settings()
    kc_admin = getKeyCloakAdmin()

    groups_names = [group["name"] for group in get_groups()]

    if("Admin" not in groups_names):
        create_new_group("Admin")

    admin = [user for user in get_users() if user["username"] == "admin"][0]

    kc_admin.update_user(admin["id"],{
        "firstName": "admin",
        "lastName": "",
        "email": "admin@admin.com",
        "emailVerified": True
    })

    group_Admin = [group for group in get_groups() if group["name"] == "Admin"][0]
    admin_groups = [dict(group)["name"] for group in get_user_kc_groups(admin["id"])]

    if("Admin" not in admin_groups):
        add_user_group(admin["id"], group_Admin["id"])


    kc_admin.update_realm(settings.kc_realm_name, {
        "accessTokenLifespan": 86400
    })
