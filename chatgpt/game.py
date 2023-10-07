import keyboard
import time

def game():
    start_time = time.time()
    score = 0
    
    while True:
        if keyboard.is_pressed('space'):
            score += 0.02
            print(f"Score: {score}")
        
        if time.time() - start_time >= 5:
            break
    
    print("Game Over")
    print(f"Final Score: {score}")

game()