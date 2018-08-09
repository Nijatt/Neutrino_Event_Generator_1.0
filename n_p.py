__author__ = 'Nijat Shukurov' \
             'id: 1784222' \
             '400 project assigment' \
             'neutrino and nucleon quasi elastic scatterring event generator'

import random
from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import xlwt
import tkMessageBox
from tkFileDialog import asksaveasfilename
import tkFileDialog
import FileDialog
##import os

#"a.py: sys.argv[0]=", sys.argv[0]
#"a.py: __file__=", __file__
#"a.py: os.getcwd()=", os.getcwd()

neutrino_types=['electron','muon','tao']
particle_kind=['particle','antiparticle']
particle_charge=['-','+','0']
global Mev_Energy
Mev_Energy=(10**6) ##Ev
c=3*(10**8) ##m/s


##Nucleons
class Proton():
    mass=938.28 ## Mev
    def __init__(self,energy,particle_kind):
        self.name="Proton"
        self.energy=energy
        self.particle_kind=particle_kind
        self.charge=particle_charge[0]

class Neutron():
    mass=939.57 ## Mev
    def __init__(self,energy,particle_kind):
        self.name="Neutron"
        self.energy=energy
        self.particle_kind=particle_kind
        self.charge=particle_charge[2]

##Leptons
class Neutrino():
    def __init__(self,neutrino_type,energy,particle_kind):
        self.name='Neutrino'
        self.neutrino_type=neutrino_type
        self.energy=energy ##Mev
        self.particle_kind=particle_kind
        self.cross_section=9.30*(10**(-42))*(((self.energy)*Mev_Energy)/(10*(10**6)))**2 ##cm^2

class Electron():
    mass=0.511 ## Mev
    def __init__(self,energy,particle_kind,scatter_angle):
        self.name="Electron"
        self.energy=energy
        self.particle_kind=particle_kind
        self.scatter_angle=scatter_angle
        if self.particle_kind==particle_kind[0]:
            self.particle_charge=particle_charge[0]
        else:
            self.particle_charge=particle_charge[1]

class Muon():
    def __init__(self,energy,particle_kind,scatter_angle):
        self.name="Muon"
        self.energy=energy
        self.particle_kind=particle_kind
        self.scatter_angle=scatter_angle
        if self.particle_kind==particle_kind[0]:
            self.particle_charge=particle_charge[0]
        else:
            self.particle_charge=particle_charge[1]

class Tao():
    def __init__(self,energy,particle_kind,scatter_angle):
        self.name="Tao"
        self.energy=energy
        self.particle_kind=particle_kind
        self.scatter_angle=scatter_angle
        if self.particle_kind==particle_kind[0]:
            self.particle_charge=particle_charge[0]
        else:
            self.particle_charge=particle_charge[1]


##QUASI ELASTIC COLLUSION
##=====================================Cos tita
def electron_scatter_cos_angle(neutrino_energy,electron_energy):
     ##fourmomentum change
     q=float((electron_energy*Mev_Energy/c)-(neutrino_energy*Mev_Energy/c))

     costita=1+((Neutron.mass*Mev_Energy*(q**2))/(neutrino_energy*Mev_Energy*(2*Neutron.mass*neutrino_energy*Mev_Energy+(q**2))))
     return costita

def electron_proton_scatter_energy(neutrino_energy,electron_energy):
    DELTA=(Proton.mass-Neutron.mass)
    return DELTA+(1/Proton.mass)*((((DELTA**2)-(Electron.mass**2))/2)+electron_energy*(electron_energy+DELTA))+electron_energy-neutrino_energy

def electron_neutron_scatter_energy(neutrino_energy,electron_energy):
    DELTA=(Neutron.mass-Proton.mass)
    return DELTA+(1/Proton.mass)*((((DELTA**2)-(Electron.mass**2))/2)+electron_energy*(electron_energy+DELTA))+electron_energy-neutrino_energy

def secant(f,x0,x1,E, TOL=0.001, NMAX=1000):
	"""
	Takes a function f, start values [x0,x1], tolerance value(optional) TOL and
	max number of iterations(optional) NMAX and returns the root of the equation
	using the secant method.
	"""
	n=1
	while n<=NMAX:
		x2 = x1 - f(E,x1)*((x1-x0)/(f(E,x1)-f(E,x0)))
		if x2-x1 < TOL:
			return x2
		else:
			x0 = x1
			x1 = x2
	return False


neutrino_energy_array=['Neutrino Energ data']
electron_cos_angle_array=['Electron scat. ang. cos(a) data']
electron_energy_array=['Electron energy data']
neutrino_cross_array=['Neutrino cross sec. data']

TOTAL_DATA=[]

#3=================test
def test_input():
    rn=False
    try:
        rnumber = int(run_number.get())
        rn=True
    except:
        tkMessageBox.showwarning("Run number input error!!", "Run number should be an integer type.")

    try:
        inital_En = int(inital_boundry.get())
        iE=True
    except:
        tkMessageBox.showwarning("Inital Energy input error!!", "Inital Energy should be an integer type.")

    try:
        final_En = int(final_boundry.get())
        if inital_En<=final_En:
            fE=True
        else:
            tkMessageBox.showwarning("Energy input error!!", "Inital Energy should be lower than Final Energy.")
            pass

    except:
        tkMessageBox.showwarning("Final Energy input error!!", "Final Energy should be an integer type.")
    try:
        nucleon_type = varia.get()
        nt=True
    except:
        tkMessageBox.showwarning("Nucleon type input error!!", "Nucleon type should be choosen from a RadiButton.")

    if rn==True and iE==True and fE==True and nt==True:
        event_generator(rnumber,inital_En,final_En,nucleon_type)
    else:
        pass

def event_generator(rnumber,inital_En,final_En,nucleon_type):
    '''intractive_root=Tk()
    intractive_root.wm_title('Interactive data')
    intractive_root.geometry("400x400+200+200")
    frame = Frame(intractive_root)
    canvas = Canvas(frame)'''


    event_root = Tk()
    event_root.wm_title("Event Data")  ## creating root title
    event_root.geometry("400x400+200+200")  ## creating root geometry
    nucleon_name=""
    for a in range(rnumber):
        print'    '
        print'------- event #',a,"-------"
        neutrino_energy = random.randint(inital_En,final_En)  ##generating energy
        neutrino_kind = particle_kind[1]
        neutrino = Neutrino(neutrino_types[0], neutrino_energy, neutrino_kind)
        if nucleon_type==1:
            print('v(anti) p--->e(anti) n')
            print "Neutrino energy=", neutrino_energy, "Mev"
            print "Neutrino cross section=", neutrino.cross_section
            electron_energy = secant(electron_proton_scatter_energy, -100, 100, neutrino_energy)
            print "Electron enegry=", electron_energy, "Mev"
            electron_scattering_angle = electron_scatter_cos_angle(neutrino_energy, electron_energy)
            print "Eletron scattering angle=", float(electron_scattering_angle)
            neutrino_energy_array.append(neutrino_energy)
            electron_cos_angle_array.append(electron_scattering_angle)
            electron_energy_array.append(electron_energy)
            neutrino_cross_array.append(neutrino.cross_section)

            nucleon_name="Proton"


            '''mytext='v(anti) p--->e(anti) n'+"\n"+"Neutrino energy="+ str(neutrino_energy)+ "Mev"+"\n"+"Neutrino cross section="+str(neutrino.cross_section)
            Label(canvas,
                  text=mytext,).pack()'''




        elif nucleon_type==2:
            print('v n--->e(-) p')
            print "Neutrino energy", neutrino_energy, "Mev"
            print "Neutrino cross section=", neutrino.cross_section
            electron_energy = secant(electron_neutron_scatter_energy, -100, 100, neutrino_energy)
            print "Electron enegry=", electron_energy, "Mev"
            electron_scattering_angle = electron_scatter_cos_angle(neutrino_energy, electron_energy)
            print "Eletron scattering angle=", electron_scattering_angle
            neutrino_energy_array.append(neutrino_energy)
            electron_cos_angle_array.append(electron_scattering_angle)
            electron_energy_array.append(electron_energy)
            neutrino_cross_array.append(neutrino.cross_section)

            nucleon_name="Neutron"

        elif nucleon_type==3:
            third = random.randint(0, 1)
            if third==0:
                print('v(anti) p--->e(anti) n')
                print "Neutrino energy=", neutrino_energy, "Mev"
                print "Neutrino cross section=", neutrino.cross_section
                electron_energy = secant(electron_proton_scatter_energy, -100, 100, neutrino_energy)
                print "Electron enegry=", electron_energy, "Mev"
                electron_scattering_angle = electron_scatter_cos_angle(neutrino_energy, electron_energy)
                print "Eletron scattering angle=", electron_scattering_angle
                neutrino_energy_array.append(neutrino_energy)
                electron_cos_angle_array.append(electron_scattering_angle)
                electron_energy_array.append(electron_energy)
                neutrino_cross_array.append(neutrino.cross_section)

            elif third==1:
                print('v n--->e(-) p')
                print "Neutrino energy", neutrino_energy, "Mev"
                print "Neutrino cross section=", neutrino.cross_section
                electron_energy = secant(electron_neutron_scatter_energy, -100, 100, neutrino_energy)
                print "Electron enegry=", electron_energy, "Mev"
                electron_scattering_angle = electron_scatter_cos_angle(neutrino_energy, electron_energy)
                print "Eletron scattering angle=", float(electron_scattering_angle)
                neutrino_energy_array.append(neutrino_energy)
                electron_cos_angle_array.append(electron_scattering_angle)
                electron_energy_array.append(electron_energy)
                neutrino_cross_array.append(neutrino.cross_section)

            nucleon_name="Proton and Neutron"
    '''scrollbar = Scrollbar(frame)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack()
    frame.pack()'''



    TOTAL_DATA.append(neutrino_energy_array)
    TOTAL_DATA.append(neutrino_cross_array)
    TOTAL_DATA.append(electron_energy_array)
    TOTAL_DATA.append(electron_cos_angle_array)

    ##GRAPH FUCNTIONS
    def show_variables():
        print(var1.get())
        print(var2.get())
        print(TOTAL_DATA[1])


    var1=IntVar(event_root)
    var1.set(1)
    for len in range(4):
        a=len*30
        Radiobutton(event_root, text=TOTAL_DATA[len][0], indicatoron=0, variable=var1, value=len+1).place(x=10, y=(10+a))
    '''    
    Radiobutton(event_root,text=TOTAL_DATA[0][0],indicatoron = 0,variable=var1,value=1,command=show_variables).place(x=10,y=10)
    Radiobutton(event_root,text=TOTAL_DATA[1][0],indicatoron = 0,variable=var1,value=2,command=show_variables).place(x=10,y=40)
    Radiobutton(event_root,text=TOTAL_DATA[2][0],indicatoron = 0,variable=var1,value=3,command=show_variables).place(x=10,y=70)
    Radiobutton(event_root,text=TOTAL_DATA[3][0],indicatoron = 0,variable=var1,value=4,command=show_variables).place(x=10,y=100)
    '''
    var2 = IntVar(event_root)
    var2.set(2)
    neutrino_energy_2 = Radiobutton(event_root, text=TOTAL_DATA[0][0],indicatoron = 0,variable=var2,value=1).place(x=200, y=10)
    neutrino_cross_2 = Radiobutton(event_root, text=TOTAL_DATA[1][0],indicatoron = 0,variable=var2,value=2).place(x=200, y=40)
    electron_energy_2 = Radiobutton(event_root, text=TOTAL_DATA[2][0],indicatoron = 0,variable=var2,value=3).place(x=200, y=70)
    electron_cos_angle_2 = Radiobutton(event_root, text=TOTAL_DATA[3][0],indicatoron = 0,variable=var2,value=4).place(x=200, y=100)
    ##==============FUNCTIONS

    def save_file(TOTAL_DATA):
        book = xlwt.Workbook()
        sheet_0 = book.add_sheet("Event Data")

        for num in range(len(TOTAL_DATA[0])):
            row = sheet_0.row(num)
            for index in range(len(TOTAL_DATA)):
                row.write(index, TOTAL_DATA[index][num])
        ##filepath=os.getcwd()

        book.save("Event data.xlsx")

    def save_file_as(TOTAL_DATA):
        book = xlwt.Workbook()
        sheet_0 = book.add_sheet("Event Data")
        for num in range(len(TOTAL_DATA[0])):
            row = sheet_0.row(num)
            for index in range(len(TOTAL_DATA)):
                row.write(index, TOTAL_DATA[index][num])

        save_filename = asksaveasfilename(defaultextension=".xlsx")
        book.save(save_filename)

    def show_plot_one(TOTAL_DATA):
        data = list(TOTAL_DATA)
        title=data[0]
        data.pop(0)
        data.sort()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(data)
        plt.title(title)
        plt.show()

    def show_hist_one(TOTAL_DATA):
        data = list(TOTAL_DATA)
        title=data[0]
        data.pop(0)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(data)
        plt.title(title)
        plt.show()

    def show_plot_both(TOTALDATA1,TOTALDATA2):
        x=list(TOTALDATA1)
        name1=x[0]
        x.pop(0)
        y=list(TOTALDATA2)
        name2=y[0]
        y.pop(0)
        fig = plt.figure()
        ax=fig.add_subplot(111)
        ax.scatter(x, y)
        plt.title(name1+" vs "+name2)
        scale_x = min(x)
        scale_y = min(y)
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_x))
        ax.xaxis.set_major_formatter(ticks_x)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
        ax.yaxis.set_major_formatter(ticks_y)
        plt.show()

    def print_data(TOTAL):
        printable=list(TOTAL)

        print('-------------')
        print(printable[0])
        printable.pop(0)
        print(printable)


    ##Buttons
    plot_one=Button(event_root,text="PLOT ONE DATA",command=lambda: show_plot_one(TOTAL_DATA[var1.get()-1])).place(x=10,y=150)
    plot_hist = Button(event_root, text="HIST ONE DATA", command=lambda: show_hist_one(TOTAL_DATA[var1.get()-1])).place(x=10, y=180)
    print_=Button(event_root,text="PRINT DATA", command=lambda: print_data(TOTAL_DATA[var1.get()-1])).place(x=10,y=210)
    plot_both = Button(event_root, text="SCAT. BOTH DATAS", command=lambda: show_plot_both(TOTAL_DATA[var1.get()-1],TOTAL_DATA[var2.get()-1  ])).place(x=200,y=150)


    Label(event_root,text="Event information").place(x=10,y=260)

    range_of_energy='Neutrino energy range: '+str(inital_En)+"-"+str(final_En)+"Mev"
    Label(event_root,text=range_of_energy).place(x=10,y=280)

    run_num='#Run: '+str(rnumber)
    Label(event_root,text=run_num).place(x=10,y=300)
    nuke_text="Nucleon type: "+nucleon_name
    Label(event_root,text=nuke_text).place(x=10,y=320)



    event_root.resizable(height=False, width=False)
    menubar = Menu(event_root)  ##creating menu bar on root
    filemenu = Menu(menubar, tearoff=0)  ## creating filemenu variable
    filemenu.add_command(label="Save", command=lambda :save_file(TOTAL_DATA))
    filemenu.add_command(label="Save as", command=lambda: save_file_as(TOTAL_DATA))
    filemenu.add_separator()
    menubar.add_cascade(label="File", menu=filemenu)
    event_root.config(menu=menubar)  ## adding menu to root
    event_root.mainloop()
    '''intractive_root.mainloop()'''


##=======================GUI CODING
root = Tk()## Creating root
root.wm_title("Quasi-Elastic Neutrino Scatterrig")## creating root title
root.geometry("300x300+100+100")## creating root geometry
root.resizable(height=False,width=False)
##Neutrino Energy random Generator
Label(root,text="Neutrino random Energy generator inputs").place(x=10,y=10)
##inital range
Label(root,text="Inital boundry in Mev").place(x=10,y=40)
inital_boundry=Entry(root,width=10)
inital_boundry.place(x=130,y=40)
##final range
Label(root,text="Final boundry in Mev").place(x=10,y=70)
final_boundry=Entry(root,width=10)
final_boundry.place(x=130,y=70)
##Choose nucleon type
varia=IntVar()
varia.set(1)
proton=Radiobutton(root,text="Proton",variable=varia,value=1).place(x=10,y=100)
neutron=Radiobutton(root,text="Neutron",variable=varia,value=2).place(x=10,y=130)
both=Radiobutton(root,text="Both nucleons",variable=varia,value=3).place(x=10,y=160)
## input run Number
Label(root,text="Run number").place(x=10,y=190)
run_number=Entry(root,width=10)
run_number.place(x=100,y=190)
##press button
Button(root,text="RUN",command=test_input).place(x=10,y=220)
root.mainloop()## running main loop



