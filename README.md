# 281 group project

- [Project Link](https://master.d350pue95ehqmp.amplifyapp.com/)
- University Name: [San Jose State University](https://www.sjsu.edu/)
- Course: [CMPE-281](http://info.sjsu.edu/web-dbgen/catalog/courses/CMPE281.html)
- Professor: [Sanjay Garje](https://www.linkedin.com/in/sanjaygarje/)
- Student: [Fuyu Zhang](https://www.linkedin.com/in/nick-fuyuzhang/)
- Group: **3 Musketeers**

## Project Introduction:
- Itemize is a **SaaS (high-availability, scalable)** product that will group and categorize receipts as well as group itemized deductions, and provide reports for current tax progress.
- This repository is only for User, File and Receipt Service(check below):
  - [UserServiceDocument](https://docs.google.com/document/d/1mFw37FflMAH4pQo6egnk_jDiAx9npc11bZhW1aBl_3A/edit#heading=h.vnx1s6kennwd)
  - [FileServiceDocument](https://docs.google.com/document/d/1a_ARMF7awQmDEbrisUtk7oTXrhmoIvs7TR6NWhrh614/edit#heading=h.759pwl7gx55k)
  - [ReceiptServiceDocument](https://docs.google.com/document/d/1IoJumF7RcuCMLGsXvg1rAxpNwx2pB1eDClIwsImgIn8/edit#heading=h.sbbjz5c86byh)

## ScreenShot:
- Invalid input & No Data
<img src="https://github.com/Handsomenick1/281grouppj/blob/main/pic/Screen%20Shot%202021-11-23%20at%2011.06.52.png" alt="1" style="text-align:center; width:1000px;"/> 
<img src="https://github.com/Handsomenick1/281grouppj/blob/main/pic/Screen%20Shot%202021-11-23%20at%2011.06.38.png" alt="2" style="text-align:center; width:1000px;"/> 

- Successed
<img src="https://github.com/Handsomenick1/281grouppj/blob/main/pic/Screen%20Shot%202021-11-23%20at%2011.08.44.png" alt="3" style="text-align:center; width:1000px;"/> 

## Feature list: 
- User Service:
  - signup, get, update
- File Service:
  - upload, get, getall, delete
- Receipt Service:
  - upload, get, getall, update, delete, deleteall 
 
## Architecture
<img src="https://github.com/Handsomenick1/281grouppj/blob/main/pic/cmpe281project.drawio.png" alt="arch" style="width:650px;"/>

## Pre-requisites Set Up:
- Required software: Browser(e.g Chrome, Firefox, etc)
- AWS S3, CloudFront, Lambda, DynamoDB, API Gateway.

## Set up locally:
- Download related library
  - [boto3](https://www.linkedin.com/pulse/install-python-aws-sdk-boto3-mac-rany-elhousieny-phd%E1%B4%AC%E1%B4%AE%E1%B4%B0/)
- Run `git clone git@github.com:Handsomenick1/281grouppj.git` to download files
- Go to your Lambda and create functions following the files
- Test them on Lambda based on documents below:
  - [Reciept API](https://docs.google.com/document/d/1IoJumF7RcuCMLGsXvg1rAxpNwx2pB1eDClIwsImgIn8/edit?usp=sharing)
  - [File API](https://docs.google.com/document/d/1a_ARMF7awQmDEbrisUtk7oTXrhmoIvs7TR6NWhrh614/edit#heading=h.759pwl7gx55k)
  - [User API](https://docs.google.com/document/d/1mFw37FflMAH4pQo6egnk_jDiAx9npc11bZhW1aBl_3A/edit#heading=h.vnx1s6kennwd)
- Each testing result will be stored in CloudWatch.
- Create APIs for each of the back-end services on API gateway to connect with the front-end.
- Connect each API as a trigger with corresponding Lambda function. 
- Configure Authorization with Cognito User Pool, and enable Lambda Proxy integration for each method.
- Test them on API gateway, and deploy each API.


## Repository:
- [Rekognition & Lex](https://github.com/pbustos97/CMPE-281-Project-2)
- [Backend](https://github.com/Handsomenick1/281grouppj)
- [Frontend](https://github.com/bfkwong/itemize)

