
from flask import Flask, render_template
from matplotlib import pyplot as plt
import pandas as pd
import db
from io import BytesIO
import base64

app = Flask(__name__)



@app.route('/')
def index():
    sql = "select * from mytest_db.house_trade_data where str_to_date(date, '%Y/%m/%d') between date_sub(now(), interval 60 day) and now();"
    na = ()
    results = db.get_record(sql, na)
    results.reverse()
    d_array = []
    for result in results:
        d_array.append([result[4], result[7], result[9]])
    data = pd.DataFrame(d_array)
    data.columns = ['new', 'old', 'date']
    data['date'] = pd.to_datetime(data['date'])

    fig, ax = plt.subplots(figsize=(20, 6))
    # data.fillna(0, inplace = True)
    data['new'] = data['new'].astype('int')
    data['old'] = data['old'].astype('int')
    ax.set_xlim(data['date'].values[-1], data['date'].values[0])
    ax.plot(data['date'], data['new'], label='new')
    ax.plot(data['date'], data['old'], label='old')
    plt.xticks(rotation = 30)
    plt.legend()

    bio = BytesIO()
    plt.savefig(bio, format = 'png')
    data = base64.encodebytes(bio.getvalue()).decode()
    src = 'data:image/png;base64,' + str(data)
    plt.close()
    return render_template('index.html', result=src)
#     return 'hhhhh'

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
