

# function that returns HTML text
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
    <h1 style="height: 49px;"><span style="color: #333399;">ColorSkate</span></h1>
    <p style="margin-top: -40px; height: 22px;"><span style="color: #333399;">controller
        webpage</span></p>
    <p>Current state: <strong>""" + current_state + """</strong></p>
    <p><a href="/?state=rainbow"><button class="button">rainbow</button></a></p>
    <p><a href="/?state=bounce"><button class="button">bounce</button></a></p>
    <p><a href="/?state=cycle"><button class="button">cycle</button></a></p>
    <p><a href="/?state=off"><button class="button button2">OFF</button></a></p>
  </body>
    </html>
    """
    return html


# ws2812b
import machine, neopixel, time
number_of_pixels = 20
rgb_pin = 14  # 14 = d5
np = neopixel.NeoPixel(machine.Pin(rgb_pin), number_of_pixels)

def clear():
  for i in range(number_of_pixels):
    np[i] = (0, 0, 0)
    np.write()

def set_color(r, g, b):
  for i in range(number_of_pixels):
    np[i] = (r, g, b)
  np.write()

def bounce(r, g, b, wait):
  for i in range(4 * number_of_pixels):
    for j in range(number_of_pixels):
      np[j] = (r, g, b)
    if (i // number_of_pixels) % 2 == 0:
      np[i % number_of_pixels] = (0, 0, 0)
    else:
        np[number_of_pixels - 1 - (i % number_of_pixels)] = (0,0,0)
#    else:
#      np[number_of_pixels – 1 – (i % number_of_pixels)] = (0, 0, 0)
    np.write()
    time.sleep_ms(wait)

def cycle(r, g, b, wait):
  for i in range(4 * number_of_pixels):
    for j in range(number_of_pixels):
      np[j] = (0, 0, 0)
    np[i % number_of_pixels] = (r, g, b)
    np.write()
    time.sleep_ms(wait)

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
        bounce(250, 0, 0, 100)
    if state_cycle == 6:
        print('CYCLE')
        current_state = 'CYCLE'
        cycle(250, 0, 0, 100)
    if state_off == 6:
        print('OFF')
        current_state = 'OFF'
        clear()
        time.sleep(0.5)

def TaskOne():
    while True:
        print('Task One')
        try:
            conn, addr = s.accept()  # conn = socket object, addr = client address
            print('Got a connection from %s' % str(addr))
            #conn.settimeout(2000)
            #conn.setblocking(0)

            request = conn.recv(1024)
            request = str(request)
            print('Content = %s' % request)
            state_rainbow = request.find('/?state=rainbow')
            state_off = request.find('/?state=off')

            response = web_page()
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()

        except:

            print('request failed')
            time.sleep(100)

        yield None

def TaskTwo():
    while True:
        print('Task Two')
        if state_rainbow == 6:
            print('RAINBOW')
            rainbow_cycle(10)
        if state_off == 6:
            print('OFF')
            clear()
        yield None

TaskQueue = [ TaskOne(), TaskTwo() ]

while True:
    # main loop here
    for task in TaskQueue:
        next(task)


while True:
    #try:
    conn, addr = s.accept()  # conn = socket object, addr = client address
    print('Got a connection from %s' % str(addr))
    conn.settimeout(2000)
    conn.setblocking(0)

    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    state_rainbow = request.find('/?state=rainbow')
    state_off = request.find('/?state=off')

    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

#    except:
#
#        print('request failed')
#
#        if state_rainbow == 6:
#            print('RAINBOW')
#            rainbow_cycle(10)
#        if state_off == 6:
#            print('OFF')
#            clear()
#
#        time.sleep(100)
