import keycloak as kc


def validate_user_credentials(username: str, password: str) -> bool:
    try:
        keycloak_openid = kc.KeycloakOpenID(
            server_url="http://172.19.0.1:8080/",
            realm_name="master",
            client_id="admin-cli"
        )
        keycloak_openid.token(username, password)
        return True
    except Exception as e:
        print(e)
        return False

