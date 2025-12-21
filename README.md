# AWS

## HW #43

#### 1. For GET request return status code 200 with body containing {status: up}
#### 2. For POST request perform the following
- 2.1 Validate body for existence "op1" as float, "op2" as float and "operation" as string (no validate concrete operation value, because it's functionality of lambda calculator)
- 2.1.1 In the case of wrong JSON the lambda function should return status code 400 with related error message
- 2.2 Debug / Error logging
- 2.3 Publishing message containing appropriate JSON with calculation data
    - 2.3.1 In the case of error the lambda function should return status code 500 with related error message
    - 2.3.2 In the case of succesful publishing the lambda function should return status code 200 with { MessageId: < MessageID value > }

### 3.Lambda function as a subscriber of appropriated SNS standard topic
No JSON validation inside a received Message that implied to be done in 2.1

If the "operation" contains wrong value (non-existed operation) the lambda function raises ValueError

If the "operation" contains correct value the lambda function should calculate in accordance with the operands and the operation. The result should be printed to CloudWatch

#### Integration Acceptance Test
##### Test normal flow
Postman sends correct JSON, result - CloudWatch in the Log group for SNS lambda subscriber function contains Log stream with appropriate result (no errors), status code 200 with {"MessageID":< message Id value >}
##### Test alternative flows
Postman sends wrong JSON, result - CloudWatch in the Log group for HTTP lamda target function contains appropriate error messages, status code 400 with {"detail" : < appropriate error message>}

Postman sends correct JSON, but wrong operation value, result - CloudWatch in the Log group for SNS lambda subscriber function contains appropriate error message, status code 200 with {"MessageID":< message Id value >}