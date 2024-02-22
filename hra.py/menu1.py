import pygame
import pole3
import main

pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_image = pygame.image.load("hra.py/obrazky/plochamenu.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
kocicka1_image = pygame.image.load("hra.py/obrazky/kocicka1.png")
kocicka1_image = pygame.transform.scale(kocicka1_image, (160, 160))
kocicka2_image = pygame.image.load("hra.py/obrazky/kocicka2.png")
kocicka2_image = pygame.transform.scale(kocicka2_image, (160, 160))
kocicka3_image = pygame.image.load("hra.py/obrazky/kocicka3.png")
kocicka3_image = pygame.transform.scale(kocicka3_image, (160, 160))
kocicka1_mnau = pygame.mixer.Sound("hra.py/zvuky/kocicka1_mnau.mp3")
kocicka2_mnau = pygame.mixer.Sound("hra.py/zvuky/kocicka2_mnau.mp3")
kocicka3_mnau = pygame.mixer.Sound("hra.py/zvuky/kocicka3_mnau.mp3")
kliknuti = pygame.mixer.Sound("hra.py/zvuky/click_button.mp3")
hra_pisnicka = pygame.mixer.music.load("hra.py/zvuky/hra_pisnicka.mp3")

pink = (150, 50, 100)
black = (0, 0, 0)
title_font = pygame.font.Font(None, 150)
podnadpis_font = pygame.font.Font(None, 70)  
back_font = pygame.font.Font(None, 50)

class Button(pygame.sprite.Sprite):
    """Třída pro tlačítka."""

    def __init__(self, text, font, primary_color, border_color, position):
        """Vytvoří tlačítko s určenou pozicí, fontem, barvou a pozicí."""
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

def check_button_click(button, position):
    """Kontroluje, jestli bylo kliknuto na tlačítko."""
    return button.rect.collidepoint(position)

title_sprite = Button("MAIN MENU", title_font, pink, black, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
play_sprite = Button("Play", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
options_sprite = Button("Options", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
quit_sprite = Button("Quit", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
choose_char_sprite = Button("Choose your character:", podnadpis_font, pink, black, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200))  
easy_sprite = Button("Easy", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
medium_sprite = Button("Medium", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
hard_sprite = Button("Hard", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
back_sprite = Button("Back", back_font, black, pink, (SCREEN_WIDTH - 100, 30))  

show_difficulty_options = False
show_back_button = False
show_options = True  
show_kocicky = False
selected_kocicka = None
play_enabled = True
selected_kocicka = None

kocicka1_rect = pygame.Rect(SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 150, 160, 160)
kocicka2_rect = pygame.Rect(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 150, 160, 160)
kocicka3_rect = pygame.Rect(SCREEN_WIDTH // 2 + 130, SCREEN_HEIGHT // 2 - 150, 160, 160)

def show_menu():
    """Zobrazí menu."""
    global show_difficulty_options, show_back_button, show_options, show_kocicky, selected_kocicka, play_enabled, running
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if show_options and check_button_click(play_sprite, (x, y)):
                    show_difficulty_options = True
                    show_options = False
                    show_back_button = True
                    kliknuti.play()
                elif show_options and check_button_click(options_sprite, (x, y)):
                    show_options = False
                    show_back_button = True
                    show_kocicky = True
                    play_enabled = False
                    kliknuti.play()
                elif show_options and check_button_click(quit_sprite, (x, y)):
                    running = False
                    kliknuti.play()
                elif show_back_button and check_button_click(back_sprite, (x, y)):
                    show_difficulty_options = False
                    show_back_button = False
                    show_options = True
                    show_kocicky = False
                    play_enabled = True
                    kliknuti.play()

                elif show_difficulty_options and check_button_click(easy_sprite, (x, y)) and selected_kocicka:
                    main.start_game("Easy", selected_kocicka) 
                    running = False
                elif show_difficulty_options and check_button_click(medium_sprite, (x, y)) and selected_kocicka:
                    main.start_game("Medium", selected_kocicka)  
                    running = False
                elif show_difficulty_options and check_button_click(hard_sprite, (x, y)) and selected_kocicka:
                    main.start_game("Hard", selected_kocicka)
                    running = False


                elif show_kocicky:
                    if kocicka1_rect.collidepoint(x, y):
                        selected_kocicka = "kocicka1"
                        kocicka1_mnau.play()
                    elif kocicka2_rect.collidepoint(x, y):
                        selected_kocicka = "kocicka2"
                        kocicka2_mnau.play()
                    elif kocicka3_rect.collidepoint(x, y):
                        selected_kocicka = "kocicka3"
                        kocicka3_mnau.play()

        screen.blit(background_image, (0, 0))

        if show_options:
            title_sprite.draw(screen)
            if play_enabled:
                play_sprite.draw(screen)
            options_sprite.draw(screen)
            quit_sprite.draw(screen)
        elif show_difficulty_options or show_back_button:
            back_sprite.draw(screen)
            if show_difficulty_options:
                easy_sprite.draw(screen)
                medium_sprite.draw(screen)
                hard_sprite.draw(screen)
            if show_kocicky:
                choose_char_sprite.draw(screen)
                screen.blit(kocicka1_image, kocicka1_rect)
                screen.blit(kocicka2_image, kocicka2_rect)
                screen.blit(kocicka3_image, kocicka3_rect)
            
                if selected_kocicka == "kocicka1":
                    pygame.draw.circle(screen, pink, kocicka1_rect.center, 90, 7)
                elif selected_kocicka == "kocicka2":
                    pygame.draw.circle(screen, pink, kocicka2_rect.center, 90, 7)
                elif selected_kocicka == "kocicka3":
                    pygame.draw.circle(screen, pink, kocicka3_rect.center, 90, 7)

        pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if show_options and check_button_click(play_sprite, (x, y)):
                show_difficulty_options = True
                show_options = False
                show_back_button = True
                kliknuti.play()
            elif show_options and check_button_click(options_sprite, (x, y)):
                show_options = False
                show_back_button = True
                show_kocicky = True
                play_enabled = False
                kliknuti.play()
            elif show_options and check_button_click(quit_sprite, (x, y)):
                running = False
                kliknuti.play()
            elif show_back_button and check_button_click(back_sprite, (x, y)):
                show_difficulty_options = False
                show_back_button = False
                show_options = True
                show_kocicky = False
                play_enabled = True
                kliknuti.play()

            elif show_difficulty_options and check_button_click(easy_sprite, (x, y)) and selected_kocicka:
                main.start_game("Easy", selected_kocicka)
                running = False
            elif show_difficulty_options and check_button_click(medium_sprite, (x, y)) and selected_kocicka:
                main.start_game("Medium", selected_kocicka)  
                running = False
            elif show_difficulty_options and check_button_click(hard_sprite, (x, y)) and selected_kocicka:
                main.start_game("Hard", selected_kocicka)
                running = False

            elif show_kocicky:
                if kocicka1_rect.collidepoint(x, y):
                    selected_kocicka = "kocicka1"
                    kocicka1_mnau.play()
                elif kocicka2_rect.collidepoint(x, y):
                    selected_kocicka = "kocicka2"
                    kocicka2_mnau.play()
                elif kocicka3_rect.collidepoint(x, y):
                    selected_kocicka = "kocicka3"
                    kocicka3_mnau.play()

    screen.blit(background_image, (0, 0))

    if show_options:
        title_sprite.draw(screen)
        if play_enabled:
            play_sprite.draw(screen)
        options_sprite.draw(screen)
        quit_sprite.draw(screen)
    elif show_difficulty_options or show_back_button:
        back_sprite.draw(screen)
        if show_difficulty_options:
            easy_sprite.draw(screen)
            medium_sprite.draw(screen)
            hard_sprite.draw(screen)
        if show_kocicky:
            choose_char_sprite.draw(screen)
            screen.blit(kocicka1_image, kocicka1_rect)
            screen.blit(kocicka2_image, kocicka2_rect)
            screen.blit(kocicka3_image, kocicka3_rect)
        
            if selected_kocicka == "kocicka1":
                pygame.draw.circle(screen, pink, kocicka1_rect.center, 90, 7)
            elif selected_kocicka == "kocicka2":
                pygame.draw.circle(screen, pink, kocicka2_rect.center, 90, 7)
            elif selected_kocicka == "kocicka3":
                pygame.draw.circle(screen, pink, kocicka3_rect.center, 90, 7)

    pygame.display.flip()


