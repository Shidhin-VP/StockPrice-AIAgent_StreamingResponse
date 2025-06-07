provider "aws" {
  region = "us-east-1"
}

data "aws_ecr_repository" "StockPriceStreamingResponse" {
  name = "stockprice-aiagent_streamingresponse"
}

resource "aws_iam_role" "IAMRole_StockPriceStreamingResponse" {
  name = "StockPriceAIAgentIamRole"
  assume_role_policy = jsonencode({
    Version="2012-10-17"
    Statement=[
        {
            Action="sts:AssumeRole",
            Effect="Allow",
            Principal={
                Service="lambda.amazonaws.com"
            }
        }
    ]
  })
}

resource "aws_iam_role_policy" "IamRolePolicy_StockPriceStreamingResponse" {
  role = aws_iam_role.IAMRole_StockPriceStreamingResponse.name
  policy = jsonencode(
    {
        Version="2012-10-17"
        Statement=[
            {
                Effect="Allow",
                Action=[
                    "logs:*",
                    "bedrock:InvokeModelWithResponseStream",
                    "bedrock:InvokeModel"
                ],
                Resource="*"
            }
        ]
    }
  )
}

resource "aws_lambda_function" "Lambda_StockPriceStreamingResponse" {
  function_name = "StockPrice_StreamingResponse"
  role = aws_iam_role.IAMRole_StockPriceStreamingResponse.arn
  package_type = "Image"
  image_uri = "${data.aws_ecr_repository.StockPriceStreamingResponse.repository_url}:latest"
  timeout = 300
  environment {
    variables = {
      AWS_LWA_INVOKE_MODE="RESPONSE_STREAM"
    }
  }
}

resource "aws_lambda_function_url" "LambdaURL_StockPriceStreamingResponse" {
  function_name = aws_lambda_function.Lambda_StockPriceStreamingResponse.function_name
  authorization_type = "NONE"
  invoke_mode = "RESPONSE_STREAM"
}

output "StockPriceStreamingResponse_URL" {
  value="${aws_lambda_function_url.LambdaURL_StockPriceStreamingResponse.function_url}ask"
}