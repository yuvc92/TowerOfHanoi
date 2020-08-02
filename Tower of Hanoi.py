import pygame, sys, time

pygame.init()
display = pygame.display.set_mode((1280, 720))    #window size
clock = pygame.time.Clock()                     #clock declaration

game_done = False                     #variable to check if game is complete
framerate = 30                     # 30 fps or refresh rate

steps = 0
n_disks = 3
disks = []
towers = [320, 640, 960]
pointing_at = 0
floating = False
floater = 0
arr = []
min_steps = -1
#order = []

# colors:
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gold = (239, 229, 51)
blue = (78, 162, 196)
grey = (170, 170, 170)
green = (77, 206, 145)
brown = ()

def TowerOfHanoi(n , source, destination, auxilliary, arr):
    if n==1:
        list1 = [1,source,destination]
        arr.append(list1)
        return
    TowerOfHanoi(n-1, source, auxilliary, destination,arr)
    list2 = [n,source,destination]
    arr.append(list2)
    TowerOfHanoi(n-1, auxilliary, destination, source, arr)

def print_out(display, text, center, font_name, size, color):#changes made
    font = pygame.font.SysFont(font_name, size)
    font_text = font.render(text, True, color)
    font_box = font_text.get_rect()
    font_box.midtop = center
    display.blit(font_text, font_box)

def menu_display():  # to be called before starting actual game loop
    global display, n_disks, game_done
    menu_done = False
    while not menu_done:  # every display/scene/level has its own loop
        display.fill(black)
        print_out(display, 'This illustration shows you how to complete the', (640, 80), font_name='sans serif', size=60, color=grey)
        print_out(display,'Towers of Hanoi game in minimum number of steps.',(640, 180), font_name='sans serif', size=60, color=grey)
        print_out(display, 'Press up or down to select number of disks.', (640, 280), font_name='sans serif', size=60,color=grey)
        print_out(display, str(n_disks), (640, 480), font_name='sans serif', size=200, color=grey)
        #print_out(display, 'Press ENTER to continue', (320, 320), font_name='sans_serif', size=30, color=black)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_UP and n_disks < 8:
                    n_disks += 1
                if event.key == pygame.K_DOWN and n_disks > 2:
                    n_disks -= 1
                if event.key == pygame.K_RETURN:
                    menu_done = True
            if event.type == pygame.QUIT:
                menu_done = True
                game_done = True
        pygame.display.flip()
        clock.tick(framerate)


def game_over():  # game over display
    global display, steps
    display.fill(black)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()


def draw_towers():
    global display
    for xpos in range(320-80, 960+1, 320):    #40, 460+1, 200
        pygame.draw.rect(display, grey, pygame.Rect(xpos, 600, 160, 20))
        pygame.draw.rect(display, grey, pygame.Rect(xpos + 75, 400, 10, 200))
    print_out(display, 'A', (towers[0], 600), font_name='mono', size=20, color=black)
    print_out(display, 'B', (towers[1], 600), font_name='mono', size=20, color=black)
    print_out(display, 'C', (towers[2], 600), font_name='mono', size=20, color=black)


def make_disks():
    global n_disks, disks
    disks = []
    height = 20
    ypos = 597 - height     #397
    width = n_disks * 23
    for i in range(n_disks):
        disk = {}
        disk['rect'] = pygame.Rect(0, 0, width, height)
        disk['rect'].midtop = (320, ypos)
        disk['val'] = n_disks - i
        disk['tower'] = 0
        disks.append(disk)
        ypos -= height + 3
        width -= 23


def draw_disks():
    global display, disks
    for disk in disks:
        pygame.draw.rect(display, gold, disk['rect'])
        print_out(display, str(disk['val']), disk['rect'].midtop, font_name='mono', size=20, color=black)
    return


def draw_ptr():
    ptr_points = [(towers[pointing_at] - 7, 640), (towers[pointing_at] + 7, 640),
                  (towers[pointing_at], 633)] #440, 440, 433
    pygame.draw.polygon(display, red, ptr_points)
    return


def check_won():
    global disks
    over = True
    for disk in disks:
        if disk['tower'] != 2:
            over = False
    if over:
        time.sleep(0.2)
        game_over()


def reset():
    global steps, pointing_at, floating, floater
    steps = 0
    pointing_at = 0
    floating = False
    floater = 0
    menu_display()
    make_disks()


menu_display()
make_disks()
TowerOfHanoi(n_disks,'A', 'C', 'B', arr) ##########
# main game loop:
while not game_done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                min_steps += 1
            if event.key == pygame.K_ESCAPE:
                reset()
            if event.key == pygame.K_q:
                game_done = True
            if event.key == pygame.K_RIGHT:
                pointing_at = (pointing_at + 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers[pointing_at], 300) #300
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_LEFT:
                pointing_at = (pointing_at - 1) % 3
                if floating:
                    disks[floater]['rect'].midtop = (towers[pointing_at], 300) #500
                    disks[floater]['tower'] = pointing_at
            if event.key == pygame.K_UP and not floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at:
                        floating = True
                        floater = disks.index(disk)
                        disk['rect'].midtop = (towers[pointing_at], 300)
                        break
            if event.key == pygame.K_DOWN and floating:
                for disk in disks[::-1]:
                    if disk['tower'] == pointing_at and disks.index(disk) != floater:
                        if disk['val'] > disks[floater]['val']:
                            floating = False
                            disks[floater]['rect'].midtop = (towers[pointing_at], disk['rect'].top - 23) #+200
                            steps += 1
                        break
                else:
                    floating = False
                    disks[floater]['rect'].midtop = (towers[pointing_at], 400 - 23+200)
                    steps += 1
    display.fill(black)
    if(min_steps == 0):
        print_out(display, "To move all disks from A to C we move first ",(640,200), font_name='sans serif', size=40, color=white)
        print_out(display, str(n_disks-1)+" disks from A to B, then the last one  " ,(640,250), font_name='sans serif', size=40, color=white)
        print_out(display, str(n_disks-1)+"",(640,200), font_name='sans serif', size=60, color=white)
    if (min_steps > 0 and min_steps <= 2**n_disks):
        print_out(display, 'Move ' + str(arr[min_steps-1][0]) + ' from '+ str(arr[min_steps-1][1]) + ' to '+ str(arr[min_steps-1][2]), (640, 200), font_name='sans serif', size=60, color=white)
    draw_towers()
    draw_disks()
    draw_ptr()
    print_out(display,"Press SPACE for help", (240, 100), font_name='mono', size=30, color=white)
    print_out(display, 'Steps: ' + str(steps), (640, 100), font_name='mono', size=60, color=white)
    pygame.display.flip()
    if not floating: check_won()
    clock.tick(framerate)