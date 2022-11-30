
from tkinter import *
import random
#mozgatás
def key_pressed(event):
    global left_pressed, right_pressed
    if lives <= 0:
        return
    if event.keysym == 'Left':
        left_pressed = True
    if event.keysym == 'Right':
        right_pressed = True
    if event.char == ' ':
        pako_coords = canvas.coords(pako)
        position_x = pako_coords[0] - 10
        position_y = pako_coords[1] - 50
        bullet = canvas.create_oval(
            position_x,
            position_y,
            position_x + 20,
            position_y + 20,
            width=3,
            outline='black',
            fill='yellow'
        )
        bullets.append(bullet)

def key_released(event):
    global left_pressed, right_pressed
    if event.keysym == 'Left':
        left_pressed = False
    if event.keysym == 'Right':
        right_pressed = False

def play():
    global counter, lives, score

    # move pako
    pako_coords = canvas.coords(pako)
    if left_pressed and pako_coords[0] > 0:
        canvas.move(pako, -1, 0)
    if right_pressed and pako_coords[0] < 1200:
        canvas.move(pako, 1, 0)

    # gyapot mozgatása
    deleted_bullets = []
    for bullet in bullets:
        if canvas.coords(bullet)[1] > 0:
            canvas.move(bullet, 0, -1)
        else:
            canvas.delete(bullet)
            deleted_bullets.append(bullet)
    for deleted_bullet in deleted_bullets:
        bullets.remove(deleted_bullet)

    # gyapot mozgatasa
    gyapots_to_delete = []
    bullets_to_delete = []
    for gyapot_struct in gyapots:
        gyapot = gyapot_struct['gyapot']
        gyapot_coords = canvas.coords(gyapot)
        for bullet in bullets:
            bullet_coords = canvas.coords(bullet)
            coord_diff_x = abs(bullet_coords[0] - gyapot_coords[0])
            coord_diff_y = abs(bullet_coords[1] - gyapot_coords[1])
            if coord_diff_x < 20 and coord_diff_y < 20:
                gyapots_to_delete.append(gyapot_struct)
                bullets_to_delete.append(bullet)
                score = score + 1
                score_nr_label['text'] = str(score)
    for gyapot_to_delete in gyapots_to_delete:
        canvas.delete(gyapot_to_delete['gyapot'])
        gyapots.remove(gyapot_to_delete)
    for bullet_to_delete in bullets_to_delete:
        canvas.delete(bullet_to_delete)
        bullets.remove(bullet_to_delete)

      # gyapot letrehozasa
    counter = counter + 1
    if counter % 100 == 0:
        gyapot = canvas.create_image(random.randint(0, 1200), 0, image=gyapot_image)
        direction = random.randint(-2, 2)
        gyapot_struct = {
            'gyapot': gyapot,
            'direction': direction,
        }
        gyapots.append(gyapot_struct)

    # gyapot utes ellenorzes
    deleted_gyapots = []
    hit = False
    for gyapot_struct in gyapots:
        gyapot = gyapot_struct['gyapot']
        direction = gyapot_struct['direction']
        gyapot_coords = canvas.coords(gyapot)
        if gyapot_coords[1] < 1000:
            if direction == 0:
                canvas.move(gyapot, 0, 1)
            elif abs(direction) == 1:
                canvas.move(gyapot, direction/3, 0.95)
            else:
                canvas.move(gyapot, direction/3, 0.75)
        else:
            canvas.delete(gyapot)
            deleted_gyapots.append(gyapot_struct)
        coord_diff_x = abs(gyapot_coords[0] - pako_coords[0])
        coord_diff_y = abs(gyapot_coords[1] - pako_coords[1])
        if coord_diff_x <= 40 and coord_diff_y <= 40:
            hit = True
            lives = lives - 1
            lives_nr_label['text'] = str(lives)
    for deleted_gyapot in deleted_gyapots:
        gyapots.remove(deleted_gyapot)
    if hit:
        for gyapot_struct in gyapots:
            canvas.delete(gyapot_struct['gyapot'])
        gyapots.clear()
        for bullet in bullets:
            canvas.delete(bullet)
        bullets.clear()

    # vege ellenorzes
    if lives <= 0:
        restart_button['state'] = 'active'
        canvas.itemconfigure(end_text, state='normal')
    else:
        root.after(2, play)

def init(first_run=False):
    global lives, score, counter, left_pressed, right_pressed, gyapots, bullets
    if not first_run:
        for gyapot_struct in gyapots:
            canvas.delete(gyapot_struct['gyapot'])
        for bullet in bullets:
            canvas.delete(bullet)
        pako_coords = canvas.coords(pako)
        canvas.move(pako, 240 - pako_coords[0], 310 - pako_coords[1])
    lives = 2
    score = 0
    counter = 0
    left_pressed = False
    right_pressed = False
    gyapots = []
    bullets = []
    lives_nr_label['text'] = str(lives)
    score_nr_label['text'] = str(score)
    restart_button['state'] = 'disabled'
    canvas.itemconfigure(end_text, state='hidden')
    root.after(2, play)
# kinezet
def start():
    global root, canvas, lives_nr_label, score_nr_label, pako, gyapot_image, end_text, restart_button
    root = Tk()
    root.title('Pákó')
    root.bind('<KeyPress>', key_pressed)
    root.bind('<KeyRelease>', key_released)
    info_frame = Frame(root)
    lives_str_label = Label(master=info_frame, text='Pákó eletei:')
    lives_str_label.grid(column=0, row=0)
    lives_nr_label = Label(master=info_frame)
    lives_nr_label.grid(column=1, row=0)
    score_str_label = Label(master=info_frame, text='Phontok:')
    score_str_label.grid(column=0, row=1)
    score_nr_label = Label(master=info_frame)
    score_nr_label.grid(column=1, row=1)
    info_frame.pack()
    restart_button = Button(master=root, text='Újráá', command=init, state='disabled')
    restart_button.pack()
    canvas = Canvas(root, width=1200, height=1000, bg='black')
    canvas.pack()
    pako_image = PhotoImage(file='pako1.png')
    pako = canvas.create_image(240, 310, image=pako_image)
    gyapot_image = PhotoImage(file='gyapotjo.png')
    end_text = canvas.create_text(600, 70, text='NAGYKANIZSA!!!', fill='yellow', font=('Times', 50), state='hidden')
    init(True)
    root.mainloop()

start()
