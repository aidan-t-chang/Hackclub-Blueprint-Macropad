# KMK Macropad Configuration
# Pin assignments and hardware configuration

# Switch Pins (4 mechanical switches)
SWITCH_PINS = {
    'SW1': 'GP26',  # Discord mute/unmute
    'SW2': 'GP27',  # Teams mute/unmute
    'SW3': 'GP28',  # Screenshot
    'SW4': 'GP29',  # Task Manager
}

# Rotary Encoder Pins
ENCODER_PINS = {
    'CLK': 'GP2',   # Encoder clock pin
    'DT': 'GP3',    # Encoder data pin
    'SW': 'GP1',    # Encoder switch pin
}

# OLED Display Pins (I2C)
OLED_PINS = {
    'SCL': 'GP5',   # I2C Clock
    'SDA': 'GP4',   # I2C Data
    'Address': '0x3C'  # I2C Address
}

# Display Settings
DISPLAY_CONFIG = {
    'WIDTH': 128,
    'HEIGHT': 64,
    'TITLE': 'KMK Macropad',
    'FONT': 'terminalio.FONT'
}

# Key Functions
KEY_FUNCTIONS = {
    'SW1': 'Discord Mute Toggle (Ctrl+Shift+M)',
    'SW2': 'Teams Mute Toggle (Ctrl+Shift+M)', 
    'SW3': 'Screenshot (Win+Shift+S)',
    'SW4': 'Task Manager (Ctrl+Shift+Esc)',
    'ENCODER_CCW': 'Volume Down',
    'ENCODER_CW': 'Volume Up',
    'ENCODER_PRESS': 'Mute Toggle'
}

# Hardware Notes
"""
Hardware Requirements:
- Raspberry Pi Pico or compatible RP2040 board
- 4x mechanical switches (Cherry MX compatible)
- 1x rotary encoder with push button
- 1x SSD1306 OLED display (128x64, I2C)
- Pull-up resistors for switches (if not built into board)

Wiring:
- Connect switches between their respective GPIO pins and ground
- Connect encoder CLK to GP2, DT to GP3, SW to GP1
- Connect OLED SCL to GP5, SDA to GP4, VCC to 3.3V, GND to GND
- Ensure proper power supply (USB or external 5V/3.3V)

Software Requirements:
- CircuitPython 8.0+
- KMK Firmware
- Adafruit CircuitPython libraries:
  - adafruit_displayio_ssd1306
  - adafruit_display_text
"""