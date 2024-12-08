# File Upload
## Create bucket
- Name
- Region
- Disable Block public access

## Setting IAM

### Create role
- AWS service 
- API Gateway
- S3owner
  - Create inline policy
    - S3
    - Putobject
    - arn:aws:s3:::*/* (ANY)
    - ARN: arn:aws:iam::039612878766:role/S3owner

## API Gateway
- RESTful API
  - APIname: fileupload

- Go into fileupload
  - Create resource
    - Resource:{bucket} 勾CORS
      - Resource:{filename}勾CORS
        - Create Method
          - Method type: PUT
          - AWS service
          - Region: {S3在哪就選哪}
          - HTTP method: PUT
          - Use path override
            - {bucket}/{filename}
            - Exec role:arn:aws:iam::039612878766:role/S3owner (授權API gateway有權限去動S3)
        - Edit Integration request
          - URL path parameters
            - [Name : bucket,  Mapping from : method.request.path.bucket]
            - [Name : filename, Mapping from : method.request.path.filename]
  - API settings
      - Manage media types
        - */*
  - Deploy API to stage

## HTTP PUT: https://spu6uhd1q7.execute-api.ap-northeast-1.amazonaws.com/finalpj/{bucket}/{filename}
- Example: https://spu6uhd1q7.execute-api.ap-northeast-1.amazonaws.com/finalpj/file-system2/test2.pdf

