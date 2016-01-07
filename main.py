from flask import Flask, request, render_template
import os.path

app = Flask(__name__)


@app.route('/')
@app.route('/hello')
def hello_world():
    name = request.args.get('name')
    name = name if name else 'Stranger'
    return render_template('hello.html', name=name)

@app.route('/page/<user12>/<password12>')
def page2(user12, password12):
    f = open(user12, "r")
    f2 = f.read()
    f.close()
    f = open(user12 + '.password', "r")
    f4 = f.read()
    f.close()
    f5 = f4.split("<!>")
    if f5[2] == password12:
        ok = "false"
    else:
        ok = "true"   
    f = open(user12 + '.comments', "r")
    f3 = f.read()
    f.close()
    if ok == "true":
        return render_template('correct.html', user=user, c=f5[2])
    else:    
        return render_template('bye.html', s=f2, user=user12, c=f3)

@app.route('/page/<user>')
def goodbye(user):
    f = open(user, "r")
    f2 = f.read()
    f.close()
    f = open(user + '.password', "r")
    f4 = f.read()
    f.close()
    f5 = f4.split("<!>")
    if len(f5) == 4:
        ok = "true"
    else:
        ok = "false"   
    f = open(user + '.comments', "r")
    f3 = f.read()
    f.close()
    if ok == "true":
        return render_template('correct.html', user=user, c=f5[2])
    else:    
        return render_template('bye.html', s=f2, user=user, c=f3)
    
@app.route('/sign-in', methods = ['POST'])
def signin():
    if request.method == 'POST':
        name = request.form['firstname']
        pas = request.form['lastname']
        f = open(name + '.password', "r")
        f2 = f.read()
        f3 = f2.split("<!>")
        f.close()
        print f3[1]
        if pas == f3[1]:
            c = '<a style="font-size:100px;" href="/edit/' + name + '/' + pas + '">Edit Blog</a><br><a style="font-size:100px;" href="/page/' + name + '">View Blog</a><br><a style="font-size:100px;" href="/?name=' + name + '">Home</a>'
        else:
            c = "Account Doesn't Exist."   
        return render_template('what.html', c=c)

@app.route('/create', methods = ['POST'])
def create():
    if request.method == 'POST':
        name = request.form['firstname']
        pas = request.form['lastname']
        passw = request.form['password']
        a = os.path.isfile(name)
        if a == False:
            f = open(name, "w")
            f.close()
            f = open(name + '.comments', "w")
            f.close()
            if passw == '': 
                f = open(name + '.password', "w")
                f.write('<!>' + pas + '<!>')
                f.close()
            else:
                f = open(name + '.password', "w")
                f.write('<!>' + pas + '<!>' + passw + '<!>')
                f.close()  
                c = '<a style="font-size:100px;" href="/edit/' + name + '/' + pas + '">Edit Blog</a><br><a style="font-size:100px;" href="/page/' + name + '">View Blog</a><br><a style="font-size:100px;" href="/?name=' + name + '">Home</a>'
        else:
            c = '<font color="red">User Already Exists!</font>'      
       
        return render_template('what.html', c=c)
        
@app.route('/edit/<user1>/<password1>', methods = ['GET', 'POST'])
def edit(user1, password1):
    if request.method == 'GET':
        f = open(user1 + '.password', "r")
        p = f.read()
        p2 = p.split("<!>")
        f.close()
        if password1 == p2[1]:
            f = open(user1, "r")
            f2 = f.read()
            f.close()
        else:
            f2 = "Wrong Password or Username."    
        return render_template('form.html', info=[f2])
    elif request.method == 'POST':
        content = request.form['content']
        f = open(user1 + '.password', "r")
        p = f.read()
        p2 = p.split("<!>")
        f.close()
        if password1 == p2[1]:
            f = open(user1, "w")
            f.write("<div style='border:8px solid white;'><font color='black'>" + content + "</font></div>")
            f.close()
            f = open(user1, "r")
            f2 = f.read()
            f.close()
        else:
            f2 = "Wrong Password or Username."    
        return render_template('form.html', info=[f2])
        
@app.route('/comment/<user2>', methods = ['POST'])
def comment(user2):
    if request.method == 'POST':
        name = request.form['1']
        comment = request.form['2']
        f = open(user2 + '.comments', "a+")
        f.write('<div style="background-color:#571B7E;border:10px solid #571B7E;><font color="black">Comment by:&nbsp;<b>' + name + '</b><br>' + comment + '</font></div><br><br>')
        f.close()
        f = open(user2 + '.comments', "r")
        f3 = f.read()
        f.close()
        f = open(user2, "r")
        f2 = f.read()
        f.close()
        return render_template('bye.html', s=f2, user=user2, c=f3)
        
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)

