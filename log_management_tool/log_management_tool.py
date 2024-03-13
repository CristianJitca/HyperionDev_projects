from tabulate import tabulate

def read_log_file(log_file):
    """
    The function `read_log_file` reads a log file, splits each non-empty line by a delimiter, and
    returns the content as a list of lists.
    
    :param log_file: The function `read_log_file` reads a log file and extracts non-empty lines,
    splitting them by the delimiter " | ". If the file is not found or there is an error reading the
    file, appropriate error messages are displayed
    :return: The function `read_log_file` returns a list of lists where each inner list contains the
    split elements of a non-empty line in the log file after stripping whitespaces.
    """
    content_line = []
    try:
        with open(log_file, "r") as file:
            content = file.readlines()          
        for line in content:
            # Check if the line is not empty after stripping whitespaces
            if line.strip():
                line_split = line.strip().split(" | ")
                content_line.append(line_split)
    except FileNotFoundError:
        print("File not found! ")
    except IOError as e:
        print(f"Error reading the file: {e}")
    return content_line


def display_placed_orders_log(log_file="placed_orders_log.txt"):
    """
    The function `display_placed_orders_log` reads a log file containing placed orders information and
    returns a list of formatted order details.
    
    :param log_file: The function `display_placed_orders_log` reads a log file containing information
    about placed orders and returns a list of formatted strings for each order entry in the log. The
    function takes an optional parameter `log_file` which specifies the file path of the log file to be
    read. If no file path, defaults to placed_orders_log.txt (optional)
    :return: The function `display_placed_orders_log` reads a log file named "placed_orders_log.txt" and
    extracts information for each line in the log file. It then formats this information into a string
    for each entry and appends it to a list called `placed_orders_list`. Finally, the function returns
    the list `placed_orders_list` containing the formatted information for each placed order entry in
    the log file
    """
    placed_orders_list = []
    for line in read_log_file(log_file):       
        date_time = line[0]
        log_type = line[1]
        order_number = line[2]
        location = line[3]
        goods_type = line[4]
        placed_orders = f"Date: {date_time}\nLOG: {log_type}\nOrder Number: {order_number}\n"\
                        +f"Location: {location}\nGoods: {goods_type}"        
        placed_orders_list.append(placed_orders)
    return placed_orders_list

        
def display_orders_details_log(log_file="orders_details_log.txt"):
    """
    The function `display_orders_details_log` reads a log file containing order details and displays
    information for a specific order number entered by the user.
    
    :param log_file: The `log_file` parameter in the `display_orders_details_log` function is a file
    path that points to the file where the orders details log is stored. By default, if no file path is
    provided when calling the function, it will use "orders_details_log.txt" as the file to read,
    defaults to orders_details_log.txt (optional)
    """
    order_info = []
    while True:
        try:
            order_number = input("Please enter the order number: ")
            for line in read_log_file(log_file):
                if order_number == line[2]: # Check if the order number entered is in any line    
                    order_info.append(line) # If it is, append the line in order_info
            if not order_info:
                print("Order number not found. Please try again.")
                continue
            else:
                print(tabulate(order_info, headers=["Date", "Tracking number", "Order number", "LOG"]))
                break
        except ValueError:
            pass


def display_returns_log(log_file="returns_log.txt"):
    """
    This function reads a log file containing return information and returns a list of formatted return
    details.
    
    :param log_file: The `display_returns_log` function reads a log file containing information about
    returns and processes each line to extract return details such as return date, order number,
    customer name, product code, quantity, and return reason. It then formats this information into a
    string for each return entry and stores them in a, defaults to returns_log.txt (optional)
    :return: The function `display_returns_log` is returning a list of formatted return information for
    each entry in the returns log file. Each entry includes the return date, order number, customer
    name, product code, quantity, and return reason.
    """
    return_info_list = []
    for line in read_log_file(log_file):
        return_date = line[0]
        order_number = line[1]
        costumer_name = line[2]
        product_code = line[3]
        quantity = line[4]
        return_reason = line[5]
        return_info = f"Return Date: {return_date}\nOrder Number: {order_number}\nCustomer name: {costumer_name}\n"\
                    + f"Product code: {product_code}\nQuantity: {quantity}\nReason: {return_reason}"
        return_info_list.append(return_info)
    return return_info_list

def main():
    """
    The main function displays a menu for a log management tool and allows the user to choose different
    log files to display or exit the program.
    """
    print("-" * 60)
    print("\t\tLOG MANAGEMENT TOOL")
    print("-" * 60)
      
    while True:
        print("""\n1.Placed Orders
2.Order Details
3.Returns
4.Exit""")   
        try:
            user_choice = int(input("Please choose the log file to display(or 4 to exit): "))            
            if user_choice == 1:
                for line in display_placed_orders_log():
                    print(f"\n{line}")                   
            elif user_choice == 2:
                display_orders_details_log()
            elif user_choice == 3:
                 for line in display_returns_log():
                    print(f"\n{line}")
            elif user_choice == 4:
                exit()
            else:
                print("Please enter a number(from 1 to 4).")                                    
        except ValueError: 
            print("Invalid input. Please enter a number(from 1 to 4).")           
        
                
if __name__ == "__main__":
    main()
