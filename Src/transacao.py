
def calculate_total_revenue(transactions): 
    
    # Initialize the variable that will store the total revenue
    total = 0 
    
    #Loop through all inncoming transactions
    for transaction in transactions: 
       
       #check if the status is 'completed' and the quantity is greater than 0
       if transaction['status'] == 'completed'and transaction ['quantity'] > 0:
           
           # Adds the item value multiplied by the quantity to the total
           total += transaction['itemPrice'] * transaction['quantity'] 

           # If total revenue is greater than 10,000 apply a 10% discount
    if total > 10000:
       
       # total = total *0.9
       total -= total * 0.1

       #Returns the final value of the total revenue(with or Without discount) 
    return total