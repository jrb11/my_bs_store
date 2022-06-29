from re import A
from urllib.request import Request
from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from datetime import datetime
from django.contrib import messages


# Create your views here.
#------------------------------------------ Home Page -------------------------------------------------
def index(request):
    return render(request, 'index.html')


#---------------------------------- User Details Registration -----------------------------------------
def user_details_registration(request):
    print("**********----- In User Details --------********************************************************************")
    
    if request.method == 'POST':

        #Users Details
        First_Name = request.POST['First_Name']
        Last_Name = request.POST['Last_Name']
        #Date_of_Birth = request.POST['Date_of_Birth']
        Email_ID = request.POST['Email_ID']
        #Mobile_No = request.POST['Mobile_No']
        Balance = request.POST['Balance']
        Password = request.POST['Password']
        #Address = request.POST['Address']


        #Users Role
        Users_Role = request.POST['Users_Role']
        print('------- Users_Role From HTML---------', Users_Role)

        print("Data Enter")

        if User_Details.objects.filter(Email_ID=Email_ID).exists():
            messages.error(request,'Email ID already exists')
            print('Email ID already exists')
            return redirect('user_details_registration')

 
        # Buyer_Seller_Role_Get
        user_role_get = User_Role.objects.get(Role_Name=Users_Role) 
        print(user_role_get)

        #User_Details DB Entry with (Foreign KEY - 'Users_Role' passing a object 'Users_Role=user_role_get'.
        user_details = User_Details.objects.create(First_Name=First_Name, Last_Name=Last_Name, Email_ID=Email_ID, Balance=Balance, Password=Password, Users_Role=user_role_get)
        
        ## ---------- Note ----------- ##
        ##Users_Role is Foreign KEY from User_Role table, So pass object in this field for Users_Role not a value
        user_details.save()

        print(user_details) 
	    
        print('----------------------------------- User Details Object Created --------------------------------')
		
        return redirect('user_details_view')
        
    else:
        return render(request, 'user_details_registration.html')


#---------------------------------- User Detaisl View  -----------------------------------------

def user_details_view(request):

    if 'email' in request.session:
        email = request.session['email']
        user_obj = User_Details.objects.filter(Email_ID=email).first()
     
        return render(request, 'user_details_view.html',{'user_data':user_obj})

    else:
        return redirect('user_login')


#---------------------------------- User Login --------------------------------------------------

def user_login(request):
    
    if request.method == 'POST':
        Email_ID = request.POST['Email_ID']
        Password = request.POST['Password']

        user_obj = User_Details.objects.filter(Email_ID=Email_ID, Password=Password).first()
        #print('-------------------------- user object name :-----------------------', user_obj)

        # SET session key name is 'email'
        request.session['email'] = Email_ID

        if user_obj is not None:

            #messages.success(request,'Successfully Login')
            print('-------------------------- Successfully Login')

            #print(user.values())
            seller_obj= User_Role.objects.filter(Role_ID=user_obj.Users_Role_id).first()
            #print(seller_obj)

            if seller_obj.Role_Name == 'Seller':
                print("--------------------------- Your are Seller ------------------------")
                return redirect('seller_product_view')

            else:
                print("--------------------------- Your are Buyer -------------------------")
                return redirect('buyer_product_view')


        else:
            messages.error(request,'Wrong Email or Password')
            print('Wrong Email or Password')
            return render(request, 'user_login.html')
    
    else:
        return render(request, 'user_login.html')

        
#---------------------------------- User Login --------------------------------------------------

def user_logout(request):
    try:
        del request.session['email']
        del request.session['total']
        del request.session['unit']
    except:
        return redirect('user_login')
    print('-------------------------- Successfully Logout')
    return redirect('user_login')
    

#---------------------------------- Product Details Registration ---------------------------------

def product_registration(request):

    #if request.session.has_key('user_obj'):
        if request.method == 'POST':

            Product_Name = request.POST['Product_Name']
            Product_Image = request.FILES['Product_Image']
            Product_Sell_Price = request.POST['Product_Sell_Price']
            Product_Cost_Price = request.POST['Product_Cost_Price']
            Stock_Unit = request.POST['Stock_Unit']
            Create_Date = request.POST['Create_Date']
            Created_By_User = request.POST['Created_By_User']

            print(Created_By_User)
            
            product_user_get = User_Details.objects.get(First_Name=Created_By_User) 
            print(product_user_get)

            #Product DB Entry with (Foreign KEY - 'Created_By_User' passing a object 'Created_By_User=product_user_get'.
            product = Product.objects.create(Product_Name=Product_Name, Product_Image=Product_Image, Product_Sell_Price=Product_Sell_Price, Product_Cost_Price=Product_Cost_Price, Stock_Unit=Stock_Unit, Create_Date=Create_Date, Created_By_User=product_user_get)
            product.save()

            print('-------------------------- Product Object Created ---------------------------')
            return redirect('seller_product_view')

        else:
            return render(request, 'product_registration.html')



#---------------------------------- Seller Product Status Update -------------------------------------------

# Status Toggle Button 'Active' and 'Deactive'
def product_status_update(request, pk):

    if request.method == 'POST':
        print("**********----- In Seller Product Status Update View --------********************************************************************")
        product_data = Product.objects.get(Product_ID=pk)

        if product_data.IS_Deleted is False:
            product_data.IS_Deleted = True
            product_data.save()
            print('Product Status : True', product_data)
            return redirect('seller_product_view')
        else:
            product_data.IS_Deleted = False
            product_data.save()
            print('Product Status : True', product_data)
            return redirect('seller_product_view')

  

#---------------------------------- Seller Product View ---------------------------------------------

def seller_product_view(request):

    print('')
    print("**********----- In Seller Product View --------********************************************************************")
    product_data = Product.objects.all().order_by('Created_By_User')
    #product_data_user = Product.objects.filter(First_Name=request.Created_By_User)
    #print(product_data_user)

    if request.method == 'POST':
        product_is_deleted = request.POST['IS_Deleted']
        print('product_is_deleted -----',product_is_deleted)

        if product_is_deleted == 'on':
            product_data.IS_Deleted = True
            product_data.save()


    # def welcomepage(request):
    # tutorial = Tutorial.objects.filter(user=user).first()
    # if tutorial:
    #     tutorial.is_tutorial = True
    #     tutorial.save()
    # return render(request, "home/welcomepage.html")   


    Email = request.session.get('email')
    #print('Session Get Data------',Email)

    login_user_obj = User_Details.objects.filter(Email_ID=Email).first()
    #print('login_user_obj--------',login_user_obj)

    login_user_balance = User_Details.objects.filter(Email_ID=Email).first()
    print('login_user_balance ------', login_user_balance.Balance)

    user_product_obj = Product.objects.filter(Created_By_User_id=login_user_obj.User_ID)
    #print('product_obj-----------',user_product_obj)
    
    
    print("------------------------ Seller Product View Object ----------------------",user_product_obj)
    return render(request,'seller_product_view.html',{'product_data':user_product_obj, 'login_user_balance':login_user_balance, 'Email_ID':Email})



#---------------------------------- Buyer Product View ---------------------------------------------

def buyer_product_view(request):

    print('')
    print("**********----- In Buyer Product View --------********************************************************************")
    
    product_data = Product.objects.filter(IS_Deleted=False)
    #product_data_user = Product.objects.filter(First_Name=request.Created_By_User)
    #print(product_data_user)

    Email = request.session.get('email')
    #print('Session Get Data------',Email)
    #login_user_obj = User_Details.objects.filter(Email_ID=Email).first()
    #print('login_user_obj--------',login_user_obj)
    #user_product_obj = Product.objects.filter(Created_By_User_id=login_user_obj.User_ID)
    #print('product_obj-----------',user_product_obj)
    login_user_balance = User_Details.objects.filter(Email_ID=Email).first()
    print('login_user_balance ------', login_user_balance.Balance)


    
    print("------------------------ Buyer Product View Object --------------------",product_data)
    return render(request,'buyer_product_view.html',{'product_data':product_data, 'login_user_balance':login_user_balance, 'Email_ID':Email})


#---------------------------------- Seller Product Update View -----------------------------------

def seller_product_update(request, pk):
    
    print("**********----- In Seller Product Update View --------********************************************************************")

    Email = request.session.get('email')
    #print('email Session Get Data_1 ----------------------',Email)

    update_product_data = Product.objects.get(Product_ID=pk)
    print('update_product_data ------', update_product_data.Product_Name)
        
    print("----------------------------- seller_product_update --------------",seller_product_update)
    
    return render(request,'seller_product_update.html',{'update_product_data': update_product_data, 'Email_ID':Email})
   

#---------------------------------- Seller Product Updated View -----------------------------------

def seller_product_updated(request, pk):
    
    if request.method == 'POST':
        print("**********----- In Seller Product Update View --------********************************************************************")
        updated_product_data = Product.objects.get(Product_ID=pk)
        print('update_product_data ------', updated_product_data.Product_Name)
        
        updated_product_data.Product_Sell_Price = request.POST['Product_Sell_Price']
        updated_product_data.Product_Cost_Price = request.POST['Product_Cost_Price']
        updated_product_data.Stock_Unit = request.POST['Stock_Unit']  

        updated_product_data.save()
        return redirect('seller_product_view')
   


#---------------------------------- Buy Product View ---------------------------------------------

def buy_product(request, pk):

    if request.method == 'POST':

        print('')
        print('**********------ In Buy Product View --------********************************************************************')

        Email = request.session.get('email')
        #print('Session Get Data----------',Email)

        product_data = Product.objects.all()

        login_user_obj = User_Details.objects.filter(Email_ID=Email).first()
        #print('login_user_balance--------',login_user_obj.Balance)

        login_user_balance = User_Details.objects.filter(Email_ID=Email).first()
        print('login_user_balance ------', login_user_balance.Balance)

        buy_data = Product.objects.get(Product_ID=pk)
        #print("----------------------------- Buy Prodcut Name--------------------",buy_data.Product_Name)

        # SET session key name is 'user_buy_product_name'
        request.session['user_buy_product_name'] = buy_data.Product_Name

        Unit = request.POST['Unit']
        #print('Unit----------', Unit)

        price = buy_data.Product_Sell_Price
        #print('Price---------',price)
        
        total = price* (int(Unit))
        #print('Total---------',total)

        # SET session key name is 'total'
        request.session['total'] = total
     
        # SET session key name is 'unit'
        request.session['unit'] = Unit


        if login_user_obj.Balance >= total:
            return render(request,'buy_product.html',{'buy_data': buy_data, 'login_user_balance':login_user_balance,'total':total, 'quntity':Unit, 'price':price, 'Email_ID':Email})
            #return render(request,'buy_product.html',{'buy_data': buy_data, 'login_user_obj':login_user_obj, 'Email_ID':Email})
        else:
            messages.error(request, 'Hello, Your balance is not sufficient to buy this product.')
            #return render(request,'buyer_product_view.html',{'product_data':product_data, 'Email_ID':Email})
            return render(request,'buy_product.html',{'buy_data': buy_data, 'login_user_balance':login_user_balance, 'total':total, 'quntity':Unit, 'Email_ID':Email})

    else:
        return render(request,'buyer_product_view.html')



#---------------------------------- Add User Purchase ---------------------------------------------

def user_purchase(request):

    if request.method == 'POST':
        print("**********----- In User Purchase View --------********************************************************************")

        Email = request.session.get('email')
        #print('email Session Get Data_1 ----------------------',Email)

        login_user_balance = User_Details.objects.filter(Email_ID=Email).first()
        print('login_user_balance ------', login_user_balance.Balance)

        user_buy_product_name = request.session.get('user_buy_product_name')
        #print('user buy product Session Get Data_2 -----------',user_buy_product_name)

        total = request.session.get('total')
        #print('total Session Get Data_3 ----------------------',total)     

        unit = request.session.get('unit')
        #print('no of unit purchase Session Get Data_4 --------',unit)    

        product_data = Product.objects.all()

        purchase_by_user_obj = User_Details.objects.filter(Email_ID=Email).first()
        #print('purchase_by_user ----------',purchase_by_user_obj)
        

        purchase_product_obj = Product.objects.filter(Product_Name=user_buy_product_name).first()
        #print('purchase_product_object ---',purchase_product_obj.Created_By_User_id)
        #print('purchase_product_object ---',purchase_product_obj)

        purchase_from_user_obj = User_Details.objects.filter(User_ID=purchase_product_obj.Created_By_User_id).first()
        #print('purchase_from_user --------',purchase_from_user_obj.First_Name)
        #print('purchase_from_user --------',purchase_from_user_obj)

        #User_Purchase DB Entry with (Foreign KEY - 'Product_ID', 'Purchase_By_User', 'Purchase_From_User' passing a objects not a value.
        user_purchase_obj = User_Purchase(Product_ID=purchase_product_obj, Total_Unit=unit, Purchase_By_User=purchase_by_user_obj, Purchase_From_User=purchase_from_user_obj)
        user_purchase_obj.save()
        print('user_purchase_obj_DB_Entry ---------',user_purchase_obj)

        #Balance After Payment store in balance variable
        balance = purchase_by_user_obj.Balance - total


        #Buyer Debit Balance After Payment ----------------------------------------------------------------------------- 
        buyer_update_balance_obj = User_Details.objects.get(First_Name=purchase_by_user_obj)
        #print('buyer_before_payment_balance -----',buyer_update_balance_obj.Balance)
        buyer_update_balance_obj.Balance = balance
        buyer_update_balance_obj.save()
        #print('buyer_after_payment_balance ------',buyer_update_balance_obj.Balance)


        #Seller Number of Unit Update After Payment ---------------------------------------------------------------------
        seller_unit_update_obj = purchase_product_obj.Stock_Unit
        #print('seller_unit_before_update --------',purchase_product_obj.Stock_Unit)
        purchase_product_obj.Stock_Unit = seller_unit_update_obj - (int(unit))
        purchase_product_obj.save()
        #print('seller_unit_after_update ---------',purchase_product_obj.Stock_Unit )


        #Seller Credit Balance After Payment -----------------------------------------------------------------------------
        seller_update_balance_obj = User_Details.objects.get(First_Name=purchase_from_user_obj)
        #print('seller_before_balance_obj----------',seller_update_balance_obj.Balance)
        seller_update_balance_obj.Balance = seller_update_balance_obj.Balance + total
        seller_update_balance_obj.save()
        #print('seller_after_balance_obj-----------',seller_update_balance_obj.Balance)


        if purchase_by_user_obj.Balance >= total:
            #print('True')
            return render(request,'user_purchase.html',{'purchase_user_obj':purchase_by_user_obj, 'login_user_balance':login_user_balance, 'user_buy_product_name':user_buy_product_name,'payable_amount':total, 'balance':balance,'Email_ID':Email})
        else:
            print('False')
            messages.error(request,'Your balance is not sufficient for this order')
            #return render(request, 'buyer_product_view.html')
            return redirect('buyer_product_view')
    else:
        return render(request, 'buyer_product_view.html')


#---------------------------------- Order History ------------------------------------------

def order_history(request):
    
    print('')
    print("**********------- In Order History --------******************************************************************")

    # user_orders_id  = request.session.get('user_buy_product_name')
    # print('user buy product Session Get Data_1 -----------',user_orders_id)

    # GET session key from 'email'
    Email = request.session.get('email')
    #print('Session Get Data----------',Email)

    login_user_obj = User_Details.objects.filter(Email_ID=Email).first()
    print('login_user_obj--------',login_user_obj) 
    print('login_user_obj--------',login_user_obj.Balance)    

    order_by_user_obj = User_Details.objects.filter(Email_ID=Email).first()
    #print('order_by_user_obj --------',order_by_user_obj)

    #purchase_product_obj = Product.objects.filter(Product_Name=user_orders_id).first()
    purchase_product_obj = Product.objects.filter(Created_By_User_id=order_by_user_obj.User_ID).first()
    #print('purchase_product_object ---',purchase_product_obj)
    #print('purchase_product_object_id-',purchase_product_obj.Created_By_User_id)

    order_history = User_Purchase.objects.filter(Purchase_From_User_id=purchase_product_obj.Created_By_User_id)
    #print('seller_order_history -----',order_history)
    #print('seller_order_history -----',order_history.query)

    order_history_new = []

    for i in order_history:
        #print(i.Purchase_By_User_id)
        buyer_name = User_Details.objects.filter(User_ID=i.Purchase_By_User_id).first()
        product_name = Product.objects.filter(Product_ID=i.Product_ID_id).first()   
        #print(user.First_Name)
        #print(product_name.Product_Name)
        #i.product_image = Product.objects.filter(Product_Image=product_name.Product_Name).first() 
        i.firstname = buyer_name.First_Name
        i.productname = product_name.Product_Name
        i.product_image = product_name.Product_Image
        #print(i.firstname)
        order_history_new.append(i)


    print("------------------------ Order History View  ----------------------",order_history_new)
    return render(request,'order_history.html',{'order_history':order_history_new, 'login_user_obj':login_user_obj, 'Email_ID':Email})


#---------------------------------- Orders -------------------------------------------------

def orders(request):
    
    print("**********------- Buyer Orders --------********************************************************************")

    # GET session key from 'email'
    Email = request.session.get('email')
    #print('Session Get Data----------',Email)

    login_user_obj = User_Details.objects.filter(Email_ID=Email).first()
    #print('login_user_obj------------',login_user_obj) 
    #print('login_user_obj_balance ---',login_user_obj.Balance)

    buyer = User_Details.objects.filter(Email_ID=Email).first()
    #print('buyer ---------------------',buyer)
    #print('buyer ---------------------',buyer.User_ID)

    #purchase_product_obj = Product.objects.filter(Product_Name=user_orders_id).first()
    # buyer_purchase_product_obj = Product.objects.filter(Created_By_User_id=buyer.User_ID).first()
    # print('buyer_purchase_product_obj ----',buyer_purchase_product_obj)
    # print('buyer_purchase_product_obj_id -',buyer_purchase_product_obj.Created_By_User_id)

    #buyer_orders = User_Purchase.objects.filter(Purchase_From_User_id=buyer_purchase_product_obj.Created_By_User_id)
    buyer_orders = User_Purchase.objects.filter(Purchase_By_User_id=buyer.User_ID)
    #print('buyer_orders_history -----',buyer_orders)
    #print('seller_order_history -----',order_history.query)

    buyer_orders_new = []

    for i in buyer_orders:
        #print(i.Purchase_By_User_id)
        seller_name = User_Details.objects.filter(User_ID=i.Purchase_From_User_id).first()
        product_name = Product.objects.filter(Product_ID=i.Product_ID_id).first()   
        #print(seller_name.First_Name)
        #print(product_name.Product_Name)
        i.product_image = Product.objects.filter(Product_Image=product_name.Product_Name).first() 
        i.firstname = seller_name.First_Name
        i.productname = product_name.Product_Name
        i.product_image = product_name.Product_Image
        #print(i.firstname)
        buyer_orders_new.append(i)

    print("------------------------ Buyer Orders View  ----------------------",buyer_orders_new)
    return render(request,'orders.html',{'order_history':buyer_orders_new, 'login_user_obj':login_user_obj, 'Email_ID':Email})