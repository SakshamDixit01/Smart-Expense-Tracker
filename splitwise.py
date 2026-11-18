from decimal import Decimal, ROUND_HALF_UP

from storage import ( 
    load_groups,
    save_groups,
    load_settlements,
    save_settlements
)

def money(value):
    """ Convert an amount to two-decimal-place rupee precision."""

    return Decimal(str(value)).quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

def get_amount(prompt):
    """ Accept a valid positive amount."""
    while True:
        try:
            amount = money(input(prompt).strip())

            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except Exception:
            print("Please Enter a valid amount e.g 250,500")

def choose_group(groups):
    """ Choose group by its ID."""
    if not groups:
        print("No groups found. Create a group first")

        return None
    print("\nAvailable Groups:")
    for group in groups:
        print(f"{group['id']}.{group['name']}")

    try:
        group_id = int(input("Enter group ID: "))
    except ValueError:
        print("Invalid group ID.")
        return None

    for group in groups:
        if group["id"] == group_id:
            return group
    print("Group Not Found")
    return None

def choose_member(members,prompt="Enter Member Number:  "):
    """ Choose a member from a list."""
    print("/nMembers:  ")
    for index , member in enumerate(members, start=1):
        print(f"{index}.{members}")

    try:
        choice = int(input(prompt))
        if 1 <= choice <= len(members):
            return members[choice - 1]
    except ValueError:
        pass
    print("Invalid member Selection.")
    return None

def create_group():
    """ Create a group with multiple memebrs."""
    print("\n --- Create Splitwise Group ---")

    name = input("Enter group name: ").strip()
    if not name:
        print("Group name cannot be empty.")
        return
    raw_members = input("Enter member names seperated by commas:  ").strip()

    members = list(dict.fromkeys(member.strip()
                                 for member in raw_members.split(",")
                                 if member.strip()))

    if len(members) < 2:
        print("Please enter at least two different members")
        return

    groups = load_groups()

    group_id = max((group.get("id",0) for group in groups), default=0) + 1

    group = {
        "id" : group_id,
        "name" : name,
        "members": members,
        "expenses": []    }

    groups.append(group)

    if save_groups(groups):
        print(f"\nGroup '{name}' created successfully!")
        print(f"Group ID: {group_id}")
        print("Members: ", ",".join(members))
    else:
        print("Could not save the group.")

def view_groups():
    """ Display all groups and thier members. """

    print("\n---- Your Groups ----")

    groups = load_groups()

    if not groups:
        print("No groups created yet.")
        return

    for group in groups:
        print(f"\nGroup ID: {group['id']}")
        print(f"Name : {group['name']}")
        print("Members: ",",".join(group["members"]))
        print(f"Shared Bills:{len(group.get('expenses',[]))}")

def add_group_expenses():
    """ Add a bill paid by one group member."""

    print("\n --- Add group Expense ---")

    groups = load_groups()
    group = choose_group(groups)

    if group is None:
        return

    members = group["members"]

    description = input("Enter Bill description:  ").strip()

    if not description:
        description = "Shared expense"

    amount = get_amount("Enter total bill amount : ")

    payer = choose_member(members, "Who paid? Enter member number: ")

    if payer is None:
        return

    print("\nSelect participants who share this bill ")
    print("Enter thier numbers seperated by commas")
    for index , member in enumerate(members , start=1):
        print(f"{index}. {member}")

    raw = input("Partcipants (e.g.1,2,3): ").strip()


    try: 
        indexes = [
            int(part.strip())
            for part in raw.split(",")
            if part.strip()
        ]

        if not indexes:
            print("Select at least one participant ")
            return
        if any(i<1 or i>len(members) for i in indexes):
            print("Invalid participant number")

            return
        if len(indexes) != len(set(indexes)):
            print("Duplicate Participant numbers are not allowed")
            return

    except ValueError:
        print("Enter participant numbers seperated by commas")
        return

    participants = [members[i - 1] for i in indexes]


    total_paise = int(amount * 100)
    base_share , remainder = divmod(total_paise, len(participants))

    shares = {}
    for index, member in enumerate(participants):
        share_paise = base_share + (1 if index < remainder else 0)
        shares[member] = str(money(Decimal(share_paise) / 100 ))

    expense_id = max((expense.get("id", 0)
                      for expense in group.get("expense",[])),default=0) + 1

    expense = {
        "id" : expense_id,
        "description": description,
        "amount": str(amount),
        "paid_by": payer,
        "participant": participants,
        "shares": shares
    }

    group.setdefault("expenses",[]).append(expense)

    if save_groups(groups):
        print("\nGroup expense added successfully")
        print(f"Bill:{description}")
        print(f"Paid By: {payer}")
        print("\nIndividual Shares: ")

        for member, share in shares.items():
            print(f"{member}: {share}")
    else:
        print("Could not save the group expense. ")

def calculate_balance(group):
    """ Calculate each member's net balance .
    Positive balance means they should recieve money.
    Negative balance means they owe money. """

    balances = {member: Decimal("0.00") for member in group['members']}

    for expense in group.get("expense", []):
        payer = expense["paid_by"]
        amount = money(expense["amount"])

        if payer not in balances:
            continue

        balances[payer] += amount

        for member, share in expense["shares"].items():
            if member in balances:
                balances[member] -= money(share)

    settlements = load_settlements()

    for settlement in settlements:
        if settlement.get("group_id") != group["id"]:
            continue
        payer = settlement["from"]

        reciever = settlement["to"]
        amount = money(settlement["amount"])

        if payer in balances and reciever in balances:
            balances[payer] += amount
            balances[reciever] -= amount

    return balances


def view_balances():
    """ Show net balances and suggested settlements """
    print("\n ---- Group Balance ----")


    groups = load_groups()
    group = choose_group(groups)


    if group is None:
        return 

    balances = calculate_balance(group)

    print(f"\nBalances for : {group['name']}")
    print("-" * 35)


    for member , balance in balances.items():
        if balance > 0:
            status = "gets back "
        elif balance < 0:
            status = "owes"
        else:
            status = "settled"

        print(f"{member:<18}{abs(balance):>9.2f}  {status}")

    print("\n Suggested settlements:  ")

    debts = [
        [member, -balance]
        for member , balance in balances.items()
            if balance < 0 ]

    credits = [
        [member, balance]
        for member , balance in balances.items()
        if balance > 0 

    ]

    i = j = 0

    while i < len(debts) and j < len(credits):
        debtor , owed = debts[i]
        creditor , credit = credits[j]

        amount = min(owed , credit)

        if amount > 0:
            print(f"{debtor} pays {creditor}: {amount:.2f}")

            debts[i][1] -= amount
            credits[j][1] -= amount

            if debts[i][1] == 0:
                i += 1
            if credits[j][1] == 0:
                j += 1

    if not any(balance != 0 for balance in balances.values()):
        print("Everyone is Settled")


def settle_balance():
    """ Record a Repayment between two members """

    print("\n --- Settle a Balance ---")

    groups = load_groups()
    group = choose_group(groups)


    if group is None:
        return 

    balances = calculate_balance(group)

    debtor = choose_member(
        group["members"], "Who is paying back ? Enter Member number : " )

    if debtor is None:
        return 

    creditor = choose_member(
        group["members"], "Who recieves the Payment ? Enter Member Number:  ")

    if creditor is None:
        return 

    if debtor == creditor:
        print("The Payer and reciever must be different.")

        return 


    if balances[debtor] >= 0 or balances[creditor] <= 0:
        print("These members do not currently have a debt in this direction. ")

        print("Check Group Balances before rcording a repayment ")
        return 


    maximum = -balances[debtor]

    amount = get_amount("Enter repayment amount:  ")

    if amount > maximum:
        print(f"That exceeds the debtor's total outstanding {maximum:.2f}.")

        return

    settlements = load_settlements()

    settlement = {
        "group_id": group["id"],
        "from": debtor,
        "to": creditor,
        "amount": str(amount)
        }

    settlements.append(settlement)

    if save_settlements(settlements):
        print("\n Repayment recorded successfully ! ")

        print(f"{debtor} paid {creditor} {amount:.2f}")

        print("View group Balances to see updated amounts.")

    else:
        print("Could not save the repayment.")