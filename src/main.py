from fastapi import FastAPI, Depends, Form, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse
from src.models import TokenResponse, UserInfo
from src.controller import AuthController
from pydantic import SecretStr
from src.config import get_openid

# Initialize the FastAPI app
app = FastAPI()

# Initialize the HTTPBearer scheme for authentication
bearer_scheme = HTTPBearer()

# Configure client
keycloak_openid = get_openid()

# Define the root endpoint
@app.get("/")
async def read_root():
    """
    Root endpoint that provides a welcome message and documentation link.
    """
    return AuthController.read_root()


# Define the login endpoint
@app.post("/login", response_model=TokenResponse)
async def login(username: str = Form(...), password: SecretStr = Form(...)):
    """
    Login endpoint to authenticate the user and return an access token.

    Args:
        username (str): The username of the user attempting to log in.
        password (str): The password of the user.

    Returns:
        TokenResponse: Contains the access token upon successful authentication.
    """
    return AuthController.login(username, password)


@app.get("/sso")
async def sso(request: Request):

    # Generate the auth URL
    auth_url = keycloak_openid.auth_url(
        redirect_uri=request.url_for('callback'),
        scope="openid profile email")

    return RedirectResponse(auth_url)

@app.get("/callback", response_model=TokenResponse, include_in_schema=False)
async def callback(request: Request):

    # Extract the code from the URL
    code = request.query_params.get('code')
    # print(f"Authorization code: {code}")

    token = keycloak_openid.token(
        grant_type='authorization_code',
        code=code,
        redirect_uri=request.url_for('callback'),
        scope="openid profile email"
    )

    return {"access_token": token["access_token"]}

# Define the protected endpoint
@app.get("/protected", response_model=UserInfo)
async def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Protected endpoint that requires a valid token for access.

    Args:
        credentials (HTTPAuthorizationCredentials): Bearer token provided via HTTP Authorization header.

    Returns:
        UserInfo: Information about the authenticated user.
    """
    return AuthController.protected_endpoint(credentials)
