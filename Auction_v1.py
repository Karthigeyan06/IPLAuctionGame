import random

# Original player database (won't be modified)
original_players = {
    "Virat Kohli": {"price": 200, "type": "Batsman"},
    "Rohit Sharma": {"price": 180, "type": "Batsman"},
    "Jasprit Bumrah": {"price": 150, "type": "Bowler"},
    "MS Dhoni": {"price": 120, "type": "Wicketkeeper"},
    "Hardik Pandya": {"price": 100, "type": "All-rounder"},
    "KL Rahul": {"price": 90, "type": "Batsman"},
    "Rishabh Pant": {"price": 80, "type": "Wicketkeeper"},
    "Ravindra Jadeja": {"price": 85, "type": "All-rounder"},
    "Yuzvendra Chahal": {"price": 70, "type": "Bowler"},
    "Mohammed Shami": {"price": 75, "type": "Bowler"}
}

# Create a copy for auction tracking
players = original_players.copy()

# Team setup
teams = {
    "Team A": {"budget": 1000, "players": {}, "spent": 0},
    "Team B": {"budget": 1000, "players": {}, "spent": 0}
}

def display_players():
    print("\nAvailable Players:")
    print("{:<5} {:<20} {:<15} {:<10}".format("No.", "Player", "Type", "Base Price"))
    print("-"*50)
    for i, (player, info) in enumerate(players.items(), 1):
        print("{:<5} {:<20} {:<15} ₹{:<10} lakhs".format(i, player, info["type"], info["price"]))

def display_teams():
    print("\nCurrent Teams Status:")
    for team, info in teams.items():
        print(f"\n{team}:")
        print(f"Budget Remaining: ₹{info['budget']} lakhs")
        print(f"Total Spent: ₹{info['spent']} lakhs")
        print(f"Players bought ({len(info['players'])}):")
        for player, details in info['players'].items():
            print(f"  - {player} ({details['type']}) - ₹{details['price']} lakhs")

def get_bid(team, player, current_bid):
    while True:
        try:
            prompt = f"{team}, enter your bid for {player} (Current: ₹{current_bid} lakhs, 0 to pass): ₹"
            bid = int(input(prompt))
            if bid < 0:
                print("Bid cannot be negative!")
                continue
            if bid > 0 and bid <= current_bid:
                print(f"Bid must be higher than current price (₹{current_bid} lakhs)!")
                continue
            if bid > teams[team]["budget"]:
                print(f"You only have ₹{teams[team]['budget']} lakhs remaining!")
                continue
            return bid
        except ValueError:
            print("Please enter a valid number!")

def conduct_auction():
    player_list = list(players.keys())
    random.shuffle(player_list)
    
    for player in player_list:
        if player not in players:
            continue
            
        base_price = players[player]["price"]
        print(f"\n{'='*50}")
        print(f"Auctioning: {player} ({players[player]['type']}) - Base Price: ₹{base_price} lakhs")
        
        active_teams = [team for team in teams if teams[team]["budget"] >= base_price]
        if not active_teams:
            print(f"No team can afford {player}! Player remains unsold.")
            continue
            
        current_bid = base_price
        bidding_teams = active_teams.copy()
        winning_team = None
        
        while len(bidding_teams) > 0:
            bids = {}
            for team in bidding_teams:
                bid = get_bid(team, player, current_bid)
                if bid == 0:
                    print(f"{team} passes on {player}")
                    bidding_teams.remove(team)
                else:
                    bids[team] = bid
            
            if bids:
                current_bid = max(bids.values())
                winning_team = max(bids, key=bids.get)
                print(f"\nCurrent highest bid: ₹{current_bid} lakhs by {winning_team}")
            elif len(bidding_teams) == 0:
                break  # All teams passed
        
        if winning_team:
            # Store player details including final price
            teams[winning_team]["players"][player] = {
                "type": original_players[player]["type"],
                "price": current_bid
            }
            teams[winning_team]["budget"] -= current_bid
            teams[winning_team]["spent"] += current_bid
            del players[player]
            print(f"\n⭐ {player} sold to {winning_team} for ₹{current_bid} lakhs! ⭐")
        else:
            print(f"\n{player} remains unsold as all teams passed")

def main():
    print("🏏 IPL Auction Terminal Game 🏏")
    print("Two teams will compete to buy 10 players with ₹1000 lakh budgets each\n")
    
    # Set team names
    teams["Team A"]["name"] = input("Enter name for Team A: ") or "Team A"
    teams["Team B"]["name"] = input("Enter name for Team B: ") or "Team B"
    
    input("\nPress Enter to start the auction...")
    display_players()
    conduct_auction()
    
    print("\n\n🎉 Auction Completed! 🎉")
    display_teams()
    
    # Determine winner
    team1, team2 = teams.keys()
    if len(teams[team1]["players"]) > len(teams[team2]["players"]):
        print(f"\n🏆 {teams[team1]['name']} wins the auction!")
    elif len(teams[team1]["players"]) < len(teams[team2]["players"]):
        print(f"\n🏆 {teams[team2]['name']} wins the auction!")
    else:
        print("\nIt's a tie! Both teams have the same number of players.")

if __name__ == "__main__":
    main()
