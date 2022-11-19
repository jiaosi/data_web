
from flask import Flask, render_template

# import db

app = Flask(__name__)



@app.route('/')
def index():
#    sql='select * from gold.gold_trend limit 15'
#    na=()
#    results=db.get_record(sql,na)
#    results.reverse()
#    d_array=[]
#    for result in results:
#        d_array.append([int(result[0]), result[1]])
#    return render_template('index.html', result=d_array)
    return 'hhhhh'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
