# 导入模块区域。
from flask import Flask, render_template, request, redirect, url_for, session
from model import db, User, Question, Option, Response
from security import encrypt_password,decrypt_password
import sqlite3
from datetime import datetime
# Flask用于创建应用，render_template用于渲染HTML模版，request用于处理请求，redirect和url_for用于重定向和生成URL


import os
print(f"Database path: {os.path.abspath('database.db')}")



# 创建Flask应用区域。
app = Flask(__name__) #创建Flask应用实例
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' #配置数据库URL，使用的是SQLite数据库，文件名为database.db
app.secret_key = 'your_secret_key' #设置应用的密钥，用于会话加密和CSRF保护
db.init_app(app) #初始化数据库，将数据库实例与Flask应用关联起来


# 创建数据库表区域。
with app.app_context(): #创建应用上下文，确保数据库操作在正确的上下文中执行
    db.create_all() #创建所有定义的数据库表格


# 路由区域
# 注册路由区域。处理用户注册请求，支持GET和POST方法。GET方法渲染注册页面，POST方法处理注册逻辑。
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        education_level = request.form['education_level']
        email = request.form['email']

        # print(f"Received username: {username}, password: {password}")
        encrypted_password = encrypt_password(password)
        # print(f"Encrypted password: {encrypted_password}")
        
        new_user = User(username=username, password=encrypted_password, age=age, education_level=education_level, email=email)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

# 创建根路径路由
@app.route('/')
def home():
    return render_template('home.html')

# 创建登录路由
@app.route('/login', methods=['GET', 'POST']) #定义/login路由，支持GET和POST请求
def login():
    # 从表单中获取用户输入的用户名和密码
    if request.method == 'POST':
        input_username = request.form['username']
        input_password = request.form['password']

        # 查找用户
        user = User.query.filter_by(username=input_username).first()

        if user:
            try:
                # 解密数据库中加密的密码
                decrypted_password = decrypt_password(user.password)

                if decrypted_password == input_password:
                    session['user_id'] = user.id  # 记录用户登录状态
                    return redirect(url_for('home'))
                else:
                    return "密码错误，请重试。"
            except Exception as e: #这里捕获异常，处理解密过程中可能出现的错误
                return f"解密失败，可能是密钥文件缺失或错误：{str(e)}"
        else:
            return "用户名不存在。"

    return render_template('login.html')

# 评估路由区域
@app.route('/submit_survey', methods=['GET', 'POST'])
def submit_survey():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    

    
    # 获取当前时间和开始时间
    from datetime import datetime
    end_time = datetime.utcnow()  # 获取当前时间
    global start_time  # 使用全局变量存储的开始时间
    time_taken = (end_time - start_time).total_seconds()  # 计算时间差（以秒为单位）

    
    #用户填写的内容传至数据库
    conn = sqlite3.connect('instance/database.db')#连接数据库
    cursor = conn.cursor()

    # 从表单数据中获取用户 ID
    userid = session.get('user_id')
    if not userid:
        return "用户 ID 缺失，请重新登录并提交评估。", 400
    # 打印表单数据
    # print("表单数据:", request.form)

    # 遍历表单数据
    for questionID, optionID in request.form.items():

        questionID = int(questionID)  # 问题 ID
        optionID = int(optionID)  # 选项 ID
        r_time = time_taken  # 使用计算的时间差
        cursor.execute("""
            INSERT INTO response (id, questionID, optionID, r_time)
            VALUES (?, ?, ?, ?)
        """, (userid, questionID, optionID,  r_time))


    # print("接受数据:",userid, questionID, optionID, r_time)

    conn.commit()# 提交事务,将插入的数据保存到数据库中
    conn.close()# 关闭数据库连接

    # 假设每个维度的权重如下（权重总和为1）
    dimension_weights = {
        '用户背景': 0.2,
        '学习能力': 0.15,
        '语言能力': 0.25,
        '适应能力': 0.1,
        '社交能力': 0.2,
        '主观能动性': 0.1
}


    # 处理用户提交的问卷，给分数
    if request.method == 'POST':
        form_data = request.form # 获取用户提交的表单数据，包括问题ID和选项ID
        scores_by_dimension = {} # 用于存储每个维度的分数
        question_scores = [] #创建一个列表用于保存“每道题的得分”

        #遍历用户提交的内容
        for question_id, option_id in form_data.items():
            question = Question.query.get(int(question_id))
            option = Option.query.get(int(option_id))
            
            #把这道题的题目和得分记录进列表
            question_scores.append({
                'question_id': question_id,
                'score': option.score
                })

            # 分类加分
            dimension = question.category
            scores_by_dimension.setdefault(dimension, 0)
            scores_by_dimension[dimension] += option.score

        # 这里我们假设每个维度满分是 10 分，标准化为百分制
        standardized = {
            dim: min(100, v / 10 * 100) for dim, v in scores_by_dimension.items()
        }

        if not standardized:
            return "未提交任何有效数据，请重新填写问卷。", 400

        # 计算加权总分
        total_score = sum(
            standardized[dim] * dimension_weights.get(dim, 0) for dim in standardized
            )


        return render_template("result.html", scores=standardized, total_score=round(total_score, 2),question_scores=question_scores)

    # GET 请求：展示问卷
    questions = Question.query.all()
    return render_template("assessment.html", questions=questions)

# 评估题目生成路由
@app.route('/survey')
def survey():
     # 检查用户是否已登录
    if 'user_id' not in session:
        return redirect(url_for('login'))  # 如果未登录，重定向到登录页面
  
     # 记等一下录用户开始评估的时间（直接获取系统时间）
    global start_time  # 使用全局变量存储开始时间
    start_time = datetime.utcnow()  # 使用 UTC 时间，避免时区问题
    
    # 连接数据库
    conn = sqlite3.connect('instance/database.db') 
    cursor = conn.cursor()

    # 获取所有题目
    cursor.execute("SELECT QuestionID, Question FROM assessment")
    questions = cursor.fetchall()
    # print(f"问题: {questions}")

    # 获取所有选项（通用选项）
    cursor.execute("SELECT optionID, content_of_option, score FROM option")
    common_options = cursor.fetchall()
    # print(f"选项: {common_options}")

    conn.close()

    # 整理成字典结构
    question_list = []
    for q in questions:
        q_id, q_content = q
        question_list.append({
            'id': q_id,
            'content': q_content,
            'options': common_options  # 所有问题使用相同的选项
        })
        # print(f"问题ID: {q_id}, 内容: {q_content}, 选项: {common_options}")
    


    return render_template('assessment.html', questions=question_list)

#历史记录路由
@app.route('/history')
def history():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    records = Response.query.filter_by(id=user_id).order_by(Response.responseid.desc()).all()
    
    
    return render_template('history.html', records=records)

# 个人资料路由
@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    return render_template('profile.html', user=user)



# 启动区域
if __name__ == '__main__': #确保只有在直接运行此文件时才启动应用，而不是在被其他文件导入时。
    app.run(debug=True) # 启动Flask应用，debug=True表示启用调试模式，便于开发和调试
