import os, pygame, argparse, math

settings = {'resolution': (1280, 720), 'fullscreen': False, 'preserve_aspect_ratio': True, 'framerate': 30, 'debug': True, 'directory': '/home/hunter/Archives/lappystuff/Art', 'transition': 'fade', 'transitiontime': 1, 'imagetime': 5}

def debug(msg):
    if settings['debug']:
        print(msg)

class Image:
    def __init__(self, path, settings):
        self.img = pygame.image.load(path).convert()

        if settings['preserve_aspect_ratio']:
            imgsize = self.img.get_size()
            ratio = min(settings['resolution'][0] / float(imgsize[0]), settings['resolution'][1] / float(imgsize[1]))
            tmpimg = pygame.transform.smoothscale(self.img, (int(imgsize[0] * ratio), int(imgsize[1] * ratio)))

            tmpimgsize = tmpimg.get_size()
            pos = ((settings['resolution'][0] - tmpimgsize[0]) / 2, (settings['resolution'][1] - tmpimgsize[1]) / 2)

            self.img = pygame.Surface(settings['resolution'])
            self.img.blit(tmpimg, pos)

        else:
            self.img = pygame.transform.smoothscale(self.img, settings['resolution'])


        self.alpha = 255

    def draw(self, surf):
        self.img.set_alpha(int(self.alpha))
        surf.blit(self.img, (0,0))

if __name__ == "__main__":
    pygame.init()
    if settings['fullscreen']:
        screen = pygame.display.set_mode(settings['resolution'], FULLSCREEN)
    else:
        screen = pygame.display.set_mode(settings['resolution'])

    images = []
    # TODO: Parse command line args, cheating for now.
    files = os.listdir(settings['directory'])
    for file in files:
        try:
            images.append(Image(os.path.join(settings['directory'], file), settings))
        except pygame.error:
            debug("Could not open file: " + os.path.join(settings['directory'], file) + ", skipping.")

    currimg = images[0]
    clock = pygame.time.Clock()

    currimg.draw(screen)
    pygame.display.flip()

    pygame.time.set_timer(pygame.USEREVENT, int(settings['imagetime'] * 1000))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); quit()
            if event.type == pygame.USEREVENT:
                previmg = images[images.index(currimg)]
                try:
                    currimg = images[images.index(currimg) + 1]
                except IndexError:
                    currimg = images[0]

                if settings['transition'] == 'none':
                    screen.blit(currimg.img, currimg.pos)
                    pygame.display.flip()

                elif settings['transition'] == 'fade':
                    steps = settings['framerate'] * settings['transitiontime']
                    stepsize = 255.0 / steps
                    
                    currimg.alpha = 0

                    for step in range(0, int(math.floor(steps))):
                        screen.fill([0,0,0])
                        previmg.draw(screen)
                        
                        currimg.alpha = currimg.alpha + stepsize
                        currimg.draw(screen)
                        pygame.display.flip()

                        debug('step: ' + str(step) + ' alpha: ' + str(currimg.alpha))

                        clock.tick(settings['framerate'])
    
                    currimg.alpha = 255
                    currimg.draw(screen)
                    pygame.display.flip()
                    
                    
