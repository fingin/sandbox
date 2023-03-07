#grab (use http) image from gelbooru and display it fullscreen on a screen with a resolution of 1920x1080

#import pygame http
import pygame

#framework for http requests
import http.client as http
import random




#main render loop
def renderLoop():
    #moved init to render loop
    pygame.init()
    pygame.display.set_caption("some game")
    position = (0, 0)
    screen = pygame.display.set_mode((1920, 1080))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                #get image and display on screen on key press space bar
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    image = getImage()


#function to get a random image from gelbooru
def getImage():
    #get a random image from gelbooru

    #proform a http get request to gelbooru to get image
    conn = http.HTTPConnection("gelbooru.com")
    conn.request("GET", "/index.php?page=post&s=view&id=%d" % random.randint(1, 100000))
    r = conn.getresponse()
    data = r.read()
    print(data)
    

    #get image tag from data

#main function
if __name__ == "__main__":
    print("im main")
    renderLoop()


