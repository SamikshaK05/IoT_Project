import ILI9341
import network
import urequests
import time
from machine import Pin, PWM

# ================= TFT LCD PINS =================
LCD_RD  = 2
LCD_WR  = 4
LCD_RST = 5
LCD_RS  = 32
LCD_CS  = 33
LCD_D0 = 12
LCD_D1 = 13
LCD_D2 = 14
LCD_D3 = 15
LCD_D4 = 18
LCD_D5 = 19
LCD_D6 = 21
LCD_D7 = 22

# ================= INITIALIZE TFT =================
tft = ILI9341.screen(
    LCD_RD, LCD_WR, LCD_RS,
    LCD_CS, LCD_RST,
    LCD_D0, LCD_D1, LCD_D2, LCD_D3,
    LCD_D4, LCD_D5, LCD_D6, LCD_D7
)
tft.begin()
tft.setrotation(1)
tft.fillscreen(0x0000)

# ================= LARGE FONT CLASS =================
class LargeText:
    FONT = { 
        # Uppercase
        'A':[0x7E,0x09,0x09,0x09,0x7E], 'B':[0x7F,0x49,0x49,0x49,0x36],
        'C':[0x3E,0x41,0x41,0x41,0x22], 'D':[0x7F,0x41,0x41,0x41,0x3E],
        'E':[0x7F,0x49,0x49,0x49,0x41], 'F':[0x7F,0x09,0x09,0x09,0x01],
        'G':[0x3E,0x41,0x49,0x49,0x2E], 'H':[0x7F,0x08,0x08,0x08,0x7F],
        'I':[0x00,0x41,0x7F,0x41,0x00], 'J':[0x20,0x40,0x41,0x3F,0x01],
        'K':[0x7F,0x08,0x14,0x22,0x41], 'L':[0x7F,0x40,0x40,0x40,0x40],
        'M':[0x7F,0x02,0x04,0x02,0x7F], 'N':[0x7F,0x02,0x04,0x08,0x7F],
        'O':[0x3E,0x41,0x41,0x41,0x3E], 'P':[0x7F,0x09,0x09,0x09,0x06],
        'Q':[0x3E,0x41,0x51,0x21,0x5E], 'R':[0x7F,0x09,0x19,0x29,0x46],
        'S':[0x46,0x49,0x49,0x49,0x31], 'T':[0x01,0x01,0x7F,0x01,0x01],
        'U':[0x3F,0x40,0x40,0x40,0x3F], 'V':[0x1F,0x20,0x40,0x20,0x1F],
        'W':[0x7F,0x20,0x10,0x20,0x7F], 'X':[0x63,0x14,0x08,0x14,0x63],
        'Y':[0x07,0x08,0x70,0x08,0x07], 'Z':[0x61,0x51,0x49,0x45,0x43],
        # Lowercase
        'a':[0x20,0x54,0x54,0x54,0x78], 'b':[0x7F,0x48,0x44,0x44,0x38],
        'c':[0x38,0x44,0x44,0x44,0x20], 'd':[0x38,0x44,0x44,0x44,0x7F],
        'e':[0x38,0x54,0x54,0x54,0x18], 'f':[0x08,0x7E,0x09,0x01,0x02],
        'g':[0x0C,0x52,0x52,0x52,0x3E], 'h':[0x7F,0x08,0x04,0x04,0x78],
        'i':[0x00,0x44,0x7D,0x40,0x00], 'j':[0x20,0x40,0x44,0x3D,0x00],
        'k':[0x7F,0x10,0x28,0x44,0x00], 'l':[0x00,0x41,0x7F,0x40,0x00],
        'm':[0x7C,0x04,0x18,0x04,0x78], 'n':[0x7C,0x08,0x04,0x04,0x78],
        'o':[0x38,0x44,0x44,0x44,0x38], 'p':[0x7C,0x14,0x14,0x14,0x08],
        'q':[0x08,0x14,0x14,0x14,0x7C], 'r':[0x7C,0x08,0x04,0x04,0x08],
        's':[0x48,0x54,0x54,0x54,0x20], 't':[0x04,0x3F,0x44,0x40,0x20],
        'u':[0x3C,0x40,0x40,0x20,0x7C], 'v':[0x1C,0x20,0x40,0x20,0x1C],
        'w':[0x3C,0x40,0x30,0x40,0x3C], 'x':[0x44,0x28,0x10,0x28,0x44],
        'y':[0x0C,0x50,0x50,0x50,0x3C], 'z':[0x44,0x64,0x54,0x4C,0x44],
        # Numbers
        '0':[0x3E,0x45,0x49,0x51,0x3E], '1':[0x00,0x41,0x7F,0x40,0x00],
        '2':[0x42,0x61,0x51,0x49,0x46], '3':[0x21,0x41,0x45,0x4B,0x31],
        '4':[0x18,0x14,0x12,0x7F,0x10], '5':[0x27,0x45,0x45,0x45,0x39],
        '6':[0x3C,0x4A,0x49,0x49,0x30], '7':[0x01,0x71,0x09,0x05,0x03],
        '8':[0x36,0x49,0x49,0x49,0x36], '9':[0x06,0x49,0x49,0x29,0x1E],
        # Extra symbols
        ' ':[0x00,0x00,0x00,0x00,0x00], ':':[0x00,0x36,0x36,0x00,0x00],
        '-':[0x08,0x08,0x08,0x08,0x08], '.':[0x00,0x60,0x60,0x00,0x00]        
    }

    def __init__(self, tft, scale=2, color=0xFFFF):
        self.tft = tft
        self.scale = scale
        self.color = color

    def draw_char(self, x, y, ch):
        glyph = self.FONT.get(ch, self.FONT[' '])
        for col in range(5):
            line = glyph[col]
            for row in range(7):
                if line & 1:
                    for dx in range(self.scale):
                        for dy in range(self.scale):
                            self.tft.drawPixel(x + col*self.scale + dx, y + row*self.scale + dy, self.color)
                line >>= 1

    def print(self, x, y, text, clear_width=None):
        width = clear_width if clear_width else len(text)*6*self.scale
        self.tft.fillRect(x, y, width, 7*self.scale, 0x0000)
        for ch in text:
            self.draw_char(x, y, ch)
            x += (5*self.scale + self.scale)

# ================== INITIALIZE ==================
txt = LargeText(tft)
txt.print(10, 20, "IRS SYSTEM READY")

servo1 = PWM(Pin(26), freq=50)
servo2 = PWM(Pin(27), freq=50)

red = Pin(25, Pin.OUT)
blue = Pin(23, Pin.OUT)


def move_servos(angle):
    duty = int((angle / 180) * 102 + 26)
    servo1.duty(duty)
    servo2.duty(duty)
    time.sleep(0.8)
    servo1.duty(0)
    servo2.duty(0)

def set_rgb(red_state, blue_state):
    red.value(red_state)
    blue.value(blue_state)
    
    

# ================== WIFI ==================
SSID = "Samiksha"
PASSWORD = "samysays"
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
print("Connecting to WiFi...")
if not wifi.isconnected():
    wifi.connect(SSID, PASSWORD)
    start = time.time()
    while not wifi.isconnected():
        time.sleep(1)
        if time.time() - start > 15:
            print("WiFi connection timeout!")
            break
print("WiFi IP:", wifi.ifconfig())

# ================== THINGSPEAK ==================
CHANNEL_ID = "3232555"
READ_API_KEY = "O5ISQ8GA969Z01WG"
url = f"http://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=1"

# ================== MAIN LOOP ==================
while True:
    try:
        response = urequests.get(url, timeout=10)
        data = response.json()
        response.close()

        if data and "feeds" in data and len(data["feeds"]) > 0:
            latest = data["feeds"][-1]
            rssi = latest.get("field1")
            if rssi is not None:
                rssi_val = int(float(rssi))

                # ---------- SIGNAL LOGIC ----------
                if -100 <= rssi_val <= -70:
                    angle = int(((rssi_val + 100) / 30) * 180)
                    angle = max(0, min(180, angle))
                    move_servos(angle)
                    set_rgb(1, 0)
                    led_status = "RED"
                    signal_text = "SIGNAL LOW"
                else:
                    servo1.duty(0)
                    servo2.duty(0)
                    set_rgb(0, 0)
                    led_status = "GREEN"
                    signal_text = "SIGNAL OK"

                # ---------- TFT DISPLAY ----------
                txt.print(10, 50, f"{signal_text}  RSSI:{rssi_val}", clear_width=200)
                txt.print(10, 70, f"LED STATUS: {led_status}", clear_width=200)
            else:
                txt.print(10, 50, "NO RSSI VALUE", clear_width=200)
                txt.print(10, 70, "LED STATUS: UNKNOWN", clear_width=200)
        else:
            txt.print(10, 50, "NO DATA", clear_width=200)
            txt.print(10, 70, "LED STATUS: UNKNOWN", clear_width=200)

    except Exception as e:
        txt.print(10, 50, "ERROR", clear_width=200)
        txt.print(10, 70, str(e)[:20], clear_width=200)

    time.sleep(15)
