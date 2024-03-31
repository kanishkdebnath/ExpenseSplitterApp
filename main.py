class Participant:

    def __init__(self, name):
        self.name = name
        self.amount_paid = 0.0
        self.amount_owed = 0.0

    def pay(self, amount):
        self.amount_paid = self.amount_paid + amount

    def owe(self, amount):
        self.amount_owed = self.amount_owed + amount

    def balance(self):
        return self.amount_paid - self.amount_owed

    def __str__(self):
        balance_state = "get"
        if self.balance() < 0:
            balance_state = "give"
        if self.balance() >= 0:
            balance_state = "get"
        return f"{self.name} has paid {self.amount_paid} and owes {self.amount_owed} and {balance_state} {abs(self.balance())}"


class Expense:

    def __init__(self, title, amount):
        self.title = title
        self.amount = amount
        self.participants = []
        self.payers = []
        self.liable_participants = []

    def add_payers(self, participants):
        self.payers = participants

    def add_participants(self, participants):
        self.participants = participants

    def add_liable_participants(self, participants):
        self.liable_participants = participants

    def __str__(self):
        return f"Title: {self.title}, Amount: {self.amount}"


class Sheet:

    def __init__(self, name):
        self.name = name
        self.participants = []
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def add_participant(self, participant):
        self.participants.append(participant)

    def __str__(self):
        return f"Sheet name : {self.name}"


def divide_absolutely(expense_total_amount, participants):
    remaining_amount = expense_total_amount
    for participant in participants:
        print(f"Remaining amount : {remaining_amount}")
        share_amount = float(input(f"Enter the amount {participant.name} has to pay : "))
        # TODO: Handle invalid cases
        participant.owe(share_amount)
        remaining_amount -= share_amount

    return participants


def divide_percentage_share(expense_total_amount, participants):
    remaining_percentage = 100
    for participant in participants:
        print(f"Remaining percentage : {remaining_percentage}")
        share_percentage = float(input(f"Enter the percentage {participant.name} has to pay : "))
        # TODO: Handle invalid cases
        share_amount = expense_total_amount * share_percentage / 100
        participant.owe(share_amount)
        remaining_percentage -= share_percentage

    return participants


def divide_equally(expense_total_amount, participants):
    for participant in participants:
        participant.owe(expense_total_amount / len(participants))

    return participants


def handle_spend():
    print("***************************************************")
    print("This is a single expense mode.")

    expense_title = input("Title: ")
    expense_total_amount = float(input("Total amount: "))
    expense = Expense(expense_title, expense_total_amount)
    participants = get_participants()
    expense.add_participants(participants)
    expense.add_liable_participants(participants)

    payers = get_payers(expense, participants)
    expense.add_payers(payers)

    print("How do you want to divide the payment?")
    division_options = ["Divide by Exact Amount", "Divide by Share Percentage", "Divide equally"]
    for index, division_option in enumerate(division_options, start=1):
        print(f"{index}. {division_option}")

    selected_division_option = int(input("Enter the Sno. of your selected option: "))

    if selected_division_option == 1:
        participants = divide_absolutely(expense_total_amount, participants)
    elif selected_division_option == 2:
        participants = divide_percentage_share(expense_total_amount, participants)
    elif selected_division_option == 3:
        participants = divide_equally(expense_total_amount, participants)

    print_all(participants)


def print_all(participants):
    print("*********************************************")
    for participant in participants:
        print(participant)


def get_payers(expense, participants):
    print("======================================================")
    for index, participant in enumerate(participants, start=1):
        print(f"{index}. {participant.name}")
    print(f"Select all the participants who paid for the expense [{expense.title}] : ")
    payer_selected_string = input("Enter the Sno. of the participants : ")
    payer_selected_indices = [int(num) for num in payer_selected_string.split()]
    payers = []
    for payer_selected_index in payer_selected_indices:
        payers.append(participants[payer_selected_index - 1])
    remaining_amount = expense.amount
    print(f"participants paid are : ")
    for payer in payers:
        print(f"Remaining amount : {remaining_amount}")
        amount_paid = float(input(f"Enter amount paid by {payer.name} : "))
        payer.pay(amount_paid)
        remaining_amount -= amount_paid

    return payers


def get_participants():
    participants = []
    names = input("Enter the name of participants separated by space : ")
    name_list = names.split()
    for name in name_list:
        participants.append(Participant(name))
    return participants


def get_liable_participants(participants):
    liable_participants = []

    for participant in participants:
        check = input(f"Should {participant.name} pay for this ? (y/n) : ")
        if check == "y":
            liable_participants.append(participant)

    return liable_participants


def print_sheet(sheet):
    print("--------------------------------------------")
    print(f"Sheet Name : {sheet.name}")
    print("--------------------------------------------")

    for expense in sheet.expenses:
        print("***************************************")
        print(f"Expense title : {expense.title}")
        print(f"Expense Amount : {expense.amount}")
        print("***************************************")

    for participants in sheet.participants:
        print(participants)

def handle_sheet():
    print("**********************************************")
    name = input("Enter the name of sheet : ")
    participants = get_participants()

    sheet = Sheet(name)
    sheet.participants = participants

    reenter = 'y'

    while reenter == 'y':
        title = input("Enter the expense title : ")
        amount = float(input(f"Enter amount for expense [{title}] : "))
        expense = Expense(title, amount)

        expense.add_participants(sheet.participants)
        payers = get_payers(expense, expense.participants)
        expense.add_payers(payers)

        liable_participants = get_liable_participants(expense.participants)

        print("How do you want to divide the payment?")
        division_options = ["Divide by Exact Amount", "Divide by Share Percentage", "Divide equally"]
        for index, division_option in enumerate(division_options, start=1):
            print(f"{index}. {division_option}")

        selected_division_option = int(input("Enter the Sno. of your selected option: "))

        if selected_division_option == 1:
            liable_participants = divide_absolutely(expense.amount, liable_participants)
        elif selected_division_option == 2:
            liable_participants = divide_percentage_share(expense.amount, liable_participants)
        elif selected_division_option == 3:
            liable_participants = divide_equally(expense.amount, liable_participants)

        expense.add_liable_participants(liable_participants)

        sheet.add_expense(expense)
        reenter = input("Would you like to add more expenses? (y/n) : ")

    print_sheet(sheet)


def create_expense():
    print("***************************************************")
    print("You are creating an expense.")
    print("Select the type of expense : ")
    expense_types = ["Single expense - (Spend)", "Multiple expenses - (Sheet)"]
    for index, expense_type in enumerate(expense_types, start=1):
        print(f"{index}. {expense_type}")

    selected_option = int(input("Enter the serial number : "))

    # TODO: handle invalid option numbers
    if selected_option == 1:
        handle_spend()
    elif selected_option == 2:
        handle_sheet()


def view_expense():
    print("You are Viewing an expense.")


def quit_app():
    print("Quitting the app.")


def start_my_app():
    print("***************************************************")
    print("This is an expense Tracker! ")
    print("Select one of the following options : ")
    options = ["Create", "View", "Quit"]
    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    # TODO : Handle error for decimal inputs
    selected_option = int(input("Enter the serial number of your selected option: "))
    while selected_option < 1 or selected_option > 3:
        print(f"Invalid option. Please try again. Enter a number between 1 and {len(options)}")
        selected_option = int(input("Enter the serial number of your selected option: "))

    if selected_option == 1:
        create_expense()
    elif selected_option == 2:
        view_expense()
    elif selected_option == 3:
        quit_app()


# Main function : Entry point of the project
if __name__ == '__main__':
    start_my_app()
