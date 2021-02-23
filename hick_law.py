import random
import pygame.gfxdraw
import time
import csv
import matplotlib.pyplot as plt
import pandas as pd

pygame.init()
scr = pygame.display.set_mode((1500, 800))
pygame.display.set_caption('Hick Hayman\'s Law')

# Open csv file
outfile = open("hick_law.csv", 'w',newline='')
outfile_field = ['SNo', 'No_Circles', 'Time']
writer = csv.DictWriter(outfile, fieldnames=outfile_field)
writer.writeheader()

colors = [(255,0,0),(0,255,0),(0,0,255),(0,0,0),(255,255,0),(255,0,255),(0,255,255),(200,200,200)]
count = 0
startingTime = 0
analysis = []

x_centre = [520,610,640,580,780,730,800,670]
y_centre = [180,370,560,280,450,350,210,290]

ques = ['Red color circle','Green color circle','Blue color circle','Black color circle','Yellow color circle',
        'Non red circle', 'Non green circle']
query = [(255,0,0),(0,255,0),(0,0,255),(0,0,0),(255,255,0)]

choice = random.randint(0,7)

circle_radius = []
for i in range(choice+1):
    circle_radius.append(random.randint(15,50))
question = ques[choice%7]

font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render(question, True, (0,0,0))
textRect = text.get_rect()
textRect.center = (750, 50)


while count<11:
    pygame.display.update()
    scr.fill((255, 255, 255))
    scr.blit(text, textRect)

    for i in range(choice+1):
        pygame.gfxdraw.filled_circle(scr, x_centre[i], y_centre[i], circle_radius[i], colors[i])

    # Mouse Click Event
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if question[:3] == 'Non':
                click = scr.get_at(pygame.mouse.get_pos()) != query[choice%5]
            else:
                click = scr.get_at(pygame.mouse.get_pos()) == query[choice%7]
            if click == 1:
                time_elapsed = round(time.time() - startingTime,2)
                analysis.append([str(count)+" "+str(time_elapsed)])
                if count!=0:
                    writer.writerow({'SNo': str(count), 'No_Circles': str(choice+1), 'Time': str(time_elapsed)})
                count += 1
                choice = random.randint(0,7)
                circle_radius = []
                for i in range(choice + 1):
                    circle_radius.append(random.randint(15, 50))
                for i in range(len(x_centre)//2):
                    x_centre[i],x_centre[len(x_centre)-1] = x_centre[len(x_centre)-1],x_centre[i]
                    y_centre[i],y_centre[len(y_centre)-1] = y_centre[len(y_centre)-1],y_centre[i]
                question = ques[choice%7]
                text = font.render(question, True, (0, 0, 0))
                textRect = text.get_rect()
                textRect.center = (750, 50)
                startingTime = time.time()

outfile.close()
pygame.quit()

# Displaying graph
import numpy as np
df = pd.read_csv('hick_law.csv')
print(df)
plt.figure(figsize=(20,8))

plt.title('Hick Hyman Law Demo')
x = df['No_Circles']
y = df['Time']
plt.scatter(x,y)
m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b)
plt.xlabel('Number of Circles')
plt.ylabel('Time')
plt.show()

# Displaying table
from tkinter import *
import tkinter.ttk as ttk
import csv

root = Tk()
root.title("Hick Hyman Law Demo Table")
width = 400
height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

TableMargin = Frame(root, width=400)
TableMargin.pack(side=TOP)
tree = ttk.Treeview(TableMargin, columns=( "No_Circles", "Time"), height=300, selectmode="extended")
tree.heading('No_Circles', text="No_Circles", anchor=W)
tree.heading('Time', text="Time", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=200)
tree.column('#2', stretch=NO, minwidth=0, width=200)
tree.pack()

with open('hick_law.csv') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        num = row['No_Circles']
        times = row['Time']
        tree.insert("", 0, values=(num, times))

if __name__ == '__main__':
    root.mainloop()

sys.exit()