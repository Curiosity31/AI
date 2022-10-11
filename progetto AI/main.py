import time
import sys as s
import tkinter as tk
from functools import partial
from threading import Thread
from tkinter import *
from tkinter import ttk
import numpy as np
from furhat_remote_api import FurhatRemoteAPI
import emotionGestureDefinition

# Creo la finestra principale definendo i parametri.
window = tk.Tk()
window.geometry("1531x780")
window.resizable(False, False)
window.title("AI")
window.configure(background="lightgreen")
frame = tk.Frame(window)
frame.pack(expand=True, fill=BOTH)
canvas = Canvas(frame, background="lightgreen")
canvas.pack(side=LEFT, expand=True, fill=BOTH)
label = tk.Label(canvas, text="Benvenuto. Scegli la configurazione iniziale", fg="green", bg="lightgreen",
                 font="TimesNewRoman 16 bold italic")
label.pack(pady=10)

# Creo un'istanza della classe FurhatRemoteAPI, fornendo l'indirizzo del robot o l'SDK che esegue il robot virtuale.
furhat = FurhatRemoteAPI("localhost")

# Ottengo la voce sul robot.
# voices = furhat.get_voices()

# Imposto la voce del robot.
furhat.set_voice(name='Carmine')

furhat.say(text="Ciao, sono Furhat")

# Creo una matrice numpy 3D per contenere i valori Q correnti per ogni coppia di stati e azioni: Q(s, a).
# La matrice contiene 12 righe (una per ogni possibile stato) e 6 colonne (una per ogni possibile azione).
# Il valore di ogni coppia (stato, azione) viene inizializzato su 0.
Q_table = np.zeros((12, 6))

# definisco un dizionario per le azioni.
actions = {0: 'rosso in 1', 1: 'rosso in 2', 2: 'rosso in 3',
           3: 'giallo in 1', 4: 'giallo in 2', 5: 'giallo in 3'}

# Definisco un dizionario per gli stati.
state = {0: 'rosso in 1 e giallo in 2', 1: 'rosso in 1 e giallo in 3', 2: 'rosso in 1 e giallo in 1',
         3: 'rosso in 2 e giallo in 1', 4: 'rosso in 2 e giallo in 3', 5: 'rosso in 2 e giallo in 2',
         6: 'rosso in 3 e giallo in 2', 7: 'rosso in 3 e giallo in 1', 8: 'rosso in 3 e giallo in 3',
         9: 'giallo in 1 e rosso in 1', 10: 'giallo in 2 e rosso in 2', 11: 'giallo in 3 e rosso in 3'}


# Definisco una funzione per la scelta del comportamento del robot.
def choice_behavior():
    choice = 0
    print("\nScelta del comportamento dell'agente")
    while choice < 1 or choice > 3:
        print("\nInserire 1 per ottenere un comportamento \'Solo parlato\'")
        print("\nInserire 2 per ottenere un comportamento \'Solo emozioni\'")
        print("\nInserire 3 per ottenere un comportamento \'Misto\'")
        choice = int(input("\nScelta: "))
        if choice < 1 or choice > 3:
            print("\nScelta errata, riprovare.")

    return choice


# Definisco una funzione per terminare il programma.
def close(sourceFile):
    global finish
    finish = True
    # Imposto il Button Chiudi in modo tale da dare la possibilità di vedere le mosse effettuate
    # nell'intefaccia attraverso la scroll bar fintanto che non si preme 'Chiudi'.
    var = tk.IntVar()
    button_chiudi = tk.Button(canvas, width=8, text="CHIUDI", font="TimesNewRoman 13 italic bold")
    canvas.create_window(1350, 80, anchor=NW, window=button_chiudi)
    button_chiudi.configure(background="red", relief=RAISED, fg="white", command=lambda: var.set(1))
    # Aspetto che venga settata la variabile trimite la pressione del pulsante e dopo finisce.
    button_chiudi.wait_variable(var)
    sourceFile.close()
    s.exit()


# Definisco una funzione per salvare dei dati prima di terminare.
def stop(initial_state, final_state, tdr, number_episode, intervals, episode_converge, sourceFile):
    global finish
    finish = True
    print("\nStato iniziale: ", state[initial_state], "\nStato finale: ", state[final_state], "\nTDRL: ", tdr,
          "\nNumero episodio: ", number_episode, file=sourceFile)
    print("\nStato iniziale: ", state[initial_state], "\nStato finale: ", state[final_state], "\nTDRL: ", tdr,
          "\nNumero episodio: ", number_episode)
    print("\nConvergenza Q_table avvenuta all'episodio: ", episode_converge)
    print("\nConvergenza Q_table avvenuta all'episodio: ", episode_converge, file=sourceFile)
    print("\n", intervals)
    print("\n", intervals, file=sourceFile)
    close(sourceFile)


# Ottengo gli indici del goal.
def goal_location(num):
    global goal
    goal = num
    canvas.delete("all")
    label.configure(text="Ottima scelta!\nLa configurazione da imparare è: ")
    canvas.create_line(730, 150, 820, 150, fill='green', width=5)

    if goal == 0:
        canvas.create_rectangle(735, 147, 755, 127, fill='red', outline='red')
        canvas.create_rectangle(765, 147, 785, 127, fill='yellow', outline='yellow')
    elif goal == 1:
        canvas.create_rectangle(735, 147, 755, 127, fill='red', outline='red')
        canvas.create_rectangle(795, 147, 815, 127, fill='yellow', outline='yellow')
    elif goal == 2:
        canvas.create_rectangle(735, 147, 755, 127, fill='red', outline='red')
        canvas.create_rectangle(735, 127, 755, 107, fill='yellow', outline='yellow')
    elif goal == 3:
        canvas.create_rectangle(765, 147, 785, 127, fill='red', outline='red')
        canvas.create_rectangle(735, 147, 755, 127, fill='yellow', outline='yellow')
    elif goal == 4:
        canvas.create_rectangle(765, 147, 785, 127, fill='red', outline='red')
        canvas.create_rectangle(795, 147, 815, 127, fill='yellow', outline='yellow')
    elif goal == 5:
        canvas.create_rectangle(765, 147, 785, 127, fill='red', outline='red')
        canvas.create_rectangle(765, 127, 785, 107, fill='yellow', outline='yellow')
    elif goal == 6:
        canvas.create_rectangle(795, 147, 815, 127, fill='red', outline='red')
        canvas.create_rectangle(765, 147, 785, 127, fill='yellow', outline='yellow')
    elif goal == 7:
        canvas.create_rectangle(795, 147, 815, 127, fill='red', outline='red')
        canvas.create_rectangle(735, 147, 755, 127, fill='yellow', outline='yellow')
    elif goal == 8:
        canvas.create_rectangle(795, 147, 815, 127, fill='red', outline='red')
        canvas.create_rectangle(795, 127, 815, 107, fill='yellow', outline='yellow')
    elif goal == 9:
        canvas.create_rectangle(735, 127, 755, 107, fill='red', outline='red')
        canvas.create_rectangle(735, 147, 755, 127, fill='yellow', outline='yellow')
    elif goal == 10:
        canvas.create_rectangle(765, 127, 785, 107, fill='red', outline='red')
        canvas.create_rectangle(765, 147, 785, 127, fill='yellow', outline='yellow')
    else:
        canvas.create_rectangle(795, 127, 815, 107, fill='red', outline='red')
        canvas.create_rectangle(795, 147, 815, 127, fill='yellow', outline='yellow')

    # Creo un thread per far funzionare l'interfaccia. La sua entry sarà training.
    thread = Thread(target=start)
    thread.daemon = True
    thread.start()


# Definisco una funzione per far scegliere all'utente la posizione dell'obiettivo.
def choice_location():
    pad = 30
    count = -1
    for index in range(6):
        pad = pad + 115
        count += 1
        canvas.create_line(460, pad, 550, pad, fill='green', width=5)
        canvas.create_line(1260, pad, 1350, pad, fill='green', width=5)
        button1 = tk.Button(canvas, text="Cliccami per scegliere questa configurazione finale",
                            command=partial(goal_location, count), font="TimesNewRoman 8 italic")
        canvas.create_window(160, pad - 23, anchor=NW, window=button1)
        button1.configure(background="lightgreen", relief=RAISED, fg="darkgreen")
        count += 1
        button2 = tk.Button(canvas, text="Cliccami per scegliere questa configurazione finale",
                            command=partial(goal_location, count), font="TimesNewRoman 8 italic")
        canvas.create_window(960, pad - 23, anchor=NW, window=button2)
        button2.configure(background="lightgreen", relief=RAISED, fg="darkgreen")

        if index == 0:
            canvas.create_rectangle(465, pad - 3, 485, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(495, pad - 3, 515, pad - 23, fill='yellow', outline='yellow')
            canvas.create_rectangle(1265, pad - 3, 1285, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(1325, pad - 3, 1345, pad - 23, fill='yellow', outline='yellow')
        elif index == 1:
            canvas.create_rectangle(465, pad - 3, 485, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(465, pad - 23, 485, pad - 43, fill='yellow', outline='yellow')
            canvas.create_rectangle(1295, pad - 3, 1315, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(1265, pad - 3, 1285, pad - 23, fill='yellow', outline='yellow')
        elif index == 2:
            canvas.create_rectangle(495, pad - 3, 515, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(525, pad - 3, 545, pad - 23, fill='yellow', outline='yellow')
            canvas.create_rectangle(1295, pad - 3, 1315, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(1295, pad - 23, 1315, pad - 43, fill='yellow', outline='yellow')
        elif index == 3:
            canvas.create_rectangle(525, pad - 3, 545, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(495, pad - 3, 515, pad - 23, fill='yellow', outline='yellow')
            canvas.create_rectangle(1325, pad - 3, 1345, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(1265, pad - 3, 1285, pad - 23, fill='yellow', outline='yellow')
        elif index == 4:
            canvas.create_rectangle(525, pad - 3, 545, pad - 23, fill='red', outline='red')
            canvas.create_rectangle(525, pad - 23, 545, pad - 43, fill='yellow', outline='yellow')
            canvas.create_rectangle(1265, pad - 23, 1285, pad - 43, fill='red', outline='red')
            canvas.create_rectangle(1265, pad - 3, 1285, pad - 23, fill='yellow', outline='yellow')
        else:
            canvas.create_rectangle(495, pad - 23, 515, pad - 43, fill='red', outline='red')
            canvas.create_rectangle(495, pad - 3, 515, pad - 23, fill='yellow', outline='yellow')
            canvas.create_rectangle(1325, pad - 23, 1345, pad - 43, fill='red', outline='red')
            canvas.create_rectangle(1325, pad - 3, 1345, pad - 23, fill='yellow', outline='yellow')


# Definisco una funzione per ottenere gli indici della locazione dello stato.
def index_location(curr_state):
    if curr_state == 'rosso in 1 e giallo in 2':
        current_red_row_index = 1
        current_red_column_index = 0
        current_yellow_row_index = 1
        current_yellow_column_index = 1
    elif curr_state == 'rosso in 1 e giallo in 3':
        current_red_row_index = 1
        current_red_column_index = 0
        current_yellow_row_index = 1
        current_yellow_column_index = 2
    elif curr_state == 'rosso in 1 e giallo in 1':
        current_red_row_index = 1
        current_red_column_index = 0
        current_yellow_row_index = 0
        current_yellow_column_index = 0
    elif curr_state == 'rosso in 2 e giallo in 1':
        current_red_row_index = 1
        current_red_column_index = 1
        current_yellow_row_index = 1
        current_yellow_column_index = 0
    elif curr_state == 'rosso in 2 e giallo in 3':
        current_red_row_index = 1
        current_red_column_index = 1
        current_yellow_row_index = 1
        current_yellow_column_index = 2
    elif curr_state == 'rosso in 2 e giallo in 2':
        current_red_row_index = 1
        current_red_column_index = 1
        current_yellow_row_index = 0
        current_yellow_column_index = 1
    elif curr_state == 'rosso in 3 e giallo in 2':
        current_red_row_index = 1
        current_red_column_index = 2
        current_yellow_row_index = 1
        current_yellow_column_index = 1
    elif curr_state == 'rosso in 3 e giallo in 1':
        current_red_row_index = 1
        current_red_column_index = 2
        current_yellow_row_index = 1
        current_yellow_column_index = 0
    elif curr_state == 'rosso in 3 e giallo in 3':
        current_red_row_index = 1
        current_red_column_index = 2
        current_yellow_row_index = 0
        current_yellow_column_index = 2
    elif curr_state == 'giallo in 1 e rosso in 1':
        current_red_row_index = 0
        current_red_column_index = 0
        current_yellow_row_index = 1
        current_yellow_column_index = 0
    elif curr_state == 'giallo in 2 e rosso in 2':
        current_red_row_index = 0
        current_red_column_index = 1
        current_yellow_row_index = 1
        current_yellow_column_index = 1
    else:  # 'giallo in 3 e rosso in 3'
        current_red_row_index = 0
        current_red_column_index = 2
        current_yellow_row_index = 1
        current_yellow_column_index = 2

    return current_red_row_index, current_red_column_index, current_yellow_row_index, current_yellow_column_index


# Definisco una funzione che stampa la posizione dei cubi.
def print_environment(red_row, red_column, yellow_row, yellow_column):
    environment = np.zeros([2, 3])
    environment[red_row, red_column] = 1
    environment[yellow_row, yellow_column] = 2
    print('\nIl codice 1 identifica il cubo rosso ed il codice 2 il giallo\n', environment, '\n')


def print_environment_in_file_log(red_row, red_column, yellow_row, yellow_column, sourceFile):
    environment_log = np.zeros([2, 3])
    environment_log[red_row, red_column] = 1
    environment_log[yellow_row, yellow_column] = 2
    print('\nIl codice 1 identifica il cubo rosso ed il codice 2 il giallo\n', environment_log, '\n', file=sourceFile)


def print_in_interface(red_row, red_column, yellow_row, yellow_column, my_canvas, pad):
    my_canvas.create_line(395, pad, 485, pad, fill='green', width=5)

    if red_row == 0 and red_column == 0:
        my_canvas.create_rectangle(400, pad - 23, 420, pad - 43, fill='red', outline='red')
    elif red_row == 0 and red_column == 1:
        my_canvas.create_rectangle(430, pad - 23, 450, pad - 43, fill='red', outline='red')
    elif red_row == 0 and red_column == 2:
        my_canvas.create_rectangle(460, pad - 23, 480, pad - 43, fill='red', outline='red')
    elif red_row == 1 and red_column == 0:
        my_canvas.create_rectangle(400, pad - 3, 420, pad - 23, fill='red', outline='red')
    elif red_row == 1 and red_column == 1:
        my_canvas.create_rectangle(430, pad - 3, 450, pad - 23, fill='red', outline='red')
    elif red_row == 1 and red_column == 2:
        my_canvas.create_rectangle(460, pad - 3, 480, pad - 23, fill='red', outline='red')

    if yellow_row == 0 and yellow_column == 0:
        my_canvas.create_rectangle(400, pad - 23, 420, pad - 43, fill='yellow', outline='yellow')
    elif yellow_row == 0 and yellow_column == 1:
        my_canvas.create_rectangle(430, pad - 23, 450, pad - 43, fill='yellow', outline='yellow')
    elif yellow_row == 0 and yellow_column == 2:
        my_canvas.create_rectangle(460, pad - 23, 480, pad - 43, fill='yellow', outline='yellow')
    elif yellow_row == 1 and yellow_column == 0:
        my_canvas.create_rectangle(400, pad - 3, 420, pad - 23, fill='yellow', outline='yellow')
    elif yellow_row == 1 and yellow_column == 1:
        my_canvas.create_rectangle(430, pad - 3, 450, pad - 23, fill='yellow', outline='yellow')
    elif yellow_row == 1 and yellow_column == 2:
        my_canvas.create_rectangle(460, pad - 3, 480, pad - 23, fill='yellow', outline='yellow')


def new_print_in_interface(old_red_row, old_red_column, old_yellow_row, old_yellow_column, new_red_row, new_red_column,
                           new_yellow_row, new_yellow_column, my_canvas):
    my_canvas.create_line(525, 550, 1025, 550, fill='green', width=5)

    if old_red_row == new_red_row and old_red_column == new_red_column:
        my_canvas.delete("yellow")
        my_canvas.create_line(50, 60, 140, 60, fill='green', width=5)
        my_canvas.create_text(95, 73, fill="green", font="TimesNewRoman 12 italic bold", text="Previous Move")
    elif old_yellow_column == new_yellow_column and old_yellow_row == new_yellow_row:
        my_canvas.delete("red")
        my_canvas.create_line(50, 60, 140, 60, fill='green', width=5)
        my_canvas.create_text(95, 73, fill="green", font="TimesNewRoman 12 italic bold", text="Previous Move")

    if new_yellow_row == 0 and new_yellow_column == 0:
        my_canvas.create_rectangle(535, 550 - 153, 685, 550 - 303, fill='yellow', outline='yellow', tags='yellow')
    elif new_yellow_row == 0 and new_yellow_column == 1:
        my_canvas.create_rectangle(700, 550 - 153, 850, 550 - 303, fill='yellow', outline='yellow', tags='yellow')
    elif new_yellow_row == 0 and new_yellow_column == 2:
        my_canvas.create_rectangle(865, 550 - 153, 1015, 550 - 303, fill='yellow', outline='yellow', tags='yellow')
    elif new_yellow_row == 1 and new_yellow_column == 0:
        my_canvas.create_rectangle(535, 550 - 3, 685, 550 - 153, fill='yellow', outline='yellow', tags='yellow')
    elif new_yellow_row == 1 and new_yellow_column == 1:
        my_canvas.create_rectangle(700, 550 - 3, 850, 550 - 153, fill='yellow', outline='yellow', tags='yellow')
    elif new_yellow_row == 1 and new_yellow_column == 2:
        my_canvas.create_rectangle(865, 550 - 3, 1015, 550 - 153, fill='yellow', outline='yellow', tags='yellow')

    if new_red_row == 0 and new_red_column == 0:
        my_canvas.create_rectangle(535, 550 - 153, 685, 550 - 303, fill='red', outline='red', tags='red')
    elif new_red_row == 0 and new_red_column == 1:
        my_canvas.create_rectangle(700, 550 - 153, 850, 550 - 303, fill='red', outline='red', tags='red')
    elif new_red_row == 0 and new_red_column == 2:
        my_canvas.create_rectangle(865, 550 - 153, 1015, 550 - 303, fill='red', outline='red', tags='red')
    elif new_red_row == 1 and new_red_column == 0:
        my_canvas.create_rectangle(535, 550 - 3, 685, 550 - 153, fill='red', outline='red', tags='red')
    elif new_red_row == 1 and new_red_column == 1:
        my_canvas.create_rectangle(700, 550 - 3, 850, 550 - 153, fill='red', outline='red', tags='red')
    elif new_red_row == 1 and new_red_column == 2:
        my_canvas.create_rectangle(865, 550 - 3, 1015, 550 - 153, fill='red', outline='red', tags='red')

    my_canvas.delete("old_yellow")
    my_canvas.delete("old_red")

    if old_red_row == 0 and old_red_column == 0:
        my_canvas.create_rectangle(55, 60 - 23, 75, 60 - 43, fill='red', outline='red', tags='old_red')
    elif old_red_row == 0 and old_red_column == 1:
        my_canvas.create_rectangle(85, 60 - 23, 105, 60 - 43, fill='red', outline='red', tags='old_red')
    elif old_red_row == 0 and old_red_column == 2:
        my_canvas.create_rectangle(115, 60 - 23, 135, 60 - 43, fill='red', outline='red', tags='old_red')
    elif old_red_row == 1 and old_red_column == 0:
        my_canvas.create_rectangle(55, 60 - 3, 75, 60 - 23, fill='red', outline='red', tags='old_red')
    elif old_red_row == 1 and old_red_column == 1:
        my_canvas.create_rectangle(85, 60 - 3, 105, 60 - 23, fill='red', outline='red', tags='old_red')
    elif old_red_row == 1 and old_red_column == 2:
        my_canvas.create_rectangle(115, 60 - 3, 135, 60 - 23, fill='red', outline='red', tags='old_red')

    if old_yellow_row == 0 and old_yellow_column == 0:
        my_canvas.create_rectangle(55, 60 - 23, 75, 60 - 43, fill='yellow', outline='yellow', tags='old_yellow')
    elif old_yellow_row == 0 and old_yellow_column == 1:
        my_canvas.create_rectangle(85, 60 - 23, 105, 60 - 43, fill='yellow', outline='yellow', tags='old_yellow')
    elif old_yellow_row == 0 and old_yellow_column == 2:
        my_canvas.create_rectangle(115, 60 - 23, 135, 60 - 43, fill='yellow', outline='yellow', tags='old_yellow')
    elif old_yellow_row == 1 and old_yellow_column == 0:
        my_canvas.create_rectangle(55, 60 - 3, 75, 60 - 23, fill='yellow', outline='yellow', tags='old_yellow')
    elif old_yellow_row == 1 and old_yellow_column == 1:
        my_canvas.create_rectangle(85, 60 - 3, 105, 60 - 23, fill='yellow', outline='yellow', tags='old_yellow')
    elif old_yellow_row == 1 and old_yellow_column == 2:
        my_canvas.create_rectangle(115, 60 - 3, 135, 60 - 23, fill='yellow', outline='yellow', tags='old_yellow')


# definisco una funzione per ottenere il prossimo stato in base allo stato corrente e all'azione scelta.
def get_next_state(next_action_index, curr_state):
    global actions
    if curr_state == 'rosso in 1 e giallo in 2':
        if actions[next_action_index] == 'giallo in 1':
            next_state = 2
        elif actions[next_action_index] == 'giallo in 3':
            next_state = 1
        elif actions[next_action_index] == 'rosso in 2':
            next_state = 10
        else:  # 'rosso in 3'
            next_state = 6
    elif curr_state == 'rosso in 1 e giallo in 3':
        if actions[next_action_index] == 'rosso in 2':
            next_state = 4
        elif actions[next_action_index] == 'rosso in 3':
            next_state = 11
        elif actions[next_action_index] == 'giallo in 1':
            next_state = 2
        else:  # 'giallo in 2'
            next_state = 0
    elif curr_state == 'rosso in 1 e giallo in 1':
        if actions[next_action_index] == 'giallo in 2':
            next_state = 0
        else:  # 'giallo in 3'
            next_state = 1
    elif curr_state == 'rosso in 2 e giallo in 1':
        if actions[next_action_index] == 'giallo in 2':
            next_state = 5
        elif actions[next_action_index] == 'giallo in 3':
            next_state = 4
        elif actions[next_action_index] == 'rosso in 1':
            next_state = 9
        else:  # 'rosso in 3'
            next_state = 7
    elif curr_state == 'rosso in 2 e giallo in 3':
        if actions[next_action_index] == 'rosso in 1':
            next_state = 1
        elif actions[next_action_index] == 'rosso in 3':
            next_state = 11
        elif actions[next_action_index] == 'giallo in 1':
            next_state = 3
        else:  # 'giallo in 2'
            next_state = 5
    elif curr_state == 'rosso in 2 e giallo in 2':
        if actions[next_action_index] == 'giallo in 1':
            next_state = 3
        else:  # 'giallo in 3'
            next_state = 4
    elif curr_state == 'rosso in 3 e giallo in 2':
        if actions[next_action_index] == 'rosso in 1':
            next_state = 0
        elif actions[next_action_index] == 'rosso in 2':
            next_state = 10
        elif actions[next_action_index] == 'giallo in 1':
            next_state = 7
        else:  # 'giallo in 3'
            next_state = 8
    elif curr_state == 'rosso in 3 e giallo in 1':
        if actions[next_action_index] == 'rosso in 1':
            next_state = 9
        elif actions[next_action_index] == 'rosso in 2':
            next_state = 3
        elif actions[next_action_index] == 'giallo in 2':
            next_state = 6
        else:  # 'giallo in 3'
            next_state = 8
    elif curr_state == 'rosso in 3 e giallo in 3':
        if actions[next_action_index] == 'giallo in 1':
            next_state = 7
        else:  # 'giallo in 2'
            next_state = 6
    elif curr_state == 'giallo in 1 e rosso in 1':
        if actions[next_action_index] == 'rosso in 2':
            next_state = 3
        else:  # 'rosso in 3'
            next_state = 7
    elif curr_state == 'giallo in 2 e rosso in 2':
        if actions[next_action_index] == 'rosso in 1':
            next_state = 0
        else:  # 'rosso in 3'
            next_state = 6
    else:  # Giallo 3 e rosso 3
        if actions[next_action_index] == 'rosso in 1':
            next_state = 1
        else:  # 'rosso in 2'
            next_state = 4
    return next_state


# definisco una funzione che determina se la posizione specificata è uno stato terminale.
def is_terminal_state(curr_state):
    global goal
    global state
    return state[goal] == state[curr_state]


# Definisco una funzione per ottenere lo stato iniziale (non terminale, scelto in modo random).
def get_starting_location():
    start_state = np.random.randint(12)
    while is_terminal_state(start_state):
        start_state = np.random.randint(12)

    return start_state


def available_actions(curr_state):
    global state
    if state[curr_state] == 'rosso in 1 e giallo in 2':
        available_act = {3: 'giallo in 1', 5: 'giallo in 3', 1: 'rosso in 2', 2: 'rosso in 3'}
    elif state[curr_state] == 'rosso in 1 e giallo in 3':
        available_act = {1: 'rosso in 2', 2: 'rosso in 3', 3: 'giallo in 1', 4: 'giallo in 2'}
    elif state[curr_state] == 'rosso in 1 e giallo in 1':
        available_act = {4: 'giallo in 2', 5: 'giallo in 3'}
    elif state[curr_state] == 'rosso in 2 e giallo in 1':
        available_act = {4: 'giallo in 2', 5: 'giallo in 3', 0: 'rosso in 1', 2: 'rosso in 3'}
    elif state[curr_state] == 'rosso in 2 e giallo in 3':
        available_act = {0: 'rosso in 1', 2: 'rosso in 3', 3: 'giallo in 1', 4: 'giallo in 2'}
    elif state[curr_state] == 'rosso in 2 e giallo in 2':
        available_act = {3: 'giallo in 1', 5: 'giallo in 3'}
    elif state[curr_state] == 'rosso in 3 e giallo in 2':
        available_act = {0: 'rosso in 1', 1: 'rosso in 2', 3: 'giallo in 1', 5: 'giallo in 3'}
    elif state[curr_state] == 'rosso in 3 e giallo in 1':
        available_act = {4: 'giallo in 2', 5: 'giallo in 3', 0: 'rosso in 1', 1: 'rosso in 2'}
    elif state[curr_state] == 'rosso in 3 e giallo in 3':
        available_act = {3: 'giallo in 1', 4: 'giallo in 2'}
    elif state[curr_state] == 'giallo in 1 e rosso in 1':
        available_act = {1: 'rosso in 2', 2: 'rosso in 3'}
    elif state[curr_state] == 'giallo in 2 e rosso in 2':
        available_act = {0: 'rosso in 1', 2: 'rosso in 3'}
    else:  # Giallo 3 e rosso 3
        available_act = {0: 'rosso in 1', 1: 'rosso in 2'}

    return available_act


# definisco un algoritmo di epsilon greedy che sceglierà quale azione intraprendere successivamente.
def get_next_action(curr_state, current_epsilon):
    global Q_table
    available_actions_for_next_action = available_actions(curr_state)
    # Se un valore scelto casualmente tra 0 e 1 è minore di epsilon,
    # allora scelgo il valore più alto dalla Q_table per questo stato.
    actions_available = list(available_actions_for_next_action)
    if np.random.uniform(0, 1) < current_epsilon:
        return actions_available[np.argmax(Q_table[curr_state, actions_available])]

    else:  # Scelgo un'azione casuale.
        return np.random.choice(actions_available)


# Definisco una funzione per ottenere il massimo futuro valore Q da un dato stato.
def max_future_q_value(curr_state):
    global Q_table
    available_actions_for_max = available_actions(curr_state)

    return np.max(Q_table[curr_state, list(available_actions_for_max)])


# Definisco una funzione per far assumere all'agente un comportamento 'solo parlato'.
def spoken_behavior(current_state, temporal_difference, reward, intervals, repetitions_intervals):
    time.sleep(0.5)

    if is_terminal_state(current_state):
        furhat.say(text="obiettivo raggiunto!")
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["goal_interval"] += 1
    elif reward == -1:
        if temporal_difference < -1:
            furhat.say(text="Pessimo!")
        else:
            furhat.say(text="Ho fallito!")
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["no_goal"] += 1
    elif temporal_difference >= 0:
        if temporal_difference <= 0.000000001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] > 1:
                furhat.say(text="Sto imparando a piccoli passi.")
                repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.say(text="Non male.")
            for string in ["zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.00001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] > 1:
                furhat.say(text="Sto migliorando!")
                repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.say(text="Bene!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove", "piu_uno",
                           "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.1:
            repetitions_intervals["zero_punto_uno"] += 1
            if repetitions_intervals["zero_punto_uno"] > 1:
                furhat.say(text="Sto imparando!")
                repetitions_intervals["zero_punto_uno"] = 0
            else:
                furhat.say(text="Molto bene!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "uno", "meno_zero_punto_zero_zero_zero_nove",
                           "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_uno"] += 1
        elif temporal_difference <= 1:
            repetitions_intervals["uno"] += 1
            if repetitions_intervals["uno"] > 1:
                furhat.say(text="Sto andando alla grande!")
                repetitions_intervals["uno"] = 0
            else:
                furhat.say(text="Benissimo!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "piu_uno", "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["uno"] += 1
        else:
            furhat.say(text="Wow, esplorare mi fa bene!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["piu_uno"] += 1
    else:
        if temporal_difference >= -0.0009:
            repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] > 1:
                furhat.say(text="Potevo fare scelta migliore!")
                repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] = 0
            else:
                furhat.say(text="#MMM01#")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "meno_zero_punto_zero_zero_uno", "piu_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
        elif temporal_difference >= -0.001:
            repetitions_intervals["meno_zero_punto_zero_zero_uno"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_uno"] > 2:
                furhat.say(text="No, non va affatto bene!")
                repetitions_intervals["meno_zero_punto_zero_zero_uno"] = 0
            elif repetitions_intervals["meno_zero_punto_zero_zero_uno"] > 1:
                furhat.say(text="Così non va bene!")
            else:
                furhat.say(text="Non dovevo!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_uno"] += 1
        elif temporal_difference >= -1:
            repetitions_intervals["meno_uno"] += 1
            if repetitions_intervals["meno_uno"] > 2:
                furhat.say(text="Deve essermi finito del sale nell'unità centrale!")
                repetitions_intervals["meno_uno"] = 0
            elif repetitions_intervals["meno_uno"] > 1:
                furhat.say(text="Questa mossa è stata anche peggiore!")
            else:
                furhat.say(text="Non è stata per nulla una buona mossa!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "piu_uno",
                           "meno_zero_punto_zero_zero_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_uno"] += 1
        else:
            furhat.say(text="Da tutti questi errori dovrei imparare qualcosa!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_meno_uno"] += 1

    time.sleep(3)


# Definisco una funzione per far assumere all'agente un comportamento 'solo emozioni'.
def emotion_behavior(current_state, temporal_difference, reward, intervals, repetitions_intervals):
    time.sleep(0.5)

    if is_terminal_state(current_state):
        furhat.gesture(body=emotionGestureDefinition.ExpressHappyHigh)
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["goal_interval"] += 1
    elif reward == -1:
        if temporal_difference < -1:
            furhat.gesture(body=emotionGestureDefinition.ExpressAngerHigh)
        else:
            furhat.gesture(body=emotionGestureDefinition.ExpressSadHigh)
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["no_goal"] += 1
    elif temporal_difference >= 0:
        if temporal_difference <= 0.000000001:
            furhat.gesture(body=emotionGestureDefinition.NodListening)
            for string in ["zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.00001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyLow)
                repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseLow)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove", "piu_uno",
                           "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.1:
            repetitions_intervals["zero_punto_uno"] += 1
            if repetitions_intervals["zero_punto_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyMedium)
                repetitions_intervals["zero_punto_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "uno", "meno_zero_punto_zero_zero_zero_nove",
                           "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_uno"] += 1
        elif temporal_difference <= 1:
            repetitions_intervals["uno"] += 1
            if repetitions_intervals["uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyHigh)
                repetitions_intervals["uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseHigh)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "piu_uno", "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["uno"] += 1
        else:
            furhat.gesture(body=emotionGestureDefinition.SurprisePositive)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["piu_uno"] += 1
    else:
        if temporal_difference >= -0.0009:
            repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadLow)
                repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressDisgustLow)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "meno_zero_punto_zero_zero_uno", "piu_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
        elif temporal_difference >= -0.001:
            repetitions_intervals["meno_zero_punto_zero_zero_uno"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadMedium)
                repetitions_intervals["meno_zero_punto_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressDisgustMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_uno"] += 1
        elif temporal_difference >= -1:
            repetitions_intervals["meno_uno"] += 1
            if repetitions_intervals["meno_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadHigh)
                repetitions_intervals["meno_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressDisgustHigh)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "piu_uno",
                           "meno_zero_punto_zero_zero_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_uno"] += 1
        else:
            furhat.gesture(body=emotionGestureDefinition.ExpressAngerHigh)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_meno_uno"] += 1
    time.sleep(3.5)


# Definisco una funzione per far assumere all'agente un comportamento misto (parlato ed emozioni).
def mixed_behavior(current_state, temporal_difference, reward, intervals, repetitions_intervals):
    time.sleep(0.5)

    if is_terminal_state(current_state):
        furhat.gesture(body=emotionGestureDefinition.ExpressHappyHigh)
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["goal_interval"] += 1
    elif reward == -1:
        if temporal_difference < -1:
            furhat.gesture(body=emotionGestureDefinition.ExpressAngerHigh)
        else:
            furhat.gesture(body=emotionGestureDefinition.ExpressSadHigh)
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["no_goal"] += 1
    elif temporal_difference >= 0:
        if temporal_difference <= 0.000000001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] > 1:
                furhat.say(text="Sto imparando a piccoli passi.")
                repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyLow)
            for string in ["zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.00001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] > 1:
                furhat.say(text="Sto migliorando!")
                repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove", "piu_uno",
                           "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.1:
            repetitions_intervals["zero_punto_uno"] += 1
            if repetitions_intervals["zero_punto_uno"] > 1:
                furhat.say(text="Molto bene!")
                repetitions_intervals["zero_punto_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseLow)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "uno", "meno_zero_punto_zero_zero_zero_nove",
                           "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_uno"] += 1
        elif temporal_difference <= 1:
            repetitions_intervals["uno"] += 1
            if repetitions_intervals["uno"] > 1:
                furhat.say(text="Benissimo!")
                repetitions_intervals["uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "piu_uno", "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["uno"] += 1
        else:
            furhat.gesture(body=emotionGestureDefinition.SurprisePositive)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["piu_uno"] += 1
    else:
        if temporal_difference >= -0.0009:
            repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] > 1:
                furhat.say(text="#MMM03#")
                repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadLow)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "meno_zero_punto_zero_zero_uno", "piu_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
        elif temporal_difference >= -0.001:
            repetitions_intervals["meno_zero_punto_zero_zero_uno"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_uno"] > 2:
                furhat.say(text="Non dovevo!")
                repetitions_intervals["meno_zero_punto_zero_zero_uno"] = 0
            elif repetitions_intervals["meno_zero_punto_zero_zero_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressFearLow)
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressDisgustLow)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_uno"] += 1
        elif temporal_difference >= -1:
            repetitions_intervals["meno_uno"] += 1
            if repetitions_intervals["meno_uno"] > 2:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadMedium)
                time.sleep(3.3)
                furhat.say(text="Deve essermi finito del sale nell'unità centrale!")
                repetitions_intervals["meno_uno"] = 0
            elif repetitions_intervals["meno_uno"] > 1:
                furhat.say(text="Non è stata per nulla una buona mossa!")
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressDisgustMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "piu_uno",
                           "meno_zero_punto_zero_zero_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_uno"] += 1
        else:
            furhat.gesture(body=emotionGestureDefinition.ExpressAngerHigh)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_meno_uno"] += 1

    time.sleep(3.5)


# Definisco una funzione per far assumere all'agente un comportamento misto (parlato ed emozioni).
def mixed_behavior2(current_state, temporal_difference, reward, intervals, repetitions_intervals):
    time.sleep(0.5)

    if is_terminal_state(current_state):
        furhat.gesture(body=emotionGestureDefinition.ExpressHappyHigh)
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["goal_interval"] += 1
    elif reward == -1:
        if temporal_difference < -1:
            furhat.gesture(body=emotionGestureDefinition.ExpressAngerHigh)
        else:
            furhat.gesture(body=emotionGestureDefinition.ExpressSadHigh)
        for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                       "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                       "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
            repetitions_intervals[string] = 0
        intervals["no_goal"] += 1
    elif temporal_difference >= 0:
        if temporal_difference <= 0.000000001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyLow)
                repetitions_intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseLow)
            for string in ["zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.00001:
            repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
            if repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressHappyMedium)
                repetitions_intervals["zero_punto_zero_zero_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.SurpriseMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove", "piu_uno",
                           "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.1:
            repetitions_intervals["zero_punto_uno"] += 1
            if repetitions_intervals["zero_punto_uno"] > 1:
                furhat.say(text="Sto imparando a piccoli passi.")
                repetitions_intervals["zero_punto_uno"] = 0
            else:
                furhat.say(text="Bene.")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "uno", "meno_zero_punto_zero_zero_zero_nove",
                           "meno_zero_punto_zero_zero_uno", "meno_uno"]:
                repetitions_intervals[string] = 0
            intervals["zero_punto_uno"] += 1
        elif temporal_difference <= 1:
            repetitions_intervals["uno"] += 1
            if repetitions_intervals["uno"] > 1:
                furhat.say(text="Si, sto proprio migliorando!")
                repetitions_intervals["uno"] = 0
            else:
                furhat.say(text="Sto migliorando!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "piu_uno", "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["uno"] += 1
        else:
            furhat.gesture(body=emotionGestureDefinition.SurprisePositive)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["piu_uno"] += 1
    else:
        if temporal_difference >= -0.0009:
            repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] > 1:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadLow)
                repetitions_intervals["meno_zero_punto_zero_zero_zero_nove"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressDisgustLow)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "zero_punto_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "meno_zero_punto_zero_zero_uno", "piu_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
        elif temporal_difference >= -0.001:
            repetitions_intervals["meno_zero_punto_zero_zero_uno"] += 1
            if repetitions_intervals["meno_zero_punto_zero_zero_uno"] > 2:
                furhat.say(text="Non dovevo!")
                repetitions_intervals["meno_zero_punto_zero_zero_uno"] = 0
            else:
                furhat.gesture(body=emotionGestureDefinition.ExpressSadMedium)
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "piu_uno",
                           "uno", "zero_punto_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_zero_punto_zero_zero_uno"] += 1
        elif temporal_difference >= -1:
            repetitions_intervals["meno_uno"] += 1
            if repetitions_intervals["meno_uno"] > 1:
                furhat.say(text="Non è stata per nulla una buona mossa!")
                repetitions_intervals["meno_uno"] = 0
            else:
                furhat.say(text="Non è stata una buona mossa!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "piu_uno",
                           "meno_zero_punto_zero_zero_uno", "meno_zero_punto_zero_zero_zero_nove"]:
                repetitions_intervals[string] = 0
            intervals["meno_uno"] += 1
        else:
            furhat.say(text="Così non va proprio bene!")
            for string in ["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno", "meno_uno",
                           "zero_punto_zero_zero_zero_zero_uno", "zero_punto_uno", "uno", "piu_uno",
                           "meno_zero_punto_zero_zero_zero_nove", "meno_zero_punto_zero_zero_uno"]:
                repetitions_intervals[string] = 0
            intervals["meno_meno_uno"] += 1

    time.sleep(3.5)


def check_intervals(intervals, temporal_difference, current_state, reward):
    if is_terminal_state(current_state):
        intervals["goal_interval"] += 1
    elif reward == -1:
        intervals["no_goal"] += 1
    elif temporal_difference >= 0:
        if temporal_difference <= 0.000000001:
            intervals["zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.00001:
            intervals["zero_punto_zero_zero_zero_zero_uno"] += 1
        elif temporal_difference <= 0.1:
            intervals["zero_punto_uno"] += 1
        elif temporal_difference <= 1:
            intervals["uno"] += 1
        else:
            intervals["piu_uno"] += 1
    else:
        if temporal_difference >= -0.0009:
            intervals["meno_zero_punto_zero_zero_zero_nove"] += 1
        elif temporal_difference >= -0.001:
            intervals["meno_zero_punto_zero_zero_uno"] += 1
        elif temporal_difference >= -1:
            intervals["meno_uno"] += 1
        else:
            intervals["meno_meno_uno"] += 1


# Definisco una funzione per far partire il training dell'agente.
def training():
    global Q_table
    global starting_state
    global state
    global finish
    global behavior
    # Definisco i parametri di training.
    epsilon = 0.95  # Probabilità con cui dovremmo intraprendere l'azione migliore (invece di un'azione casuale).
    discount_factor = 0.9  # Fattore di sconto per ricompense future. Importanza delle ricompense future.
    learning_rate = 0.9  # Velocità con cui l'AI dovrebbe imparare.In che misura le nuove inf sovrascrivono le vecchie.
    num_episodes = 31
    max_steps_per_episodes = 15  # L'agente AI eseguirà massimo 15 step per episodio.

    # Creo un array per tenere traccia di come variano gli errori di differenza temporale nel tempo in ogni stato.
    variations_of_TDRL = []
    first = True
    converge = True
    episode_converge = -1
    first_solution = -1
    count_converge = 0

    # Creo un file di log.
    sourceFile = open('log.txt', 'w')

    # Button Stop
    button_stop = tk.Button(canvas, width=8, text="STOP", font="TimesNewRoman 13 italic bold")
    canvas.create_window(1350, 80, anchor=NW, window=button_stop)
    button_stop.configure(background="red", relief=RAISED, fg="white")
    button_stop.configure(command=partial(close, sourceFile))

    # ScrollBar per l'interfaccia.
    wrapper = LabelFrame(window, background="lightgreen", width=700, height=490)
    wrapper.pack(fill="both", expand="yes")
    my_canvas = Canvas(wrapper, background="lightgreen", width=700, height=490)
    my_canvas.config(width=700, height=490)
    my_canvas.pack(side=LEFT, expand=True, fill=BOTH)
    my_scrollbar = ttk.Scrollbar(wrapper, orient=VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    my_canvas.config(yscrollcommand=my_scrollbar.set)

    pad = 0

    # Definisco un array per monitorare quante volte si entra in un determinato intervallo.
    intervals = {"goal_interval": 0, "no_goal": 0, "zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno": 0,
                 "zero_punto_zero_zero_zero_zero_uno": 0, "zero_punto_uno": 0, "uno": 0, "piu_uno": 0,
                 "meno_zero_punto_zero_zero_zero_nove": 0, "meno_zero_punto_zero_zero_uno": 0, "meno_uno": 0,
                 "meno_meno_uno": 0}

    # Definisco un array per monitorare quante volte consecutive si entra in un determinato intervallo.
    repetitions_intervals = {"zero_punto_zero_zero_zero_zero_zero_zero_zero_zero_uno": 0, "meno_uno": 0,
                             "zero_punto_zero_zero_zero_zero_uno": 0, "zero_punto_uno": 0, "uno": 0, "piu_uno": 0,
                             "meno_zero_punto_zero_zero_zero_nove": 0, "meno_zero_punto_zero_zero_uno": 0}

    # Eseguo 50 episodi di allenamento.
    for episode in range(1, num_episodes):
        if not finish:
            if episode > 1:
                my_canvas.delete("all")
                furhat.say(text="Riproviamo")
                time.sleep(3)

        # Ottengo la locazione iniziale per questo episodio.
        current_state = starting_state
        red_row_index, red_column_index, yellow_row_index, yellow_column_index = index_location(state[current_state])

        count = 0
        reward = 0
        # Creo una matrice che mi servirà per vedere quando converge la Q_table.
        old_Q_table = np.copy(Q_table)

        if not finish:
            print("\nLocazione iniziale episodio ", episode, ":")
            print_environment(red_row_index, red_column_index, yellow_row_index, yellow_column_index)

            pad += 100
            # my_canvas.create_text(450, pad, fill="green", font="TimesNewRoman 16 italic bold",
            #                     text="Locazione iniziale episodio " + str(episode) + " :")

            my_canvas.create_text(760, 30, fill="green", font="TimesNewRoman 16 italic bold",
                                  text="Locazione iniziale episodio " + str(episode) + " :", tags="init")
            pad += 90
            # print_in_interface(red_row_index, red_column_index, yellow_row_index, yellow_column_index, my_canvas, pad)
            new_print_in_interface(-1, -1, -1, -1, red_row_index, red_column_index, yellow_row_index,
                                   yellow_column_index, my_canvas)
            # my_canvas.config(scrollregion=my_canvas.bbox("all"))
            # my_canvas.yview_moveto(1.0)
            time.sleep(1.5)

        # Continuo a intraprendere azioni fino a raggiungere uno stato terminale,
        # oppure il numero massimo di steps per episodio.
        while not is_terminal_state(current_state) and count != max_steps_per_episodes:
            count += 1
            if not finish:
                print_environment_in_file_log(red_row_index, red_column_index, yellow_row_index, yellow_column_index,
                                              sourceFile)

            # Scelgo quale azione intraprendere.
            action_index = get_next_action(current_state, epsilon)

            # Memorizzo il vecchio stato.
            old_state = current_state

            # Memorizzo i vecchi indici dei cubi
            old_red_row_index = red_row_index
            old_red_column_index = red_column_index
            old_yellow_row_index = yellow_row_index
            old_yellow_column_index = yellow_column_index

            # Eseguo l'azione scelta e passo allo stato successivo.
            current_state = get_next_state(action_index, state[current_state])
            red_row_index, red_column_index, yellow_row_index, yellow_column_index = index_location(
                state[current_state])

            # Ricevo la ricompensa per il passaggio al nuovo stato e calcolo la differenza temporale.
            if is_terminal_state(current_state):
                reward = 1.
            elif count == max_steps_per_episodes:
                reward = -1.
            else:
                reward = -0.001

            if not finish:
                print('\nold state: ', old_state, '->', state[old_state], ',  action: ', action_index, ',  new_state: ',
                      current_state, '->', state[current_state], ',  reward : ', reward, 'episode : ', episode,
                      file=sourceFile)

            old_Q_value = Q_table[old_state, action_index]
            max_future_Q_value = max_future_q_value(current_state)
            # print("\n\n max future: ", max_future_Q_value, "\n", file=sourceFile)
            temporal_difference = reward + (discount_factor * max_future_Q_value) - old_Q_value

            if not finish:
                print_environment(red_row_index, red_column_index, yellow_row_index, yellow_column_index)
                pad += 90
                # print_in_interface(red_row_index, red_column_index, yellow_row_index, yellow_column_index,
                # my_canvas, pad)

                print('temporal difference: ', temporal_difference, file=sourceFile)
                if count == 1:
                    my_canvas.delete("init")

                new_print_in_interface(old_red_row_index, old_red_column_index, old_yellow_row_index,
                                       old_yellow_column_index, red_row_index, red_column_index, yellow_row_index,
                                       yellow_column_index, my_canvas)
                # my_canvas.config(scrollregion=my_canvas.bbox("all"))
                # my_canvas.yview_moveto(1.0)

                if behavior == 1:
                    spoken_behavior(current_state, temporal_difference, reward, intervals, repetitions_intervals)
                elif behavior == 2:
                    emotion_behavior(current_state, temporal_difference, reward, intervals, repetitions_intervals)
                else:
                    mixed_behavior2(current_state, temporal_difference, reward, intervals, repetitions_intervals)

                variations_of_TDRL.append(temporal_difference)

            # Aggiorno i valori Q per le coppie stato azione.
            Q_table[old_state, action_index] = old_Q_value + (learning_rate * temporal_difference)

            if not finish:
                print('\nQ_table\n', Q_table, file=sourceFile)

                if reward != -0.001:
                    print_environment_in_file_log(red_row_index, red_column_index, yellow_row_index,
                                                  yellow_column_index, sourceFile)

                    print('\n----------------------------- NUOVO STEP -------------------------------------\n',
                          file=sourceFile)
            else:
                check_intervals(intervals, temporal_difference, current_state, reward)
            # Configuro il comando del bottone Stop
            button_stop.configure(command=partial(stop, starting_state, current_state, temporal_difference, episode,
                                                  intervals, episode_converge, sourceFile),
                                  font="TimesNewRoman 13 italic bold")

        if reward == 1 and first:
            first = False
            first_solution = episode

        # print('\nQ_table\n', Q_table, file=sourceFile)

        if converge and np.min((Q_table - old_Q_table)) > -0.01 and np.max((Q_table - old_Q_table)) < 0.01:
            count_converge += 1
            if count_converge == 3:
                episode_converge = episode
                converge = False
        else:
            count_converge = 0

    print("\nConvergenza VERA Q_table avvenuta all'episodio: ", episode_converge, file=sourceFile)
    print("\nIntervals", intervals, file=sourceFile)
    print("\nConvergenza VERA Q_table avvenuta all'episodio: ", episode_converge)
    print("\nIntervals", intervals)

    if not finish:
        print('variations_of_TDRL: ', variations_of_TDRL, '\n', "len: ", len(variations_of_TDRL), file=sourceFile)
        print('min_tdrl: ', np.min(variations_of_TDRL), '\nmax_tdrl: ', np.max(variations_of_TDRL), file=sourceFile)
        print("\n Prima soluzione trovata all'episodio: ", first_solution, file=sourceFile)
        print("\n La Q_table converge all'episodio:", episode_converge, file=sourceFile)
        print("\n Training completato!")
        sourceFile.close()

        print('variations_of_TDRL: ', variations_of_TDRL, '\n', "len: ", len(variations_of_TDRL))
        print('min_tdrl: ', np.min(variations_of_TDRL), '\nmax_tdrl: ', np.max(variations_of_TDRL))

        print('\n----------------------------- FINE FASE TRAINING -------------------------------------\n')

        # Configuro il comando del bottone Stop.
        button_stop.configure(command=partial(close, sourceFile))

        pad += 100
        my_canvas.create_text(450, pad, fill="green", font="TimesNewRoman 16 italic bold", text="Fine fase Training")
        # my_canvas.config(scrollregion=my_canvas.bbox("all"))
        # my_canvas.yview_moveto(1.0)

        furhat.say(text="Il training è terminato, adesso ti mostro cosa ho imparato.")
        time.sleep(5.5)
        # Mostro cosa ha appreso l'agente.
        show_what_AI_learned(my_canvas, pad, button_stop, sourceFile)


# Definisco una funzione che esegue un episodio per vedere come si comporta l'agente dopo il training.
def show_what_AI_learned(my_canvas, pad, button_stop, sourceFile):
    global starting_state
    global state
    global finish

    # Configuro il bottone Stop.
    button_stop.configure(command=partial(close, sourceFile))

    # Ottengo una locazione iniziale per questo episodio.
    current_state = starting_state

    # Ottengo gli indici dei cubi in base allo stato.
    red_row_index, red_column_index, yellow_row_index, yellow_column_index = index_location(state[current_state])

    # Stampo l'ambiente allo stato iniziale.
    print_environment(red_row_index, red_column_index, yellow_row_index, yellow_column_index)
    pad += 100
    # my_canvas.create_text(450, pad, fill="green", font="TimesNewRoman 16 italic bold", text="Locazione iniziale")
    pad += 100
    my_canvas.delete("all")
    my_canvas.create_text(450, 30, fill="green", font="TimesNewRoman 16 italic bold", text="Locazione iniziale")
    # my_canvas.create_text(450, pad, fill="green", font="TimesNewRoman 16 italic bold", text="Locazione iniziale")
    # print_in_interface(red_row_index, red_column_index, yellow_row_index, yellow_column_index, my_canvas, pad)
    new_print_in_interface(-1, -1, -1, -1, red_row_index, red_column_index, yellow_row_index, yellow_column_index,
                           my_canvas)
    # my_canvas.config(scrollregion=my_canvas.bbox("all"))
    # my_canvas.yview_moveto(1.0)
    time.sleep(1)

    while not is_terminal_state(current_state) and not finish:
        pad += 100

        # Memorizzo i vecchi indici dei cubi
        old_red_row_index = red_row_index
        old_red_column_index = red_column_index
        old_yellow_row_index = yellow_row_index
        old_yellow_column_index = yellow_column_index

        # Scelgo quale azione intraprendere passandogli 1 come valore di epsilon.
        action_index = get_next_action(current_state, 1)

        # Eseguo l'azione scelta e passo allo stato successivo.
        current_state = get_next_state(action_index, state[current_state])

        # Ottengo gli indici dei cubi in base allo stato.
        red_row_index, red_column_index, yellow_row_index, yellow_column_index = index_location(state[current_state])

        # Stampo l'ambiente.
        print_environment(red_row_index, red_column_index, yellow_row_index, yellow_column_index)
        # print_in_interface(red_row_index, red_column_index, yellow_row_index, yellow_column_index, my_canvas, pad)
        new_print_in_interface(old_red_row_index, old_red_column_index, old_yellow_row_index,
                               old_yellow_column_index, red_row_index, red_column_index, yellow_row_index,
                               yellow_column_index, my_canvas)
        # my_canvas.config(scrollregion=my_canvas.bbox("all"))
        # my_canvas.yview_moveto(1.0)
        time.sleep(0.5)

    furhat.say(text="Visto? Cosa ne pensi?")
    time.sleep(2)
    furhat.gesture(body=emotionGestureDefinition.ExpressHappyHigh)


# Definisco alcune variabili globali.
goal = -1
starting_state = -1
finish = False
behavior = choice_behavior()
choice_location()


def start():
    global state
    global starting_state
    goal_red_row_index, goal_red_column_index, goal_yellow_row_index, goal_yellow_column_index = \
        index_location(state[goal])

    # Stampo la soluzione che l'agente deve imparare.
    print("\nLa soluzione da indovinare e':", state[goal])
    print_environment(goal_red_row_index, goal_red_column_index, goal_yellow_row_index, goal_yellow_column_index)

    # Ottengo uno stato iniziale che sarà lo stesso per ogni episodio.
    starting_state = get_starting_location()

    # Faccio partire il training dell'agente.
    training()


if __name__ == "__main__":
    window.mainloop()
