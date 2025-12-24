# AWS

## HW #44 Login Lambda Function
Created lambda function processing event from HTTP Gateway
 -   1.1 Body event should contain JSON with following fields:
        - username (required)
        - password (required)
        - new password (optional, required only if new password required)
 -   1.2 Following flows

        1.2.1 Normal Flow - response with status code 200 and {"access_token":< access token >, "id_token": < id_token >, "refresh_token" : < refresh token >}

        1.2.1 Alternative Flows - response with status code 400 and {"error": "invalid username or password"}
