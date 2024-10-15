import vgamepad as vg
import time
from pynput import mouse, keyboard

gamepad = vg.VX360Gamepad()

joystick_x = 0

sensitivity = 200 

gamepad_active = True
space_pressed = False

previous_x = None

def on_move(x, y):
    global joystick_x, previous_x
    
    if gamepad_active and previous_x is not None:
        delta_x = x - previous_x
        
        joystick_x += delta_x * sensitivity
    
        joystick_x = max(min(joystick_x, 32767), -32767)
        
        print(f"Mouse Delta X: {delta_x}, Joystick X Position: {joystick_x}")
    
    previous_x = x

def update_joystick_position():
    if gamepad_active:
        gamepad.left_joystick(x_value=int(joystick_x), y_value=0)
        
        if space_pressed:
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
        else:
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.left_joystick(x_value=0, y_value=0)

def keep_alive_gamepad():
    while True:
        update_joystick_position()

        if gamepad_active:
            gamepad.right_joystick(x_value=0, y_value=0)  
            gamepad.right_trigger(value=0)  
            gamepad.left_trigger(value=0)  
            
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
            gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        
        gamepad.update()
        
        time.sleep(0.01)

def on_press(key):
    global gamepad_active, space_pressed
    
    if key == keyboard.Key.space:
        space_pressed = True
        
    if key == keyboard.Key.end:
        gamepad_active = not gamepad_active
        print(f"Gamepad {'Activated' if gamepad_active else 'Deactivated'}")

def on_release(key):
    global space_pressed
    
    if key == keyboard.Key.space:
        space_pressed = False

mouse_listener = mouse.Listener(on_move=on_move)
mouse_listener.start()

keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

keep_alive_gamepad()
