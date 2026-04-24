import pygame
import random

pygame.init()

# Размеры
width = 800
height = 500

# Окно
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Пинг-понг - Игра до 10")
clock = pygame.time.Clock()

# Ракетки
paddle_w = 10
paddle_h = 100

left_paddle = pygame.Rect(10, height//2 - 50, paddle_w, paddle_h)
right_paddle = pygame.Rect(width - 20, height//2 - 50, paddle_w, paddle_h)

# Мяч
ball = pygame.Rect(width//2 - 10, height//2 - 10, 20, 20)

# Скорости
ball_speed = 3
paddle_speed = 12

ball_dx = ball_speed * random.choice([-1, 1])
ball_dy = ball_speed * random.choice([-1, 1])

# Счёт
score_left = 0
score_right = 0
font = pygame.font.Font(None, 36)
font_big = pygame.font.Font(None, 72)

# Состояние игры
game_over = False
winner = None

# ставит мяч в центр поля после того, как забит гол
def reset_ball():
    global ball_dx, ball_dy, ball_speed
    
    # Ставим мяч в центр
    ball.center = (width//2, height//2)
    
    # Случайное направление (немного случайности по вертикали)
    ball_dx = ball_speed * random.choice([-1, 1])
    ball_dy = ball_speed * random.uniform(-1, 1)  # разный угол
    
    # Чтобы мяч не летел строго горизонтально
    if abs(ball_dy) < 1:
        ball_dy = ball_speed * 0.5 if ball_dy > 0 else -ball_speed * 0.5

def increase_speed():
    global ball_speed, ball_dx, ball_dy, paddle_speed
    
    # Увеличиваем скорость мяча
    ball_speed = min(ball_speed + 0.5, 15)
    
    # Ракетки быстрее мяча
    paddle_speed = ball_speed + 5
    paddle_speed = min(paddle_speed, 20)
    
    # Сохраняем направление, меняем скорость
    direction_x = 1 if ball_dx > 0 else -1
    direction_y = 1 if ball_dy > 0 else -1
    
    ball_dx = ball_speed * direction_x
    ball_dy = ball_speed * direction_y

# Игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_SPACE:
                game_over = False
                winner = None
                score_left = 0
                score_right = 0
                ball_speed = 3
                paddle_speed = 12
                reset_ball()
                left_paddle.center = (10 + paddle_w//2, height//2)
                right_paddle.center = (width - 20 + paddle_w//2, height//2)
    
    if not game_over:
        keys = pygame.key.get_pressed()
        
        # Левая ракетка
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < height:
            left_paddle.y += paddle_speed
        
        # Правая ракетка
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < height:
            right_paddle.y += paddle_speed
        
        # Движение мяча
        ball.x += ball_dx
        ball.y += ball_dy
        
        # Столкновение с верхом/низом
        if ball.top <= 0:
            ball.top = 0  # прижимаем к границе
            ball_dy = -ball_dy
        if ball.bottom >= height:
            ball.bottom = height
            ball_dy = -ball_dy
        
        # Столкновение с левой ракеткой
        if ball.colliderect(left_paddle) and ball_dx < 0:
            # Отодвигаем мяч от ракетки, чтобы не застревал
            ball.left = left_paddle.right
            ball_dx = -ball_dx
            
            # Добавляем эффект: куда ударила ракетка, туда и отскок
            hit_pos = (ball.centery - left_paddle.centery) / (paddle_h / 2)
            hit_pos = max(-1, min(1, hit_pos))  # от -1 до 1
            ball_dy = hit_pos * ball_speed * 1.5
        
        # Столкновение с правой ракеткой
        if ball.colliderect(right_paddle) and ball_dx > 0:
            # Отодвигаем мяч от ракетки
            ball.right = right_paddle.left
            ball_dx = -ball_dx
            
            # Эффект от удара
            hit_pos = (ball.centery - right_paddle.centery) / (paddle_h / 2)
            hit_pos = max(-1, min(1, hit_pos))
            ball_dy = hit_pos * ball_speed * 1.5
        
        # Голы
        if ball.left <= 0:
            score_right += 1
            increase_speed()
            reset_ball()
            
            if score_right >= 10:
                game_over = True
                winner = "ПРАВЫЙ"
        
        if ball.right >= width:
            score_left += 1
            increase_speed()
            reset_ball()
            
            if score_left >= 10:
                game_over = True
                winner = "ЛЕВЫЙ"
    
    # Рисование
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 255, 255), left_paddle)
    pygame.draw.rect(screen, (255, 255, 255), right_paddle)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    
    score_text = font.render(f"{score_left} : {score_right}", True, (255, 255, 255))
    screen.blit(score_text, (width//2 - 30, 30))
    
    ball_speed_text = font.render(f"Ball speed: {ball_speed:.1f}", True, (200, 200, 200))
    screen.blit(ball_speed_text, (10, 10))
    
    paddle_speed_text = font.render(f"Paddle speed: {paddle_speed:.1f}", True, (200, 200, 200))
    screen.blit(paddle_speed_text, (10, 40))
    
    # Линия по середине
    for i in range(0, height, 30):
        pygame.draw.rect(screen, (255, 255, 255), (width//2 - 2, i, 4, 15))
    
    if game_over:
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        win_text = font_big.render(f"{winner} ИГРОК ПОБЕДИЛ!", True, (255, 255, 0))
        screen.blit(win_text, (width//2 - win_text.get_width()//2, height//2 - 50))
        
        restart_text = font.render("Нажми ПРОБЕЛ чтобы играть снова", True, (255, 255, 255))
        screen.blit(restart_text, (width//2 - restart_text.get_width()//2, height//2 + 50))
        
        final_text = font.render(f"{score_left} : {score_right}", True, (255, 255, 255))
        screen.blit(final_text, (width//2 - 30, height//2 + 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()