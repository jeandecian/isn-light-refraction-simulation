# Projet Noel version 3.3.3.19.5.23

from tkinter import *
import math

def getEnvironmentValues(value):
    image = air
    graphText = "AIR"
    fillColor = "white"
    
    if value == 2.42:
        image = diamant
        graphText = "DIAMANT"
        fillColor = "black"
    elif value == 1.50:
        image = verre
        graphText = "PLEXIGLAS/VERRE"
        fillColor = "black"
    elif value == 1.36:
        image = ethanol
        graphText = "ETHANOL"
    elif value == 1.33:
        image = eau
        graphText = "EAU"
        fillColor = "black"

    return image, graphText, fillColor

def graphe():
    # fonction qui permet de calculer la valeur de l'angle réfracté et de tracer les angles réfracté, incident et réfléchi

    global incident, reflechi, refracte, angle_refracte, milieu1, milieu2
    global air, eau, ethanol, verre, diamant, text1, text2

    try:
        # la valeur du scale prend la valeur de la saisie
        scale_angle.set(saisie.get())

    except:
        saisie.set(0.0)

    sinI2 = value1.get() * math.sin(math.radians(saisie.get())) / value2.get()

    a.set("sin(i2) = " + str(value1.get()) + "*sin(" + str(saisie.get()) + ")/" + str(value2.get()))
    b.set("sin(i2) = " + str(sinI2))

    if sinI2 > 1:
        c.set("i2 = ø")
    else:
        c.set("i2 = " + str(math.degrees(math.asin(sinI2))))

    # on trace les angles incident et réfléchi selon la valeur saisie
    tanSaisie = math.tan(math.radians(saisie.get()))
    if 0 <= saisie.get() < 45:
        X = 250 * (1 - tanSaisie)
        Graphe.delete(incident, reflechi)
        incident = Graphe.create_line(X,0,250,250, width=3, fill="red")
        reflechi = Graphe.create_line(250,250,500-X,0, width=3, fill="orange")
    elif 45 < saisie.get() <= 90:
        Y = 250 * (1 - 1/tanSaisie)
        Graphe.delete(incident, reflechi)
        incident = Graphe.create_line(0,Y,250,250, width=3, fill="red")
        reflechi = Graphe.create_line(250,250,500,Y, width=3, fill="orange")
    elif saisie.get() == 45:
        Graphe.delete(incident, reflechi)
        incident = Graphe.create_line(0,0,250,250, width=3, fill="red")
        reflechi = Graphe.create_line(250,250,500,0, width=3, fill="orange")
    else:
        Graphe.delete(incident, reflechi)

    try:
        # on calcul la valeur de l'angle réfracté
        if 0 <= saisie.get() <= 90:
            angle_refracte = round(math.degrees(math.asin(sinI2)),1)
            resultat.set("Angle réfracté : "+str(angle_refracte)+"°")
        else:
            saisie.set(42.0)
            angle_refracte = -1

    except ValueError:
        resultat.set("Le phénomène de diffraction n'existe pas pour cette valeur d'angle incident ! Tout est réfléchi !")
        Graphe.delete(refracte)
        angle_refracte = -1

    # on trace l'angle réfracté selon le résultat
    Graphe.delete(refracte)
    tanAngleRefracte = math.tan(math.radians(angle_refracte))
    if 0 <= angle_refracte < 45:
        X = 250 * (1 + tanAngleRefracte)
        refracte = Graphe.create_line(250,250,X,500, width=3, fill="green")
    elif 45 < angle_refracte <= 90:
        Y = 250 * (1 + 1/tanAngleRefracte)
        refracte = Graphe.create_line(250,250,500,Y, width=3, fill="green")
    elif angle_refracte == 45:
        refracte = Graphe.create_line(250,250,500,500, width=3, fill="green")

    # associe une image au milieu 1 selon le milieu choisi
    Graphe.delete(milieu1, text1)
    image, graphText, fillColor = getEnvironmentValues(value1.get())

    milieu1 = Graphe.create_image(0,0, image=image, anchor="nw")
    text1 = Graphe.create_text(10,240, text="MILIEU 1 : "+graphText, font=("Arial", 20), fill=fillColor, anchor="sw")

    # associe une image au milieu 2 selon le milieu choisi
    Graphe.delete(milieu2, text2)
    image, graphText, fillColor = getEnvironmentValues(value2.get())

    milieu2 = Graphe.create_image(0,250, image=image, anchor="nw")
    text2 = Graphe.create_text(10,490, text="MILIEU 2 : "+graphText, font=("Arial", 20), fill=fillColor, anchor="sw")

    Graphe.tag_lower(milieu1)
    Graphe.tag_lower(milieu2)

    # fonction qui s'actualise tous les 100ms
    Main.after(100, graphe)

def update(self):
    # fonction qui associe à la saisie la valeur du scale

    # la valeur de la saisie prend la valeur du scale
    saisie.set(scale_angle.get())

# on crée une fenetre de taille non-modifiable
Main = Tk()
Main.title("Phénomène de réfraction de la lumière")
Main.geometry("1070x715")
Main.resizable(width=False, height=False)

# on importe les images
imagesPath = "images/"
air = PhotoImage(file= imagesPath + "air.gif")
eau = PhotoImage(file= imagesPath + "eau.gif")
ethanol = PhotoImage(file= imagesPath + "ethanol.gif")
verre = PhotoImage(file= imagesPath + "verre.gif")
diamant = PhotoImage(file= imagesPath + "diamant.gif")

# on crée un menu
menubar = Menu(Main)

menu1 = Menu(menubar, tearoff=0)
menubar.add_command(label="Quitter", command=Main.destroy)

Main.config(menu=menubar)

# on crée un label-frame destiné à afficher des messages
message_box = LabelFrame(Main, text="BOITE DE DIALOGUE", bg='bisque', padx=20, pady=20)
message_box.pack(side=BOTTOM, fill=X)

# on crée un label-frame destiné à contenir le scale
scale_box = LabelFrame(Main, text="SCALE", bg='bisque', padx=20, pady=20)
scale_box.pack(side=RIGHT, fill=Y)

# on crée un label-frame destiné à contenur le canvas
graphe_frame = LabelFrame(Main, text="GRAPHE", bg='bisque', padx=20, pady=20)
graphe_frame.pack(side=RIGHT, fill=Y)

# on crée le canvas
Graphe = Canvas(graphe_frame, bg='white', height=500, width=500)
Graphe.pack()

# on crée l'axe des abscisses, l'axe X ou la dioptre en forme continue
Graphe.create_line(0,250,500,250, width=3, fill="black")

# on crée l'axe des ordonnées, l'axe Y ou la normale en forme discontinue
Z1 = 0
Z2 = 20

for i in range(13):
    Graphe.create_line(250,Z1,250,Z2, width=3, fill="brown")
    Z1 += 40
    Z2 += 40

# on initialise quelques variables
incident = Graphe.create_line(0,0,0,0, width=0, fill="white")
reflechi = Graphe.create_line(250,250,250,250, width=0, fill="white")
refracte = Graphe.create_line(250,250,250,250, width=0, fill="white")
milieu1 = Graphe.create_rectangle(0,0,500,250, width=0, fill="white")
milieu2 = Graphe.create_rectangle(0,250,500,500, width=0, fill="grey")
text1 = Graphe.create_text(10,10, text="", font=("Arial", 20), anchor="nw")
text2 = Graphe.create_text(10,260, text="", font=("Arial", 20), anchor="nw")

# on déclare et on initialise "scale_angle"
scale_angle = DoubleVar()
scale_angle.set(42)

# on crée le scale
Scale(scale_box, from_=90, to=0, resolution=0.1, orient=VERTICAL, tickinterval=10, variable=scale_angle, command=update).pack(side=RIGHT, fill=Y)

# on crée un label-frame destiné à contenir des radios-boutons des deux milieux
milieux_frame = LabelFrame(Main, text="MILIEUX", bg='bisque', padx=20, pady=20)
milieux_frame.pack(side=TOP, fill=X)

# on crée un label-frame qui va contenir des radios-boutons pour le milieu 1
Fen1 = LabelFrame(milieux_frame, text="MILIEU 1", bg='bisque', padx=20, pady=20)
Fen1.pack(side=LEFT)

# on déclare et initialise "value1"
value1 = DoubleVar()
value1.set(1)

# radios-boutons pour le niveau 1
Radiobutton(Fen1, text="Air (1)", bg='bisque', height=2, width=15, variable=value1, value=1, command=graphe).grid(row=0, column=1)
Radiobutton(Fen1, text="Eau (1.33)", bg='bisque', height=2, width=15, variable=value1, value=1.33, command=graphe).grid(row=1, column=1)
Radiobutton(Fen1, text="Ethanol (1.36)", bg='bisque', height=2, width=15, variable=value1, value=1.36, command=graphe).grid(row=2, column=1)
Radiobutton(Fen1, text="Plexiglas/Verre (1.50)", bg='bisque', height=2, width=15, variable=value1, value=1.50, command=graphe).grid(row=3, column=1)
Radiobutton(Fen1, text="Diamant (2.42)", bg='bisque', height=2, width=15, variable=value1, value=2.42, command=graphe).grid(row=4, column=1)

# on crée un label-frame qui va contenir des radios-boutons pour le milieu 2
Fen2 = LabelFrame(milieux_frame, text="MILIEU 2", bg='bisque', padx=20, pady=20)
Fen2.pack(side=RIGHT)

# on déclare et initialise "value2"
value2 = DoubleVar()
value2.set(1.33)

# radios-boutons pour le niveau 2
Radiobutton(Fen2, text="Air (1)", bg='bisque', height=2, width=15, variable=value2, value=1, command=graphe).grid(row=0, column=1)
Radiobutton(Fen2, text="Eau (1.33)", bg='bisque', height=2, width=15, variable=value2, value=1.33, command=graphe).grid(row=1, column=1)
Radiobutton(Fen2, text="Ethanol (1.36)" , bg='bisque', height=2, width=15, variable=value2, value=1.36, command=graphe).grid(row=2, column=1)
Radiobutton(Fen2, text="Plexiglas/Verre (1.50)" , bg='bisque', height=2, width=15, variable=value2, value=1.50, command=graphe).grid(row=3, column=1)
Radiobutton(Fen2, text="Diamant (2.42)", bg='bisque', height=2, width=15, variable=value2, value=2.42, command=graphe).grid(row=4, column=1)

# on déclare "saisie", "resultat", "angle_refracte" puis on initialise "saisie"
saisie, resultat, angle_refracte = DoubleVar(), DoubleVar(), DoubleVar()
saisie.set(42)

# on crée un frame destiné à contenir la légende pour le canvas
caption_frame = Frame(graphe_frame, bg='bisque', padx=20, pady=20)
caption_frame.pack(side=TOP, fill=Y)

Label(caption_frame, text="     ", bg="black").grid(row=0, column=1)
Label(caption_frame, text="     ", bg="brown").grid(row=0, column=3)
Label(caption_frame, text="     ", bg="red").grid(row=1, column=1)
Label(caption_frame, text="     ", bg="orange").grid(row=1, column=3)
Label(caption_frame, text="     ", bg="green").grid(row=1, column=5)
Label(caption_frame, text="  Dioptre  ", bg="bisque").grid(row=0, column=2)
Label(caption_frame, text="  Normale  ", bg="bisque").grid(row=0, column=4)
Label(caption_frame, text="  Angle incident  ", bg="bisque").grid(row=1, column=2)
Label(caption_frame, text="  Angle réfléchi  ", bg="bisque").grid(row=1, column=4)
Label(caption_frame, text="  Angle réfracté  ", bg="bisque").grid(row=1, column=6)

# on crée un label-frame destiné à contenir la saisie de l'angle incident
saisie_frame = LabelFrame(Main, text="ANGLE INCIDENT", bg="bisque", padx=20, pady=20)
saisie_frame.pack(side=TOP, fill=X)

# permet de crée une zone centrée
centre = Frame(saisie_frame, bg='bisque')
centre.pack(side=TOP)

# où l'on saisie la valeur de l'angle incident
Label(centre, text='Angle incident :', bg='bisque').grid(row=0, column=1)
Entry(centre, textvariable=saisie, bg='bisque', width=6).grid(row=0, column=2)
Label(centre, text="°", bg='bisque').grid(row=0, column=3)

# on affiche le message
Label(message_box, textvariable=resultat, bg='bisque').pack()

# on crée un label-frame destiné à contenir le détail du calcul de la valeur de l'angle réfracté
calcul_frame = LabelFrame(Main, text="CALCUL", bg='bisque', padx=20, pady=20)
calcul_frame.pack(side=TOP, fill="both")

# on déclare et initialise les variables "a", "b", "c"
a, b, c = StringVar(), StringVar(), StringVar()
a.set("sin(i2) = "+str(value1.get())+"*sin("+str(saisie.get())+")/"+str(value2.get()))
b.set("sin(i2) = "+str(value1.get()*math.sin(math.radians(saisie.get()))/value2.get()))
c.set("i2 = "+str(math.degrees(math.asin(value1.get()*math.sin(math.radians(saisie.get()))/value2.get()))))

# on affiche le détail du calcul de la valeur de l'angle réfracté    
Label(calcul_frame, text="FORMULE : n1*sin(i1) = n2*sin(i2)", bg="bisque").pack()
Label(calcul_frame, text="---------------------------------", bg="bisque").pack()
Label(calcul_frame, text="", bg="bisque").pack()
Label(calcul_frame, text="sin(i2) = n1*sin(i1)/n2", bg="bisque").pack()
Label(calcul_frame, textvariable=a, bg="bisque").pack()
Label(calcul_frame, textvariable=b, bg="bisque").pack()
Label(calcul_frame, textvariable=c, bg="bisque").pack()
Label(calcul_frame, text="", bg="bisque").pack()
Label(calcul_frame, text="", bg="bisque").pack()

graphe()

Main.mainloop()
