import stamp_round_carrier_board as board
import time
import neopixel

import mfrc522

# Update this to match the number of NeoPixel LEDs connected to your board.
# The Stamp Round Carrier has 16 NeoPixel LEDs in the ring.
num_pixels = 16
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, auto_write=False)
pixels.brightness = 1.0

CLEAR = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

# Pattern to display for each card UID
# Colours go clockwise starting at left of USB connector

# You will need to replace the card UIDs with the UIDs of your cards

moods = {
    '0xb3aebba9': [CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, ],
    '0x23ae73a9': [RED, RED, RED, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, CLEAR, RED, RED, RED],
    '0xf334aaa9': [CLEAR, YELLOW, YELLOW, CLEAR, CLEAR, YELLOW, YELLOW, CLEAR, CLEAR, YELLOW, YELLOW, CLEAR, CLEAR, YELLOW, YELLOW, CLEAR],
    '0xc34219aa': [BLUE, BLUE, BLUE, BLUE, PURPLE, CYAN, CYAN, PURPLE, BLUE, BLUE, BLUE, BLUE, PURPLE, CYAN, CYAN, PURPLE]
    
    }

pixels.fill(CLEAR)
pixels.show()

rdr = mfrc522.MFRC522(board.SCK, board.MOSI, board.MISO, board.D26, board.SDA)
rdr.set_antenna_gain(0x07 << 4)

print('')
print("Place card before reader to read from address 0x08")
print('')

try:
    while True:

        (stat, tag_type) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:

            (stat, raw_uid) = rdr.anticoll()

            if stat == rdr.OK:
                print("New card detected")
                print("  - tag type: 0x%02x" % tag_type)
                print("  - uid\t : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
                print('')
                
                uid = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                if uid in moods:
                    pixels.fill(CLEAR)
                    for i in range(num_pixels):
                        pixels[i] = moods[uid][i]
                        
                    pixels.show()
                else:
                    print("Unknown card: %s" % uid)

except KeyboardInterrupt:
    print("Bye")
