import pygame

class ChessClock:
    def __init__(self, screen, font, color, pos):
        self.screen = screen
        self.font = font
        self.color = color
        self.pos = pos
        self.time = 300  # Startzeit in Sekunden
        self.paused = False

    def update(self):
        if not self.paused:
            self.time -= 1

    def draw(self):
        print("draw")
        minutes = self.time // 60
        seconds = self.time % 60
        time_str = f"{minutes:02}:{seconds:02}"
        text_surface = self.font.render(time_str, True, self.color)
        self.screen.blit(text_surface, self.pos)
