# -*- coding: utf-8 -*-

from flask import Flask, render_template, flash, redirect, url_for, request, session, jsonify
from database import DBhandler
import hashlib
import sys
import math

application = Flask(__name__)
application.config["SECRET_KEY"]="helloosp"

DB=DBhandler()


@application.route("/")
def hello():
    #return render_template("index.html")
    return redirect(url_for('view_list'))

@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")


@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup")
def signup():
    return render_template("signup.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash=hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else :
        flash("user id already exist!")
        return render_template("signup.html")

@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int)  # 페이지를 0부터 시작하도록 조정
    category = request.args.get("category", "all")
    per_page = 6
    per_row = 3
    row_count = int(per_page / per_row)
    start_idx = per_page * page  # 시작 인덱스를 조정
    end_idx = per_page * (page + 1)
    if category == "all":
        data = DB.get_items()
    else:
        data = DB.get_items_bycategory(category)
    data = dict(sorted(data.items(), key=lambda x: x[0], reverse=False))
    item_counts = len(data)

    # 데이터 길이를 넘어가지 않도록 끝 인덱스를 조정
    end_idx = min(end_idx, item_counts)

    data = dict(list(data.items())[start_idx:end_idx])

    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count - 1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i * per_row:(i + 1) * per_row])

    return render_template(
        "list.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts / per_page)),  # 페이지 수 계산 수정
        total=item_counts,
        category=category
        )

@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@application.route("/submit_item_post", methods=['POST'])
def reg_item_submit_post():
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    data=request.form
    DB.insert_item(data['name'], data, image_file.filename)
    return redirect(url_for('view_item_detail', name=data['name']))

@application.route("/reg_review_init/<name>/")
def reg_review_init(name):
    return render_template("reg_reviews.html", name=name)

@application.route("/reg_review", methods=['POST'])
def reg_review():
    data=request.form
    image_file=request.files["file"]
    image_file.save("static/images/{}".format(image_file.filename))
    DB.reg_review(session['id'], data, image_file.filename)
    return redirect(url_for('view_review'))

@application.route("/review")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page=6 # item count to display per page
    per_row=3 # item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_reviews() #read the table
    item_counts = len(data)
    end_idx = min(end_idx, item_counts)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "review.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)

@application.route("/view_mypage_sell/<name>/")
def view_mypage_sell(name):
    data = DB.get_item_byseller(str(name))
    page = request.args.get("page", 0, type=int)
    per_page = 9
    per_row = 3
    row_count = int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page*(page+1)
    data = dict(sorted(data.items(), key=lambda x:x[0], reverse=False))
    item_counts = len(data)
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else :
        data = dict(list(data.items())[start_idx:end_idx])
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "mypage_sell.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)+1),
        total=item_counts,
        name=name)

@application.route("/view_mypage_review/<name>/")
def view_mypage_review(name):    
    data = DB.get_review_byseller(str(name))
    page = request.args.get("page", 0, type=int)
    per_page = 9
    per_row = 3
    row_count = int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page*(page+1)
    data = dict(sorted(data.items(), key=lambda x:x[0], reverse=False))
    item_counts = len(data)
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else :
        data = dict(list(data.items())[start_idx:end_idx])
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "mypage_review.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)+1),
        total=item_counts,
        name=name)

@application.route("/view_review_detail/<name>/")
def view_review_detail(name):
    print("###name:", name)
    data = DB.get_review_byname(str(name))
    print("###data:", data)
    return render_template("review_detail.html", name=name, data=data)

@application.route("/view_mypage_like/<name>/")
def view_mypage_like(name):
    data = DB.get_item_bylike(str(name))
    page = request.args.get("page", 0, type=int)
    per_page = 9
    per_row = 3
    row_count = int(per_page/per_row)
    start_idx = per_page * page
    end_idx = per_page*(page+1)
    data = dict(sorted(data.items(), key=lambda x:x[0], reverse=False))
    item_counts = len(data)
    if item_counts <= per_page:
        data = dict(list(data.items())[:item_counts])
    else :
        data = dict(list(data.items())[start_idx:end_idx])
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)

    for i in range(row_count):
        if (i == row_count-1) and (tot_count % per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else:
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])

    return render_template(
        "mypage_like.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int(math.ceil(item_counts/per_page)+1),
        total=item_counts,
        name=name)
    

@application.route('/dynamicurl/<varible_name>/')
def DynamicUrl(varible_name):
           return str(varible_name)

@application.route("/view_detail/<name>/")
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name))
    print("####data:",data)
    return render_template("detail.html", name=name, data=data)
    
@application.route('/buy_item/<name>/')
def buy_item(name):
    data = DB.get_item_byname(str(name))
    data = DB.update_sold(session['id'], name, data)
    return redirect(url_for('reg_review_init', name=name))

@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})

@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})

@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '안좋아요 완료!'})

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)