class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(item['amount'] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {category.name}')
            category.deposit(amount, f'Transfer from {self.name}')
            return True
        return False


    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = f"*************{self.name}*************"
        items = "\n".join(f"{item['description'][:23]:<23}{item['amount']:>7.2f}" for item in self.ledger)
        total = f"Total: {self.get_balance():.2f}"
        return f"{title}\n{items}\n{total}"

def create_spend_chart(categories):
    total_spent = sum(sum(item['amount'] for item in category.ledger if item['amount'] < 0) for category in categories)
    chart = ['Percentage spent by category']

    # Calculate spending percentage for each category
    spending_percentages = []
    for category in categories:
        category_spent = sum(item['amount'] for item in category.ledger if item['amount'] < 0)
        spending_percentages.append((category.name, category_spent / total_spent * 100 if total_spent > 0 else 0))

    # Calculate the height of the bars (rounded down to nearest 10)
    bar_heights = [int(percentage[1] // 10) * 10 for percentage in spending_percentages]

    # Determine the height of the chart
    max_height = 100
    chart_width = len(categories) * 3 + 1  # 3 characters per category for the bars and an additional space
    # Build the chart from top to bottom
    for i in range(max_height, -1, -10):
        line = f"{i:3}| "
        for height in bar_heights:
            if height >= i:
                line += 'o  '  # 'o' for a filled bar, two spaces after
            else:
                line += '   '  # Empty space between bars
        chart.append(line.rstrip())  # Remove trailing spaces after the final bar

    # Add the horizontal line
    chart.append('    ' + '-' * (len(categories) * 3 + 1))  # 3 dashes per category, plus an extra space

    # Add category names under the chart
    max_name_length = max(len(category.name) for category in categories)
    for i in range(max_name_length):
        line = '     '
        for name, _ in spending_percentages:
            line += (name[i] if i < len(name) else ' ') + '  '  # 2 spaces after each character
        chart.append(line.rstrip())  # Remove trailing spaces after the final name

    return "\n".join(chart)


# Example Usage
food = Category('Food')
food.deposit(1000, 'initial deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing = Category('Clothing')
food.transfer(50, clothing)

print(food)
print(clothing)

categories = [food, clothing]
print(create_spend_chart(categories))