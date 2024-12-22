from keycloak import KeycloakOpenID
import httpx

# Configure client
keycloak_openid = KeycloakOpenID(server_url="https://localhost:8443/auth",
                                 client_id="zidp",
                                 realm_name="zidp",
                                 client_secret_key="iwj45woMQbbsQeDC2xyFSPZsmxSFq027",
                                 verify=False)


# Get WellKnown
config_well_known = keycloak_openid.well_known()

# Get Code With Oauth Authorization Request
auth_url = keycloak_openid.auth_url(
    redirect_uri="http://127.0.0.1:8000",
    scope="email",
    state="your_state_info")


# # Get Access Token With Code
# access_token = keycloak_openid.token(
#     grant_type='authorization_code',
#     code='f26e27d2-cdbb-4940-983a-4698b8a22df4.819bcae0-a089-4106-9777-f2102d2024f0.c9a01826-150d-485f-83d9-3ae44cd89c60',
#     redirect_uri="http://127.0.0.1:8000",)


# print(access_token)

token = keycloak_openid.token("zidp", "zidp")

userinfo = keycloak_openid.userinfo(token['access_token'])
token = keycloak_openid.refresh_token(token['refresh_token'])
print(token)

print(userinfo)
