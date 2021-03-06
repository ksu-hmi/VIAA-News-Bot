# Import the class `Flask` from the `flask` module
from flask import Flask, render_template, request, make_response
from Resultsfromkeywordsearch import *
from keywordsearchscript import *
from twitter import *

# Instantiate a new web application called `app`, with `__name__` representing the current file
app=Flask(__name__)
#The@app.route commands define the URLs in the website. 
#The specific functions directly after@app.route define what happens when those URLs are visited 
@app.route('/results', methods=['POST','GET'])
#The greet() function sets up the response for the submission form in home.html returning the response to home.htm

#Show search results
def results():
    if request.method == 'POST':
        inputName = request.form['myName']
        inputUserId = request.form['userID']
    else:
        inputUserId = request.cookies.get('userID')
        inputName = request.cookies.get('myName')    
        
    results = url_table(inputUserId)
    ip = request.remote_addr
    #write data to file or to DB
    inputName = inputName.title()

    resp = make_response(render_template("results.html",myName=inputName, results=results))
    resp.set_cookie('myName', inputName)
    resp.set_cookie('userID', inputUserId)

    return resp


#Show user their keywords
@app.route('/keyword', methods=['POST', 'GET'])

def keyword():
    inputUserId = request.cookies.get('userID')
    inputName = request.cookies.get('myName')

    if request.method == 'POST':
         inputnew_word = request.form['new_keywords']
         create_keyword(inputUserId,inputnew_word)
         do_searches(inputnew_word)
         
         
    keywords = keyword_table(inputUserId)

    #inputword = request.form['word']

    #write data to file or to DB
    return render_template("keyword.html",keywords=keywords, myName=inputName)

#Tweet the url
@app.route('/tweet', methods=['POST'])
def tweet():
    post=request.form['Tweet']
    postTweet(post)
    print(post)
    inputUserId = request.cookies.get('userID')
    inputName = request.cookies.get('myName')

    return render_template("twitter.html",myName=inputName)
  
#Delete url record
@app.route('/deleterecord', methods=['POST'])
def deleterecord():
    delurl = request.form['Delete']
    inputUserId = request.cookies.get('userID')
    inputName = request.cookies.get('myName')
    
    query = "DELETE FROM url WHERE  url = ?;"

    try:
        
        # execute the query
        conn = create_connection(r"dbVIAA.db")
        cur = conn.cursor()
        cur.execute(query, (delurl,))

        # accept the change
        conn.commit()

    except Error as error:
        print(error, ": Failed to delete record")

    finally:
        cur.close()
        conn.close()
    return render_template("deletedrecord.html",myName=inputName)
    
    

#Delete keyword 
@app.route('/deletekey', methods=['POST'])
def deletekey():
    delkey = request.form['DeleteWord']
    inputUserId = request.cookies.get('userID')
    inputName = request.cookies.get('myName')
    
    print(delkey)

    query = "DELETE FROM keyword WHERE  keyword = ?;"

    try:
        
        # execute the query
        conn = create_connection(r"dbVIAA.db")
        cur = conn.cursor()
        cur.execute(query, (delkey,))

        # accept the change
        conn.commit()

    except Error as error:
        print(error, ": Failed to delete keyword")

    finally:
        cur.close()
        conn.close()
    return render_template("deletekeyword.html",myName=inputName)


# Homepage
@app.route('/')
#In home(), Python callsFlask’s render_template function, which looks in the “templates” folder for the file mentioned
#and passes the variable myName to the template as blank by default. The home.html file says
#it extends layout.html. So, the render_template function goes to layout.html and assembles
#the html response, inserting home.html as a block named “content” where indicated
def home():
    
    return render_template("home.html",myName="")

if __name__=="__main__":
    app.run(debug=True)



