import pandas as pd
import tkinter as tk
from tkinter.messagebox import askyesno
#from PyQt4 import QtGui

QUITTER = False
SELECT = ""
RESS = []

def normalise(txt, in_list):
    '''
    Prend une chaine de caractère et la renvoie en retirant
    ses accents et ses espaces (  _ - ')
    Remplace également Saint par st, Mont par mt et Sous par ss

    Si la station entrée est dans la liste, on enlève :
        - accents
        - espaces
        - majuscules
        - on normalise saint, mont et sous

    Sinon, on enlève juste :
        - majuscules
        - accents
    '''

    #On liste tous les caractères avec accent et leur fait
    #correspondre les caractères sans accent
    accents = "àâçéèêëîïìôùûüÿ"
    no_accents = "aaceeeeiiiouuuy"
    #On liste tous les caractères considérés comme des espaces
    spaces = " _-'"
    #Nouvelle string qu'on va compléter au fur et a mesure
    result = ""
    transl = txt.lower().replace("saint", "st").replace("mont ", "mt").replace("sous", "ss")
    #Pour chaque caractère de notre string
    if in_list:
        for character in transl:
            i = accents.find(character)
            j = spaces.find(character)
            #Si notre caractère a un accent, on le remplace
            if i >= 0:
                result += no_accents[i]
            #Si c'est pas un espace, on remplit la nouvelle string
            elif j < 0:
                result += character
    else:
        for character in txt.lower():
            i = accents.find(character)
            if i >= 0:
                result += no_accents[i]
            else:
                result += character
    return result

def gui(df):
    fenetre = tk.Tk()
    fenetre.title("Adding data")

    #fenetre.eval('tk::PlaceWindow %s center' % fenetre.winfo_pathname(fenetre.winfo_id()))

    you = tk.Label(fenetre, text="You played : Pichu")
    against = tk.Label(fenetre, text="Your opponent was a lv.9 : ")
    opp_sel = tk.StringVar()
    opp_sel.set("Mario")
    lab_opp_sel = tk.Label(fenetre, textvariable=opp_sel)
    opp_ent = tk.StringVar()
    entry = tk.Entry(fenetre, textvariable=opp_ent, width=22)
    liste_scroll = tk.Frame(fenetre)
    liste = tk.Listbox(liste_scroll)
    scroll = tk.Scrollbar(liste_scroll)

    and_you = tk.Label(fenetre, text="and you : ")
    won_lost = tk.StringVar()
    won_lost.set("win")
    rb_won = tk.Radiobutton(fenetre, text="won", variable=won_lost, value="win")
    rb_lost = tk.Radiobutton(fenetre, text="lost", variable=won_lost, value="lose")

    def press_enter():
        '''
        Lorsque l'utilisateur appuye sur Entrée, on valide en détruisant la fenêtre
        On aurait utilisé quit() à la place s'il y avait besoin de récupérer des
        données gérées par la fenêtre
        '''
        if liste.curselection():
            global SELECT
            global RESS
            SELECT = RESS[int(liste.curselection()[0])]
            if askyesno(title="Are you sure ?", \
                message="You " + won_lost.get() + " against " \
                + opp_sel.get() + "\nIs that so ?"):
                fenetre.destroy()
            else:
                entry.focus()

    def quitter():
        '''
        Indique que l'utilisateur a cliqué sur le bouton Quitter via la variable
        globale QUITTER
        '''
        global QUITTER
        QUITTER = True
        fenetre.destroy()

    def update():
        '''
        Permet de recharger la liste à chaque fois que l'Entry est modifiée
        par l'utilisateur
        '''
        global RESS
        liste.delete("0", "end")
        RESS = []
        for char in df.index.values:
            if normalise(opp_ent.get(), True) in normalise(char, True):
                liste.insert("end", char)
                RESS.append(char)
        if len(RESS) == 1:
            liste.selection_set(0)
            liste.activate(0)
            opp_sel.set(liste.get(liste.curselection()[0]))

    def press_down():
        '''
        Déplace la sélection après avoir appuyé sur la flèche du bas
        '''
        if liste.curselection():
            index = int(liste.curselection()[0])
            if index != len(RESS):
                liste.selection_set(index+1)
                liste.selection_clear(index)
                liste.activate(index+1)
                liste.see(index+1)
        else:
            liste.selection_set(0)
            liste.activate(0)
            liste.see(0)

    def press_up():
        '''
        Déplace la sélection après avoir appuyé sur la flèche du haut
        '''
        if liste.curselection():
            index = int(liste.curselection()[0])
            if index != 0:
                liste.selection_set(index-1)
                liste.selection_clear(index)
                liste.activate(index-1)
                liste.see(index-1)
        else:
            liste.selection_set(0)
            liste.activate(0)
            liste.see(0)

    def selected():
        opp_sel.set(liste.get(liste.curselection()[0]))

    bouton_valider = tk.Button(fenetre, text="Confirm", command=lambda:press_enter())

    fenetre.protocol("WM_DELETE_WINDOW", quitter)
    entry.bind("<Return>", lambda x: press_enter())
    liste.bind("<Double-1>", lambda x: press_enter())
    liste.bind("<Return>", lambda x: press_enter())
    liste.bind("<Escape>", lambda x: quitter())
    fenetre.bind("<Up>", lambda x: press_up())
    fenetre.bind("<Down>", lambda x: press_down())
    fenetre.bind("<Escape>", lambda x: quitter())
    liste.bind("<<ListboxSelect>>", lambda x: selected())

    opp_ent.trace("w", lambda x, y, z: update())

    you.grid(row=0, columnspan=3)
    against.grid(row=1, columnspan=1)
    lab_opp_sel.grid(row=1, column=1, columnspan=2)
    entry.grid(row=2, column=0, columnspan=3)
    liste_scroll.grid(row=3, column=0, columnspan=3)
    liste.pack(side="left")
    scroll.pack(side="right", fill="y")
    and_you.grid(row=4, column=0)
    rb_won.grid(row=4, column=1)
    rb_lost.grid(row=4, column=2)
    bouton_valider.grid(row=5, column=0, columnspan=3)
    liste.config(yscrollcommand=scroll.set)
    scroll.config(command=liste.yview)


    update()

    fenetre.after(1, lambda: fenetre.focus_force())
    entry.focus()

    fenetre.mainloop()

    return (SELECT, won_lost.get())

def main():
    global QUITTER
    while QUITTER == False:
        try:
            df = pd.read_csv("./csv/pichu_lv9.csv", index_col=False)
            df.set_index("opponent", inplace=True)
            (opp, result) = gui(df)
            df.loc[opp][result] += 1
            df.reset_index(inplace=True, drop=False)
            df.to_csv("./csv/pichu_lv9.csv", index=False)
        except:
           None
    return

main()