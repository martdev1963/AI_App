from fastapi import HTTPException
from clerk_backend_api import Clerk, AuthenticateRequestOptions
import os
from dotenv import load_dotenv

load_dotenv()

'''
---------------------------------------------------------------------------------------------------------
                                        **DOCUMENTATION**
This is within the realm of "Technical Writing"...                                        
We have the front-end, Clerk will authenticate us on the front-end.
and it will issue something called a JWT token which is a JSON web token.
This token can then be sent to the back-end, and on the back-end which this file utils.py is from,
we need to make sure that this token is actually valid...
So from the back-end what we're going to do is connect to Clerk essentially, by using this secret key...
and we're going to ask Clerk, if the token is valid.
Now, there are two ways that we can do this... We can do this over the network, which means we actually
send a request to Clerk's server, and we say hey server, is this token valid?
or the way that I'm going to show you how is using network lists.
What that means is that there will be no latency. We don't need to wait for Clerk to respond.
and the reason how we can do this network list is because we have that value that we just brought into our
.env variable file, which is this JWT key. So this key and this secret key are enough for us on our 
back-end to be able to look at these Clerk tokens and see if they're valid or not.
The code in this file will validate whether the keys are valid and we can reuse this code in our app.
---------------------------------------------------------------------------------------------------------
'''
#--------------------------------------------------------------
# vid_time: 1:19:08 / 2:31:54
# create thorough documentation throughout all the code files
# including notes.txt
# explaining every nook and cranny...
# -------------------------------------------------------------
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












