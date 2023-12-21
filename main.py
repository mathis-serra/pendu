import pygame
import random
import sys


pygame.init()

# Importer les mots depuis le fichier texte
def charger_mots():
    try:
        with open("mots", "r") as fichier:
            mots = [mot.strip().upper() for mot in fichier.readlines()]
        return mots
    except FileNotFoundError:
        print("Fichier de mots introuvable.")
        sys.exit()

# Fenêtre de jeu
Blanc = (255, 255, 255)
Noir = (0, 0, 0)
Grey = (128, 128, 128)
largeur = 800
hauteur = 600
# Not hide the image of hearts
hide_image = False


# New background image file path
new_background_image_path = "images/wallpaper.jpeg"
font = pygame.font.Font("minecraft_font.ttf", 40)
font_win = pygame.font.Font("minecraft_font.ttf", 20)
# Reload button rectangle 
reload_rect = pygame.Rect(200, 375, 400, 50)
# Load music file
music_file = "minecraft.mp3"  # Replace with the path to your music file
pygame.mixer.music.load(music_file)

# Set volume (optional)
pygame.mixer.music.set_volume(0.5)  # Adjust the volume (0.0 to 1.0)

# Start playing the music (infinite loop by default)
pygame.mixer.music.play()



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
    pygame.image.load("images/heart3.png"),
    pygame.image.load("images/heart2.png"),
    pygame.image.load("images/heart1.png"),
    pygame.image.load("images/heart3.png")
]


clock = pygame.time.Clock()



        
    
    
#Main loop
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer_music.stop() 
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            event.pos=pygame.mouse.get_pos()
            if reload_rect.collidepoint(event.pos):  
                new_game = True
                mot_a_trouver = random.choice(mots)
                parties_pendu = 0
                lettres_trouvees = []
                lettres_incorrectes = []
                hide_image = False
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


            
        #Show masked word
        texte_mot = font.render(mot_masque, True, Blanc)
        gameWindow.blit(texte_mot, (largeur // 2 - texte_mot.get_width() // 2, hauteur // 2 - texte_mot.get_height() // 2))

        # Show incorrect letters
        texte_incorrect = font.render("Lettres incorrectes: " + " ".join(lettres_incorrectes), True, Blanc)
        gameWindow.blit(texte_incorrect, (50, 50))

       

        # Verify if victory
        if set(mot_a_trouver) == set(lettres_trouvees):
            new_game = False
            hide_image  = True
            #new font to change size of it
            
            texte_win = font_win.render("Felicitations, vous avez trouve le mot !",  True, Blanc)
            gameWindow.blit(texte_win, (largeur // 2 - texte_win.get_width() // 2, hauteur // 3  - texte_win.get_height() // 2))
            lettres_incorrectes = []
            lettres_trouvees = []
            text_reload = font_win.render("Appuyez ici pour recommencer", True, Blanc)
            pygame.draw.rect(gameWindow, Grey, reload_rect)
            gameWindow.blit(text_reload, (largeur // 2 +2 - texte_win.get_width() // 3 - 32, hauteur // 3*2  - text_reload.get_height() // 2))
              
            
        
        # Verify if defeat
        if len(lettres_incorrectes) == 3:
            new_game = False
            if new_game == False:                 
                texte_lose = font_win.render("Vous avez perdu", True, Blanc)
                gameWindow.blit(texte_lose, (largeur // 2 - texte_lose.get_width() // 2, hauteur // 3 - texte_lose.get_height() // 2))
                text_reload = font_win.render("Appuyez ici pour recommencer", True, Blanc)
                pygame.draw.rect(gameWindow, Grey, reload_rect)  
                gameWindow.blit(text_reload, (largeur // 3 + 20 - texte_lose.get_width() // 3 , hauteur // 3 * 2 - 3 - text_reload.get_height() // 2))
                
            
        # Show the number of hearts 
        if not hide_image and parties_pendu < len(images_pendu) -1:
            gameWindow.blit(images_pendu[parties_pendu], (largeur // 2 - images_pendu[parties_pendu].get_width() // 2, hauteur // 3 * 2 + 40  - images_pendu[parties_pendu].get_height() // 2))


        pygame.display.flip()
        clock.tick(30)

        
    
    