import pygame
from timer import Timer
import numpy as np
import tools
import time

class Colour:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

class RandomDotDecisionTask:
    # game cosntants
    DOT_RADIUS = 3
    DOT_RADIUS = 3
    CENTER_DOT_RADIUS = 4
    CIRCLE_RADIUS = 300
    ARROW_SCALE = 1
    PREFERRED_DIRECTION = [np.pi/2, 3*np.pi / 2] # 90° = upwards, 270° = downwards
    SPEED = 4
    NUM_DOTS = 500

    def __init__(self, screen_width, screen_height, motion_strengths) -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Random Dot Decision Task")

        self.clock = pygame.time.Clock()

        self.timer = Timer()

        # state parameter
        self.running = True
        self.show_cum_dir = False
        self.game_start = False
        self.show_info = False

        # task parameter
        self.round_counter = 0
        self.center = (screen_width // 2, screen_height // 2)
        self.motion_strengths = motion_strengths

        # task state
        self.dots = []
        self.coherence = 0
        self.pref_dir = 0

        self.answers = []

    def run(self, rounds):
        self.dots, self.coherence, self.pref_dir = self._new_trial_initialization()
        while self.running:
            self.handle_events()
            if self.round_counter >= rounds:
                break

            self.update()
            self.draw()
            self.clock.tick(30)

        if self.running:
            self._draw_end_screen()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.game_start:
                    if event.key == pygame.K_x:
                        self.show_cum_dir = not self.show_cum_dir

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        decision_time = self.timer.stop()
                        self.round_counter += 1
                        self.timer.reset()

                        check = self._check_answer(1, tools.pos_to_angle(*self._get_cumulative_direction()))

                        self.answers.append((decision_time, check, self.coherence, self.pref_dir))

                        self.dots, self.coherence, self.pref_dir = self._new_trial_initialization()
                        self._after_trial_wait(check)
                        self.timer.start()

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        decision_time = self.timer.stop()
                        self.round_counter += 1
                        self.timer.reset()

                        check = self._check_answer(0, tools.pos_to_angle(*self._get_cumulative_direction()))

                        self.answers.append((decision_time, check, self.coherence, self.pref_dir))

                        self.dots, self.coherence, self.pref_dir = self._new_trial_initialization()
                        self._after_trial_wait(check)
                        self.timer.start()

                    if event.key == pygame.K_i:
                        self.show_info = not self.show_info

                if event.key == pygame.K_SPACE:
                    if self.game_start == False:
                        self.game_start = True
                        self._draw_scene()
                        pygame.display.flip()
                        time.sleep(2)
                        self.timer.start()
                        
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self._update_dots()

    def draw(self):
        self._draw_scene()
        if not self.game_start:
            self._draw_start_screen()
        else:
            self._draw_dots()

        if self.show_cum_dir:
            self._draw_prefered_direction()

        if self.show_info:
            self._draw_info()

        pygame.display.flip()

    def quit(self):
        pygame.quit()
        
    def _draw_scene(self):
        self.screen.fill(Colour.BLACK)
        pygame.draw.circle(self.screen, Colour.BLUE, self.center, RandomDotDecisionTask.CIRCLE_RADIUS, 1) # outer boundary circle
        pygame.draw.circle(self.screen, Colour.RED, self.center, RandomDotDecisionTask.CENTER_DOT_RADIUS) # center dot

    def _get_direction(self, pref_dir, motion_strength):
        if np.random.rand() < motion_strength:  
           return np.random.uniform(pref_dir - np.pi / 10, pref_dir + np.pi / 10)
        else: 
            return np.random.uniform(0, 2*np.pi)
        
    def _init_dots(self, size, prefered_direction, motion_strength):
        dots = []
        for _ in range(size):
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, RandomDotDecisionTask.CIRCLE_RADIUS)
            x = self.center[0] + radius * np.cos(angle)
            y = self.center[1] + radius * np.sin(angle)

            # Introduce a bias towards the preferred direction for most dots
            direction = self._get_direction(prefered_direction, motion_strength)
            
            dots.append([x, y, direction])

        return dots
    
    def _update_dots(self):
        # update dot positions
        for dot in self.dots:
            dx = RandomDotDecisionTask.SPEED * np.cos(dot[2])
            dy = RandomDotDecisionTask.SPEED * np.sin(dot[2])
            dot[0] += dx
            dot[1] += dy

            # If a dot moves outside the inner circle, reposition it randomly within the inner circle
            if (dot[0] - self.center[0])**2 + (dot[1] - self.center[1])**2 > RandomDotDecisionTask.CIRCLE_RADIUS**2:
                angle = np.random.uniform(0, 2 * np.pi)
                radius = np.random.uniform(0, RandomDotDecisionTask.CIRCLE_RADIUS)
                dot[0] = self.center[0] + radius * np.cos(angle)
                dot[1] = self.center[1] + radius * np.sin(angle)
                
                dot[2] = self._get_direction(self.pref_dir, self.coherence)

    def _draw_dots(self):
        for dot in self.dots:
            pygame.draw.circle(self.screen, Colour.WHITE, (int(dot[0]), int(dot[1])), RandomDotDecisionTask.DOT_RADIUS)
        
    def _get_cumulative_direction(self):
        cum_dx = np.sum([RandomDotDecisionTask.SPEED*np.cos(dot[2]) for dot in self.dots])
        cum_dy = np.sum([RandomDotDecisionTask.SPEED*np.sin(dot[2]) for dot in self.dots])

        return cum_dx, cum_dy
        
    def _draw_prefered_direction(self):
        cumulative_dx, cumulative_dy = self._get_cumulative_direction()
        # Calculate the cumulative direction and draw the arrow
        cumulative_angle = np.arctan2(cumulative_dy, cumulative_dx)
        arrow_length = np.sqrt(cumulative_dx**2 + cumulative_dy**2) * RandomDotDecisionTask.ARROW_SCALE
        arrow_end = (self.center[0] + arrow_length * np.cos(cumulative_angle),
                    self.center[1] + arrow_length * np.sin(cumulative_angle))

        pygame.draw.line(self.screen, Colour.GREEN, self.center, arrow_end, 3)
    
    def _draw_info(self):
        font_size = 32
        font = pygame.font.Font(None, font_size)
        text = f"coherence: {self.coherence * 100}%"

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, text_rect)
        pass

    def _draw_start_screen(self):
        font_size = 32
        font = pygame.font.Font(None, font_size)
        text = "Press SPACE to start"

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.center)
        self.screen.blit(text_surface, text_rect)

    def _draw_end_screen(self):
        self.screen.fill(Colour.BLACK)

        font_size = 32
        font = pygame.font.Font(None, font_size)
        text = "Thank you for participating"

        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.center)
        self.screen.blit(text_surface, text_rect)

        pygame.display.flip()
        time.sleep(3)

    # think how to build this in
    def _after_trial_wait(self, check):
        self.screen.fill(Colour.BLACK)

        self._draw_scene()
        pygame.display.flip()

        time.sleep(1)

        #penalty waiting time
        if check == False:
            time.sleep(2)

    def _new_trial_initialization(self):
        coherence = np.random.choice(self.motion_strengths)
        prefered_direction = np.random.choice(RandomDotDecisionTask.PREFERRED_DIRECTION)
        dots = self._init_dots(RandomDotDecisionTask.NUM_DOTS, prefered_direction, coherence)

        return dots, coherence, prefered_direction
    
    def _check_answer(self, direction_idx, actual_direction):
        if np.abs(RandomDotDecisionTask.PREFERRED_DIRECTION[direction_idx] - actual_direction) < np.abs(RandomDotDecisionTask.PREFERRED_DIRECTION[1 - direction_idx] - actual_direction):
            return True
        else:
            return False