# StockPrice-AIAgent_StreamingResponse

# About
This project is a Chatbot that has the capability to fetch Real-Time and Historical Prices of the stock the user wants. This project gives the output same like [StockPrice-AIAgent](https://github.com/Shidhin-VP/StockPrice-AIAgent), but with differnt technologies, which are described below and with a Streaming Response.
## Technologies Used. 
### For Backend
***Backend Infrastructures are Built Using Terraform***
1. AWS Lambda
2. AWS Lambda URL
3. AWS Bedrock
4. AWS ECR

This Image can be considered for reference to know how the Infrastructure is connected for this project: 
![image](https://github.com/user-attachments/assets/6c7f8b1f-1a8d-4861-8c1f-0c74b1aef742) 

### For Frontend
1. Flutter for Mobile App (Android & iOS)
2. Streamlit for Web as a prototype
   
# Prerequisite
## For Backend
1. Need to Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
2. Need to Install [Terraform](https://developer.hashicorp.com/terraform/install)
3. Signup to [AWS Console](https://aws.amazon.com/)
4. Download Docker [Docker](https://www.docker.com/)

## For Frontend
1. Install [Flutter](https://flutter.dev/)
2. Install [Streamlit](https://streamlit.io/) 

# Installation Instructions
* After installing all the required prerequisite, this project can be Cloned using this command: 
```python
git clone https://github.com/Shidhin-VP/StockPrice-AIAgent_StreamingResponse.git
```
* After cloning the Infrastructures can be deleted or activated from the Terraform Code from path:
```python
src/terraform/main.tf
```


