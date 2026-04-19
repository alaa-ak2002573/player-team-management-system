PLAYERS_FILE = "players.txt"
TEAMS_FILE = "teams.txt"
STATISTICS_FILE = "statistics.txt"


def load_teams():
    teams = {}
    try:
        with open(TEAMS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    team_id, team_name = line.split(",", 1)
                    teams[int(team_id)] = team_name
    except FileNotFoundError:
        pass
    return teams


def save_teams(teams):
    with open(TEAMS_FILE, "w") as file:
        for team_id, team_name in teams.items():
            file.write(f"{team_id},{team_name}\n")


def load_players():
    players = []
    try:
        with open(PLAYERS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    player_id, name, goals, yellow_cards, red_cards, team_id = line.split(",")
                    players.append({
                        "id": int(player_id),
                        "name": name,
                        "goals": int(goals),
                        "yellow_cards": int(yellow_cards),
                        "red_cards": int(red_cards),
                        "team_id": int(team_id)
                    })
    except FileNotFoundError:
        pass
    return players


def save_players(players):
    with open(PLAYERS_FILE, "w") as file:
        for player in players:
            file.write(
                f"{player['id']},{player['name']},{player['goals']},"
                f"{player['yellow_cards']},{player['red_cards']},{player['team_id']}\n"
            )


def display_menu():
    print("\nMenu:")
    print("1. Add Player")
    print("2. Update Player Statistics")
    print("3. Show Statistics")
    print("4. Add Team")
    print("5. Display All Players")
    print("6. Show Players Without Teams")
    print("7. Delete a Player")
    print("8. Delete a Team")
    print("9. Exit")


def get_valid_choice():
    while True:
        try:
            choice = int(input("Enter your choice (1-9): "))
            if 1 <= choice <= 9:
                return choice
            print("Error: please enter a number between 1 and 9.")
        except ValueError:
            print("Error: please enter a valid number.")


def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: please enter a valid integer.")


def find_player_by_id(players, player_id):
    for player in players:
        if player["id"] == player_id:
            return player
    return None


def add_player(players, teams):
    print("\n*** Add Player ***")
    player_id = get_valid_int("Enter player ID: ")

    if find_player_by_id(players, player_id) is not None:
        print("Error: Player ID already exists.")
        return

    name = input("Enter player name: ").strip()
    goals = get_valid_int("Enter number of goals: ")
    yellow_cards = get_valid_int("Enter number of yellow cards: ")
    red_cards = get_valid_int("Enter number of red cards: ")
    team_id = get_valid_int("Enter team ID (Enter 0 if no team): ")

    if team_id != 0 and team_id not in teams:
        print("Error: Please enter a valid team ID.")
        return

    players.append({
        "id": player_id,
        "name": name,
        "goals": goals,
        "yellow_cards": yellow_cards,
        "red_cards": red_cards,
        "team_id": team_id
    })

    save_players(players)
    print("Player added successfully.")


def update_player_statistics(players, teams):
    print("\n*** Update Player Statistics ***")
    player_id = get_valid_int("Enter the ID of the player to update: ")
    player = find_player_by_id(players, player_id)

    if player is None:
        print("Error: Player not found.")
        return

    print("Update options:")
    print("1. Add goal")
    print("2. Add yellow card")
    print("3. Add red card")
    print("4. Change team")

    update_choice = get_valid_int("Enter your choice (1-4): ")

    if update_choice == 1:
        player["goals"] += 1
    elif update_choice == 2:
        player["yellow_cards"] += 1
    elif update_choice == 3:
        player["red_cards"] += 1
    elif update_choice == 4:
        new_team_id = get_valid_int("Enter team ID (Enter 0 if no team): ")
        if new_team_id != 0 and new_team_id not in teams:
            print("Error: Please enter a valid team ID.")
            return
        player["team_id"] = new_team_id
    else:
        print("Error: Invalid choice.")
        return

    save_players(players)
    print("Player data updated successfully.")


def show_statistics(players):
    print("\nStatistics:")

    if not players:
        print("No player data available.")
        return

    total_goals = sum(player["goals"] for player in players)
    total_yellow = sum(player["yellow_cards"] for player in players)
    total_red = sum(player["red_cards"] for player in players)
    average_goals = total_goals / len(players)

    max_goals_player = max(players, key=lambda p: p["goals"])
    max_yellow_player = max(players, key=lambda p: p["yellow_cards"])
    max_red_player = max(players, key=lambda p: p["red_cards"])

    print(f"Total goals: {total_goals}")
    print(f"Average goals per player: {average_goals:.2f}")
    print(f"Total yellow cards: {total_yellow}")
    print(f"Total red cards: {total_red}")
    print(f"Player with highest goals: {max_goals_player['name']} ({max_goals_player['goals']} goals)")
    print(
        f"Player with highest yellow cards: "
        f"{max_yellow_player['name']} ({max_yellow_player['yellow_cards']} yellow cards)"
    )
    print(
        f"Player with highest red cards: "
        f"{max_red_player['name']} ({max_red_player['red_cards']} red cards)"
    )

    with open(STATISTICS_FILE, "w") as file:
        file.write(f"Total goals: {total_goals}\n")
        file.write(f"Average goals per player: {average_goals:.2f}\n")
        file.write(f"Total yellow cards: {total_yellow}\n")
        file.write(f"Total red cards: {total_red}\n")
        file.write(
            f"Player with highest goals: "
            f"{max_goals_player['name']} ({max_goals_player['goals']} goals)\n"
        )
        file.write(
            f"Player with highest yellow cards: "
            f"{max_yellow_player['name']} ({max_yellow_player['yellow_cards']} yellow cards)\n"
        )
        file.write(
            f"Player with highest red cards: "
            f"{max_red_player['name']} ({max_red_player['red_cards']} red cards)\n"
        )

    print("Statistics saved to statistics.txt")


def add_team(teams):
    print("\n*** Add Team ***")
    team_id = get_valid_int("Enter team ID: ")

    if team_id in teams:
        print("Error: Team ID already exists.")
        return

    team_name = input("Enter team name: ").strip()
    teams[team_id] = team_name
    save_teams(teams)
    print("Team added successfully.")


def display_all_players(players, teams):
    print("\nAll Players:")
    print("{:<5} {:<20} {:<10} {:<10} {:<10} {:<15}".format(
        "ID", "Name", "Goals", "Y-Cards", "R-Cards", "Team"
    ))
    print("-" * 75)

    if not players:
        print("No players found.")
        return

    for player in players:
        team_name = teams.get(player["team_id"], "NO TEAM") if player["team_id"] != 0 else "NO TEAM"
        print("{:<5} {:<20} {:<10} {:<10} {:<10} {:<15}".format(
            player["id"],
            player["name"],
            player["goals"],
            player["yellow_cards"],
            player["red_cards"],
            team_name
        ))


def show_players_without_teams(players):
    print("\nPlayers Without a Team:")
    print("{:<5} {:<20} {:<10} {:<10} {:<10}".format(
        "ID", "Name", "Goals", "Y-Cards", "R-Cards"
    ))
    print("-" * 60)

    found = False
    for player in players:
        if player["team_id"] == 0:
            found = True
            print("{:<5} {:<20} {:<10} {:<10} {:<10}".format(
                player["id"],
                player["name"],
                player["goals"],
                player["yellow_cards"],
                player["red_cards"]
            ))

    if not found:
        print("No players without teams found.")


def delete_player(players):
    print("\n*** Delete a Player ***")
    player_id = get_valid_int("Enter the player ID to delete: ")
    player = find_player_by_id(players, player_id)

    if player is None:
        print("Error: Player not found.")
        return

    players.remove(player)
    save_players(players)
    print(f"Player with ID {player_id} deleted successfully.")


def delete_team(players, teams):
    print("\n*** Delete a Team ***")
    team_id = get_valid_int("Enter the team ID to delete: ")

    if team_id not in teams:
        print("Error: Team not found.")
        return

    del teams[team_id]
    save_teams(teams)

    players[:] = [player for player in players if player["team_id"] != team_id]
    save_players(players)

    print(f"Team with ID {team_id} and its players deleted successfully.")


def main():
    while True:
        players = load_players()
        teams = load_teams()

        display_menu()
        choice = get_valid_choice()

        if choice == 1:
            add_player(players, teams)
        elif choice == 2:
            update_player_statistics(players, teams)
        elif choice == 3:
            show_statistics(players)
        elif choice == 4:
            add_team(teams)
        elif choice == 5:
            display_all_players(players, teams)
        elif choice == 6:
            show_players_without_teams(players)
        elif choice == 7:
            delete_player(players)
        elif choice == 8:
            delete_team(players, teams)
        elif choice == 9:
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
