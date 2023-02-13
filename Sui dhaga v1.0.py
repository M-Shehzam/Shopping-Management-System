import PySimpleGUI as sg
import pandas as pd
import datetime
import os

class Error(Exception):
    pass
class ValueTooSmallError(Error):
    pass

class Product:
    t = False
    k = False
    username = 'designer'
    password = 'abc'

    def GetProduct(self):
        layout = [
            [sg.Text('Enter Product ID: ', size=(35), font=("Helvetica", 14))],
            [sg.InputText(key='id', size=(40,3), font=("Helvetica", 12))],
            [sg.Text('Enter Rate: ', size=(35), font=("Helvetica", 14))],
            [sg.InputText(key='rate', size=(40,3), font=("Helvetica", 12))],
            [sg.Text('Enter Available Stock: ', size=(35), font=("Helvetica", 14))],
            [sg.InputText(key='stock', size=(40,3), font=("Helvetica", 12))],
            [sg.Button('Submit', bind_return_key=True)],
            ]
        window = sg.Window('Product Info', resizable=True).Layout(layout)
        event, values = window.read()
        window.close()
        if event == 'Submit':
            self.id = values['id']

            while True:
                try:
                    self.rate = int(values['rate'])
                    if (self.rate <= 0):
                        raise ValueTooSmallError
                    break
                except ValueError as e:
                    sg.popup_error("INVALID LITERAL for int() with Base 10", e)
                    sg.popup("Try again!")
                except ValueTooSmallError:
                    sg.popup("Rate can Never be Zero-0 or any Negative Value!")

            while True:
                try:
                    self.stock = int(values['stock'])
                    if (self.stock <= 0):
                        raise ValueTooSmallError
                    break
                except ValueError as e:
                    sg.popup_error("INVALID LITERAL for int() with Base 10", e)
                    sg.popup("Try again!")

#------Writing details of added product to text file:---------

            # Variables used for formatting the receipt before writing the record to file:
            # Load the XLSX file into a pandas DataFrame
            df = pd.read_excel('products.xlsx')
            # Write the updated DataFrame back to the XLSX file
            df = df.append({'Product ID': self.id, 'Rate': self.rate, 'Stock': self.stock}, ignore_index=True)
            df.to_excel('products.xlsx', index=False)

    def authority(self):
        layout = [[sg.Text("A.O.A - Welcome To Stylish Enterprises!\n", size=(35,2), font=("Helvetica", 14))],
            [sg.Text('Username ID: ', size=(35), font=("Helvetica", 14))],
            [sg.InputText(key='username', size=(40,3), font=("Helvetica", 12))],
            [sg.Text('Enter Password: ', size=(35), font=("Helvetica", 14))],
            [sg.InputText(key='password', size=(40,9), font=("Helvetica", 12))],
            [sg.Button('Submit', bind_return_key=True)],
        ]
        window = sg.Window('SUI DHAGA', resizable=True).Layout(layout)
        event, values = window.read()

        for i in range(3):
            if event == 'Submit':
                m = values['username'].lower()
                if (m == Product.username):
                    Product.t = True
                    break
                else:
                    sg.popup("Wrong Username!")
                    Product.k = False
                    return False

        if (Product.t == True):
            for j in range(3):
                w = values['password'].lower()
                if (w == Product.password):
                        sg.popup("YOU HAVE BEEN SUCCESSFULLY LOGGED IN!")
                        Product.k = True
                        window.close()
                        return True
                else:
                        sg.popup("Wrong Password!")
                        Product.k = False
                        return False
        else:
            Product.k = False
            return False

    def check(self):
        if Product.k == True:
            return True
        else:
            sg.popup("You have Entered Wrong Credentials!\nYou have been LOGGED - OUT!")
            return False
    
    def Check_id(self, id):
        if self.id == id:
            return True
        else:
            return False
    
    def SearchPutProduct(self):
        sg.popup("(ID: " + str(self.id) + ") (Price: " + str(self.rate) + ") (Stock: " + str(self.stock) + ")")
    
    def PutProduct(self,L):
        product_list = []
        for product in L:
            product_list.append("(ID: " + product.id + ") (Price: " + str(product.rate) + ") (Stock: " + str(product.stock) + ")")
        sg.popup('\n'.join(product_list))

    def Sale(self, L):
        product_list = []
        id_list = []
        rate_list = []
        stock = 0
        rate = 0
        total_bought = []

        layout = [[sg.Text("Enter Customer Name:", size=(35), font=("Helvetica", 14))],
        [sg.Input(key='d', size=(40,3), font=("Helvetica", 12))],
        [sg.Text("How many Products to order?", size=(35), font=("Helvetica", 14))],
        [sg.Input(key='m', size=(40,3), font=("Helvetica", 12))],
        [sg.Button("Submit", bind_return_key=True)], 
        [sg.Button("Cancel")]
        ]
        window = sg.Window("Purchase", resizable=True).Layout(layout)
        event, values = window.read()
        if event in (None, 'Cancel'):
            window.close()
            return

        d = values['d']
        m = int(values['m'])
        window.close()

        for i in range(m):
            layout4 = [[sg.Text("Enter Product ID:", size=(35), font=("Helvetica", 14))],
            [sg.Input(key='product_id', size=(40,3), font=("Helvetica", 12))],
            [sg.Button("Submit", bind_return_key=True)], 
            [sg.Button("Cancel")]
            ]
            window = sg.Window("ID", resizable=True).Layout(layout4)
            event, values = window.read()
            if event in (None, 'Cancel'):
                window.close()
                return
            
            product_id = values['product_id']
            window.close()

            found = False
            for product in L:
                if product.id == product_id:
                    found = True
                    product_list.append(str(product.id)+str(product.rate)+str(product.stock))
                    id_list.append(product.id)
                    rate_list.append(product.rate)
                    sg.popup("Current Stock:",product.stock)
                    while True:
                        layout2 = [[sg.Text("Enter Quantity you Want to Buy:", size=(35), font=("Helvetica", 14))],
                        [sg.Input(key='b', size=(40,3), font=("Helvetica", 12))],
                        [sg.Text("How much discount in percent?", size=(35), font=("Helvetica", 14))],
                        [sg.Input(key='e', size=(40,3), font=("Helvetica", 12))],
                        [sg.Button("Submit", bind_return_key=True)], 
                        [sg.Button("Cancel")]
                        ]
                        window = sg.Window("Quantity & Discount:", resizable=True).Layout(layout2)
                        event, values = window.read()
                        if event in (None, 'Cancel'):
                            window.close()
                            return
                        b = int(values['b'])
                        e = int(values['e'])
                        window.close()

                        if product.stock > 0:
                            if (b <= product.stock):
                                stock += b
                                totalamount = b * product.rate
                                rate += totalamount
                                product.stock -= b
                                #---------------------------------
                                df = pd.read_excel('products.xlsx')
                                row = df.loc[df['Product ID'] == product_id]
                                row['Stock'] -= b
                                row.to_excel('products.xlsx', index=False)
                                #---------------------------------
                                total_bought.append(b)
                                break
                            else:
                                sg.popup("Not Enough Quantity Available!")
                        else:
                            sg.popup("Not Enough Quantity Available!")
            if not found:
                sg.popup("Record Not Found!")
        
        df = pd.read_excel('receipts.xlsx')
        try:
            r_n = df['Receipt No'].iloc[-1]
            r_n += 1
        except:
            r_n = 1
        r_space = 26 - len(str(r_n))    
        #discount:
        discount = e / 100 * rate
        final_price = rate - discount
        sg.popup("Discount Given, Which in Rupees is:",discount)

        sg.popup("RECEIPT:","\n** ****** ******** *\n ****** ******** ***\n* *******SD***** *\n*** ********** *****\n******* ********** *\n"+ (" ")*r_space + str(r_n)+ "\n\nYour Article(s) are:\n\nProducts = "+str(id_list)+"\n    Rates = "+str(rate_list)+"\n\nDiscount-Deduction = "+str(rate)+"-"+str(discount)+"\n\nTo Pay: "+str(final_price)+"/- Rupees Only!"+"\n\n\nThank-You For Puchasing with us!\nMR/MRS "+str(d))

#---Writing details of receipt to the text file:-------------------

        df = pd.read_excel('receipts.xlsx')

        t = datetime.datetime.now()

        # Adding a new row to the dataframe
        df = df.append({'Receipt No': r_n, 'Date': t.strftime('%x'), 'Product ID': id_list, 'Customer Name': d, 'Discount': discount, 'Quantity Bought': total_bought, 'Price Paid': final_price}, ignore_index=True)

        # Writing the updated dataframe to the xlsx file
        df.to_excel('receipts.xlsx', index=False)

    def updater_all(self, id):
        layout = [[sg.Text("Enter new Product ID: ", size=(35), font=("Helvetica", 14))],
        [sg.Input(key='id', size=(40,3), font=("Helvetica", 12))],
        [sg.Text("Enter new Rate: ", size=(35), font=("Helvetica", 14))],
        [sg.Input(key='rate', size=(40,3), font=("Helvetica", 12))],
        [sg.Text("Enter new Available Stock: ", size=(35), font=("Helvetica", 14))],
        [sg.Input(key='stock', size=(40,3), font=("Helvetica", 12))],
        [sg.Button("Submit", bind_return_key=True)], 
        [sg.Button("Cancel")]]
        window = sg.Window("Update Product", resizable=True).Layout(layout)
        event, values = window.read()
        if event in (None, 'Cancel'):
            window.close()
            return
        self.id = values['id']
        self.rate = int(values['rate'])
        self.stock = int(values['stock'])  
        sg.popup("Updated ID: " + str(self.id),"Updated Rate: " + str(self.rate),"Updated Stock: " + str(self.stock))
        window.close()

#----Updating 'products.txt' file details:-----------------------
        df = pd.read_excel('products.xlsx')
        # Find the row with the specified ID
        row = df.loc[df['Product ID'] == id]
        # Update the values in the row
        row['Product ID'] = self.id
        row['Rate'] = self.rate
        row['Stock'] = self.stock
        # Write the updated DataFrame back to the XLSX file
        row.to_excel('products.xlsx', index=False)

    def updater_stock(self, id):
        layout = [[sg.Text('Enter New Stock:', size=(35), font=("Helvetica", 14))],
                [sg.InputText(key='d',size=(40,3), font=("Helvetica", 12))],
                [sg.Button('Submit', bind_return_key=True)],
                [sg.Button("Cancel")]]
        window = sg.Window('Update Stock', resizable=True).Layout(layout)
        event, values = window.Read()
        if event in (None, 'Cancel'):
            window.close()
            return
        x = int(values['d'])
        self.stock += x
        sg.Popup("Stock now: " + str(self.stock))
        window.close()

#----Updating 'products.txt' file details:----------------------
        df = pd.read_excel('products.xlsx')
        # Find the product with the specified product ID
        product = df.loc[df['Product ID'] == id]
        # Update the stock of the product
        product['Stock'] = self.stock
        # Write the updated data back to the Excel file
        product.to_excel('products.xlsx', index=False)

    def display(self):
        sg.popup("GoodBye!\n\nThank-You For Choosing our Serivces!\nFor any Complains:\nContact us at: +923147800668\nOr Mail us at: m.shehzamtariq@gmail.com\n\nMade By: Muhammad Shehzam")

###########################
###########################
L = []
P = Product()
###########################
###########################
# File for current available products to buy:
if not os.path.exists('products.xlsx'):
    # Create a new Excel file
    productDatabase = pd.DataFrame({'Product ID': [], 'Rate': [], 'Stock': []})
    productDatabase.to_excel('products.xlsx', index=False)
else:
    # Load the existing Excel file
    productDatabase = pd.read_excel('products.xlsx')

productData = []
for index, row in productDatabase.iterrows():
    id = row['Product ID']
    rate = row['Rate']
    stock = row['Stock']
    g = Product()
    g.id = str(id) 
    g.rate = int(rate)
    g.stock = int(stock)
    L.append(g)
# File for recording receipts of customers when they purchase products:
if not os.path.exists('receipts.xlsx'):
    # Create a new Excel file
    receiptDatabase = pd.DataFrame({'Receipt No': [], 'Date': [], 'Product ID': [], 'Customer Name': [], 'Discount': [], 'Quantity Bought': [], 'Price Paid': []})
    receiptDatabase.to_excel('receipts.xlsx', index=False)
else:
    # Load the existing Excel file
    receiptDatabase = pd.read_excel('receipts.xlsx')
###########################
###########################
def show_all_products(L):
    if L == []:
        sg.popup("No Products Currently Available!")
    else:
        P.PutProduct(L)

def add_new_products(L):
    if P.authority() == True:
        layout = [[sg.Text("How many Products You wanna add? ", size=(35), font=("Helvetica", 14))],
                  [sg.Input(key='x', size=(40,3), font=("Helvetica", 12))],
                  [sg.Button("Submit", bind_return_key=True), sg.Button("Cancel")]]
        window = sg.Window("Add New Products").Layout(layout)
        event, values = window.Read()
        window.Close()

        if event != "Cancel":
            x = int(values['x'])
            for i in range(x): 
                g = Product()
                g.GetProduct()
                L.append(g)

def search_by_id(L):
    if L == []:
        sg.popup("No Products Currently Available!")
    else:
        layout = [[sg.Text("Enter Product ID to Search: ", size=(35), font=("Helvetica", 14))],
                [sg.Input(key='id', size=(40,3), font=("Helvetica", 12))],
                [sg.Button("Submit", bind_return_key=True),sg.Button("Cancel")]]
        window = sg.Window("Search by ID", layout)
        event, values = window.read()
        if event in (None, 'Cancel'):
            window.close()
            return
        id = values['id']
        found = False
        for c in L:
            found = c.Check_id(id)
            if found == True:
                #sg.popup("ID Found:")
                c.SearchPutProduct()
                break
        if not found:
            sg.popup("Record Not Found!!!")
        window.close()

def Delete_Specific_ID(L):
    if L == []:
        sg.popup("No Products Currently Available!")
    else:
        layout = [[sg.Text("Enter Product ID to Delete: ", size=(35), font=("Helvetica", 14))],
                [sg.Input(key='id', size=(40,3), font=("Helvetica", 12))],
                [sg.Button("Submit", bind_return_key=True), sg.Button("Cancel")]]
        window = sg.Window("Delete by ID", layout)
        event, values = window.read()
        if event in (None, 'Cancel'):
            window.close()
            return
        id = values['id']
        found = False
        for c in L:
            found = c.Check_id(id)
            if found == True:
                    L.remove(c)

                    #------Removing from text file:-------
                    # Load the Excel file into a DataFrame
                    productsDatabase = pd.read_excel('products.xlsx')

                    # Remove the row with the specified product ID
                    productsDatabase = productsDatabase[productsDatabase['Product ID'] != id]

                    # Write the updated DataFrame back to the Excel file
                    productsDatabase.to_excel('products.xlsx', index=False)
                    #-------------------------------------

                    sg.popup("ID has Been Deleted!")
                    break
        if not found:
            sg.popup("Record Not Found!!!")
        window.close()

def Delete_All_Products(L):
    if L == []:
        sg.popup("No Products Currently Available!")
    else:
        L.clear()
        #----Deleting all files from text file:-----------------
        productsDatabase = pd.DataFrame({'Product ID': [], 'Rate': [], 'Stock': []})
        productsDatabase.to_excel('products.xlsx', index=False)
        #-------------------------------------------------------
        sg.popup("\nAll Product Details has been DELETED!")

def Purchase(L):
    P.Sale(L)
    P.display()

def Details_Updater(L):
    layout = [[sg.Text("Enter Product ID to Update: ", size=(35), font=("Helvetica", 14))],
    [sg.Input(key='id', size=(40,3), font=("Helvetica", 12))],
    [sg.Button("Submit", bind_return_key=True), sg.Button("Cancel")]]
    window = sg.Window("Update Product", layout)
    event, values = window.read()
    if event in (None, 'Cancel'):
        window.close()
        return
    id = values['id']
    found = False
    for c in L:
        found = c.Check_id(id)
        if found == True:
            c.updater_all(id)
            break
    if not found:
        sg.popup("Record was Not Found!!!")
    window.close()

def Update_Stock(L):
    layout = [[sg.Text('Enter Product ID to Update:', size=(35), font=("Helvetica", 14))],
              [sg.InputText(size=(40,3), font=("Helvetica", 12))],
              [sg.Button('Submit', bind_return_key=True), sg.Button("Cancel")]]
    window = sg.Window('Update Stock').Layout(layout)
    event, values = window.Read()
    if event in (None, 'Cancel'):
        window.close()
        return
    id = values[0]
    found = False
    for c in L:
        found = c.Check_id(id)
        if found == True:
            c.updater_stock(id)
            break
    if not found:
        sg.Popup('Record was Not Found!!!')
    window.Close()

###########################
###########################
sg.theme('Dark Grey 11')

layout = [[sg.Text("Main - Menu:\n", size=(30,1), font=("Helvetica", 14))],
          [sg.Button("Show All Products", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Add New Products", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Search By ID", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Delete Specific ID", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Delete All Products", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Purchase", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Details Updater", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Update Stock", size=(30,1.5), font=("Helvetica", 12))],
          [sg.Button("Exit", size=(30,1.5), font=("Helvetica", 12))]]

window = sg.Window("Product Management", resizable=True).Layout(layout)
if P.authority() == True:
    while P.check():
        event, values = window.Read()
        if event == "Show All Products":
            show_all_products(L)
######################################################
        elif event == "Add New Products":
            add_new_products(L)
######################################################
        elif event == "Search By ID":
            search_by_id(L)
######################################################
        elif event == "Delete Specific ID":
            Delete_Specific_ID(L)
######################################################
        elif event == "Delete All Products":
            Delete_All_Products(L)
######################################################
        elif event == "Purchase":
            Purchase(L)
######################################################
        elif event == "Details Updater":
            Details_Updater(L)
######################################################
        elif event == "Update Stock":
            Update_Stock(L)
######################################################
        elif event == "Exit":
            window.Close()
            P.display()
            break
        else:
            window.Close()
            break