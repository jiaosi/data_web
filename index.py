
from flask import Flask, render_template
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import db
from io import BytesIO
import base64
from wsgiref.simple_server import make_server


app = Flask(__name__)



@app.route('/')
def index():
    sql = "select * from mytest_db.house_trade_data where str_to_date(date, '%Y/%m/%d') between date_sub(now(), interval 60 day) and now();"
    mydb = db.DB()
    data = pd.read_sql(sql, mydb.db)
    mydb.close()
    data['date'] = pd.to_datetime(data['date'], format='%Y/%m/%d')
    data = data.sort_values('date')

    fig, ax = plt.subplots(figsize=(20, 6))
    # data.fillna(0, inplace = True)
    data['new_residence_num'] = data['new_residence_num'].astype('int')
    data['old_residence_num'] = data['old_residence_num'].astype('int')
    ax.set_xlim(data['date'].values[-1], data['date'].values[0])
    ax.bar(data['date'], data['new_residence_num'], label='new_residence_num')
    ax.bar(data['date'], data['old_residence_num'], label='old_residence_num', alpha=0.5)
    plt.legend(loc='upper left')
    plt.xticks(rotation=30)

    ax2 = ax.twinx()
    ax2.plot(data['date'],
             data[['new_residence_area', 'date']].apply(lambda x: np.nan if x[1].weekday() in (5, 6) else float(x[0]),
                                                        axis=1)
             / data['new_residence_num'], label='average_new_area',
             linestyle='-.')
    ax2.plot(data['date'],
             data[['old_residence_area', 'date']].apply(lambda x: np.nan if x[1].weekday() in (5, 6) else float(x[0]),
                                                        axis=1)
             / data['old_residence_num'], label='average_old_area',
             linestyle='-.')
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

# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0')

# server = make_server("", 6001, app)
# server.serve_forever()  # poll_interval轮询时间
