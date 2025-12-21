import json
import boto3
import logging 

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def getOperandValue(calcData:dict, operandName:str) -> float:
    try:
        operand = float(calcData[operandName])
    except KeyError:
        raise AttributeError(f"Missing {operandName}") 
    except ValueError:
        raise AttributeError(f"{operandName} should be a number")
    return operand

def lambda_handler(event, __):
    logger.debug(f"Received: {event}")
    error: str | None = None
    res: str | None = None
    status: int = 200
    
    if event['requestContext']['http']['method'] == 'POST':
        try:
            message = json.loads(event['body'])
            logger.debug(f"Processing {message}")
        except Exception as e:
            error = str(e)
            status = 400
            logger.error("Error parsing json: " + str(e))

        if error is None:
            try:
                getOperandValue(message, "op1")
                getOperandValue(message, "op2")
                op: str = message['operation']
            except KeyError:
                error = "Missing 'operation'"
                status = 400
            except Exception as e:
                error = str(e)
                status = 400

            if error is None:
                client = boto3.client('sns')
                try:
                    resp = client.publish(
                        TopicArn='arn:aws:sns:us-east-1:096753666022:Simple-topic',
                        Message=json.dumps(message),
                        Subject='Lambda SNS Test'
                    )
                    logger.debug(resp)
                    res = json.dumps({"MessageId": resp['MessageId']})
                except Exception as e:
                    error = "Error publishing to SNS: " + str(e)
                    status = 500
    else:
        res = json.dumps({"status": "up"})

    return {
        'statusCode': status,
        'body': res if res is not None else json.dumps({"detail": error})
    }
