import pygame
import random
import sys


pygame.init()

# Importer les mots depuis le fichier texte
def charger_mots():
    try:
        with open("/Users/mathisserra/Desktop/Github/pendu/mots", "r") as fichier:
            mots = [mot.strip().upper() for mot in fichier.readlines()]
        return mots
    except FileNotFoundError:
        print("Fichier de mots introuvable.")
        sys.exit()

# Fenêtre de jeu
Blanc = (255, 255, 255)
Noir = (0, 0, 0)
largeur = 800
hauteur = 600


# New background image file path
new_background_image_path = "/Users/mathisserra/Desktop/Github/pendu/wallpaper.jpeg"
font = pygame.font.Font("minecraft_font.ttf", 40)
reload_rect = pygame.Rect(200, 375, 400, 50)


# Load the new background image
    
new_background_image = pygame.image.load(new_background_image_path)
# Charger l'image de fond
gameWindow = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Jeu du Pendu")

#Random word selection

mots = charger_mots()
mot_a_trouver = random.choice(mots)
lettres_trouvees = []

#Incorrect letters
lettres_incorrectes = []
new_game = True




parties_pendu = 0
#images of hearts
images_pendu = [
    pygame.image.load("/Users/mathisserra/Desktop/Github/pendu/heart3.png"),
    pygame.image.load("/Users/mathisserra/Desktop/Github/pendu/heart2.png"),
    pygame.image.load("/Users/mathisserra/Desktop/Github/pendu/heart1.png"),
]


clock = pygame.time.Clock()


def dessiner_pendu(parties):
    largeur_image = images_pendu[parties].get_width()
    hauteur_image = images_pendu[parties].get_height()
    
    facteur_reduction = 0.3  # Adjust the reduction factor to resize the image

    nouvelle_largeur = int(largeur_image * facteur_reduction)
    nouvelle_hauteur = int(hauteur_image * facteur_reduction)

    image_redimensionnee = pygame.transform.scale(images_pendu[parties], (nouvelle_largeur, nouvelle_hauteur))
    #change the position of the image in that case it goes bellow the masked word
    x = (largeur - nouvelle_largeur) // 2
    y = (hauteur - nouvelle_hauteur) +1

    gameWindow.blit(image_redimensionnee, (x, y))
    
    
def draw_text(text):
    texte = font.render(text, True, Blanc)
    gameWindow.blit(texte, (largeur // 2 - texte.get_width() // 2, hauteur // 2 - texte.get_height() // 2))
        
    
    
#Main loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.pos=pygame.mouse.get_pos()
            if reload_rect.collidepoint(event.pos):
                print("recommencer")    
                new_game = True
                mot_a_trouver = random.choice(mots)
                parties_pendu = 0
                lettres_trouvees = []
                lettres_incorrectes = []
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                lettre = event.unicode.upper()
                if lettre not in lettres_trouvees and lettre not in lettres_incorrectes:
                    if lettre in mot_a_trouver:
                        lettres_trouvees.append(lettre)
                    else:
                        lettres_incorrectes.append(lettre)
                        parties_pendu += 1
    
    if new_game:    
        # Blit the new background image
        gameWindow.blit(new_background_image, (0, 0))
        
        # masked word
        mot_masque = ""
        for lettre in mot_a_trouver:
            if lettre in lettres_trouvees:
                mot_masque += lettre
            else:
                mot_masque += "_"


            #Show mascked word
        
        texte_mot = font.render(mot_masque, True, Blanc)
        gameWindow.blit(texte_mot, (largeur // 2 - texte_mot.get_width() // 2, hauteur // 2 - texte_mot.get_height() // 2))

        # Show incorrect letters
        texte_incorrect = font.render("Lettres incorrectes: " + " ".join(lettres_incorrectes), True, Blanc)
        gameWindow.blit(texte_incorrect, (50, 50))

        dessiner_pendu(parties_pendu)

        # Verify if victory
        if set(mot_a_trouver) == set(lettres_trouvees):
            new_game = False
            if new_game == False:
                font_win = pygame.font.Font("minecraft_font.ttf", 20)
                texte_win = font_win.render("Felicitations, vous avez trouve le mot !",  True, Blanc)
                gameWindow.blit(texte_win, (largeur // 2 - texte_win.get_width() // 2, hauteur // 3  - texte_win.get_height() // 2))
                lettres_incorrectes = []
                lettres_trouvees = []
                text_reload = font_win.render("Appuyez ici pour recommencer", True, Blanc)
                pygame.draw.rect(gameWindow, Noir, reload_rect)
                gameWindow.blit(text_reload, (largeur // 2 +2 - texte_win.get_width() // 3 - 32, hauteur // 3*2  - text_reload.get_height() // 2))
                
        if set(lettres_incorrectes) == set(images_pendu):
                new_game = False
                if new_game == False:
                    font_lose = pygame.font.Font("minecraft_font.ttf", 20)
                    texte_lose = font_lose.render("Vous avez perdu, le mot etait: " + mot_a_trouver, True, Blanc)
                    gameWindow.blit(texte_lose, (largeur // 2 - texte_lose.get_width() // 2, hauteur // 3  - texte_lose.get_height() // 2))
                    lettres_incorrectes = []
                    lettres_trouvees = []
                    text_reload = font_lose.render("Appuyez ici pour recommencer", True, Blanc)
                    pygame.draw.rect(gameWindow, Noir, reload_rect)
                    gameWindow.blit(text_reload, (largeur // 2 +2 - texte_win.get_width() // 3 - 32, hauteur // 3*2  - text_reload.get_height() // 2))
            
        # Update the display
        pygame.display.flip()
        clock.tick(30)

        
    
    