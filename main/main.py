

################################################################################
# function that returns HTML text
################################################################################
def web_page():

    current_state = 'OFF'

    html = """
    <html>
      <head>
        <title>ESP Web Server</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,">
        <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
             h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
             border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
             .button2{background-color: #4286f4;}
          </style>
      </head>
      <body>
        <h1 style="height: 65px; margin-top: 34.4333px;"><span style="color:#ff0000;">C</span><span

            style="color:#ff4000;">o</span><span style="color:#ff7f00;">l</span><span

            style="color:#ffbf00;">o</span><span style="color:#ffff00;">r</span><span

            style="color:#00ff00;">s</span><span style="color:#00ff80;">k</span><span

            style="color:#00ffff;">a</span><span style="color:#0080ff;">t</span><span

            style="color:#0000ff;">e</span></h1>
        <p style="margin-top: -40px; height: 22px;"><span style="color: #333399;">controller
            webpage</span></p>
        <p>Current state: <strong>""" + current_state + """</strong></p>
        <p><a href="/?state=rainbow"><button class="button">rainbow</button></a></p>
        <p><a href="/?state=bounce"><button class="button">bounce</button></a></p>
        <p><a href="/?state=cycle"><button class="button">cycle</button></a></p>
        <p><a href="/?state=glitch"><button class="button">glitch</button></a></p>
        <p><a href="/?state=woop"><button class="button">woop</button></a></p>
        <p><a href="/?state=traffic"><button class="button">traffic</button></a></p>

        <p><a href="/?state=off"><button class="button button2">OFF</button></a></p>
      </body>
      </html>
    """

    return html


################################################################################
# function to generate random numbers
################################################################################
def rand( floor, mod=0, negative = False):
    # return random value from -floor.mod to floor.nod if negative is True

    from os import urandom as rnd

    sign = 1 if ord(rnd(1))%10 > 5 else -1
    sign = sign if negative else 1

    if mod:
        value = float(('{}.{}').format(ord(rnd(1))%floor, ord(rnd(1))%mod))
    else:
        value = int(('{}').format(ord(rnd(1))%floor))

    return sign*value


################################################################################
# function to generate random colors
################################################################################
def rand_color():
    value = rand(255, 0, False)
    return wheel(value)
    
    # choice of random color
    r = rand(255, 0, False)
    g = rand(255, 0, False)
    b= rand(255, 0, False)
    color_tuple = (r,g,b)
    return color_tuple

def rand_color_from_list():
    color_list = [(255,255,255),
                  (255,0,0),
                  (0,255,0),
                  (0,0,255),
                  (255,255,0),
                  (0,255,255),
                  (255,0,255),
                  (128,0,0),
                  (128,128,0),
                  (0,128,0),
                  (128,0,128),
                  (0,128,128),
                  (0,0,128)]
    index = rand(len(color_list)-1, 0, False)
    return color_list[index]
                  


# ws2812b
import machine, neopixel, time
number_of_pixels = 20
rgb_pin = 14  # 14 = d5
np = neopixel.NeoPixel(machine.Pin(rgb_pin), number_of_pixels)

################################################################################
# function for turning off all number_of_pixels
################################################################################
def clear():
  for i in range(number_of_pixels):
    np[i] = (0, 0, 0)
    np.write()

################################################################################
# function for setting color of a pixel
################################################################################
def set_color(r, g, b):
  for i in range(number_of_pixels):
    np[i] = (r, g, b)
  np.write()

################################################################################
# ANIMATION - bounce of turned off pixels back and forth
################################################################################
def bounce(colors, wait):
  r = colors[0]
  g = colors[1]
  b = colors[2]

  for i in range(2 * number_of_pixels):
    for j in range(number_of_pixels):
      np[j] = (r, g, b)
    if (i // number_of_pixels) % 2 == 0:
      try:
        np[(i % number_of_pixels) - 1] = (r//3, g//3, b//3)
      except:
        pass
      try:
        np[(i % number_of_pixels) + 1] = (r//3, g//3, b//3)
      except:
        pass
      np[i % number_of_pixels] = (0, 0, 0)

    else:
        np[number_of_pixels - 1 - (i % number_of_pixels)] = (0,0,0)
        try:
            np[number_of_pixels - 1 - (i % number_of_pixels) - 1] = (r//3, g//3, b//3)
        except:
            pass
        try:
            np[number_of_pixels - 1 - (i % number_of_pixels) + 1] = (r//3, g//3, b//3)
        except:
            pass
            
    np.write()
    time.sleep_ms(wait)


################################################################################
# ANIMATION - cycle around of pixels
################################################################################
def cycle(colors, wait):
  r = colors[0]
  g = colors[1]
  b = colors[2]
  for i in range(number_of_pixels):
    for j in range(number_of_pixels):
      np[j] = (0, 0, 0)
    np[i % number_of_pixels] = (r, g, b)
    
    try:
        np[i % number_of_pixels+1] = (r, g, b)
    except:
        pass
    try:
        np[i % number_of_pixels-1] = (r, g, b)
    except:
        pass

    np.write()
    time.sleep_ms(wait)

################################################################################
# ANIMATION - all random colors
################################################################################
def glitch(wait):
    for i in range(number_of_pixels):
        for j in range(number_of_pixels):
            colors = rand_color()
            r = colors[0]
            g = colors[1]
            b = colors[2]
            np[j] = (r, g, b)
        np.write()
        time.sleep_ms(wait)

################################################################################
# ANIMATION - rainbow colors
################################################################################
def wheel(pos):
  # Input a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
  for j in range(255):
    for i in range(number_of_pixels):
      rc_index = (i * 256 // number_of_pixels) + j
      np[i] = wheel(rc_index & 255)
    np.write()
    time.sleep_ms(wait)
    
################################################################################
# ANIMATION - police lights
################################################################################
def woop(wait):
    for i in range(number_of_pixels):
        for j in range(number_of_pixels):
            np[j] = (0,0,0)
        np[(i-2) % number_of_pixels] = (255,0,0)
        np[(i-1) % number_of_pixels] = (255,0,0)
        np[i] = (255,0,0)
        np[(i+1) % number_of_pixels] = (255,0,0)
        np[(i+2) % number_of_pixels] = (255,0,0)
        
        np[(i + number_of_pixels//2 - 2) % number_of_pixels] = (0,0,255)
        np[(i + number_of_pixels//2 - 1) % number_of_pixels] = (0,0,255)
        np[(i + number_of_pixels//2) % number_of_pixels] = (0,0,255)
        np[(i + number_of_pixels//2 + 1) % number_of_pixels] = (0,0,255)
        np[(i + number_of_pixels//2 + 2) % number_of_pixels] = (0,0,255)
        np.write()
        time.sleep_ms(wait)

################################################################################
# ANIMATION - traffic
################################################################################
def traffic():
    np[0] = (255,0,0)
    np[1] = (255,0,0)
    np[2] = (255,0,0)
    
    np[7] = (255,255,255)
    np[8] = (255,255,255)
    np[9] = (255,255,255)
    np[10] = (255,255,255)
    np[11] = (255,255,255)
    np[12] = (255,255,255)
    
    np[17] = (255,0,0)
    np[18] = (255,0,0)
    np[19] = (255,0,0)
    
    np.write()




import select
# specification of socket type
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind socket to an address
s.bind(('',80))  # '' = localhost
# listen to connections, max 5
s.listen(5)

state_rainbow = 0
state_bounce = 0
state_cycle = 0
state_glitch = 0
state_woop = 0
state_traffic = 0
state_off = 0

readable = [s]
i = 0


while True:
     # r will be a list of sockets with readable data
    r,w,e = select.select(readable,[],[],0)
    for rs in r: # iterate through readable sockets
        if rs is s: # is it the server
            c,a = s.accept()
            print('\r{}:'.format(a),'connected')
            readable.append(c) # add the client

        else:
            # read from a client
            data = rs.recv(1024)
            if not data:
                print('disconnected')
                readable.remove(rs)
                rs.close()
            else:
                try:
                    request = str(data)
                    print('Content = %s' % request)
                    state_rainbow = request.find('/?state=rainbow')
                    state_bounce = request.find('/?state=bounce')
                    state_cycle = request.find('/?state=cycle')
                    state_glitch = request.find('/?state=glitch')
                    state_woop = request.find('/?state=woop')
                    state_traffic = request.find('/?state=traffic')
                    state_off = request.find('/?state=off')

                    response = web_page()
                    rs.send('HTTP/1.1 200 OK\n')
                    rs.send('Content-Type: text/html\n')
                    rs.send('Connection: close\n\n')
                    rs.sendall(response)
                    rs.close()
                except:
                    print('failed request')


    if state_rainbow == 6:
        print('RAINBOW')
        current_state = 'RAINBOW'
        rainbow_cycle(10)
    if state_bounce == 6:
        print('BOUNCE')
        current_state = 'BOUNCE'
        colors = rand_color()
        bounce(colors, 100)
    if state_cycle == 6:
        print('CYCLE')
        current_state = 'CYCLE'
        colors = rand_color()
        cycle(colors, 30)
    if state_glitch == 6:
        print('GLITCH')
        current_state = 'GLITCH'
        glitch(25)
    if state_woop == 6:
        print('WOOP')
        current_state = 'WOOP'
        woop(30)
    if state_traffic == 6:
        print('TRAFFIC')
        current_state = 'TRAFFIC'
        traffic()
    if state_off == 6:
        print('OFF')
        current_state = 'OFF'
        clear()
        time.sleep(0.5)

