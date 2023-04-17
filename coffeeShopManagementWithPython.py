import mysql.connector
import prettytable
import time


# This is where I enter information about my database.
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  port="",
  database=""
)

cursor = mydb.cursor()


class db:
    def __init__(self, coffee_id, coffee_quantity):
        self.coffee_id = coffee_id
        self.coffee_quantity = coffee_quantity
    
    def get_coffee(self):
        print('''
        Menu:
        1. Americano
        2. Latte
        3. Cappuccino
        ''')


    def get_coffee_resource(self):
        global water_needed, coffeeBean_needed, sugar_needed

        cursor.execute(f"SELECT \
  material.mat_water, material.mat_cofbean, material.mat_sugar \
  FROM coffee \
  INNER JOIN material on coffee.mat_id=material.mat_id where coffee_id={float(self.coffee_id)}")
        dataOnCoffee = cursor.fetchall()
        water_needed = float(self.coffee_quantity)*(dataOnCoffee[0][0])
        coffeeBean_needed = float(self.coffee_quantity)*(dataOnCoffee[0][1])
        sugar_needed = float(self.coffee_quantity)*(dataOnCoffee[0][2])

    def check_material(self):
        global remainingSugar, remainingCoffeeBean, remainingWater
        cursor.execute(f"SELECT resource.water, resource.cof_bean, resource.sugar FROM resource")

        dataOnResource = cursor.fetchall()

        
        remainingWater = dataOnResource[0][0]
        remainingCoffeeBean = dataOnResource[0][1]
        remainingSugar = dataOnResource[0][2]
        if(remainingWater<water_needed):
            print("There is not enough water to brew the coffee. Please refill the water in the inventory.")
        if(remainingCoffeeBean<coffeeBean_needed):
            print("There is not enough coffee bean to brew the coffee. Please refill the coffee bean in the inventory.")
        if(remainingSugar<sugar_needed):
            print("There is not enough coffee bean to brew the coffee. Please refill the coffee bean in the inventory.")
        
    def deduct_resource(self):
        global remainingWater, remainingCoffeeBean, remainingSugar, coffee_id
        if(remainingWater>=water_needed):
            remainingWater = float(remainingWater)-float(water_needed)
            cursor.execute(f"UPDATE resource SET water = {remainingWater} WHERE res_id = 1")
            mydb.commit()
        if(remainingCoffeeBean>=coffeeBean_needed):
            remainingCoffeeBean = float(remainingCoffeeBean) - float(coffeeBean_needed)
            cursor.execute(f"UPDATE resource SET cof_bean = {remainingCoffeeBean} WHERE res_id = 1")
            mydb.commit()
        if(remainingSugar>=sugar_needed):
            remainingSugar = float(remainingSugar) - float(sugar_needed)
            cursor.execute(f"UPDATE resource SET sugar = {remainingSugar} WHERE res_id = 1")
            mydb.commit()

    def make_coffee(self):
        print("Brewing Coffee ...")
        print("...")
        time.sleep(5)

        cursor.execute(f"SELECT coffee.coffee_price FROM coffee where coffee_id = {float(self.coffee_id)}")
        coffee_price_asList = cursor.fetchall()

        coffee_price = float(self.coffee_quantity)*(coffee_price_asList[0][0])
        


        print(f"Your total price is {coffee_price}")

        print("Done! The Coffee Is Ready To Be Served So GET TO WORK.")
    


    


     


            
    
class membership:
    def __init__(self):
        pass

    def refill_inventory(self):
        
        cursor.execute(f"SELECT resource.water, resource.cof_bean, resource.sugar FROM resource")

        dataOnResource = cursor.fetchall()

        
        remainingWater = dataOnResource[0][0]
        remainingCoffeeBean = dataOnResource[0][1]
        remainingSugar = dataOnResource[0][2]
        refill_choice = input('''
        Please select which resource you want to refill:
        1. Water (ml)
        2. Coffee Bean (g)
        3. Sugar (g)
        Key Input: 
        ''')
        if(refill_choice=="1"):
            refill_amount = input("Amount: ")
            remainingWater = remainingWater + float(refill_amount)
            cursor.execute(f"UPDATE resource SET water = {remainingWater} WHERE res_id = 1")
            mydb.commit()
            print("Successfully Refilled!")

        elif(refill_choice=="2"):
            refill_amount = input("Amount: ")
            remainingCoffeeBean = remainingCoffeeBean + float(refill_amount)
            cursor.execute(f"UPDATE resource SET cof_bean = {remainingCoffeeBean} WHERE res_id = 1")
            mydb.commit()
            print("Successfully Refilled!")

        elif(refill_choice=="3"):
            refill_amount = input("Amount: ")
            remainingSugar = remainingSugar + float(refill_amount)
            cursor.execute(f"UPDATE resource SET sugar = {remainingSugar} WHERE res_id = 1")
            mydb.commit()
            print("Successfully Refilled!")

    def gen_sell_report_all(self):
        cursor.execute("SELECT \
  sell.sell_id, \
  customer.cus_firstname, customer.cus_lastname, coffee.coffee_name, sell.sell_total, sell.sell_date \
  FROM sell \
  INNER JOIN customer on customer.cus_id=sell.cus_id \
    inner join coffee on coffee.coffee_id=sell.coffee_id")
        all_sell_report = cursor.fetchall()

        

        all_sell_report_table = prettytable.PrettyTable()

        all_sell_report_table.field_names = ["Sell ID", "First Name", "Last Name", "Coffee", "Total Price", "Date"]
        all_sell_report_table.add_rows(all_sell_report)   

        print(all_sell_report_table)

    def gen_sell_report_specific(self):

        start_date = input("Please input your starting date in this format (YYYY-MM-DD): ")
        end_date = input("Please input your ending date in this format (YYYY-MM-DD): ")

        cursor.execute(f"SELECT \
  sell.sell_id, \
  customer.cus_firstname, customer.cus_lastname, coffee.coffee_name, sell.sell_total, sell.sell_date \
  FROM sell \
  INNER JOIN customer on customer.cus_id=sell.cus_id \
    inner join coffee on coffee.coffee_id=sell.coffee_id where sell_date>='{start_date}' and sell_date<='{end_date}'")

        specific_sell_report_table = cursor.fetchall()

        specific_table = prettytable.PrettyTable()

        specific_table.field_names = ["Sell ID", "First Name", "Last Name", "Coffee", "Total Price", "Date"]
        specific_table.add_rows(specific_sell_report_table) 

        print(specific_table)

    def gen_allMember(self):
        cursor.execute("SELECT customer.cus_id, customer.cus_firstname, customer.cus_lastname, customer.cus_ph FROM customer")
        all_member_report = cursor.fetchall()

        all_member_table = prettytable.PrettyTable()
        all_member_table.field_names = ["Customer ID", "First Name", "Last Name", "Phone Number"]
        all_member_table.add_rows(all_member_report)

        print(all_member_table)

    def register_user(self):
        firstname = input("Please input the guest's first name: ")
        lastname = input("Please input your lastname: ")
        phoneNumber = input("Please input the guest's phone number: ")

        cursor.execute(f"INSERT INTO customer(cus_firstname, cus_lastname, cus_ph) VALUES ('{firstname}', '{lastname}', '{phoneNumber}')")

        mydb.commit()

        print("Registered Successfully!")

    def member(self):
        global member_phoneNumber, member_firstname, member_lastname, member_id, guest_data
        input_phoneNumber = input("Please input the guest's phone number: ")
        cursor.execute(f"SELECT customer.cus_id, customer.cus_lastname, customer.cus_firstname, customer.cus_ph from customer where cus_ph={input_phoneNumber}")
        guest_data = cursor.fetchall()
        
        if(guest_data==[]):
            print("The guest is not a member, yet. Please register him or her or they as a member.")
        else:
            print("The guest is indeed a member.")
            member_id = guest_data[0][0]
            member_lastname = guest_data[0][1]
            member_firstname = guest_data[0][2]
            member_phoneNumber = guest_data[0][3]
            

    def checkout_for_member(self):
        global member_phoneNumber, member_firstname, member_lastname, member_id, coffee_id, coffee_quantity, coffee_price

        cursor.execute(f"SELECT coffee.coffee_price FROM coffee where coffee_id={float(coffee_id)}")
        
        coffee_price_asList = cursor.fetchall()

        coffee_price = (float(coffee_quantity)*(coffee_price_asList[0][0]))*0.9


        
        cursor.execute(f"INSERT INTO sell(cus_id, coffee_id, sell_total) VALUES ({member_id}, {float(coffee_id)}, {coffee_price})")
        mydb.commit()


    def checkout_for_guest(self):
        global member_phoneNumber, member_firstname, member_lastname, member_id, coffee_id, coffee_quantity, coffee_price
        cursor.execute(f"SELECT coffee.coffee_price FROM coffee where coffee_id={float(coffee_id)}")

        coffee_price_asList = cursor.fetchall()

        coffee_price = float(coffee_quantity)*(coffee_price_asList[0][0])

        cursor.execute(f"INSERT INTO sell(cus_id, coffee_id, sell_total) VALUES (1, {float(coffee_id)}, {coffee_price})")
        mydb.commit()

    



# coffee_id = input("Coffee ID: ")
# coffee_quantity = input("Coffee Quantity: ")
        


loopMainMenu = True

loopSellCoffee = True





while loopMainMenu:
    print('''
    ======= CS111 Coffee Shop =======
    
    1. Sell Coffee
    2. Report
    3. Inventory
    e. Exit

    ''')

    user_choice_main_menu = input("Key in: ")

    if(user_choice_main_menu == "1"):

        while loopSellCoffee:
            print('''

            Is this order for member or guest?
            1. Guest
            2. Member 
            3. Register
            e. Exit

            ''')
            user_choice_membership = input("Key in: ")

            if(user_choice_membership=="1"):
                print('''
            
            Menu:
            1. Americano - $2
            2. Latte - $2
            3. Cappuccino - $2.5
            
            ''')
                coffee_id = input("Please choose the coffee: ")
                coffee_quantity = input("How many cups for this order?: ")
                
                coffee_db = db(coffee_id, coffee_quantity)
                coffee_db.get_coffee_resource()
                coffee_db.check_material()
                if(remainingWater<water_needed or remainingCoffeeBean<coffeeBean_needed or remainingSugar<sugar_needed):
                    break

                else:
                    coffee_db.deduct_resource()
                    coffee_db.make_coffee()

                    guest_checkout = membership()
                    guest_checkout.checkout_for_guest()
                    break


            elif(user_choice_membership=="2"):
                isMember_checkout = membership()
                isMember_checkout.member()
                if(guest_data==[]):
                    break
                else: 
                    print('''
            
            Menu:
            1. Americano - $2
            2. Latte - $2
            3. Cappuccino - $2.5
            
            ''')
                    
                    coffee_id = input("Please choose the coffee: ")
                    coffee_quantity = input("How many cups for this order?: ")

                    coffee_db = db(coffee_id, coffee_quantity)
                    coffee_db.get_coffee_resource()
                    coffee_db.check_material()
                    if(remainingWater<water_needed or remainingCoffeeBean<coffeeBean_needed or remainingSugar<sugar_needed):
                        break

                    else:
                        
                        coffee_db.deduct_resource()
                        coffee_db.make_coffee()

                        
                        isMember_checkout.checkout_for_member()
                        break
            
            elif(user_choice_membership=="3"):
                register_member = membership()
                register_member.register_user()
                break

            elif(user_choice_membership=="e" or user_choice_membership=="E"):
                break

    elif(user_choice_main_menu=="2"):
        loopReport = True
        while loopReport:
        
            print('''

            Report Option:
            1. Get all sale records
            2. Get sale records by date
            3. Get all member report
            4. Get Resource Report
            e. exit

            ''')
            getReport = membership()
            user_choice_report = input("Key in: ")
            if(user_choice_report=="1"):
                getReport.gen_sell_report_all()

            elif(user_choice_report=="2"):
                getReport.gen_sell_report_specific()

            elif(user_choice_report=="3"):
                getReport.gen_allMember()

            elif(user_choice_report=="4"):
                cursor.execute("SELECT resource.water, resource.cof_bean, resource.sugar FROM resource")
                resource_data = cursor.fetchall()

                resource_table = prettytable.PrettyTable()
                resource_table.field_names = ["Water", "Coffee Bean", "Sugar"]
                resource_table.add_rows(resource_data)

                print(resource_table)

            elif(user_choice_report=="e" or user_choice_report=="E"):
                break
    
    elif(user_choice_main_menu=="3"):
          refill = membership()
          refill.refill_inventory()

    elif(user_choice_main_menu=="e" or user_choice_main_menu=="E"):
        print("Exiting the app ...")
        break






            


    

            





    
    
        





        
            

        

        




    

    



        






