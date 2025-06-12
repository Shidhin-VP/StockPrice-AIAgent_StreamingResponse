# StockPrice-AIAgent_StreamingResponse

## 📚 Table of Contents
- [About](#About)
- [Working Model](#working-model)
- [Technologies Used](#technologies-used)
- [Prerequisites](#prerequisites)
- [Installation & Program Running Instructions](#installation--program-running-instructions)
  - [How To Install](#how-to-install)
  - [How To Run](#how-to-run)
    - [Web Interface](#to-run-and-deploy-web-interface)
    - [Mobile Application](#to-run-mobile-application)

# About
This project is a Chatbot that has the capability to fetch Real-Time and Historical Prices of the stock the user wants. This project gives the output same like [StockPrice-AIAgent](https://github.com/Shidhin-VP/StockPrice-AIAgent), but with differnt technologies, which are described below and with a Streaming Response.
# Working Model
![Github Profiling 1](https://github.com/user-attachments/assets/579bee05-883e-4f6e-a6a3-095def450f20)

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
1. Install [VsCode](https://code.visualstudio.com/)
2. Install [Flutter](https://flutter.dev/)
3. Install [Android Studio](https://developer.android.com/studio)
4. Install [Streamlit](https://streamlit.io/) 

# Installation & Program Running Instructions
## How To Install
* After installing all the required prerequisite, this project can be Cloned using this command: 
```python
git clone https://github.com/Shidhin-VP/StockPrice-AIAgent_StreamingResponse.git
```
* After cloning the Infrastructures for the backend can be deleted or activated from the Terraform Code from path:
```python
src/terraform/main.tf
```
* After confirming the Backend Infrastructure, follow these commands:
     * ```
       terraform init
       ```
     * ```
       terraform apply
       ```
* Also can use ``` terraform destroy ``` to destroy all the infrastuctures later if needed.
## How To Run.
### To run and deploy Web Interface
* Navigate to path and Run **Streamlit run frontend.py**:
```
src/frontend/frontend.py
```
   * An Error can occur like the image shown below, because the access code is integrated to the Streamlit website, which will be explained in the **Deployment Section**

     <img width="1280" alt="image" src="https://github.com/user-attachments/assets/401bface-7475-473c-b8d6-23c180ea7420" />
* Click the Deploy button at the top right corner, later you can select the free version and press **Deploy Now**:
  
  <img width="1280" alt="image" src="https://github.com/user-attachments/assets/828989d0-9b21-412e-9755-a5c12d7e16bf" />
  * Later: 
     * Signin to Streamlit
     * Connect via GitHub
     * Click **Deploy**
* After deploying the webpage will be up-to-date as the code gets updated to GitHub. (***Don't forget to pull git to localhost after Deploying the web to streamlit***)
* Push all the changes that are done to the ***UI Frontend Python Code*** to Github.
### To run Mobile Application
* Navigate to the below shown path via VsCode:
```
src/mobile_frontend
```
* At the bottom right corrner, find **No Device** or any **Device** options that are available like the below shown image:
  
     <img width="1280" alt="image" src="https://github.com/user-attachments/assets/de5d7583-e2e0-4b40-936e-422954e7634b" />
* Click the **No Device** option and select any intrested devices from the shown **Mobile** options that are available:
  
     <img width="1280" alt="image" src="https://github.com/user-attachments/assets/6d1b64fa-f33c-4ac4-80d0-aa022e67ad11" />

     * if no mobile options are shown **Install Android Studio** if not or if Installed follow the below Steps
       * Open **CMD (Command Prompt) for Windows or Terminal for Other OS**
       * Run ```flutter doctor```, check if all required components are installed:
         
            <img width="862" alt="image" src="https://github.com/user-attachments/assets/cac14447-23b1-45b5-8c84-ba543647696b" />
       * if any of these are not installed, install and update the components.
* A Mobile Simulation will be opened like the image shown below:
  
     <img width="1280" alt="image" src="https://github.com/user-attachments/assets/2cc291c6-c479-417d-901c-1fdf7558798e" />
* Navigate to the Path:
```
src/mobile_frontend/lib/main.dart
```
* Click **Run** as shown in the image:
  
     <img width="1280" alt="image" src="https://github.com/user-attachments/assets/be847536-7f18-47a7-a2be-85c08f93c5d8" />
     <img width="168" alt="image" src="https://github.com/user-attachments/assets/e07ac80f-67c1-40a7-a84f-dffe1cf6d5cb" />

* After the app runs, click the top right button to enter the link that got as an output after running ```terraform apply```
  
  <img width="1280" alt="image" src="https://github.com/user-attachments/assets/a0c146b1-0506-4c71-a8a6-2e88d7af24e0" />
  <img width="1280" alt="image" src="https://github.com/user-attachments/assets/e812b09b-ed0a-4f74-9cc4-06f4c3b46b1b" />
  
* Start asking question and have fun
  
  <img width="1280" alt="image" src="https://github.com/user-attachments/assets/4208194e-ef1e-4c05-9341-af44c8611f2a" />
  <img width="1280" alt="image" src="https://github.com/user-attachments/assets/bede3e35-8da9-4940-bb72-655d029260be" />





