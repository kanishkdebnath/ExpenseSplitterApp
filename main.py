class Participant:

    def __init__(self, name):
        self.name = name
        self.amount_paid = 0.0
        self.amount_owed = 0.0

    def pay(self, amount):
        self.amount_paid = self.amount_paid + amount

    def owe(self, amount):
        self.amount_owed = self.amount_owed + amount

    def __str__(self):
        return f"{self.name} has paid {self.amount_paid} and owes {self.amount_owed}"


def handle_spend():
    print("This is a single expense mode.")

    expense_title = input("Title: ")
    expense_total_amount = float(input("Total amount: "))
    participants = []

    reenter = "y"
    index = 1
    while reenter == "y":
        name = input(f"Enter the name of #{index} participant : ")
        reenter = input("Would you like to add more (y/n) ? : ")
        index += 1
        participants.append(Participant(name))

    index = 1
    print("===========================================================")
    for participant in participants:
        print(f"{index}. {participant.name}")
        index += 1

    print(f"Select all the participants who paid for the expense [{expense_title}] : ")
    payer_selected_string = input("Enter the Sno. of the participants : ")
    payer_selected_indices = [int(num) for num in payer_selected_string.split()]
    payers = []

    for payer_selected_index in payer_selected_indices:
        payers.append(participants[payer_selected_index - 1])

    print(f"participants paid are : ")
    for payer in payers:
        amount_paid = float(input(f"Enter amount paid by {payer.name} : "))
        payer.pay(amount_paid)

    for participant in participants:
        participant.owe(expense_total_amount/ len(participants))
        print(participant)


def handle_sheet():
    pass


def create_expense():
    print("You are creating an expense.")
    print("Select the type of expense : ")
    expense_types = ["Single expense - (Spend)", "Multiple expenses - (Sheet)"]
    index = 1
    for expense_type in expense_types:
        print(f"{index}. {expense_type}")
        index += 1

    selected_option = int(input("Enter the serial number : "))

    # TODO: handle invalid option numbers
    if selected_option == 1:
        handle_spend()
    elif selected_option == 2:
        handle_sheet()


def view_expense():
    print("You are Viewing an expense.")


def start_my_app():
    print("This is an expense Tracker! ")
    print("Select one of the following options : ")
    options = ["Create", "View", "Quit"]
    index = 1
    for option in options:
        print(f"{index}. {option}")
        index += 1

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
        print("Quitting the app.")


# Main function : Entry point of the project
if __name__ == '__main__':
    start_my_app()
