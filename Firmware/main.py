import board
import busio
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_ssd1306
import rotaryio
import digitalio

# firmware is not the most polished, but want to get it done to submit macropad :)
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.keypad import KeysScanner
from kmk.keys import KC
from kmk.modules.macros import Press, Release, Tap, Macros
from kmk.modules.encoder import EncoderHandler

keyboard = KMKKeyboard()

# Initialize modules
macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)

# OLED Display Setup
displayio.release_displays()
i2c = busio.I2C(scl=board.GP5, sda=board.GP4)  # Adjust pins as needed
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

# Create display group
splash = displayio.Group()
display.show(splash)

# Add text to display
text = "KMK Macropad"
text_area = label.Label(terminalio.FONT, text=text, color=0xFFFFFF, x=10, y=15)
splash.append(text_area)

status_text = label.Label(terminalio.FONT, text="Ready", color=0xFFFFFF, x=10, y=35)
splash.append(status_text)

# Rotary Encoder Setup (adjust pins as needed)
encoder = rotaryio.IncrementalEncoder(board.GP2, board.GP3)
encoder_button = digitalio.DigitalInOut(board.GP1)
encoder_button.direction = digitalio.Direction.INPUT
encoder_button.pull = digitalio.Pull.UP

# Define switch pins (4 switches)
SWITCH_PINS = [board.GP26, board.GP27, board.GP28, board.GP29]

# Tell kmk we are not using a key matrix
keyboard.matrix = KeysScanner(
    pins=SWITCH_PINS,
    value_when_pressed=False,
)

# Setup encoder
keyboard.encoder_handler.pins = ((board.GP2, board.GP3, board.GP1, False),)

# Define macros for common tasks
DISCORD_MUTE = KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.M), Release(KC.LCTRL, KC.LSHIFT, KC.M))
TEAMS_MUTE = KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.M), Release(KC.LCTRL, KC.LSHIFT, KC.M))
SCREENSHOT = KC.MACRO(Press(KC.LGUI, KC.LSHIFT, KC.S), Release(KC.LGUI, KC.LSHIFT, KC.S))
TASK_MANAGER = KC.MACRO(Press(KC.LCTRL, KC.LSHIFT, KC.ESC), Release(KC.LCTRL, KC.LSHIFT, KC.ESC))

# Keymap for 4 switches + encoder
# Switch layout: [SW1, SW2, SW3, SW4, ENCODER_CCW, ENCODER_CW, ENCODER_PRESS]
keyboard.keymap = [
    [
        DISCORD_MUTE,      # Switch 1: Discord mute/unmute
        TEAMS_MUTE,        # Switch 2: Teams mute/unmute  
        SCREENSHOT,        # Switch 3: Screenshot
        TASK_MANAGER,      # Switch 4: Task Manager
        KC.AUDIO_VOL_DOWN, # Encoder counter-clockwise: Volume down
        KC.AUDIO_VOL_UP,   # Encoder clockwise: Volume up
        KC.AUDIO_MUTE,     # Encoder press: Mute toggle
    ]
]

# Function to update display
def update_display(action):
    status_text.text = action
    display.show(splash)

# Custom key handling for display updates
class CustomKeyboard(KMKKeyboard):
    def __init__(self):
        super().__init__()
        self.last_encoder_value = 0
        
    def during_bootup(self):
        super().during_bootup()
        self.last_encoder_value = encoder.position
        
    def before_matrix_scan(self):
        super().before_matrix_scan()
        
        # Check encoder rotation
        current_encoder_value = encoder.position
        if current_encoder_value != self.last_encoder_value:
            if current_encoder_value > self.last_encoder_value:
                update_display("Vol Up")
            else:
                update_display("Vol Down")
            self.last_encoder_value = current_encoder_value
        
        # Check encoder button
        if not encoder_button.value:  # Button pressed (active low)
            update_display("Mute")
            
    def after_hid_send(self, sandbox):
        super().after_hid_send(sandbox)
        # Update display based on last pressed key
        if hasattr(sandbox, 'active_keys') and sandbox.active_keys:
            key = sandbox.active_keys[-1]
            if key == DISCORD_MUTE:
                update_display("Discord")
            elif key == TEAMS_MUTE:
                update_display("Teams")
            elif key == SCREENSHOT:
                update_display("Screenshot")
            elif key == TASK_MANAGER:
                update_display("Task Mgr")

# Replace the keyboard instance
keyboard = CustomKeyboard()

# Re-initialize modules for custom keyboard
macros = Macros()
encoder_handler = EncoderHandler()

keyboard.modules.append(macros)
keyboard.modules.append(encoder_handler)

# Re-setup the matrix and encoder
keyboard.matrix = KeysScanner(
    pins=SWITCH_PINS,
    value_when_pressed=False,
)

keyboard.encoder_handler.pins = ((board.GP2, board.GP3, board.GP1, False),)

# Start kmk!
if __name__ == '__main__':
    keyboard.go()