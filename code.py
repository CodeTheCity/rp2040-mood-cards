import stamp_round_carrier_board as board
import time
import neopixel

import mfrc522

# Update this to match the number of NeoPixel LEDs connected to your board.
num_pixels = 16
pixels = neopixel.NeoPixel(board.NEOPIXEL, num_pixels, auto_write=False)
pixels.brightness = 0.5

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

pixels.fill(RED)
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

                if rdr.select_tag(raw_uid) == rdr.OK:

                    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

                    if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
                        print("Address 8 data: %s" % rdr.read(8))
                        rdr.stop_crypto1()
                        
                        for i in range(num_pixels):
                            pixels[i] = (0, 0, 0)
                        for i in range(0, 8):
                            pixles[i] = GREEN
                            
                        pixles.show()
                    else:
                        print("Authentication error")
                else:
                    print("Failed to select tag")

except KeyboardInterrupt:
    print("Bye")
