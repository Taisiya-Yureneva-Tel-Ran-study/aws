import json
import boto3
import logging

logger = logging.getLogger()
CLIENT_ID = '44bg8n6sno3gfb3adon2psel91'

loginScheme = {
    'username': str,
    'password': str
}

client = boto3.client('cognito-idp')

def __validate(data, scheme):
    for field, ftype in scheme.items():
        if field not in data:
            raise ValueError(f'Missing field {field}, {ftype}')
        if not isinstance(data[field], ftype):
            raise ValueError(f'Field {field} is not of type {ftype}')
    logger.info("Data is valid")

def __newPassChallenge(username: str, password: str, session: str):
    logger.info(f"New password challenge for user {username}")
    return client.respond_to_auth_challenge(
        ClientId=CLIENT_ID,
        ChallengeName='NEW_PASSWORD_REQUIRED',
        Session=session,
        ChallengeResponses={
            'USERNAME': username,
            'NEW_PASSWORD': password
        }
    )

def __login(body):
    resp = client.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': body['username'],
            'PASSWORD': body['password']
        }
    )
    if resp.get('ChallengeName') is not None:
        if resp['ChallengeName'] == "NEW_PASSWORD_REQUIRED":
            if body.get('newPassword') is None:
                raise ValueError("New password required!")
            else:
                resp = __newPassChallenge(body['username'], body['newPassword'], resp['SessionId'])
        else:
            raise Exception("Unknown challenge!")
    return resp['AuthenticationResult']    

def lambda_handler(event, __):
    logger.debug(f"Received event: {event}")
    resp = None
    error = None
    statusCode = 200
    if event['rawPath'] == '/login' and event.get('body') is not None:
        try:
            body = json.loads(event['body'])
            __validate(body, loginScheme)
        except Exception as e:
            error = json.dumps(str(e))
            statusCode = 400

        if error is None:
            try:
                resp = __login(body)
            except ValueError as e:
                error = json.dumps({"error": str(e)})
                statusCode = 400
            except client.exceptions.NotAuthorizedException as e:
                error = json.dumps({"error": str(e)})
                statusCode = 400
            except Exception as e:
                error = json.dumps({"error": str(e)})
                statusCode = 500
    else:
        statusCode = 400
        error = json.dumps({"error": "Invalid path or missing body"})

    return {
        'statusCode': statusCode,
        'body': json.dumps(resp) if error is None else error
    }
