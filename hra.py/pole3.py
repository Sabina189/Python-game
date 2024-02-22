import pygame
import random

pygame.mixer.init()
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 750

black = (0, 0, 0)
pink = (150, 50, 100)
light_pink = (255, 192, 203)
white = (255, 255, 255)

maze = [
    "##############################",
    "##############################",
    "#.............##.............#",
    "#.####.######.##.######.####.#",
    "#.####.######.##.######.####.#",
    "#.####.######.##.######.####.#",
    "#............................#",
    "#.####.###.########.###.####.#",
    "#.####.###.########.###.####.#",
    "#......###...####...###......#",
    "#.####.#####.####.#####.####.#",
    "#.####.#####.####.#####.####.#",
    "#.####.###..........###.####.#",
    "#.####.###.###..###.###.####.#",
    "#.####.###.#......#.###.####.#",
    "...........#......#...........",
    "######.###.#......#.###.######",
    "######.###.########.###.######",
    "######.###..........###.######",
    "######.###.########.###.######",
    "######.###.########.###.######",
    "#.............##.............#",
    "#.####.######.##.######.####.#",
    "#.####.######.##.######.####.#",
    "#...##..................##...#",
    "###.##.##.##########.##.##.###",
    "###.##.##.##########.##.##.###",
    "#......##.....##.....##......#",
    "#.###########.##.###########.#",
    "#.###########.##.###########.#",
    "#.###########.##.###########.#",
    "#............................#",
    "##############################",
    "##############################",
    ]

cell_size = min(SCREEN_WIDTH // len(maze[0]), SCREEN_HEIGHT // len(maze))

class Granulky:
    """Třída pro granulky, které kočička ve hře sbírá. Bere se to jako score."""
    
    def __init__(self, x, y, size):
        """Vytvoří granulku na určené pozici, určené barvě a určené velikosti."""
        center_x = x * cell_size + cell_size // 2
        center_y = y * cell_size + cell_size // 2
        self.rect = pygame.Rect(center_x - size // 2, center_y - size // 2, size, size)
        self.color = white
        self.size = size

    def draw(self, screen):
        """Vykreslí granulky na obrazovku."""
        pygame.draw.circle(screen, self.color, self.rect.center, self.size // 2)

special_granulky = [(1, 7), (1, 28), (28, 7 ), (28, 28)]
special_granulky_size = cell_size // 1-6
normal_granulky_size = cell_size //  3

granulky_list = [Granulky(x, y, special_granulky_size if (x, y) in special_granulky else normal_granulky_size) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == '.']

class Kocicka:
    """třída pro charaktery ve hře - kočičky."""
    def __init__(self, x, y, image):
        """Vytvoří kočičku na určené pozici a s určeným obrázkem."""
        self.rect = pygame.Rect((x * cell_size) + 1, (y * cell_size) + 1, cell_size + 1, cell_size + 1)
        self.direction = (0, 0)
        self.image = image

    def move(self):
        """Charakter se pohybuje v určeném směru a aktualizuje svoji pozici. Pokud se charakter nachází na okrají herního pole,
        tak se teleportuje na opačný kraj pole."""
        
        new_rect = self.rect.move(self.direction[0] * cell_size, self.direction[1] * cell_size)
        if self.is_valid_move(new_rect):
            self.rect = new_rect
        else:
            x, y = self.rect.x // cell_size, self.rect.y // cell_size
            if x == 0 and self.direction[0] < 0 or y == 0 and self.direction[1] < 0:
                self.rect.x = (len(maze[0]) - 1) * cell_size
            elif x == len(maze[0]) - 1 and self.direction[0] > 0 or y == len(maze) - 1 and self.direction[1] > 0:
                self.rect.x = 0
    

    def is_valid_move(self, new_rect):
        """Ověřuje, jestli je pohyb na novou pozici možný. Kontroluje, jestli na nové pozici není překážka (stěna bludiště)"""
        x, y = new_rect.x // cell_size, new_rect.y // cell_size
        if 0 <= x < len(maze[0]) and 0 <= y < len(maze):
            return maze[y][x] == '.'
        return False

    def draw(self, screen):
        """Vykreslí kočičku na obrazovku."""
        screen.blit(self.image, self.rect)

    def collision_granulky(self, granulky_list, score):
        """Kontroluje, jestli došlo ke kolizi kočičky a granulky. Pokud ano, tak se granulka odstraní z herního pole a kočičce se přičte bod/body."""
        for granulky in granulky_list:
            if self.rect.colliderect(granulky.rect):
                if granulky.size == special_granulky_size:
                    score.add_points(5)
                else:
                    score.add_points(1)
                granulky_list.remove(granulky)
    
    def check_collision_with_ghosts(self, duchy):
        """Kontroluje, jestli došlo ke kolizi kočičky s duchem. Pokud ano, tak se hra ukončí."""
        for duch in duchy:
            if self.rect.colliderect(duch.rect):
                return True

class Duch:
    """Třída pro charaktery ve hře - duchy."""
    def __init__(self, x, y, image):
        """Vytvoří ducha na určené pozici a s určeným obrázkem. Pohyb duchů je náhodný."""
        self.rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        self.image = image
        self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
      
        self.speed_multiplier = 1

    def move(self):
        """Duch se pohybuje nějakým směrem - až narazí na stěnu, tak si určí nový směr pohybu"""
        new_x = self.rect.x + self.direction[0] * cell_size * self.speed_multiplier
        new_y = self.rect.y + self.direction[1] * cell_size * self.speed_multiplier

        if 0 <= new_x // cell_size < len(maze[0]) and 0 <= new_y // cell_size < len(maze) and maze[new_y // cell_size][new_x // cell_size] == '.':
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            self.direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])

    def draw(self, screen):
        """Vykreslí ducha na obrazovku."""
        screen.blit(self.image, self.rect)

class Button(pygame.sprite.Sprite):
    """Třída pro tlačítka"""

    def __init__(self, text, font, primary_color, border_color, position):
        """Vytvoří tlačítko s určeným textem, fontem, barvou a pozicí."""
        super().__init__()
        self.primary_text = font.render(text, True, primary_color)
        self.border_text = font.render(text, True, border_color)
        self.rect = self.primary_text.get_rect(center=position)

    def set_rect(self):
        """Nastaví pozici tlačítka."""
        self.render_text = self.font.render(self.text, True, self.color)
        

    def draw(self, screen):
        """Vykreslí tlačítko na obrazovku."""
        screen.blit(self.border_text, self.rect.move(-2, -2))
        screen.blit(self.border_text, self.rect.move(2, -2))
        screen.blit(self.border_text, self.rect.move(-2, 2))
        screen.blit(self.border_text, self.rect.move(2, 2))
        screen.blit(self.primary_text, self.rect)
    def is_clicked(self, x, y):
        """Ověřuje, jestli došlo ke kliknutí na tlačítko."""
        return self.rect.collidepoint(x, y)
    
class Score:
    """Třída pro skóre ve hře."""
    def __init__(self):
        """Nastaví score na 0."""
        self.value = 0

    def add_points(self, points):
        """Přičte kočičce body."""
        self.value += points

    def draw(self, screen, font, color, position):
        """Vykreslí skóre na obrazovku."""
        score_text = font.render(f'Score: {self.value}', True, color)
        screen.blit(score_text, position)

    
def draw_maze(screen, granulky_list):
    """Vykreslí bludiště a granulky na obrazovku."""
    for granulky in granulky_list:
        pygame.draw.circle(screen, granulky.color, granulky.rect.center, cell_size // 6)

def draw_walls(screen, maze):
    """Vykreslí stěny bludiště na obrazovku."""
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '#':
                pygame.draw.rect(screen, pink, (x * cell_size, y * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, light_pink, (x * cell_size + cell_size // 6, y * cell_size + cell_size // 6, cell_size * 2 // 3, cell_size * 2 // 3), 1)