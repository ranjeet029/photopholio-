import mysql.connector
from flask import session
from datetime import date

class user_operation:
    def connection(self):
        con=mysql.connector.connect(host="localhost",port="3306",user="root",password="root",database="b2_full_stack")
        return con
    
    def user_signup_insert(self,fname,lname,email,mobile,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into user (fname,lname,email,mobile,password) values(%s,%s,%s,%s,%s)"

        record=[fname,lname,email,mobile,password]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return  
    
    def user_delete(self,email):
        db=self.connection()
        mycursor=db.cursor()
        sq="delete from user where email=%s"

        record=[email]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return  
    
    def user_login(self,email,password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select fname,email,mobile from user where email=%s and password=%s"
        record=[email,password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        rc=mycursor.rowcount
        if(rc==0):
            return 0
        else:
            session['fname']=row[0][0]
            session['email']=row[0][1]
            session['mobile']=row[0][2]
            return 1
        

    def user_profile(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select fname,lname,email,mobile from user where email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        return row
    
    def user_profile_update(self,fname,lname,mobile):
        db=self.connection()
        mycursor=db.cursor()
        sq="update user set fname=%s,lname=%s,mobile=%s where email=%s"

        record=[fname,lname,mobile,session['email']]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        session['fname']=fname
        session['mobile']=mobile
        return  
    
    def user_password(self,old_password,new_password):
        db=self.connection()
        mycursor=db.cursor()
        sq="select password from user where email=%s and password=%s"
        record=[session['email'],old_password]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        rc=mycursor.rowcount
        if(rc==1):
            sq="update user set password=%s where email=%s"
            record=[new_password,session['email']]
            mycursor.execute(sq,record)
            db.commit()
            mycursor.close()
            db.close()
            return 1
        
        return 0
    
    def user_photo_upload(self,category,descp,charges,path):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into photo (category,descp,charges,path,user_email) values(%s,%s,%s,%s,%s)"

        record=[category,descp,charges,path,session['email']]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return  

    def user_photo_delete(self,photo_id):
        db=self.connection()
        mycursor=db.cursor()
        sq="delete from photo where photo_id=%s"
        record=[photo_id]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return  

    def user_photo_details(self,photo_id):
        db=self.connection()
        mycursor=db.cursor()
        sq="select category,path,descp,charges,photo_id from photo where photo_id=%s"
        record=[photo_id]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        return row

    def user_photo_details_update(self,photo_id,category,descp,charges):
        db=self.connection()
        mycursor=db.cursor()
        sq="update photo set category=%s,descp=%s,charges=%s where photo_id=%s"
        record=[category,descp,charges,photo_id]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_photo_view(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select category,path,descp,charges,photo_id from photo where user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        return row
    

    def user_photo_category(self,category):
        db=self.connection()
        mycursor=db.cursor()
        sq="select category,path,descp,charges,photo_id from photo where category=%s and user_email !=%s"
        
        record=[category,session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        return row
    
    def payment(self,pid,ordid):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into payment (pid,ordid,user_email,pay_date) values(%s,%s,%s,%s)"
        pay_date=date.today()
        record=[pid,ordid,session['email'],pay_date]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        return  
    
    def user_cart(self,photo_id):
        db=self.connection()
        mycursor=db.cursor()
        sq="insert into cart (user_email,photo_id,cart_date) values(%s,%s,%s)"
        cart_date=date.today()
        record=[session['email'],photo_id,cart_date]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        self.cart_count()  #call cart_count function
        return  
    
    def cart_count(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select count(*) from cart where user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        session['cart']=row[0][0]
        return
    
    def user_cart_view(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select cart_id,c.photo_id,category,path,charges,cart_date from cart c,photo p where c.photo_id=p.photo_id and c.user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        return row
    
    def cart_sum(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select sum(charges) from cart c,photo p where c.photo_id=p.photo_id and c.user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        return row[0][0]

    def cart_delete_all(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="delete from cart where user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        db.commit()
        mycursor.close()
        db.close()
        self.cart_count()  #call cart_count function
        return  
    
    def purchase(self,pid,ordid):
        db=self.connection()
        mycursor=db.cursor()
        sq="select photo_id from cart where user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()

        for r in row:
            sq="insert into purchase(photo_id,pid,ordid,user_email,purchase_date) values(%s,%s,%s,%s,%s)"
            record=[r[0],pid,ordid,session['email'],date.today()]
            mycursor.execute(sq,record)
        
        
        db.commit()
        mycursor.close()
        db.close()
        return

    def user_purchase_history(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select p.photo_id,path from photo p, purchase pu where p.photo_id=pu.photo_id and pu.user_email=%s"
        record=[session['email']]
        mycursor.execute(sq,record)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row

    def category_chart(self):
        db=self.connection()
        mycursor=db.cursor()
        sq="select category,count(category) from photo group by category"
        # record=[session['email']]
        mycursor.execute(sq)
        row=mycursor.fetchall()
        mycursor.close()
        db.close()
        return row