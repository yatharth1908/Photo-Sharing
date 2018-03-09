from flask import Flask , render_template, request,session
import os

import boto3
from botocore.client import Config


import pymysql

host="*****************"
port=3306
dbname="*****************"
user="*****************"
password="*****************"

conn = pymysql.connect(host, user=user, port=port, passwd=password, db=dbname)

cur = conn.cursor()

allow_reuse_address = True

app = Flask(__name__)
app.secret_key = os.urandom(24)

ACCESS_KEY_ID = "*****************"
ACCESS_SECRET_KEY = "*****************"
BUCKET_NAME = "*****************"

##########################

s3Client = boto3.client('s3',aws_access_key_id=ACCESS_KEY_ID,
  aws_secret_access_key=ACCESS_SECRET_KEY,
  config=Config(signature_version='s3v4'))
#########################

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    config=Config(signature_version='s3v4')
)

directory = "*****************"
url = "*****************"


@app.route('/')
def hello_world():
    return render_template("login.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        total = request.form['img']
        size = request.form['total']
        # print(session.values())
        uname = session['username']
        cur.execute("""INSERT INTO **** VALUES (%s,%s,%s);""", (session['username'],total,size))
    return render_template("index.html")





@app.route('/post', methods=['POST'])
def post():

    if request.method == 'POST':


        f = request.files['file']
        title = request.form['title']
        ratings = request.form['ratings']
        comments = request.form['comments']
        print(f)

        filename = f.filename
        data = directory + filename


        if request.form['click'] == 'Upload Image':
            s3.Bucket(BUCKET_NAME).put_object(Key=filename, Body=open(data, 'rb'), ACL='public-read')
            keys = []
            resp = s3Client.list_objects_v2(Bucket=BUCKET_NAME)
            for obj in resp['Contents']:
                keys.append(obj['Key'])

            image_links = []
            z = len(keys)
            print(z)
            for i in range(z):
                image_links.append(url + keys[i])
            #
            cur.execute("SELECT CONVERT_TZ(NOW(),'-06:00','+00:00')")
            date_time = cur.fetchone()

            print("zero index")
            print(image_links[0])
            print("last index")
            print(image_links[-1])

            print(session['username'])
            cur.execute("""INSERT INTO **** VALUES (%s,%s,%s,%s,%s,%s);""", (image_links[-1], title, ratings, comments, date_time,session['username']))
            conn.commit()


            return "upload successful"

@app.route('/upload', methods=['GET','POST'])
def upload():

    if request.method == 'POST':

        if request.form['click'] == 'View Image':

            cur.execute("""SELECT * FROM ****""")
            data = (cur.fetchall())
            print(data[0])
            instagram = [dict(****=row[0],
                              ****=row[1],
                              ****=row[2],
                              ****=row[3],
                              ****=row[4]) for row in data]

            print(instagram)

            # return '<img src="' + image_links[0]+ '"/>'
            return render_template("gallary.html", instagram=instagram)


@app.route('/download', methods=['POST'])
def download():
    if request.method == 'POST':
        img_name = request.form['files']

        if request.form['download'] == 'Download Image':
            cur.execute("""SELECT **** FROM **** WHERE **** = (%s)""",(img_name))
            img_key = (cur.fetchall())
            str = ''.join(img_key[0])
            str_key= str[43:]
            print(str_key)
            down_path= "*****************"+str_key
            s3Client.download_file(BUCKET_NAME,str_key,down_path)


            return "file downloaded"

        elif request.form['download'] == 'Edit Image':
            cur.execute("""SELECT ****,**** FROM **** WHERE **** = (%s)""",(img_name))
            img_edit = (cur.fetchall())
            instagram_edit = [dict(****=row[0],
                              ****=row[1])
                               for row in img_edit]



            # return '<img src="' + image_links[0]+ '"/>'
            return render_template("edit.html", instagram=instagram_edit)


            return "file edited"


        elif request.form['download'] == 'Delete Image':

         key = request.form['files']
        cur.execute("""SELECT *** FROM *** WHERE ***** = (%s)""", (img_name))
        img_key = (cur.fetchall())
        str = ''.join(img_key[0])
        str_key = str[45:]

        s3Client.delete_object(Bucket=BUCKET_NAME, Key=str_key)
        cur.execute("""DELETE FROM **** WHERE ****** = (%s)""", (key))
        conn.commit()

        return "deleted"





@app.route('/save', methods=['POST'])
def save():
    if request.method == 'POST':
        edit_name= request.form['****']
        ratings_edit = request.form['****']
        comments_edit = request.form['****']

        if request.form['save'] == 'Save Changes':

            cur.execute("""UPDATE **** SET **** = (%s), **** = (%s), **** = (%s) WHERE **** = (%s);""", (ratings_edit,comments_edit,session['username'],edit_name))
            conn.commit()

            return "saved"

if __name__== '__main__':
    app.run(debug=True)