from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
import os
from twilio.rest import Client

app = Flask(__name__,template_folder='templates',static_folder='static')
app.secret_key='a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID= gwh62384;PWD=eIGC0Tj1qTFaHzj6;", "", "")
print(conn)
print('connected')
