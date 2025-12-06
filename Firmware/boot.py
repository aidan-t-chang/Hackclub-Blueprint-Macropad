# boot.py for KMK Macropad
# This file runs when the device boots up

import storage
import usb_cdc
import usb_hid

# Enable USB HID for keyboard functionality
usb_hid.enable(
    (usb_hid.Device.KEYBOARD,)
)

# Optional: Enable USB CDC (serial communication) for debugging
# Uncomment the line below if you want serial debugging
# usb_cdc.enable(console=True, data=True)

# Optional: Disable USB mass storage if you don't need file access
# Uncomment the line below to disable mass storage
# storage.disable_usb_drive()

print("KMK Macropad boot complete!")