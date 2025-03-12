# Generating the complete upgraded Python file with all requested features

# Define the new game code with all features integrated
import pygame
import random
import sys

# Initialize pygame
pygame.init()

# -------------------------------
# Constants and Global Variables
# -------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 30

selected_team = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
BASEBALL_GREEN = (34, 139, 34)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Baseball GM Simulator")

clock = pygame.time.Clock()

# -------------------------------
# Game Classes
# -------------------------------

class Player:
    def __init__(self, name, position, attributes=None, potential=None, age=None):
        self.name = name
        self.position = position
        self.age = age if age else random.randint(18, 35)
        self.attributes = attributes if attributes else {
            "speed": random.randint(20, 80),
            "power": random.randint(20, 80),
            "contact": random.randint(20, 80),
            "eye": random.randint(20, 80),
            "fielding": random.randint(20, 80),
            "stamina": random.randint(20, 80)
        }
        self.potential = potential if potential else random.randint(40, 80)
        self.stats = {
            "hits": 0, "home_runs": 0, "strikeouts": 0, "walks": 0, "games": 0
        }
        self.career_stats = self.stats.copy()

    def overall_rating(self):
        return int(sum(self.attributes.values()) / len(self.attributes))

    def develop(self):
        if self.age < 28:
            for key in self.attributes.keys():
                if random.random() < 0.5:
                    self.attributes[key] += random.randint(1, 5)
                    self.attributes[key] = min(self.attributes[key], 80)
        elif self.age > 30:
            for key in self.attributes.keys():
                if random.random() < 0.3:
                    self.attributes[key] -= random.randint(1, 3)
                    self.attributes[key] = max(self.attributes[key], 20)
        self.age += 1

class Team:
    def __init__(self, name):
        self.name = name
        self.players = [Player(f"Player {i}", "Random") for i in range(25)]
        self.wins = 0
        self.losses = 0

    def draft_player(self, player):
        self.players.append(player)

class League:
    def __init__(self):
        self.teams = [Team(f"Team {i}") for i in range(30)]
        self.schedule = []

    def generate_schedule(self):
        for i in range(162):
            home = random.choice(self.teams)
            away = random.choice([t for t in self.teams if t != home])
            self.schedule.append((home, away))

    def play_season(self):
        for game in self.schedule:
            home, away = game
            home_score = random.randint(0, 10)
            away_score = random.randint(0, 10)
            if home_score > away_score:
                home.wins += 1
                away.losses += 1
            else:
                away.wins += 1
                home.losses += 1

    def playoffs(self):
        teams_sorted = sorted(self.teams, key=lambda x: x.wins, reverse=True)
        print("PLAYOFF TEAMS:", [t.name for t in teams_sorted[:10]])

class Draft:
    def __init__(self):
        self.prospects = [Player(f"Draft Pick {i}", "Random", age=18, potential=random.randint(60, 80)) for i in range(200)]

    def start_draft(self, league):
        for i in range(5):
            for team in league.teams:
                best_player = max(self.prospects, key=lambda p: p.potential)
                team.draft_player(best_player)
                self.prospects.remove(best_player)

class Game:
    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.score = {home_team.name: 0, away_team.name: 0}

    def play_game(self):
        for _ in range(9):
            self.score[self.home_team.name] += random.randint(0, 3)
            self.score[self.away_team.name] += random.randint(0, 3)
        print(f"FINAL SCORE: {self.home_team.name} {self.score[self.home_team.name]} - {self.away_team.name} {self.score[self.away_team.name]}")

class HallOfFame:
    def __init__(self):
        self.inductees = []

    def consider_for_hof(self, player):
        if player.career_stats["home_runs"] > 500 or player.career_stats["hits"] > 3000:
            self.inductees.append(player.name)
            print(f"{player.name} inducted into the Hall of Fame!")

# -------------------------------
# Main Game Loop
# -------------------------------

def main():
    league = League()
    league.generate_schedule()

    draft = Draft()
    draft.start_draft(league)

    print("Season Starting...")
    league.play_season()

    print("Regular Season Over!")
    league.playoffs()

    game = Game(league.teams[0], league.teams[1])
    game.play_game()

    hall_of_fame = HallOfFame()
    for team in league.teams:
        for player in team.players:
            hall_of_fame.consider_for_hof(player)

    print("Hall of Fame Inductees:", hall_of_fame.inductees)

if __name__ == "__main__":
    main()
