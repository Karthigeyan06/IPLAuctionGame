import tkinter as tk
from tkinter import messagebox
import random

class IPLAuctionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🏏 IPL Auction Game 🏏")
        self.root.geometry("800x600")
        
        # Original player database
        self.original_players = {
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
        self.players = self.original_players.copy()
        
        # Team setup
        self.teams = {
            "Team A": {"budget": 1000, "players": {}, "spent": 0, "name": "Team A"},
            "Team B": {"budget": 1000, "players": {}, "spent": 0, "name": "Team B"}
        }
        
        # Auction variables
        self.current_player = None
        self.current_bid = 0
        self.bidding_teams = []
        self.auction_active = False
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Team name entry
        self.team_frame = tk.Frame(self.root)
        self.team_frame.pack(pady=10)
        
        tk.Label(self.team_frame, text="Team A Name:").grid(row=0, column=0)
        self.team_a_entry = tk.Entry(self.team_frame)
        self.team_a_entry.grid(row=0, column=1, padx=5)
        self.team_a_entry.insert(0, "Team A")
        
        tk.Label(self.team_frame, text="Team B Name:").grid(row=1, column=0)
        self.team_b_entry = tk.Entry(self.team_frame)
        self.team_b_entry.grid(row=1, column=1, padx=5)
        self.team_b_entry.insert(0, "Team B")
        
        # Start button
        self.start_button = tk.Button(self.root, text="Start Auction", command=self.start_auction)
        self.start_button.pack(pady=10)
        
        # Player info display
        self.player_frame = tk.LabelFrame(self.root, text="Player Auction", padx=10, pady=10)
        self.player_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.player_name_label = tk.Label(self.player_frame, text="", font=("Arial", 14, "bold"))
        self.player_name_label.pack(pady=5)
        
        self.player_type_label = tk.Label(self.player_frame, text="", font=("Arial", 12))
        self.player_type_label.pack(pady=5)
        
        self.bid_label = tk.Label(self.player_frame, text="Current Bid: ₹0 lakhs", font=("Arial", 12, "bold"))
        self.bid_label.pack(pady=10)
        
        # Bidding buttons
        self.bid_button_frame = tk.Frame(self.player_frame)
        self.bid_button_frame.pack(pady=10)
        
        self.team_a_bid_button = tk.Button(
            self.bid_button_frame, 
            text="Bid +50L", 
            command=lambda: self.place_bid("Team A"),
            state=tk.DISABLED
        )
        self.team_a_bid_button.grid(row=0, column=0, padx=10)
        
        self.pass_button = tk.Button(
            self.bid_button_frame, 
            text="Pass", 
            command=self.pass_bid,
            state=tk.DISABLED
        )
        self.pass_button.grid(row=0, column=1, padx=10)
        
        self.team_b_bid_button = tk.Button(
            self.bid_button_frame, 
            text="Bid +50L", 
            command=lambda: self.place_bid("Team B"),
            state=tk.DISABLED
        )
        self.team_b_bid_button.grid(row=0, column=2, padx=10)
        
        # Team info display
        self.team_info_frame = tk.Frame(self.root)
        self.team_info_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.team_a_info = tk.Label(self.team_info_frame, text="", justify="left")
        self.team_a_info.grid(row=0, column=0, padx=10, sticky="w")
        
        self.team_b_info = tk.Label(self.team_info_frame, text="", justify="left")
        self.team_b_info.grid(row=0, column=1, padx=10, sticky="w")
        
        # Results button
        self.results_button = tk.Button(
            self.root, 
            text="Show Final Results", 
            command=self.show_results,
            state=tk.DISABLED
        )
        self.results_button.pack(pady=10)
        
        # Initialize displays
        self.update_team_displays()
    
    def start_auction(self):
        # Set team names
        self.teams["Team A"]["name"] = self.team_a_entry.get() or "Team A"
        self.teams["Team B"]["name"] = self.team_b_entry.get() or "Team B"
        
        # Shuffle players
        self.player_list = list(self.players.keys())
        random.shuffle(self.player_list)
        self.player_index = 0
        
        # Disable start button
        self.start_button.config(state=tk.DISABLED)
        
        # Start first auction
        self.start_next_auction()
    
    def start_next_auction(self):
        if self.player_index >= len(self.player_list):
            self.auction_complete()
            return
            
        self.current_player = self.player_list[self.player_index]
        self.player_index += 1
        
        base_price = self.players[self.current_player]["price"]
        self.current_bid = base_price
        self.bidding_teams = [team for team in self.teams if self.teams[team]["budget"] >= base_price]
        
        if not self.bidding_teams:
            messagebox.showinfo("Player Unsold", f"No team can afford {self.current_player}! Player remains unsold.")
            del self.players[self.current_player]
            self.start_next_auction()
            return
        
        # Update display
        self.player_name_label.config(text=self.current_player)
        self.player_type_label.config(text=f"Type: {self.players[self.current_player]['type']}")
        self.bid_label.config(text=f"Current Bid: ₹{self.current_bid} lakhs")
        
        # Enable buttons for active teams
        self.team_a_bid_button.config(
            state=tk.NORMAL if "Team A" in self.bidding_teams else tk.DISABLED,
            text=f"{self.teams['Team A']['name']} +50L"
        )
        self.team_b_bid_button.config(
            state=tk.NORMAL if "Team B" in self.bidding_teams else tk.DISABLED,
            text=f"{self.teams['Team B']['name']} +50L"
        )
        self.pass_button.config(state=tk.NORMAL)
        
        self.auction_active = True
    
    def place_bid(self, team):
        if not self.auction_active or team not in self.bidding_teams:
            return
            
        new_bid = self.current_bid + 50
        
        if new_bid > self.teams[team]["budget"]:
            messagebox.showwarning("Budget Exceeded", f"{team} doesn't have enough budget for this bid!")
            return
        
        self.current_bid = new_bid
        self.bid_label.config(text=f"Current Bid: ₹{self.current_bid} lakhs")
        
        # If only one team remains, they get the player
        if len(self.bidding_teams) == 1:
            self.sell_player(self.bidding_teams[0])
    
    def pass_bid(self):
        if not self.auction_active:
            return
            
        # Determine which team is passing (the one not currently able to bid)
        active_team = None
        for team in self.teams:
            if self.team_a_bid_button["state"] == tk.NORMAL and team == "Team A":
                active_team = "Team B"
            elif self.team_b_bid_button["state"] == tk.NORMAL and team == "Team B":
                active_team = "Team A"
        
        if active_team and active_team in self.bidding_teams:
            self.bidding_teams.remove(active_team)
            messagebox.showinfo("Team Passed", f"{self.teams[active_team]['name']} has passed on {self.current_player}")
            
            # If only one team remains, they get the player
            if len(self.bidding_teams) == 1:
                self.sell_player(self.bidding_teams[0])
    
    def sell_player(self, team):
        self.teams[team]["players"][self.current_player] = {
            "type": self.original_players[self.current_player]["type"],
            "price": self.current_bid
        }
        self.teams[team]["budget"] -= self.current_bid
        self.teams[team]["spent"] += self.current_bid
        del self.players[self.current_player]
        
        messagebox.showinfo(
            "Player Sold", 
            f"⭐ {self.current_player} sold to {self.teams[team]['name']} for ₹{self.current_bid} lakhs! ⭐"
        )
        
        self.auction_active = False
        self.update_team_displays()
        self.start_next_auction()
    
    def update_team_displays(self):
        for team in self.teams:
            info = f"{self.teams[team]['name']}\n"
            info += f"Budget: ₹{self.teams[team]['budget']} lakhs\n"
            info += f"Spent: ₹{self.teams[team]['spent']} lakhs\n"
            info += f"Players: {len(self.teams[team]['players'])}\n"
            
            if team == "Team A":
                self.team_a_info.config(text=info)
            else:
                self.team_b_info.config(text=info)
    
    def auction_complete(self):
        messagebox.showinfo("Auction Complete", "The auction has finished!")
        self.results_button.config(state=tk.NORMAL)
        
        # Disable all buttons
        self.team_a_bid_button.config(state=tk.DISABLED)
        self.team_b_bid_button.config(state=tk.DISABLED)
        self.pass_button.config(state=tk.DISABLED)
    
    def show_results(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Auction Results")
        
        # Determine winner
        team1, team2 = self.teams.keys()
        if len(self.teams[team1]["players"]) > len(self.teams[team2]["players"]):
            winner = f"🏆 {self.teams[team1]['name']} wins the auction!"
        elif len(self.teams[team1]["players"]) < len(self.teams[team2]["players"]):
            winner = f"🏆 {self.teams[team2]['name']} wins the auction!"
        else:
            winner = "It's a tie! Both teams have the same number of players."
        
        tk.Label(result_window, text=winner, font=("Arial", 14, "bold")).pack(pady=10)
        
        # Team A results
        team_a_frame = tk.LabelFrame(result_window, text=self.teams["Team A"]["name"], padx=10, pady=10)
        team_a_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        team_a_text = f"Budget Remaining: ₹{self.teams['Team A']['budget']} lakhs\n"
        team_a_text += f"Total Spent: ₹{self.teams['Team A']['spent']} lakhs\n"
        team_a_text += f"Players bought ({len(self.teams['Team A']['players'])}):\n"
        
        for player, details in self.teams["Team A"]["players"].items():
            team_a_text += f"  - {player} ({details['type']}) - ₹{details['price']} lakhs\n"
        
        tk.Label(team_a_frame, text=team_a_text, justify="left").pack()
        
        # Team B results
        team_b_frame = tk.LabelFrame(result_window, text=self.teams["Team B"]["name"], padx=10, pady=10)
        team_b_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        team_b_text = f"Budget Remaining: ₹{self.teams['Team B']['budget']} lakhs\n"
        team_b_text += f"Total Spent: ₹{self.teams['Team B']['spent']} lakhs\n"
        team_b_text += f"Players bought ({len(self.teams['Team B']['players'])}):\n"
        
        for player, details in self.teams["Team B"]["players"].items():
            team_b_text += f"  - {player} ({details['type']}) - ₹{details['price']} lakhs\n"
        
        tk.Label(team_b_frame, text=team_b_text, justify="left").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = IPLAuctionGame(root)
    root.mainloop()
