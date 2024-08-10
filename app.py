from flask import Flask,send_file,render_template,request,redirect,url_for,flash,session
from user import user_operation
from encryption import Encryption
from myrandom import randomalphanum,randomnumber
from captcha.image import ImageCaptcha
from myemail import Email
from validate import myvalidate
import voice_search
import razorpay
from datetime import datetime
from chart import chart_op

app = Flask(__name__)
app.secret_key='futyu567fuf6r6fh'

client = razorpay.Client(auth=("rzp_test_ncA8cq0QRQXDlq", "oAa0hlEpbvYHrg3Of8G139kE"))

m = Email(app)   # activate Email object

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user_signup',methods=['GET','POST'])
def user_signup():
    if(request.method=='GET'):
        text = randomalphanum()
        img = ImageCaptcha(width = 280, height = 90)
        # Image captcha text
        global captcha_text
        captcha_text = text  
        # write the image on the given file and save it
        img.write(captcha_text,'static/captcha/user_captcha.png')
        return render_template("user_signup.html")
    elif(request.method=='POST'):
        if(captcha_text != request.form['captcha']):
            flash("invalid captcha.....")
            return redirect(url_for('user_signup'))
        
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        #-- password encryption---------
        e = Encryption()
        password = e.convert(password)
        #---insertion-------------------
        ob = user_operation() # object create
        ob.user_signup_insert(fname,lname,email,mobile,password)
        #------ email otp send-----------------
        global otp
        otp = randomnumber()
        subject="dzinex verification code"
        message="hi "+fname+" "+lname+"\nYour OTP is: "+ str(otp)+"\n Thank You\n Dzinex Technologies"
        m.compose_mail(subject,email,message)  # calling
        return render_template("user_email_verify.html",email=email)

@app.route('/user_email_verify',methods=['GET','POST'])
def user_email_verify():
    if(request.method=='POST'):
        if(str(otp) == request.form['otp']):
            flash("Your Email is Verified... You can Login Now!!")
            return redirect(url_for('user_login'))
        else:
            email=request.form['email']
            ob = user_operation()
            ob.user_delete(email)
            flash("Invalid OTP...Your Email is not verified.. Try Again to Register!!")
            return redirect(url_for('user_signup'))
    else:
        return "page can not be access!!"


@app.route('/user_login',methods=['GET','POST'])
def user_login():
    if(request.method=='GET'):
        return render_template("user_login.html")
    else:
        email = request.form['email']
        password = request.form['password']
        #-- validatation ---------------
        v = myvalidate()
        frm=[email,password]
        if(not v.required(frm)):
            flash("field can not be empty!!")
            return redirect(url_for('user_login'))

        #-- password encryption---------
        e = Encryption()
        password = e.convert(password)

        ob = user_operation()
        rc=ob.user_login(email,password)
        if(rc==0):
            flash("invalid email or password!!")
            return redirect(url_for('user_login'))
        else:
            return redirect(url_for('user_dashboard'))
            # return session['fname']

@app.route('/user_logout',methods=['GET','POST'])
def user_logout():
    if('email' in session):
        if(request.method=='GET'):
            session.clear()
            return redirect(url_for('index'))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))



@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    if('email' in session):
        if(request.method=='GET'):
            ob=user_operation()
            ob.cart_count()
            c = chart_op()
            c.chart_show()
            return render_template("user_dashboard.html")
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))
    

@app.route('/user_profile',methods=['GET','POST'])
def user_profile():
    if('email' in session):
        if(request.method=='GET'):
            ob = user_operation()
            record = ob.user_profile()
            return render_template("user_profile.html",record=record)
        else:
            fname = request.form['fname']
            lname = request.form['lname']
            mobile = request.form['mobile']
            ob = user_operation()
            ob.user_profile_update(fname,lname,mobile)
            flash("your profile is updated successfully!!")
            return redirect(url_for('user_profile'))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_password',methods=['GET','POST'])
def user_password():
    if('email' in session):
        if(request.method=='GET'):
            return render_template("user_password.html")
        else:
            old_password = request.form['old_password']
            new_password = request.form['new_password']
            
            #-- password encryption---------
            e = Encryption()
            old_password = e.convert(old_password)
            new_password = e.convert(new_password)

            ob = user_operation()
            r=ob.user_password(old_password,new_password)
            if(r==1):
                session.clear()
                flash("your password is updated successfully!!")
                return redirect(url_for('user_login'))
            else:
                flash("your old password is invalid...")
                return redirect(url_for('user_password'))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_account_delete',methods=['GET','POST'])
def user_account_delete():
    if('email' in session):
        if(request.method=='GET'):
            ob = user_operation()
            ob.user_delete(session['email'])
            flash("your account is deleted permanently!!")
            return redirect(url_for('index'))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_photo_upload',methods=['GET','POST'])
def user_photo_upload():
    if('email' in session):
        if(request.method=='GET'):
            return render_template("user_photo_upload.html")
        else:
            category = request.form['category']
            descp = request.form['descp']
            charges = request.form['charges']
            photo = request.files['photo']

            p = photo.filename  # retrive photo name with extention
            d = datetime.now() #current date time
            t=int(round(d.timestamp()))
            path = str(t)+'.'+p.split('.')[-1]
            photo.save("static/photo/" + path)
           
            ob = user_operation()
            ob.user_photo_upload(category,descp,charges,path)
            flash("photo is uploaded successfully!!")
            return redirect(url_for('user_photo_upload'))            
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))   

@app.route('/user_photo_delete', methods=["GET", "POST"])
def user_photo_delete():
    if('email' in session):
        if(request.method=='GET'):
            photo_id=request.args.get('photo_id')
            ob = user_operation()
            ob.user_photo_delete(photo_id)
            flash("photo is deteled successfully!!")
            return redirect(url_for('user_photo_view'))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_photo_details', methods=["GET", "POST"])
def user_photo_details():
    if('email' in session):
        if(request.method=='GET'):
            photo_id=request.args.get('photo_id')
            ob = user_operation()
            record=ob.user_photo_details(photo_id)
            return render_template("user_photo_details.html",
                                   record=record)    
        else:
            photo_id=request.args.get('photo_id')
            category = request.form['category']
            descp = request.form['descp']
            charges = request.form['charges']
            ob = user_operation()
            record=ob.user_photo_details_update(photo_id,category,descp,charges)
            flash("your photo is updated successfully!!")
            return redirect(url_for('user_photo_details',photo_id=photo_id))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_photo_view',methods=['GET','POST'])
def user_photo_view():
    if('email' in session):
        if(request.method=='GET'):
            ob = user_operation()
            record=ob.user_photo_view()
            return render_template("user_photo_view.html",
                                   record=record)      
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))   

@app.route('/user_photo_category',methods=['GET','POST'])
def user_photo_category():
    if('email' in session):
        if(request.method=='GET'):
            category = request.args.get('category')
            ob = user_operation()
            record=ob.user_photo_category(category)
            return render_template("user_photo_search.html",record=record)      
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))   

@app.route('/user_voice_search',methods=['GET','POST'])
def user_voice_search():
    if('email' in session):
        if(request.method=='GET'):
            try:  
                category = voice_search.search()
            except:
                flash("voice is not audible!!")
                return render_template("user_photo_search.html")
            
            ob = user_operation()
            record=ob.user_photo_category(category)
            return render_template("user_photo_search.html",record=record,category=category)      
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))



@app.route('/user_cart', methods=["GET", "POST"])
def user_cart():
    if('email' in session):
        if(request.method=='GET'):
            photo_id=request.args.get('photo_id')

            ob = user_operation()
            ob.user_cart(photo_id)
            flash("product is added successfully in your cart!!")
            return redirect(url_for('user_photo_view'))
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))
    
@app.route('/user_cart_view', methods=["GET", "POST"])
def user_cart_view():
    if('email' in session):
        if(request.method=='GET'):
            ob = user_operation()
            record=ob.user_cart_view()
            total=ob.cart_sum()
            return render_template("user_cart.html",record=record,total=total)
            
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/pay', methods=["GET", "POST"])
def pay():
    if('email' in session):
        if(request.method=='GET'):
            amount=int(request.args.get('total'))

            data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            pdata=[amount*100, payment["id"]]
            return render_template("payment.html", pdata=pdata)
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/success', methods=["POST"])
def success():
    if('email' in session):
        if(request.method=='POST'):
            pid=request.form.get("razorpay_payment_id")
            ordid=request.form.get("razorpay_order_id")
            sign=request.form.get("razorpay_signature")
            # created_at=request.form.get("razorpay_created_at")
            params={
            'razorpay_order_id': ordid,
            'razorpay_payment_id': pid,
            'razorpay_signature': sign
            }
            final=client.utility.verify_payment_signature(params)
            if final == True:
                ob = user_operation()
                ob.payment(pid,ordid)
                ob.purchase(pid,ordid)
                ob.cart_delete_all()
                flash("Payment Done Successfully!! payment ID is "+str(pid))
                return redirect(url_for('user_purchase_history'))
            return "Something Went Wrong Please Try Again"
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_purchase_history', methods=["GET", "POST"])
def user_purchase_history():
    if('email' in session):
        if(request.method=='GET'):
            ob = user_operation()
            record=ob.user_purchase_history()
            return render_template("user_purchase_history.html",record=record)  
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))

@app.route('/user_photo_download', methods=["GET", "POST"])
def user_photo_download():
    if('email' in session):
        if(request.method=='GET'):
            path=request.args.get('path')
            return send_file('static/photo/'+path,as_attachment=True)            
    else:
        flash("you are not authorized to access this page.. please login first")
        return redirect(url_for('user_login'))


if __name__=='__main__':
    app.run(debug=True)      #server activate




