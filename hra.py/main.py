import sys
import pygame
import menu1
from pole3 import Granulky, Kocicka, Duch, Score, Button, draw_walls, normal_granulky_size, special_granulky_size, special_granulky, maze

pygame.mixer.init()
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 750

black = (0, 0, 0)
pink = (150, 50, 100)
light_pink = (255, 192, 203)
white = (255, 255, 255)

kocicka1 = pygame.image.load("hra.py/obrazky/kocicka1.png")
kocicka1 = pygame.transform.scale(kocicka1, (45, 45))
kocicka2 = pygame.image.load("hra.py/obrazky/kocicka2.png")
kocicka2 = pygame.transform.scale(kocicka2, (45, 45))
kocicka3 = pygame.image.load("hra.py/obrazky/kocicka3.png")
kocicka3 = pygame.transform.scale(kocicka3, (45, 45))
duch1_obrazek = pygame.image.load("hra.py/obrazky/duch1.png")
duch1_obrazek = pygame.transform.scale(duch1_obrazek, (27, 27))
duch2_obrazek = pygame.image.load("hra.py/obrazky/duch2.png")
duch2_obrazek = pygame.transform.scale(duch2_obrazek, (27, 27))
duch3_obrazek = pygame.image.load("hra.py/obrazky/duch3.png")
duch3_obrazek = pygame.transform.scale(duch3_obrazek, (27, 27))
duch4_obrazek = pygame.image.load("hra.py/obrazky/duch4.png")
duch4_obrazek = pygame.transform.scale(duch4_obrazek, (27, 27))
duch5_obrazek = pygame.image.load("hra.py/obrazky/duch5.png")
duch5_obrazek = pygame.transform.scale(duch5_obrazek, (27, 27))
crying_cat = pygame.image.load("hra.py/obrazky/game_over.jpeg")
crying_cat = pygame.transform.scale(crying_cat, (660, 750))
win_cat = pygame.image.load("hra.py/obrazky/win.jpeg")
win_cat = pygame.transform.scale(win_cat, (660, 750))
kliknuti = pygame.mixer.Sound("hra.py/zvuky/click_button.mp3")
game_over_song = pygame.mixer.Sound("hra.py/zvuky/game_over1.mp3")
win_song = pygame.mixer.Sound("hra.py/zvuky/win_song.mp3")
hra_pisnicka = pygame.mixer.music.load("hra.py/zvuky/hra_pisnicka.mp3")

def restart_game(difficulty, selected_kocicka):
    """Restartuje hru s určitou obtížností a určitou kočičkou."""
    pygame.mixer.music.play(0)
    main(difficulty, selected_kocicka)

def start_game(difficulty, selected_kocicka):
    """Spustí hru s určitou obtížností a určitou kočičkou."""
    pygame.mixer.music.play(0)
    main(difficulty, selected_kocicka)
    

def main(difficulty, selected_kocicka):
    """Hlavní funkce hry."""
    score = Score()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Kočičky')

    nadpis_font = pygame.font.Font(None, 140)
    podnadpis_font = pygame.font.Font(None, 70)
    score_font = pygame.font.Font(None, 30)
    win_sprite = Button("YOU WIN!", nadpis_font, pink, black, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    konec_sprite = Button("GAME OVER!", nadpis_font, pink, black, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    menu_sprite = Button("Menu", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    again_sprite = Button("Play Again", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    quit_sprite = Button("Quit", podnadpis_font, black, pink, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))

    if selected_kocicka == "kocicka1":
        selected_image = kocicka1
    elif selected_kocicka == "kocicka2":
        selected_image = kocicka2
    elif selected_kocicka == "kocicka3":
        selected_image = kocicka3

    clock = pygame.time.Clock()

    granulky_list = [Granulky(x, y, special_granulky_size if (x, y) in special_granulky else normal_granulky_size) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == '.']
    
    kocicka = Kocicka(1, 2, selected_image)

    duchy = [
        Duch(28, 1, duch1_obrazek),
        Duch(16, 12, duch2_obrazek),
        Duch(1, 28, duch3_obrazek), 
        Duch(16, 12, duch4_obrazek),
        Duch(28, 1, duch5_obrazek)]
    
    if difficulty == "Easy":
        duchy = duchy[:3]
    elif difficulty == "Medium":
        duchy = duchy[:4]
    elif difficulty == "Hard":
        duchy = duchy[:5]

    game_over = False
    all_granulky_collected = False
    game_over_played = False
    win_played = False

    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y, = event.pos
                if quit_sprite.is_clicked(x, y):
                    kliknuti.play()
                    pygame.quit()
                    sys.exit()
                elif again_sprite.is_clicked(x, y):
                    restart_game(difficulty, selected_kocicka)
                    kliknuti.play()
                    return 
                elif menu_sprite.is_clicked(x, y):
                    kliknuti.play()
                    menu1.show_difficulty_options = False
                    menu1.show_back_button = False
                    menu1.show_options = True
                    menu1.show_kocicky = False
                    menu1.play_enabled = True
                    menu1.show_menu()
                    kliknuti.play()
                    return

            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    kocicka.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    kocicka.direction = (1, 0)
                elif event.key == pygame.K_UP:
                    kocicka.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    kocicka.direction = (0, 1)
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    kocicka.direction = (0, 0)

        if not game_over and not all_granulky_collected:
            screen.fill(black)

            kocicka.move()
            kocicka.collision_granulky(granulky_list, score)
            if kocicka.check_collision_with_ghosts(duchy):
                game_over = True

            for i in range(len(duchy)):
                duchy[i].move()
                
            for i in range(len(duchy)):
                duchy[i].draw(screen)

            for granulky in granulky_list:
                granulky.draw(screen)

            if len(granulky_list) == 0:
                all_granulky_collected = True

            draw_walls(screen, maze)
            score.draw(screen, score_font, white, (10, 10))
            
            screen.blit(selected_image, (kocicka.rect.x - 12, kocicka.rect.y - 12))
            pygame.display.flip()
            clock.tick(12)
            
        if game_over:
            screen.blit(crying_cat, (0, 0))
            konec_sprite.draw(screen)
            menu_sprite.draw(screen)
            again_sprite.draw(screen)
            quit_sprite.draw(screen)
            pygame.mixer.music.stop()
            if not game_over_played:
                game_over_song.play()
                game_over_played = True
            pygame.display.flip()

        elif all_granulky_collected:
            screen.blit(win_cat, (0, 0))
            win_sprite.draw(screen)
            menu_sprite.draw(screen)
            again_sprite.draw(screen)
            quit_sprite.draw(screen)
            pygame.mixer.music.stop()
            if not win_played:
                win_song.play()
                win_played = True
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
    