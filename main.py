from starlette.responses import RedirectResponse
import boto3
from botocore.exceptions import ClientError
from fastapi import  Request, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://itgeeky.github.io/portfolio-eng/",
    "https://itgeeky.github.io",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')


@app.post("/ses_mail", tags=["GENERAL"])
async def ses_mail(data: str, request: Request):
    SENDER = f'Notificaciones Kiva <info@zitus.mx>'
    RECIPIENT = 'carlos.asp44@gmail.com'
    CONFIGURATION_SET = "Track_Opens_Clicks"
    AWS_REGION = "us-west-1"
    SUBJECT = "Notificación de Portafolio"
  
    BODY_HTML = """<html>
        <head></head>
        <body>
          <h1>Amazon SES Test (SDK for Python)</h1>
          <p>This email is a notification of your portfolio.</p>
          <p>Here is the data:</p>
          <p>{data}</p>
        </body>
        </html>
        """.format(data=data)
    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
           "This email is a notification of your portfolio.\r\n"
           "Here is the data:\n{data}\n".format(data=data)) 
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                        region_name=AWS_REGION)
    
    try:
      response = client.send_email(
          Destination={
              'ToAddresses': [
                  RECIPIENT,
              ],
          },
          Message={
              'Body': {
                  'Html': {
                      'Charset': CHARSET,
                      'Data': BODY_HTML,
                  },
                  'Text': {
                      'Charset': CHARSET,
                      'Data': BODY_TEXT,
                  },
              },
              'Subject': {
                  'Charset': CHARSET,
                  'Data': SUBJECT,
              },
          },
          Source=SENDER,
          # If you are not using a configuration set, comment or delete the
          # following line
          ConfigurationSetName=CONFIGURATION_SET,
      )
  # Display an error if something goes wrong.	
    except ClientError as e:
        raise HTTPException(status_code=400, detail="Error: {0}".format(e.response['Error']['Message']))
    else:
        return {"message": "Email sent! Message ID: {0}".format(response['MessageId'])}
      