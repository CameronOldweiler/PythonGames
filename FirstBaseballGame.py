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
FPS = 30  # Frames per second for the game loop

selected_team = None  # Stores the currently chosen team

# Define some basic colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)  # Background color (like a baseball field)
BASEBALL_GREEN = (34, 139, 34)
RED = (255, 0, 0)
DODGER_BLUE = (0, 90, 156)
ROCKIES_PURPLE = (51, 0, 111)
DIAMONDBACK_RED = (167, 25, 48)
PADRE_BROWN = (47, 36, 29)
GIANT_ORANGE = (253, 90, 30)

# Set up the main display window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Baseball GM Simulator")

# Load the pitcher image and convert it for faster blitting
pitcher_image = pygame.image.load("Graphics/Baseball Game/player.jpg").convert()

# Remove the white background by setting it as transparent
pitcher_image.set_colorkey(WHITE)

# (Optional) Scale the image if it's too big:
pitcher_image = pygame.transform.scale(pitcher_image, (100, 100))

# Load the baseball image and convert it for faster blitting
baseball_image = pygame.image.load("Graphics/Baseball Game/Baseball.png").convert()

# Remove the white background by setting it as transparent
baseball_image.set_colorkey(WHITE)

# (Optional) Scale the image if it's too big:
baseball_image = pygame.transform.scale(baseball_image, (100, 125))

baseball_diamond_image = pygame.image.load("Graphics/Baseball Game/baseballdiamond.jpg").convert()

baseball_diamond_image.set_colorkey(WHITE)

baseball_diamond_image = pygame.transform.scale(baseball_diamond_image, (250, 250))

rockies_logo = pygame.image.load("Graphics/Baseball Game/RockiesLogo.png").convert()

rockies_logo.set_colorkey(BLACK)

rockies_logo = pygame.transform.scale(rockies_logo, (100, 100))

# Create a clock object to help control the game's frame rate
clock = pygame.time.Clock()

# -------------------------------
# Game Classes
# -------------------------------

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font_size=36, border_radius=20):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
        self.border_radius = border_radius

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class Coach:
    def __init__(self, name, role, experience = None, hitting = None,
                 pitching = None, fielding = None):
        self.name = name
        self.role = role
        self.attributes = {
            "experience": experience if experience is not None else random.randint(0, 20),
            "hitting": hitting if hitting is not None else random.randint(20, 80),
            "pitching": pitching if pitching is not None else random.randint(20, 80),
            "fielding": fielding if fielding is not None else random.randint(20, 80)
        }
        self.stats = {
            "wins": 0,
            "losses": 0,
            "championships": 0
        }

class Pitcher:
    def __init__(self, name, position,
                 velocity=None, stuff=None,
                 movement=None, control=None,
                 stamina=None):
        self.name = name
        self.position = position
        self.attributes = {
            "velocity": velocity if velocity is not None else random.randint(20, 80),
            "stuff": stuff if stuff is not None else random.randint(20, 80),
            "movement": movement if movement is not None else random.randint(20, 80),
            "control": control if control is not None else random.randint(20, 80),
            "stamina": stamina if stamina is not None else random.randint(20, 80)
        }
        self.stats = {
            "ERA": 0.00,
            "WHIP": 0.00,
            "Runs Allowed": 0,
            "Innings Pitched": 0.0,
            "Hits Allowed": 0,
            "Walks Allowed": 0,
            "Home Runs Allowed": 0,
            "Batters Faced": 0,
            "Strikeouts": 0
        }

    def updateStats(self):
        hits_allowed = self.stats["Hits Allowed"]
        walks_allowed = self.stats["Walks Allowed"]
        runs_allowed = self.stats["Runs Allowed"]
        innings_pitched = self.stats["Innings Pitched"]
        batters_faced = self.stats["Batters Faced"]

        if batters_faced > 0:
            self.stats["WHIP"] = (hits_allowed + walks_allowed) / innings_pitched
            self.stats["ERA"] = runs_allowed / innings_pitched
        else:
            self.stats["WHIP"] = 0.000
            self.stats["ERA"] = 0.00

class Batter:
    def __init__(self, name, position,
                 speed = None, framing = None, blocking = None, arm = None,
                 range = None, arm_strength = None, power = None, contact = None,
                 eye = None, gap_power = None, triple = None, framing_pot = None,
                 blocking_pot = None, arm_pot = None, range_pot = None,
                 arm_stength_pot = None, power_pot = None, contact_pot = None,
                 eye_pot = None, gap_power_pot = None, triple_pot = None):
        self.name = name
        self.position = position
        self.attributes = {
            "speed": speed if speed is not None else random.randint(20, 80),
            "framing": framing if framing is not None else random.randint(20, 35),
            "blocking": blocking if blocking is not None else random.randint(20, 35),
            "arm": arm if arm is not None else random.randint(20, 35),
            "range": range if range is not None else random.randint(20, 50),
            "arm_strength": arm_strength if arm_strength is not None else random.randint(20, 50),
            "power": power if power is not None else random.randint(20, 50),
            "contact": contact if contact is not None else random.randint(20, 50),
            "eye": eye if eye is not None else random.randint(20, 50),
            "gap_power": gap_power if gap_power is not None else random.randint(20, 50),
            "triple": triple if triple is not None else random.randint(20, 50),
            "framing_pot": framing_pot if framing_pot is not None else random.randint(25, 40),
            "blocking_pot": blocking_pot if blocking_pot is not None else random.randint(25, 40),
            "arm_pot": arm_pot if arm_pot is not None else random.randint(25, 40),
            "range_pot": range_pot if range_pot is not None else random.randint(25, 55),
            "arm_strength_pot": arm_stength_pot if arm_stength_pot is not None else random.randint(25, 55),
            "power_pot": power_pot if power_pot is not None else random.randint(25,55),
            "contact_pot": contact_pot if contact_pot is not None else random.randint(25, 55),
            "eye_pot": eye_pot if eye_pot is not None else random.randint(25, 55),
            "gap_power_pot": gap_power_pot if gap_power_pot is not None else random.randint(25, 55),
            "triple_pot": triple_pot if triple_pot is not None else random.randint(25, 55)
        }
        self.stats = {
            "hits": 0,
            "at_bats": 0,
            "plate_appearances": 0,
            "home_runs": 0,
            "triples": 0,
            "doubles": 0,
            "walks": 0,
            "total_bases": 0,
            "batting_average": 0.000,
            "on_base_percentage": 0.000,
            "slugging_percentage": 0.000,
            "on_base_plus_slugging": 0.000
        }

    def update_stats(self):
        at_bats = self.stats["at_bats"]
        hits = self.stats["hits"]
        walks = self.stats["walks"]
        doubles = self.stats["doubles"]
        triples = self.stats["triples"]
        home_runs = self.stats["home_runs"]
        plate_appearances = self.stats["plate_appearances"]

        if plate_appearances > 0:
            self.stats["total_bases"] = (home_runs * 4) + (triples * 3) + (doubles * 2) + (hits - (home_runs + triples + doubles))
        else:
            self.stats["total_bases"] = 0

        if at_bats > 0:
            self.stats["batting_average"] = hits / at_bats
        else:
            self.stats["batting_average"] = 0.000

        if plate_appearances > 0:
            self.stats["on_base_percentage"] = (hits + walks) / plate_appearances
        else:
            self.stats["on_base_percentage"] = 0.000

        if at_bats > 0:
            self.stats["slugging_percentage"] = self.stats["total_bases"] / at_bats
        else:
            self.stats["slugging_percentage"] = 0.000

        self.stats["on_base_plus_slugging"] = (self.stats["on_base_percentage"] +
                                               self.stats["slugging_percentage"])

    def atbat(self, pitcher):
        self.stats["plate_appearances"] += 1
        pitcher.stats["Batters Faced"] += 1

        contact_probability = self.attributes["contact"] / 100.0
        gap_power_probability = self.attributes["gap power"] / 100.0
        power_probability = self.attributes["power"] / 100.0
        walk_probability = self.attributes["eye"] / 100.0
        triple_probability = self.attributes["triple"] / 100.0

        if random.random() < contact_probability:
            self.stats["at_bats"] += 1
            self.stats["hits"] += 1
            pitcher.stats["Hits Allowed"] += 1

            if random.random() < triple_probability:
                self.stats["triples"] += 1
                return 3
            elif random.random() < gap_power_probability:
                self.stats["doubles"] += 1
                return 2
            elif random.random() < power_probability:
                self.stats["home_runs"] += 1
                pitcher.stats["Home Runs Allowed"] += 1
                return 4
            else:
                return 1

        if random.random() < walk_probability:
            self.stats["walks"] += 1
            pitcher.stats["Walks Allowed"] += 1
            return 0.5

        pitcher.stats["Strikeouts"] += 1
        return 0

class Team:
    """
    Represents a baseball team.
    """
    def __init__(self, name, batters, pitchers, staff):
        self.name = name
        self.batters = batters
        self.pitchers = pitchers
        self.staff = staff
        self.score = 0
        self.current_batter_index = 0
        self.current_pitcher_index = 0

    def get_next_batter(self):
        batter = self.batters[self.current_batter_index]
        self.current_batter_index = (self.current_batter_index + 1) % 9
        return batter

    def get_next_pitcher(self):
        pitcher = self.pitchers[self.current_pitcher_index]
        # FIX: Update the pitcher index correctly using self.current_pitcher_index
        self.current_pitcher_index = (self.current_pitcher_index + 1) % len(self.pitchers)
        return pitcher

    def update_bases_and_score(self, hit_type, bases):
        runs_scored = 0

        if hit_type == 4:  # Home run: everyone scores
            runs_scored += sum(1 for base in bases if base is not None) + 1
            bases[:] = [None, None, None]
        else:
            if bases[2] is not None:
                runs_scored += 1
                bases[2] = None
            if hit_type == 0.5:
                bases.insert(0, True)
                bases.pop()
            if hit_type == 1:
                bases.insert(0, True)
                bases.pop()
            elif hit_type == 2:
                if bases[1] is not None:
                    runs_scored += 1
                    bases[1] = None
                if bases[2] is not None:
                    runs_scored += 1
                    bases[2] = None
                bases.insert(1, True)
                bases.pop()
            elif hit_type == 3:
                if bases[0] is not None:
                    runs_scored += 1
                    bases[0] = None
                if bases[1] is not None:
                    runs_scored += 1
                    bases[1] = None
                if bases[2] is not None:
                    runs_scored += 1
                    bases[2] = None
                bases.insert(2, True)
                bases.pop()
        return runs_scored

    def play_half_inning(self):
        outs = 0
        total_runs = 0
        bases = [None, None, None]
        while outs < 3:
            current_pitcher = self.get_next_pitcher()
            current_batter = self.get_next_batter()
            result = current_batter.atbat(current_pitcher)
            if result == 0:
                outs += 1
            else:
                runs_on_play = self.update_bases_and_score(result, bases)
                total_runs += runs_on_play
        return total_runs

class Game:
    """
    Represents a baseball game simulation.
    """
    def __init__(self, home_team, away_team, innings=9):
        self.home_team = home_team
        self.away_team = away_team
        self.innings = innings
        self.current_inning = 1

    def play_inning(self):
        print(f"Inning {self.current_inning} begins.")
        away_runs = self.away_team.play_half_inning()
        home_runs = self.home_team.play_half_inning()
        self.away_team.score += away_runs
        self.home_team.score += home_runs
        print(f"Inning {self.current_inning}: {self.away_team.name} scored {away_runs}, {self.home_team.name} scored {home_runs}.")
        self.current_inning += 1

    def is_game_over(self):
        return self.current_inning > self.innings

    def get_scoreboard(self):
        return f"{self.away_team.name}: {self.away_team.score} | {self.home_team.name}: {self.home_team.score}"

# -------------------------------
# Utility Functions for Pygame
# -------------------------------
def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

def get_rating_color(value):
    """
    Returns a color based on the numeric rating value.
    Ratings:
      20-30: red
      30-50: yellow
      50-60: green
      60-70: light blue
      70-80: dark blue
    """
    try:
        v = float(value)
    except ValueError:
        return BLACK  # default if conversion fails
    if 20 <= v < 30:
        return (255, 0, 0)  # Red
    elif 30 <= v < 50:
        return (255, 255, 0)  # Yellow
    elif 50 <= v < 60:
        return GREEN  # Using your already defined GREEN
    elif 60 <= v < 70:
        return (173, 216, 230)  # Light Blue
    elif 70 <= v <= 80:
        return (0, 0, 139)  # Dark Blue
    else:
        return BLACK


def draw_table(surface, headers, data, start_x, start_y, row_height=30,
               scroll_offset_y=0, scroll_offset_x=0, max_visible_rows=10, max_visible_cols=5,
               name_col_width=200, col_width=125):
    """
    Draws a table with the first column (index 0) fixed.
    If a row in data is a tuple, its second element (a list) is used for drawing.
    max_visible_cols is the total number of visible columns (including the fixed one).
    scroll_offset_x applies only to the scrollable part (columns 1+).
    """
    font = pygame.font.SysFont(None, 24)
    # Number of scrollable columns visible (total minus fixed column)
    scrollable_cols_visible = max_visible_cols - 1
    # Total table width is fixed column + scrollable columns
    table_width = name_col_width + col_width * scrollable_cols_visible
    table_height = row_height * (max_visible_rows + 1)  # header + rows

    # Draw overall table background in white
    pygame.draw.rect(surface, WHITE, (start_x, start_y, table_width, table_height))

    # --- Draw Header Row ---
    # Fixed first header cell
    fixed_rect = pygame.Rect(start_x, start_y, name_col_width, row_height)
    pygame.draw.rect(surface, WHITE, fixed_rect)
    pygame.draw.rect(surface, BLACK, fixed_rect, 1)
    header_text = font.render(headers[0], True, BLACK)
    surface.blit(header_text, header_text.get_rect(center=fixed_rect.center))

    # Scrollable header cells (columns 1+)
    x_pos = start_x + name_col_width
    for i in range(1 + scroll_offset_x, min(len(headers), 1 + scroll_offset_x + scrollable_cols_visible)):
        cell_rect = pygame.Rect(x_pos, start_y, col_width, row_height)
        pygame.draw.rect(surface, WHITE, cell_rect)
        pygame.draw.rect(surface, BLACK, cell_rect, 1)
        header_text = font.render(headers[i], True, BLACK)
        surface.blit(header_text, header_text.get_rect(center=cell_rect.center))
        x_pos += col_width

    # --- Draw Data Rows ---
    for row_idx in range(min(len(data) - scroll_offset_y, max_visible_rows)):
        # If each data row is stored as a tuple (player, values), extract the list of values.
        row_item = data[row_idx + scroll_offset_y]
        row_data = row_item[1] if isinstance(row_item, tuple) else row_item

        # Fixed first cell (Name) always visible
        fixed_rect = pygame.Rect(start_x, start_y + (row_idx + 1) * row_height, name_col_width, row_height)
        pygame.draw.rect(surface, WHITE, fixed_rect)
        pygame.draw.rect(surface, BLACK, fixed_rect, 1)
        cell_text = font.render(str(row_data[0]), True, BLACK)
        surface.blit(cell_text, cell_text.get_rect(center=fixed_rect.center))

        # Scrollable cells for columns 1+
        x_pos = start_x + name_col_width
        for col_idx in range(1 + scroll_offset_x, min(len(row_data), 1 + scroll_offset_x + scrollable_cols_visible)):
            cell_rect = pygame.Rect(x_pos, start_y + (row_idx + 1) * row_height, col_width, row_height)
            pygame.draw.rect(surface, WHITE, cell_rect)
            pygame.draw.rect(surface, BLACK, cell_rect, 1)
            # For column 1 (e.g. Position) use black text; for rating columns, use color.
            if col_idx < 2:
                text_color = BLACK
            else:
                text_color = get_rating_color(row_data[col_idx])
            cell_text = font.render(str(row_data[col_idx]), True, text_color)
            surface.blit(cell_text, cell_text.get_rect(center=cell_rect.center))
            x_pos += col_width


def player_detail_view(player):
    """
    Displays a new screen showing the player's ratings as horizontal bars.
    Each bar is filled proportionally (20 to 80 mapped to 0%–100%) and is colored per the rating.
    """
    detail_running = True
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    font = pygame.font.SysFont(None, 24)
    title_font = pygame.font.SysFont(None, 36)
    # Define the order of attributes to display (keys in player.attributes)
    rating_keys = list(player.attributes.keys())
    bar_width = 300
    bar_height = 20
    start_y = 100  # starting y-coordinate for first bar
    spacing = 10

    while detail_running:
        screen.fill((211, 211, 211))  # white background for clarity
        # Draw the player's name at the top
        title_text = title_font.render(f"{player.name} - Ratings", True, BLACK)
        screen.blit(title_text, (50, 30))

        # Draw each attribute as a bar
        current_y = start_y
        for key in rating_keys:
            rating = player.attributes[key]
            # Draw attribute name and rating value
            attr_text = font.render(f"{key}: {rating}", True, BLACK)
            screen.blit(attr_text, (50, current_y))
            # Bar background (light gray)
            bar_x = 200
            bar_rect = pygame.Rect(bar_x, current_y, bar_width, bar_height)
            pygame.draw.rect(screen, (200, 200, 200), bar_rect)
            # Compute fill percentage (assuming ratings range from 20 to 80)
            fill_pct = (rating - 20) / 60.0
            fill_width = int(bar_width * fill_pct)
            fill_rect = pygame.Rect(bar_x, current_y, fill_width, bar_height)
            bar_color = get_rating_color(rating)
            pygame.draw.rect(screen, bar_color, fill_rect)
            # Draw bar border
            pygame.draw.rect(screen, BLACK, bar_rect, 1)
            current_y += bar_height + spacing

        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                detail_running = False
    # Return to the roster view when finished.

# -------------------------------
# Menus and Game Modes
# -------------------------------
def main_menu():
    start_button = Button(260, 150, 300, 75, "Start a Dynasty", BLACK, GREEN)
    pygame.event.clear()
    pygame.event.pump()
    menu_running = True
    while menu_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Baseball GM Simulator", pygame.font.SysFont(None, 72), BLACK, 150, 50)
        screen.blit(pitcher_image, (150, 140))
        screen.blit(baseball_image, (575, 130))
        screen.blit(baseball_diamond_image, (290, 275))
        start_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if start_button.is_clicked(event):
                return "league_menu"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(FPS)

def national_league_west_menu():
    back_button = Button(30, 525, 200  , 50, "Back", BLACK, GREEN)
    rockies_button = Button(270, 100, 275, 75, "ROCKIES", BLACK, GREEN)
    dodgers_button = Button(270, 200, 275, 75, "DODGERS", BLACK, GREEN)
    diamondbacks_button = Button(270, 300, 275, 75, "DIAMONDBACKS", BLACK, GREEN)
    padres_button = Button(270, 400, 275, 75, "PADRES", BLACK, GREEN)
    giants_button = Button(270, 500, 275, 75, "GIANTS", BLACK, GREEN)
    national_league_west_running = True
    while national_league_west_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Select a Team", pygame.font.SysFont(None, 48), BLACK, 290, 25)
        back_button.draw(screen)
        rockies_button.draw(screen)
        dodgers_button.draw(screen)
        diamondbacks_button.draw(screen)
        padres_button.draw(screen)
        giants_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if rockies_button.is_clicked(event):
                return "rockies_menu"
            if dodgers_button.is_clicked(event):
                return "dodgers_menu"
            if diamondbacks_button.is_clicked(event):
                return "diamondbacks_menu"
            if padres_button.is_clicked(event):
                return "padres_menu"
            if giants_button.is_clicked(event):
                return "giants_menu"
            if back_button.is_clicked(event):
                return "division_menu_national"
        clock.tick(FPS)

def national_league_central_menu():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    national_league_central_running = True
    while national_league_central_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Select a Team", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return "division_menu_national"
        clock.tick(FPS)

def national_league_east_menu():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    national_league_east_running = True
    while national_league_east_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Select a Team", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return "division_menu_national"
        clock.tick(FPS)

def american_league_west_menu():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    american_league_west_running = True
    while american_league_west_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Select a Team", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return "division_menu_american"
        clock.tick(FPS)

def american_league_central_menu():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    american_league_central_running = True
    while american_league_central_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Select a Team", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return "division_menu_american"
        clock.tick(FPS)

def american_league_east_menu():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    american_league_east_running = True
    while american_league_east_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Select a Team", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                return "division_menu_american"
        clock.tick(FPS)

def league_menu():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    national_league_button = Button(75, 200, 300, 75, "National League", BLACK, GREEN)
    american_league_button = Button(425, 200, 300, 75, "American League", BLACK, GREEN)

    league_menu_running = True
    while league_menu_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Pick a League", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        national_league_button.draw(screen)
        american_league_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if national_league_button.is_clicked(event):
                return "division_menu_national"
            if american_league_button.is_clicked(event):
                return "division_menu_american"
            if back_button.is_clicked(event):
                return "main_menu"

def division_menu_national():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    central_division = Button(250, 150, 300, 75, "Central", BLACK, GREEN)
    east_division = Button(250, 250, 300, 75, "East", BLACK, GREEN)
    west_division = Button(250, 350, 300, 75, "West", BLACK, GREEN)
    divison_menu_national_running = True
    while divison_menu_national_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Pick a Division", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        central_division.draw(screen)
        east_division.draw(screen)
        west_division.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if central_division.is_clicked(event):
                return "national_league_central"
            if east_division.is_clicked(event):
                return "national_league_east"
            if west_division.is_clicked(event):
                return "national_league_west"
            if back_button.is_clicked(event):
                return "league_menu"
        clock.tick(FPS)

def division_menu_american():
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    central_division = Button(250, 150, 300, 75, "Central", BLACK, GREEN)
    east_division = Button(250, 250, 300, 75, "East", BLACK, GREEN)
    west_division = Button(250, 350, 300, 75, "West", BLACK, GREEN)
    divison_menu_american_running = True
    while divison_menu_american_running:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Pick a Division", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        central_division.draw(screen)
        east_division.draw(screen)
        west_division.draw(screen)
        back_button.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if central_division.is_clicked(event):
                return "american_league_central"
            if east_division.is_clicked(event):
                return "american_league_east"
            if west_division.is_clicked(event):
                return "american_league_west"
            if back_button.is_clicked(event):
                return "league_menu"
        clock.tick(FPS)

def play_baseball_game(game):
    simulate_inning = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                simulate_inning = True

        screen.fill(GREEN)
        draw_text(screen, "Baseball GM Simulator", pygame.font.SysFont(None, 36), WHITE, 250, 20)
        draw_text(screen, "Press SPACE to simulate the next inning", pygame.font.SysFont(None, 24), WHITE, 220, 60)
        draw_text(screen, f"Inning: {min(game.current_inning, game.innings)} / {game.innings}",
                  pygame.font.SysFont(None, 36), WHITE, 50, 100)
        draw_text(screen, game.get_scoreboard(), pygame.font.SysFont(None, 36), WHITE, 50, 150)

        if simulate_inning and not game.is_game_over():
            game.play_inning()
            simulate_inning = False

        if game.is_game_over():
            winner = game.home_team if game.home_team.score > game.away_team.score else game.away_team
            draw_text(screen, f"Game Over! {winner.name} wins!", pygame.font.SysFont(None, 48), RED, 200, 250)
            pygame.display.flip()
            # Instead of quitting immediately, show the post-game menu
            post_game_menu(game)
            running = False  # Exit the game loop to return to the main menu

        pygame.display.flip()
        clock.tick(FPS)
    # End of game; return to team menu instead of quitting
    return

def post_game_menu(game):
    # Create two buttons: one for the box score and one for returning to the team menu
    box_score_button = Button(250, 300, 300, 75, "View Box Score", BLACK, GREEN)
    return_button = Button(250, 400, 300, 75, "Return to Team Menu", BLACK, GREEN)

    in_post_game_menu = True
    while in_post_game_menu:
        screen.fill(BASEBALL_GREEN)
        draw_text(screen, "Game Over!", pygame.font.SysFont(None, 48), BLACK, 300, 200)
        box_score_button.draw(screen)
        return_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if box_score_button.is_clicked(event):
                box_score_view(game)
            if return_button.is_clicked(event):
                in_post_game_menu = False  # Exit the post-game menu to return to the team menu

def box_score_view(game):
    # This function displays the final box score.
    # You can expand this to include detailed stats for each team or player.
    back_button = Button(30, 525, 200, 50, "Back", GREEN, BLACK)
    in_box_score = True
    while in_box_score:
        screen.fill(BLACK)
        draw_text(screen, "Box Score", pygame.font.SysFont(None, 48), WHITE, 300, 20)
        draw_text(screen, f"{game.away_team.name}: {game.away_team.score}", pygame.font.SysFont(None, 36), WHITE, 50,
                  100)
        draw_text(screen, f"{game.home_team.name}: {game.home_team.score}", pygame.font.SysFont(None, 36), WHITE, 50,
                  150)
        # (Optional) Add additional stats or inning-by-inning data here
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if back_button.is_clicked(event):
                in_box_score = False  # Return to the post-game menu

def rockies_menu():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    view_roster = Button(30, 75, 200, 50, "View Roster", BLACK, GREEN)
    play_game = Button(30, 195, 200, 50, "Play Game!", BLACK, GREEN)
    view_staff = Button(30, 135, 200, 50, "View Staff", BLACK, GREEN)
    rockies_running = True
    while rockies_running:
        screen.fill(ROCKIES_PURPLE)
        draw_text(screen, "Rockies GM", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        screen.blit(rockies_logo, (650, 25))
        back_button.draw(screen)
        view_roster.draw(screen)
        play_game.draw(screen)
        view_staff.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if view_roster.is_clicked(event):
                selected_team = create_rockies_team()
                return "rockies_roster"
            if play_game.is_clicked(event):
                selected_team = create_rockies_team()
                return "play_game"
            if view_staff.is_clicked(event):
                return "rockies_staff"
            if back_button.is_clicked(event):
                return "national_league_west"
        clock.tick(FPS)

def create_rockies_team():
    rockies_batters = [
        Batter("Jacob Stallings", "C", speed = 25, framing = 35, framing_pot = 35, blocking = 70, blocking_pot = 70,
               arm = 40, arm_pot = 40, triple = 25, triple_pot = 25, power = 35, power_pot = 35, contact = 40, contact_pot = 40,
               eye = 45, eye_pot = 45),
        Batter("Hunter Goodman", "C"),
        Batter("Drew Romo", "C"),
        Batter("Michael Toglia", "1B"),
        Batter("Thairo Estrada", "2B"),
        Batter("Kyle Farmer", "2B"),
        Batter("Ryan McMahon", "3B"),
        Batter("Ezequiel Tovar", "SS"),
        Batter("Nolan Jones", "LF"),
        Batter("Brenton Doyle", "CF"),
        Batter("Jordan Beck", "RF"),
        Batter("Sam Hillard", "RF"),
        Batter("Kris Bryant", "DH")
    ]
    rockies_pitchers = [
        Pitcher("Kyle Freeland", "SP"),
        Pitcher("German Marquez", "SP"),
        Pitcher("Austin Gomber", "SP"),
        Pitcher("Ryan Feltner", "SP"),
        Pitcher("Antonio Senzatela", "SP"),
        Pitcher("Bradley Blalock", "SP"),
        Pitcher("Tanner Gordon", "SP"),
        Pitcher("Seth Halvorsen", "RP"),
        Pitcher("Victor Vodnik", "RP"),
        Pitcher("Tyler Kinley", "RP"),
        Pitcher("Luis Peralta", "RP"),
        Pitcher("Scott Alexander", "RP"),
        Pitcher("Angel Chivilli", "RP"),
        Pitcher("Jake Bird", "RP"),
        Pitcher("Jimmy Herget", "RP"),
        Pitcher("Lucase Gilbreath", "RP"),
        Pitcher("Jeff Criswell", "RP"),
        Pitcher("Jaden Hill", "RP")
    ]
    rockies_staff = [
        Coach("Bud Black", "MA"),
        Coach("Todd Helton", "1B"),
        Coach("Alex English", "3B"),
        Coach("Demariyus Thomas", "HC"),
        Coach("Patrick Roy", "PC")
    ]
    return Team("Colorado Rockies", rockies_batters, rockies_pitchers, rockies_staff)
# Need to add more kinds of staff (doctors, scouts, trainers) and add specified player ratings based on performance (20-80 scale)
def rockies_roster():
    global selected_team
    # Sorting state variables – initially no sort column
    sort_col = None
    sort_desc = True  # True means descending order

    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    if selected_team is None or selected_team.name != "Colorado Rockies":
        selected_team = create_rockies_team()
    headers = ["Name", "Position", "Speed", "Power", "Contact", "Eye", "Gap Power", "Triple",
               "Framing", "Blocking", "Catcher Arm", "Range", "Arm Strength", "Power Pot.",
               "Contact Pot.", "Eye Pot.", "Gap Power Pot.", "Triple Pot.",
               "Framing Pot.", "Blocking Pot.", "Catcher Arm Pot.", "Range Pot.",
               "Arm Strength Pot."]
    # Create data as a list of tuples (player, values) so we can retrieve the player object later.
    data = [
        (player, [player.name, player.position, player.attributes["speed"], player.attributes["power"],
                  player.attributes["contact"], player.attributes["eye"], player.attributes["gap_power"],
                  player.attributes["triple"], player.attributes["framing"], player.attributes["blocking"],
                  player.attributes["arm"], player.attributes["range"], player.attributes["arm_strength"],
                  player.attributes["power_pot"], player.attributes["contact_pot"], player.attributes["eye_pot"],
                  player.attributes["gap_power_pot"], player.attributes["triple_pot"], player.attributes["framing_pot"],
                  player.attributes["blocking_pot"], player.attributes["arm_pot"], player.attributes["range_pot"],
                  player.attributes["arm_strength_pot"]])
        for player in selected_team.batters
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 5  # Total visible columns: 1 fixed (Name) + 4 scrollable.
    name_col_width = 200
    col_width = 125
    row_height = 30  # Height of each cell and header row
    table_start_x = 50
    header_y = 100  # y-coordinate where the table starts

    rockies_roster_running = True
    while rockies_roster_running:
        screen.fill(ROCKIES_PURPLE)
        draw_text(screen, "Rockies Roster", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        # Draw table with fixed first column
        draw_table(screen, headers, data, start_x=table_start_x, start_y=header_y,
                   scroll_offset_y=scroll_offset_y, scroll_offset_x=scroll_offset_x,
                   max_visible_rows=max_visible_rows, max_visible_cols=max_visible_cols,
                   name_col_width=name_col_width, col_width=col_width)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "rockies_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset_y -= event.y
                scroll_offset_y = max(0, min(scroll_offset_y, len(data) - max_visible_rows))
                scroll_offset_x -= event.x
                scroll_offset_x = max(0, min(scroll_offset_x, len(headers) - max_visible_cols))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Fallback scrolling with mouse buttons
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.button == 6 and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.button == 7 and scroll_offset_x > 0:
                    scroll_offset_x -= 1
                elif event.button == 1:
                    mouse_x, mouse_y = event.pos
                    # Check if click is in header area (for sorting)
                    if header_y <= mouse_y < header_y + row_height:
                        rel_x = mouse_x - table_start_x
                        # Determine clicked header column
                        if rel_x < name_col_width:
                            clicked_col = 0
                        else:
                            rel_x_scroll = rel_x - name_col_width
                            current_x = 0
                            clicked_col = None
                            for i in range(1 + scroll_offset_x,
                                           min(len(headers), 1 + scroll_offset_x + (max_visible_cols - 1))):
                                if current_x <= rel_x_scroll < current_x + col_width:
                                    clicked_col = i
                                    break
                                current_x += col_width
                        if clicked_col is not None:
                            if sort_col == clicked_col:
                                sort_desc = not sort_desc
                            else:
                                sort_col = clicked_col
                                sort_desc = True
                            # When sorting, work on the tuple's second element.
                            if clicked_col < 2:
                                data.sort(key=lambda item: item[1][clicked_col], reverse=sort_desc)
                            else:
                                data.sort(key=lambda item: float(item[1][clicked_col]), reverse=sort_desc)
                    else:
                        # Click outside header area but within table bounds? Determine if a data row was clicked.
                        if header_y + row_height <= mouse_y < header_y + row_height * (
                                max_visible_rows + 1) and table_start_x <= mouse_x < table_start_x + name_col_width + col_width * (
                                max_visible_cols - 1):
                            # Compute the row index relative to visible rows.
                            clicked_row = (mouse_y - header_y - row_height) // row_height
                            actual_row = clicked_row + scroll_offset_y
                            if actual_row < len(data):
                                # Retrieve the corresponding player object from the tuple.
                                player_obj = data[actual_row][0]
                                # Open the player detail view
                                player_detail_view(player_obj)

def rockies_staff():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    if selected_team is None or selected_team.name != "Colorado Rockies":
        selected_team = create_rockies_team()
    headers = ["Name", "Role", "Experience", "Hitting", "Pitching", "Fielding"]
    data = [
        [staff.name, staff.role, staff.attributes["experience"], staff.attributes["hitting"],
         staff.attributes["pitching"], staff.attributes["fielding"]] for staff in selected_team.staff
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    rockies_staff_running = True
    while rockies_staff_running:
        screen.fill(ROCKIES_PURPLE)
        draw_text(screen, "Rockies Staff", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x = 50, start_y = 100,
                   scroll_offset_y = scroll_offset_y, scroll_offset_x = scroll_offset_x,
                   max_visible_rows = max_visible_rows, name_col_width = name_col_width, col_width = col_width)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "rockies_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def dodgers_menu():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    view_roster = Button(30, 75, 200, 50, "View Roster", BLACK, GREEN)
    play_game = Button(30, 195, 200, 50, "Play Game!", BLACK, GREEN)
    view_staff = Button(30, 135, 200, 50, "View Staff", BLACK, GREEN)
    dodgers_running = True
    while dodgers_running:
        screen.fill(DODGER_BLUE)
        draw_text(screen, "Dodgers GM", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        view_roster.draw(screen)
        play_game.draw(screen)
        view_staff.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if view_roster.is_clicked(event):
                selected_team = create_dodgers_team()
                return "dodgers_roster"
            if play_game.is_clicked(event):
                selected_team = create_dodgers_team()
                return "play_game"
            if view_staff.is_clicked(event):
                return "dodgers_staff"
            if back_button.is_clicked(event):
                return "national_league_west"
        clock.tick(FPS)

def create_dodgers_team():
    dodgers_batters = [
        Batter("Will Smith", "C"),
        Batter("Austin Barnes", "C"),
        Batter("Freddie Freeman", "1B"),
        Batter("Hye-Song Kim", "2B"),
        Batter("Enrique Hernandez", "2B"),
        Batter("Max Muncy", "3B"),
        Batter("Mookie Betts", "SS"),
        Batter("Miguel Rojas", "SS"),
        Batter("Michael Conforto", "LF"),
        Batter("Tommy Edman", "CF"),
        Batter("Chris Taylor", "CF"),
        Batter("Andy Pages", "CF"),
        Batter("Teoscar Hernandez", "RF"),
        Batter("Shohei Ohtani", "DH")
    ]
    dodgers_pitchers = [
        Pitcher("Blake Snell", "SP"),
        Pitcher("Yoshinobu Yamamoto", "SP"),
        Pitcher("Tyler Glasnow", "SP"),
        Pitcher("Shohei Ohtani", "SP"),
        Pitcher("Roki Sasaki", "SP"),
        Pitcher("Tony Gonsolin", "SP"),
        Pitcher("Clayton Kershaw", "SP"),
        Pitcher("Dustin May", "SP"),
        Pitcher("Landon Knack", "SP"),
        Pitcher("Emmet Sheehan", "SP"),
        Pitcher("Gavin Stone", "SP"),
        Pitcher("River Ryan", "SP"),
        Pitcher("Michael Kopech", "RP"),
        Pitcher("Blake Treinen", "RP"),
        Pitcher("Tanner Scott", "RP"),
        Pitcher("Alex Vesia", "RP"),
        Pitcher("Brusdar Graterol", "RP"),
        Pitcher("Kirby Yates", "RP"),
        Pitcher("Anthony Banda", "RP"),
        Pitcher("Ben Casparius", "RP")
    ]
    dodgers_staff = [
        Coach("Dave Roberts", "MA"),
        Coach("Kobe Bryant", "1B"),
        Coach("Jerry West", "3B"),
        Coach("Wayne Gretzky", "HC"),
        Coach("Sandy Koufax", "PC")
    ]
    return Team("Los Angeles Dodgers", dodgers_batters, dodgers_pitchers, dodgers_staff)
# Need to add more kinds of staff (doctors, scouts, trainers) and add specified player ratings based on performance (20-80 scale)
def dodgers_roster():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", GREEN, BLACK)
    if selected_team is None or selected_team.name != "Los Angeles Dodgers":
        selected_team = create_dodgers_team()
    headers = ["Name", "Position", "Speed", "Power", "Contact", "Fielding", "Eye"]
    data = [
        [player.name, player.position, player.attributes["speed"], player.attributes["power"],
         player.attributes["contact"], player.attributes["fielding"], player.attributes["eye"]]
        for player in selected_team.batters
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    dodgers_roster_running = True
    while dodgers_roster_running:
        screen.fill(DODGER_BLUE)
        draw_text(screen, "Dodgers Roster", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x=50, start_y=100,
                   scroll_offset_y=scroll_offset_y, scroll_offset_x=scroll_offset_x,
                   max_visible_rows=max_visible_rows, name_col_width=name_col_width, col_width=col_width)
        back_button.draw(screen)
        pygame.display.flip()
        # FIX: Throttle the loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "dodgers_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def dodgers_staff():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    if selected_team is None or selected_team.name != "Los Angeles Dodgers":
        selected_team = create_dodgers_team()
    headers = ["Name", "Role", "Experience", "Hitting", "Pitching", "Fielding"]
    data = [
        [staff.name, staff.role, staff.attributes["experience"], staff.attributes["hitting"],
         staff.attributes["pitching"], staff.attributes["fielding"]] for staff in selected_team.staff
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    dodgers_staff_running = True
    while dodgers_staff_running:
        screen.fill(DODGER_BLUE)
        draw_text(screen, "Dodgers Staff", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x = 50, start_y = 100,
                   scroll_offset_y = scroll_offset_y, scroll_offset_x = scroll_offset_x,
                   max_visible_rows = max_visible_rows, name_col_width = name_col_width, col_width = col_width)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "dodgers_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def diamondbacks_menu():
    """
    Display the diamondback team menu with options to play a game or view the roster
    """

    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    view_roster = Button(30, 75, 200, 50, "View Roster", BLACK, GREEN)
    play_game = Button(30, 195, 200, 50, "Play Game!", BLACK, GREEN)
    view_staff = Button(30, 135, 200, 50, "View Staff", BLACK, GREEN)

    diamondbacks_menu_running = True
    while diamondbacks_menu_running:
        screen.fill(DIAMONDBACK_RED)
        draw_text(screen, "Diamondbacks GM", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        view_roster.draw(screen)
        play_game.draw(screen)
        view_staff.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if view_roster.is_clicked(event):
                selected_team = create_diamondbacks_team()
                return "diamondbacks_roster"
            if play_game.is_clicked(event):
                selected_team = create_diamondbacks_team()
                return "play_game"
            if view_staff.is_clicked(event):
                return "diamondbacks_staff"
            if back_button.is_clicked(event):
                return "national_league_west"
        clock.tick(FPS)

def create_diamondbacks_team():
    diamondbacks_batters = [
        Batter("Gabriel Moreno", "C"),
        Batter("Jose Herrera", "C"),
        Batter("Adrian Del Castillo", "C"),
        Batter("Rene Pinto", "C"),
        Batter("Josh Naylor", "1B"),
        Batter("Trey Mancini", "1B"),
        Batter("Ketel Marte", "2B"),
        Batter("Garrett Hampson", "2B"),
        Batter("Eugenio Suarez", "3B"),
        Batter("Grae Kessinger", "3B"),
        Batter("Geraldo Perdomo", "SS"),
        Batter("Jordan Lawalr", "SS"),
        Batter("Lourdes Gurriel Jr.", "LF"),
        Batter("Randal Grichuk", "LF"),
        Batter("Jake McCarthy", "CF"),
        Batter("Alek Thomas", "CF"),
        Batter("Corbin Carroll", "RF"),
        Batter("Pavin Smith", "DH")
    ]
    diamondbacks_pitchers = [
        Pitcher("Corbin Burnes", "SP"),
        Pitcher("Zac Gallen", "SP"),
        Pitcher("Merrill Kelly", "SP"),
        Pitcher("Eduardo Rodriguez", "SP"),
        Pitcher("Brandon Pfaadt", "SP"),
        Pitcher("Jordan Montgomery", "SP"),
        Pitcher("Ryne Nelson", "SP"),
        Pitcher("Kevin Ginkel", "RP"),
        Pitcher("Joe Mantiply,", "RP"),
        Pitcher("A.J. Puk", "RP"),
        Pitcher("Ryan Thomspon", "RP"),
        Pitcher("Justin Martinez", "RP"),
        Pitcher("Kendall Graveman", "RP"),
        Pitcher("Kyle Nelson", "RP"),
        Pitcher("Scott McGough", "RP")
    ]
    diamondbacks_staff = [
        Coach("Salvatore Lovullo", "MA"),
        Coach("Steve Nash", "1B"),
        Coach("Luis Gonzalez", "3B"),
        Coach("Charles Barkley", "HC"),
        Coach("Sean Elliot", "PC")
    ]
    return Team("Arizona Diamondbacks", diamondbacks_batters, diamondbacks_pitchers, diamondbacks_staff)
# Need to add more kinds of staff (doctors, scouts, trainers) and add specified player ratings based on performance (20-80 scale)
def diamondbacks_roster():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", GREEN, BLACK)
    if selected_team is None or selected_team.name != "Arizona Diamondbacks":
        selected_team = create_diamondbacks_team()
    headers = ["Name", "Position", "Speed", "Power", "Contact", "Fielding", "Eye"]
    data = [
        [player.name, player.position, player.attributes["speed"], player.attributes["power"],
         player.attributes["contact"], player.attributes["fielding"], player.attributes["eye"]]
        for player in selected_team.batters
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    diamondbacks_roster_running = True
    while diamondbacks_roster_running:
        screen.fill(DIAMONDBACK_RED)
        draw_text(screen, "Diamondbacks Roster", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x=50, start_y=100,
                   scroll_offset_y=scroll_offset_y, scroll_offset_x=scroll_offset_x,
                   max_visible_rows=max_visible_rows, name_col_width=name_col_width, col_width=col_width)
        back_button.draw(screen)
        pygame.display.flip()
        # FIX: Throttle the loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "diamondbacks_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def diamondbacks_staff():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    if selected_team is None or selected_team.name != "Arizona Diamondbacks":
        selected_team = create_diamondbacks_team()
    headers = ["Name", "Role", "Experience", "Hitting", "Pitching", "Fielding"]
    data = [
        [staff.name, staff.role, staff.attributes["experience"], staff.attributes["hitting"],
         staff.attributes["pitching"], staff.attributes["fielding"]] for staff in selected_team.staff
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    diamondbacks_staff_running = True
    while diamondbacks_staff_running:
        screen.fill(DIAMONDBACK_RED)
        draw_text(screen, "Diamondbacks Staff", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x = 50, start_y = 100,
                   scroll_offset_y = scroll_offset_y, scroll_offset_x = scroll_offset_x,
                   max_visible_rows = max_visible_rows, name_col_width = name_col_width, col_width = col_width)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "diamondbacks_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def padres_menu():

    global selected_team

    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    view_roster = Button(30, 75, 200, 50, "View Roster", BLACK, GREEN)
    play_game = Button(30, 195, 200, 50, "Play Game!", BLACK, GREEN)
    view_staff = Button(30, 135, 200, 50, "View Staff", BLACK, GREEN)

    padres_menu_running = True
    while padres_menu_running:
        screen.fill(PADRE_BROWN)
        draw_text(screen, "Padres GM", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        back_button.draw(screen)
        view_roster.draw(screen)
        play_game.draw(screen)
        view_staff.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if view_roster.is_clicked(event):
                selected_team = create_padres_team()
                return "padres_roster"
            if play_game.is_clicked(event):
                selected_team = create_padres_team()
                return "play_game"
            if view_staff.is_clicked(event):
                return "padres_staff"
            if back_button.is_clicked(event):
                return "national_league_west"
        clock.tick(FPS)

def create_padres_team():
    padres_batters = [
        Batter("Elias Diaz", "C"),
        Batter("Luis Campusano", "C"),
        Batter("Brett Sullivan", "C"),
        Batter("Luis Arraez", "1B"),
        Batter("Jake Cronenworth", "2B"),
        Batter("Eguy Rosario", "2B"),
        Batter("Manny Machado", "3B"),
        Batter("Tyler Wade", "3B"),
        Batter("Xander Bogarts", "SS"),
        Batter("Mason McCoy", "SS"),
        Batter("Jason Heyward", "LF"),
        Batter("Tirso Ornelas", "LF"),
        Batter("Jackson Merrill", "CF"),
        Batter("Brandon Lockridge", "CF"),
        Batter("Fernando Tatis Jr.", "RF"),
        Batter("Connor Joe", "DH")
    ]
    padres_pitchers = [
        Pitcher("Dylan Cease", "SP"),
        Pitcher("Michael King", "SP"),
        Pitcher("Yu Darvish", "SP"),
        Pitcher("Nick Pivetta", "SP"),
        Pitcher("Matt Waldron", "SP"),
        Pitcher("Randy Vasquez", "SP"),
        Pitcher("Kyle Hart", "SP"),
        Pitcher("Jhony Brito", "SP"),
        Pitcher("Stephen Kolek", "SP"),
        Pitcher("Joe Musgrove", "SP"),
        Pitcher("Robert Suarez", "RP"),
        Pitcher("Jason Adam", "RP"),
        Pitcher("Jeremiah Estrada", "RP"),
        Pitcher("Adrian Morejon", "RP"),
        Pitcher("Bryan Hoeing", "RP"),
        Pitcher("Yuki Matsui", "RP"),
        Pitcher("Sean Reynolds", "RP"),
        Pitcher("Wandy Peralta", "RP"),
        Pitcher("Alek Jacob", "RP"),
        Pitcher("Jose Espada", "RP"),
        Pitcher("Tom Cosgrove", "RP"),
        Pitcher("Juan Nunez", "RP"),
        Pitcher("Ron Marinaccio", "RP"),
        Pitcher("Logan Gillaspie", "RP"),
        Pitcher("Luis Patino", "RP")
    ]
    padres_staff = [
        Coach("Mike Shildt", "MA"),
        Coach("LaDainian Tomlinson", "1B"),
        Coach("Marcus Allen", "3B"),
        Coach("Tony Gwynn", "HC"),
        Coach("Shaun White", "PC")
    ]
    return Team("San Diego Padres", padres_batters, padres_pitchers, padres_staff)
# Need to add more kinds of staff (doctors, scouts, trainers) and add specified player ratings based on performance (20-80 scale)
def padres_roster():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", GREEN, BLACK)
    if selected_team is None or selected_team.name != "San Diego Padres":
        selected_team = create_padres_team()
    headers = ["Name", "Position", "Speed", "Power", "Contact", "Fielding", "Eye"]
    data = [
        [player.name, player.position, player.attributes["speed"], player.attributes["power"],
         player.attributes["contact"], player.attributes["fielding"], player.attributes["eye"]]
        for player in selected_team.batters
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    padres_roster_running = True
    while padres_roster_running:
        screen.fill(PADRE_BROWN)
        draw_text(screen, "Padres Roster", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x=50, start_y=100,
                   scroll_offset_y=scroll_offset_y, scroll_offset_x=scroll_offset_x,
                   max_visible_rows=max_visible_rows, name_col_width=name_col_width, col_width=col_width)
        back_button.draw(screen)
        pygame.display.flip()
        # FIX: Throttle the loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "padres_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def padres_staff():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    if selected_team is None or selected_team.name != "San Diego Padres":
        selected_team = create_padres_team()
    headers = ["Name", "Role", "Experience", "Hitting", "Pitching", "Fielding"]
    data = [
        [staff.name, staff.role, staff.attributes["experience"], staff.attributes["hitting"],
         staff.attributes["pitching"], staff.attributes["fielding"]] for staff in selected_team.staff
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    padres_staff_running = True
    while padres_staff_running:
        screen.fill(PADRE_BROWN)
        draw_text(screen, "Padres Staff", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x = 50, start_y = 100,
                   scroll_offset_y = scroll_offset_y, scroll_offset_x = scroll_offset_x,
                   max_visible_rows = max_visible_rows, name_col_width = name_col_width, col_width = col_width)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "padres_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def giants_menu():

    global selected_team

    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    view_roster = Button(30, 75, 200, 50, "View Roster", BLACK, GREEN)
    play_game = Button(30, 195, 200, 50, "Play Game!", BLACK, GREEN)
    view_staff = Button(30, 135, 200, 50, "View Staff", BLACK, GREEN)
    giants_menu_running = True
    while giants_menu_running:
        screen.fill(GIANT_ORANGE)
        draw_text(screen, "Giants GM", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        view_roster.draw(screen)
        play_game.draw(screen)
        back_button.draw(screen)
        view_staff.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if view_roster.is_clicked(event):
                selected_team = create_giants_team()
                return "giants_roster"
            if play_game.is_clicked(event):
                selected_team = create_giants_team()
                return "play_game"
            if view_staff.is_clicked(event):
                return "giants_staff"
            if back_button.is_clicked(event):
                return "national_league_west"

def create_giants_team():
    giants_batters = [
        Batter("Patrick Bailey", "C"),
        Batter("Tom Murphy", "C"),
        Batter("Sam Huff", "C"),
        Batter("LaMonte Wade Jr.", "1B"),
        Batter("Wilmer Flores", "1B"),
        Batter("Tyler Fitzgerald", "2B"),
        Batter("Brett Wisely", "2B"),
        Batter("Matt Chapman", "3B"),
        Batter("Casey Schmitt", "3B"),
        Batter("Willy Adames", "SS"),
        Batter("Osleivis Basabe", "SS"),
        Batter("Heliot Ramos", "LF"),
        Batter("Jung Hoo Lee", "CF"),
        Batter("Grant McCray", "CF"),
        Batter("Mike Yastremski", "RF"),
        Batter("Jerar Encarnacion", "DH")
    ]
    giants_pitchers = [
        Pitcher("Logan Webb", "SP"),
        Pitcher("Robbie Ray", "SP"),
        Pitcher("Justin Verlander", "SP"),
        Pitcher("Jordan Hicks", "SP"),
        Pitcher("Kyle Harrison", "SP"),
        Pitcher("Hayden Birdsong", "SP"),
        Pitcher("Landen Roupp", "SP"),
        Pitcher("Keaton Winn", "SP"),
        Pitcher("Ryan Walker", "RP"),
        Pitcher("Tyler Rogers", "RP"),
        Pitcher("Sean Hjelle", "RP"),
        Pitcher("Erik Miller", "RP"),
        Pitcher("Camilo Doval", "RP"),
        Pitcher("Tristan Beck", "RP"),
        Pitcher("Spencer Bivens", "RP"),
        Pitcher("Randy Rodriguez", "RP")
    ]
    giants_staff= [
        Coach("Bob Melvin", "MA"),
        Coach("Jerry Rice", "1B"),
        Coach("Stephen Curry", "3B"),
        Coach("Barry Bonds", "HC"),
        Coach("Joe Montana", "PC")
    ]
    return Team("San Francisco Giants", giants_batters, giants_pitchers, giants_staff)
# Need to add more kinds of staff (doctors, scouts, trainers) and add specified player ratings based on performance (20-80 scale)
def giants_roster():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", GREEN, BLACK)
    if selected_team is None or selected_team.name != "San Francisco Giants":
        selected_team = create_giants_team()
    headers = ["Name", "Position", "Speed", "Power", "Contact", "Fielding", "Eye"]
    data = [
        [player.name, player.position, player.attributes["speed"], player.attributes["power"],
         player.attributes["contact"], player.attributes["fielding"], player.attributes["eye"]]
        for player in selected_team.batters
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    giants_roster_running = True
    while giants_roster_running:
        screen.fill(GIANT_ORANGE)
        draw_text(screen, "Giants Roster", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x=50, start_y=100,
                   scroll_offset_y=scroll_offset_y, scroll_offset_x=scroll_offset_x,
                   max_visible_rows=max_visible_rows, name_col_width=name_col_width, col_width=col_width)
        back_button.draw(screen)
        pygame.display.flip()
        # FIX: Throttle the loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "giants_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def giants_staff():
    global selected_team
    back_button = Button(30, 525, 200, 50, "Back", BLACK, GREEN)
    if selected_team is None or selected_team.name != "San Francisco Giants":
        selected_team = create_giants_team()
    headers = ["Name", "Role", "Experience", "Hitting", "Pitching", "Fielding"]
    data = [
        [staff.name, staff.role, staff.attributes["experience"], staff.attributes["hitting"],
         staff.attributes["pitching"], staff.attributes["fielding"]] for staff in selected_team.staff
    ]
    scroll_offset_y = 0
    scroll_offset_x = 0
    max_visible_rows = 10
    max_visible_cols = 4
    name_col_width = 200
    col_width = 100
    giants_staff_running = True
    while giants_staff_running:
        screen.fill(GIANT_ORANGE)
        draw_text(screen, "Giants Staff", pygame.font.SysFont(None, 48), BLACK, 10, 10)
        draw_table(screen, headers, data, start_x = 50, start_y = 100,
                   scroll_offset_y = scroll_offset_y, scroll_offset_x = scroll_offset_x,
                   max_visible_rows = max_visible_rows, name_col_width = name_col_width, col_width = col_width)
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif back_button.is_clicked(event):
                return "giants_menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1
                elif event.key == pygame.K_UP and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.key == pygame.K_RIGHT and scroll_offset_x < len(headers) - max_visible_cols:
                    scroll_offset_x += 1
                elif event.key == pygame.K_LEFT and scroll_offset_x > 0:
                    scroll_offset_x -= 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll_offset_y > 0:
                    scroll_offset_y -= 1
                elif event.button == 5 and scroll_offset_y < len(data) - max_visible_rows:
                    scroll_offset_y += 1

def main():
    global selected_team
    available_teams = [create_rockies_team, create_dodgers_team, create_diamondbacks_team, create_padres_team, create_giants_team]
    current_menu = "main_menu"
    while True:
        if current_menu == "main_menu":
            current_menu = main_menu()
        elif current_menu == "league_menu":
            current_menu = league_menu()
        elif current_menu == "division_menu_national":
            current_menu = division_menu_national()
        elif current_menu == "division_menu_american":
            current_menu = division_menu_american()
        elif current_menu == "national_league_west":
            current_menu = national_league_west_menu()
        elif current_menu == "national_league_central":
            current_menu = national_league_central_menu()
        elif current_menu == "national_league_east":
            current_menu = national_league_east_menu()
        elif current_menu == "american_league_west":
            current_menu = american_league_west_menu()
        elif current_menu == "american_league_central":
            current_menu = american_league_central_menu()
        elif current_menu == "american_league_east":
            current_menu = american_league_east_menu()
        elif current_menu == "rockies_menu":
            current_menu = rockies_menu()
        elif current_menu == "dodgers_menu":
            current_menu = dodgers_menu()
        elif current_menu == "diamondbacks_menu":
            current_menu = diamondbacks_menu()
        elif current_menu == "padres_menu":
            current_menu = padres_menu()
        elif current_menu == "giants_menu":
            current_menu = giants_menu()
        elif current_menu == "rockies_roster":
            current_menu = rockies_roster()
        elif current_menu == "dodgers_roster":
            current_menu = dodgers_roster()
        elif current_menu == "diamondbacks_roster":
            current_menu = diamondbacks_roster()
        elif current_menu == "padres_roster":
            current_menu = padres_roster()
        elif current_menu == "giants_roster":
            current_menu = giants_roster()
        elif current_menu == "rockies_staff":
            current_menu = rockies_staff()
        elif current_menu == "dodgers_staff":
            current_menu = dodgers_staff()
        elif current_menu == "diamondbacks_staff":
            current_menu = diamondbacks_staff()
        elif current_menu == "padres_staff":
            current_menu = padres_staff()
        elif current_menu == "giants_staff":
            current_menu = giants_staff()
        elif current_menu == "play_game":
            if selected_team is None:
                print("Error: No team selected! Returning to menu.")
                current_menu = "dynasty_menu"
            else:
                # Instantiate all teams and filter out the selected one
                all_teams = [team_func() for team_func in available_teams]
                possible_opponents = [team for team in all_teams if team.name != selected_team]

                if not possible_opponents:
                    print("No valid opponent found!")
                    current_menu = "dynasty_menu"
                    continue

                opponent_team = random.choice(possible_opponents)

                # Randomly determine home and away teams
                if random.choice([True, False]):
                    home_team = selected_team
                    away_team = opponent_team
                else:
                    home_team = opponent_team
                    away_team = selected_team

                game = Game(home_team, away_team)
                play_baseball_game(game)

            # After the game, return to the same team menu
            if selected_team.name == "Colorado Rockies":
                current_menu = "rockies_menu"
            elif selected_team.name == "Los Angeles Dodgers":
                current_menu = "dodgers_menu"
            else:
                current_menu = "dynasty_menu"  # Fallback if more teams are added

if __name__ == "__main__":
    # Start directly with main() as it calls main_menu internally.
    main()