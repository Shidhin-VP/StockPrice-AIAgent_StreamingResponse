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
                    "bedrock:InvokeModel",
                    "bedrock:ApplyGuardrail"
                ],
                Resource="*"
            }
        ]
    }
  )
}

# resource "aws_bedrock_guardrail" "Guardrail_StockPriceStreamingResponse" {
#   name = "StockPriceStreamingResponse_Guardrails"
#   blocked_input_messaging = "Your input has blocked due to policy restrictions."
#   blocked_outputs_messaging = "Your output has blocked due to policy restrictions."
#   description = "Guardrail for StockPrice Streaming Project"

#   content_policy_config {
#     filters_config {
#       input_strength = "MEDIUM"
#       output_strength = "HIGH"
#       type = "HATE"
#     }
#     filters_config {
#       input_strength = "MEDIUM"
#       output_strength = "HIGH"
#       type = "INSULTS"
#     }
#     filters_config {
#       input_strength = "HIGH"
#       output_strength = "HIGH"
#       type = "SEXUAL"
#     }
#     filters_config {
#       input_strength = "HIGH"
#       output_strength = "HIGH"
#       type = "VIOLENCE"
#     }
#     filters_config {
#       input_strength = "MEDIUM"
#       output_strength = "HIGH"
#       type = "MISCONDUCT"
#     }
#     filters_config {
#       input_strength = "HIGH"
#       output_strength = "NONE"
#       type = "PROMPT_ATTACK"
#     }
#   }

#   sensitive_information_policy_config {
#     # pii_entities_config {
#     #   action = "BLOCK"
#     #   type = "NAME"
#     # }
#     pii_entities_config {
#       action = "BLOCK"
#       type = "EMAIL"
#     }
#     pii_entities_config {
#       action = "BLOCK"
#       type = "USERNAME"
#     }
#     regexes_config {
#       action = "BLOCK"
#       description = "SSN Pattern"
#       name = "StockPriceStreamingResponse_SSNRegex"
#       pattern = "^\\d{3}-\\d{2}-\\d{4}$"
#     }
#   }
# #   topic_policy_config {
# #     topics_config {
# #       name = "Investment_topic"
# #       examples = ["Should I buy AAPL?",
# #       "Where should I need to invest my money?",
# #       "Is Tesla a good investment?",
# #       "Can you recommend some stocks to invest in?",
# #       "Will it be good investing my money to Google?"]
# #       type = "DENY"
# #       definition = "Investment advice is not allowed. Only stock prices are permitted."
# #     }
# #   }
#   word_policy_config {
#     managed_word_lists_config {
#       type = "PROFANITY"
#     }
#     words_config {
#       text = "eval"
#     }
#     words_config {
#       text = "exec"
#     }
#     words_config {
#       text = "import"
#     }
#     words_config {
#       text = "os"
#     }
#     words_config {
#       text = "subprocess"
#     }
#     words_config {
#       text = "system"
#     }
#     words_config {
#       text = "socket"
#     }
#     words_config {
#       text = "compie"
#     }
#     words_config {
#       text = "eval()"
#     }
#     words_config {
#       text = "exec()"
#     }
#     words_config {
#       text = "os.system()"
#     }
#   }

# }

resource "aws_lambda_function" "Lambda_StockPriceStreamingResponse" {
  function_name = "StockPrice_StreamingResponse"
  role = aws_iam_role.IAMRole_StockPriceStreamingResponse.arn
  package_type = "Image"
  image_uri = "${data.aws_ecr_repository.StockPriceStreamingResponse.repository_url}:latest"
  memory_size = 512
  timeout = 300

  environment {
    variables = {
      AWS_LWA_INVOKE_MODE="RESPONSE_STREAM",
      #GUARDRAIL_ID=aws_bedrock_guardrail.Guardrail_StockPriceStreamingResponse.guardrail_id
    }
  }
}

resource "aws_lambda_function_url" "LambdaURL_StockPriceStreamingResponse" {
  function_name = aws_lambda_function.Lambda_StockPriceStreamingResponse.function_name
  authorization_type = "NONE"
  invoke_mode = "RESPONSE_STREAM"
}

output "StockPriceStreamingResponse_URL" {
  value="${aws_lambda_function_url.LambdaURL_StockPriceStreamingResponse.function_url}question"
}