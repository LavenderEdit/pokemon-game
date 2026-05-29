import pygame

class SpriteSheet:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        
        image.blit(self.sheet, (0, 0), rect)
        
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
            
        return image

    def images_at(self, rects, colorkey=None):
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_grid_images(self, num_x, num_y, start_x=0, start_y=0, sprite_w=64, sprite_h=64):
        images = []
        for y in range(num_y):
            for x in range(num_x):
                rect = (start_x + (x * sprite_w), start_y + (y * sprite_h), sprite_w, sprite_h)
                images.append(self.image_at(rect))
        return images