"""

#Aha! That error explains everything.

    ❌ clerk-sdk does not exist on PyPI (Python Package Index).

The import you tried:

from clerk_backend_api import Clerk, AuthenticateRequestOptions

— is either:

    ❓ From a tutorial using a custom-made module (e.g., a clerk_backend_api.py file someone built)

    ❌ Or it’s pretending a Clerk Python SDK exists — but Clerk has no official backend SDK for Python at this time.
# ✅ The Solution
#
# Since clerk-sdk is not installable via pip, and clerk_backend_api is not real unless you wrote it yourself...
# 🧠 TL;DR
#
#     clerk-sdk is a fictional or unofficial module — it doesn’t exist on PyPI.
#
#     ✅ Instead: Use PyJWT or Clerk's REST API.
#
#     🔐 If you want to decode JWTs server-side without network calls (i.e., “serverless”), PyJWT is the way to go.

from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
from clerk import Clerk, AuthenticateRequestOptions

import os
from dotenv import load_dotenv

load_dotenv()


clerk_sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

# accepts the request from our front-end to our back-end
def authenticate_and_get_user_details(request):
    try: # being that we are using the JWT_KEY below, this request will happen serverless...
        # no need to send a network request to Clerk server in order to authorize the key...serverless is much faster
        request_state = clerk_sdk.authenticate_request(
            request,
            AuthenticateRequestOptions(
                authorized_parties=["http://localhost:5173"],
                jwt_key=os.getenv("JWT_KEY")
            )
        )
        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="HAL SAYS: Invalid Token!")

        user_id = request_state.payload.get("sub") # the sub will store the decoded user's id...

        return {"user_id": user_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

import jwt
from fastapi import HTTPException, Request
import os
from dotenv import load_dotenv

load_dotenv()

JWT_KEY = os.getenv("JWT_KEY")

def authenticate_and_get_user_details(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        # Strip "Bearer " prefix if present
        token = token.replace("Bearer ", "")
        payload = jwt.decode(token, JWT_KEY, algorithms=["HS256"])  # Adjust algorithm as needed
        return {"user_id": payload.get("sub")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")










