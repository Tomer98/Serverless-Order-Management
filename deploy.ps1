$acc = $(aws sts get-caller-identity --query Account --output text).Trim()
$region = "us-east-1"
$apiId = "y7zcu18r70"

aws apigateway put-method --rest-api-id $apiId --resource-id pbk84k --http-method GET --authorization-type NONE --region $region

aws apigateway put-integration --rest-api-id $apiId --resource-id pbk84k --http-method GET --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${region}:lambda:path/2015-03-31/functions/arn:aws:lambda:${region}:${acc}:function:OrderStats/invocations" --region $region

aws lambda add-permission --function-name OrderStats --statement-id apigateway-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:${region}:${acc}:${apiId}/*/GET/stats" --region $region

aws apigateway create-deployment --rest-api-id $apiId --stage-name prod --region $region
