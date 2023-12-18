class Category:
    def __init__(self,name):
        self.name = name
        self.ledger = []
        self.balance = bool(0)
        self.withdrawls = []
        self.deposits = []
    
    def get_balance(self):
        return self.balance
    
    def check_funds(self, amount):
        if self.balance < amount:
            return False
        else:
            return True
        
    def deposit(self, amount, description=""):
        self.balance = self.balance + amount
        self.ledger.append({"amount":amount, "description": description})
        self.deposits.append(amount)

    def withdraw(self, amount, description=""):
        if self.check_funds(amount) is True:
            self.balance = self.balance - amount
            self.withdrawls.append(amount)
            amount = -abs(amount)
            self.ledger.append({"amount":amount, "description": description})
            return True
        else:
            return False
    
    def transfer(self,amount, destination):
        if self.check_funds(amount) is False:
            return False
        else:
            self.withdraw(amount, f"Transfer to {destination.name}")
            destination.deposit(amount, f"Transfer from {self.name}")
            return True
    
    def __str__(self):
        middle_num = int((30-len(self.name))/2)
        output_text = ('*' * middle_num) + self.name + ('*' * middle_num) + '\n'
        for entry in self.ledger:
            entry_description = entry["description"]
            if len(entry_description) > 23:
                entry_description = entry_description[:23]
            number_len = len(str(format(entry["amount"],'.2f'))) 
            space_to_add = 30 - number_len - len(entry_description)
            part_text =  entry_description + (' ' * space_to_add) + str(format(entry["amount"],'.2f')) + '\n'
            output_text = output_text + part_text
        
        total_text = 'Total: ' + str(self.balance)
        output_text = output_text + total_text
        return output_text

def check_percent(target,number):
    if number >= target:
        return "o"
    else:
        return " "

def create_spend_chart(categories):
     # Calculate Percent
    total_amount = 0
    for category in categories:
        total_amount = total_amount + abs(sum(category.withdrawls))
    percentage_list = []
    for category in categories:
        percent_of_number = (abs(sum(category.withdrawls)) / total_amount) * 100
        rounded_number = round(percent_of_number/10)*10
        if rounded_number > percent_of_number:
            rounded_number = rounded_number - 10
        percentage_list.append(rounded_number)

    #sort by size
    sorted_percentage_list = []
    sorted_categories_list = []

    # for x in range(0, len(percentage_list)):
    #     max_number = max(percentage_list)
    #     max_number_index = percentage_list.index(max_number)
    #     sorted_percentage_list.append(max_number)
    #     sorted_categories_list.append(categories[max_number_index].name)
    #     percentage_list.remove(max_number)
    #     categories.remove((categories[max_number_index]))

    for x in categories:
        sorted_categories_list.append(x.name)

    for x in percentage_list:
        sorted_percentage_list.append(x)

    # create text
    text_out = 'Percentage spent by category' + '\n'
    
    # #100
    # text_out = text_out + '100| '
    # for entry in sorted_percentage_list:
    #     text_out = text_out + (check_percent(100,entry)) + ' '
    # text_out = text_out + '\n'

    # #90
    # text_out = text_out + '90| '
    # for entry in sorted_percentage_list:
    #     text_out = text_out + (check_percent(90,entry)) + ' '
    # text_out = text_out + '\n'

    flag = 100
    while flag >= 0:
        flag_space_length = 3 - len(str(flag))
        text_out = text_out + (' ' * flag_space_length ) +  str(flag) +'| '
        for entry in sorted_percentage_list:
            text_out = text_out + (check_percent(flag,entry)) + '  '
        text_out = text_out + '\n'
        flag -=10
    
    #Line
    text_out = text_out + '    -' + ('---' * len(sorted_percentage_list)) + '\n'

    # Letters
    longest_catagory = 0
    for x in sorted_categories_list:
        if len(x) > longest_catagory:
            longest_catagory = len(x)

    for x in range (0, longest_catagory):
        text_to_add = '     '
        for z in range (0, len(sorted_categories_list)):
            try:
                text_to_add = text_to_add + sorted_categories_list[z][x] + '  '
            except:
                text_to_add = text_to_add + '   '
        text_to_add = text_to_add + '\n'
        text_out = text_out + text_to_add



    return text_out[:-1]