import pygame
import random
from sys import exit
from pygame import Vector2 as v

class Food:
    def __init__(self, color):
        self.color = color
        self.x = random.randint(0, 1200)
        self.y = random.randint(60, 600)

        self.pos = v(self.x, self.y)
        self.rect = pygame.Rect(self.x, self.y, 5, 5)

    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)

class PLAYER:
    def __init__(self, color, style='arrows'):
        self.scores = 0
        self.size = 5
        self.style = style

        if self.style == 'arrows':
            self.player = 'Player1'
            self.x = 1000
            self.y = 100
        else:
            self.player = 'Player2'
            self.x = 100
            self.y = 100

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.color = color
        self.pos = v(self.x, self.y)

    def movement(self):
        keys = pygame.key.get_pressed()
        if self.style == 'arrows':
            if keys[pygame.K_LEFT]:
                self.x -= 5
            if keys[pygame.K_RIGHT]:
                self.x += 5
            if keys[pygame.K_DOWN]:
                self.y += 5
            if keys[pygame.K_UP]:
                self.y -= 5
        else:
            if keys[pygame.K_q]:
                self.x -= 5
            if keys[pygame.K_d]:
                self.x += 5
            if keys[pygame.K_s]:
                self.y += 5
            if keys[pygame.K_z]:
                self.y -= 5

        self.x = max(0, min(self.x, 1200 - self.rect.width))
        self.y = max(55, min(self.y, 600 - self.rect.height))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def score(self):
        player_text = Font.render(f'{self.player}', 1, 'Black')
        score_text = Font.render(f'score: {self.scores}', 1, 'Black')

        if self.style == 'arrows':
            screen.blit(player_text, (1110, 10))
            screen.blit(score_text, (1110, 35))
        else:
            screen.blit(player_text, (10, 10))
            screen.blit(score_text, (10, 35))

    def update(self):
        self.movement()
        pygame.draw.ellipse(screen, self.color, self.rect)
        

class AIPLAYER:
    def __init__(self):
        self.reset()
        
    def draw(self):
        pygame.draw.ellipse(screen, self.color, self.rect)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.x = max(0, min(self.x, 1200 - self.rect.width))
        self.y = max(55, min(self.y, 600 - self.rect.height))

    def follow_point(self, target_pos):
        if self.pos != target_pos:
            direction = (target_pos - self.pos).normalize()
            self.pos += direction * 3

            self.x, self.y = self.pos.x, self.pos.y
            self.rect.topleft = self.pos
        pygame.draw.ellipse(screen, self.color, self.rect)
    
    def reset(self):
        self.color = '#FFFFFF'
        self.scores = 0
        self.size = 5
        self.x = random.randint(200, 800)
        self.y = random.randint(200, 400)

        self.pos = v(self.x, self.y)
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.target = 'Food'

    def score(self):
        player_text = Font.render(("Computer:"), 1, 'Black')
        score_text = Font.render(f'score: {self.scores}', 1, 'Black')

        screen.blit(player_text, (10, 10))
        screen.blit(score_text, (10, 35))



class MAIN:
    def __init__(self):
        self.front = True    
        self.colors = ['#FF5733', '#33FF57', '#3357FF', '#F1C40F', '#9B59B6',
                       '#1ABC9C', '#E74C3C', '#8E44AD', '#2ECC71', '#3498DB',
                       '#E67E22', '#95A5A6', '#34495E', '#16A085',
                       '#27AE60', '#2980B9', '#8E44AD', '#2C3E50', '#D35400']

        self.ai_mode = None
        self.ai = AIPLAYER()
        self.food = [Food(random.choice(self.colors)) for _ in range(151)]
        self.game_on = False
        self.winner = False
        self.players= []

    def collision(self):
        for player in self.players:
            for bite in self.food:
                if player.rect.colliderect(bite.rect):
                    player.size += 1
                    player.scores += 1
                    self.food.remove(bite)
                
        if not self.ai_mode:
            if self.players[0].rect.colliderect(self.players[-1].rect):
                if self.players[0].scores < self.players[-1].scores:
                    self.winner = True
                    self.game_on = False
            
                elif self.players[0].scores > self.players[-1].scores:
                    self.winner = True
                    self.game_on = False
      

    def win(self):
        screen.fill('#13262F')
        if self.winner:
            if not self.ai_mode:
                if self.players[0].scores > self.players[1].scores:
                    winner_text = Font.render(f'{self.players[0].player} wins!', 1, 'White')
                else:
                    winner_text = Font.render(f'{self.players[1].player} wins!', 1, 'White')
            else:
                if self.players[0].scores > self.ai.scores:
                    winner_text = Font.render(f'{self.players[0].player} wins!', 1, 'White')
                else:
                    winner_text = Font.render('Computer wins!', 1, 'White')
            screen.blit(winner_text, (600, 200))


        self.replay_text = Font.render('Replay', 1, 'Black', 'Yellow')
        self.replay_text_rect = self.replay_text.get_rect(center=(600, 400))

        if self.replay_text_rect.collidepoint(pygame.mouse.get_pos()):
            self.replay_text = Font.render('Replay', 1, 'Black', 'Green')

        screen.blit(self.replay_text, self.replay_text_rect)


    def front_page(self):
        screen.fill('#13262F')
        self.new_text = Font.render('Play with Friend', 1, 'Black', 'Yellow')
        self.new_text_rect = self.new_text.get_rect(center=(600, 400))

        self.ai_option = Font.render('Play with Computer', 1, 'Black', 'Yellow')
        self.ai_option_rect = self.ai_option.get_rect(center=(600, 450))

        if self.front:
            instruction_text = Font.render(f'Player1 uses Arrow keys for and Player2 uses ZQSD', 1, 'White')
            screen.blit(instruction_text, (390, 200))

        if self.new_text_rect.collidepoint(pygame.mouse.get_pos()):
            self.new_text = Font.render('Play with Friend', 1, 'Black', 'Green')
        if self.ai_option_rect.collidepoint(pygame.mouse.get_pos()):
            self.ai_option = Font.render('Play with Computer', 1, 'Black', 'Green')

        screen.blit(self.new_text, self.new_text_rect)
        screen.blit(self.ai_option, self.ai_option_rect)

    def scores(self):
        if self.ai_mode:
            self.ai.score()
            self.players[0].score()
        else:
            for player in self.players:
                player.score()
        

    def restart(self):
        self.players.clear()
        self.ai.reset()

        self.food = [Food(random.choice(self.colors)) for _ in range(151)]
        self.game_on = False
        self.winner = False
        self.front = True
        self.ai_mode = None
        
    def determine_mode(self):
        if self.front:
            if self.ai_mode:
                self.players = [PLAYER(random.choice(self.colors))]
            elif not self.ai_mode:
                self.players = [PLAYER(random.choice(self.colors)),PLAYER(random.choice(self.colors),'zqsd')]

    def ai_target(self):
            if (self.players[0].scores + 3) > self.ai.scores:
                self.ai.target = 'Food' 
            elif self.players[0].scores < self.ai.scores:
                self.ai.target = 'Player'
            
    def follow_player(self):
        if self.ai.target == 'Player':
            self.ai.follow_point((self.players[0].x,self.players[0].y))

    def follow_food(self):
        if self.ai.target == 'Food':
            self.x_pos=[]
            self.y_pos = []

            for bite in self.food:
                self.x_pos.append(bite.x)
                self.y_pos.append(bite.y)
                
            if self.food:
                closest_x = min(self.x_pos, key=lambda x:abs(x-self.ai.x))
                closest_y = min(self.y_pos, key=lambda x:abs(x-self.ai.y))

                distance_to_closest_x = abs(closest_x - self.ai.x)
                distance_to_closest_y = abs(closest_y - self.ai.y)

                if distance_to_closest_x < distance_to_closest_y:
                    self.ai.follow_point((closest_x, self.food[self.x_pos.index(closest_x)].y))
                else:
                    self.ai.follow_point((self.food[self.y_pos.index(closest_y)].x, closest_y))

    def ai_collision(self):
        for bite in self.food:
            if self.ai.rect.colliderect(bite.rect):
                self.food.remove(bite)
                self.ai.size += 1
                self.ai.scores += 1 

        if self.players[0].rect.colliderect(self.ai.rect):
            if self.players[0].scores < self.ai.scores:
                self.winner = True
                self.game_on = False
            elif self.players[0].scores > self.ai.scores:
                self.winner = True 
                self.game_on = False

    def update(self):
        screen.fill('#13262F')
        self.determine_mode()
        
        if self.game_on:
            pygame.draw.line(screen, 'Yellow', (0, 0), (1200, 0), 110)
            self.scores()

            for bite in self.food:
                bite.draw()

            for player in self.players:
                player.update()
            
            self.collision()

            if self.ai_mode:
                self.ai.draw()
                self.ai_target()
                self.ai_collision()
                self.follow_food()
                self.follow_player()

        if self.winner:
            self.win()
        if self.front:
            self.front_page()


pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
pygame.display.set_caption('Hungry Shapes')

Font = pygame.font.Font(None, 30)
main = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if main.front and main.new_text_rect.collidepoint(pygame.mouse.get_pos()):
                main.ai_mode = False
                main.front = False
                main.game_on = True
            elif main.front and main.ai_option_rect.collidepoint(pygame.mouse.get_pos()):
                main.ai_mode = True
                main.front = False
                main.game_on = True
            
            
            elif main.replay_text_rect.collidepoint(pygame.mouse.get_pos()):
                main.restart()

    main.update()
    pygame.display.update()
    clock.tick(60)