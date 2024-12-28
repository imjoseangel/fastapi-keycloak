from fastapi import HTTPException, status, Request
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakPostError
from src.config import keycloak_openid
from src.models import UserInfo


class AuthService:
    @staticmethod
    def authenticate_user(keycode: str, request: Request) -> str:
        """
        Authenticate the user using Keycloak and return an access token.
        """
        try:

            token = keycloak_openid.token(
                grant_type='authorization_code',
                code=keycode,
                redirect_uri=str(request.url_for('callback')),
                scope="openid profile email"
            )
            return token["access_token"]
        except KeycloakAuthenticationError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Login",
            ) from exc
        except KeycloakPostError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Grant",
            ) from exc

    @staticmethod
    def verify_token(token: str) -> UserInfo:
        """
        Verify the given token and return user information.
        """
        try:
            user_info = keycloak_openid.userinfo(token)
            print(user_info)
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
                )
            return UserInfo(
                preferred_username=user_info["preferred_username"],
                email=user_info.get("email"),
                full_name=user_info.get("name"),
            )
        except KeycloakAuthenticationError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            ) from exc
