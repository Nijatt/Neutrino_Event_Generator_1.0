__author__ = 'Nijat Shukurov' \
             'id: 1784222' \
             '400 project assigment' \
             'neutrino and nucleon quasi elastic scatterring event generator'
import random
from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib
import tkMessageBox
from tkFileDialog import askopenfilename
import tkFileDialog
import FileDialog
import os

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
        self.cross_section=9.30*(10**(-42))*\
                           (((self.energy)*Mev_Energy)/(10*(10**6)))**2 ##cm^2

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





##TOTAL_DATA=[]


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
    global TOTAL_DATA
    TOTAL_DATA = []
    neutrino_energy_array = ['Neutrino Energ data']
    electron_cos_angle_array = ['Electron scat. ang. cos(a) data']
    electron_energy_array = ['Electron energy data']
    neutrino_cross_array = ['Neutrino cross sec. data']

    print(len(TOTAL_DATA))
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
    for leni in range(4):
        a=leni*30
        Radiobutton(event_root, text=TOTAL_DATA[leni][0], indicatoron=0, variable=var1, value=leni+1).place(x=10, y=(10+a))
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
    global TOTAL_DATA2
    TOTAL_DATA2 = []
    def open_file_test():
        '''This fucntions tests file before opening it this file extension should fit one of the array objects of
        excel_extension arrays then it opens the file. If it fails program shows warning screen dialoge
        '''
        excel_extensions = ['txt','xlsx', 'xlsm', 'xlsb', 'xltx', 'xltm', 'xlt', 'xls', 'xml', 'xlam', 'xla', 'xlw','txt']
        try:
            filename = askopenfilename(parent=root)
            name_array = filename.split('.')
            print(name_array)
            print(filename)
            global path
            path = name_array[0]
            global name
            name = name_array[1]
            for a in range(len(excel_extensions)):
                if str(name_array[1]) == excel_extensions[a]:
                    openfile(filename,path)
                    break
                else:
                    tkMessageBox.showwarning("FILE TYPE ERROR",
                                             "Can not open this file ' \n(%s) ' because of it is not excell or txt type " % filename)
                    break
        except:
            tkMessageBox.showwarning("FILE OPENING ERROR 1", " Can not open file due to name or path ")

    def openfile(filename,path):
        '''After open_file_test() function runs clears and not shows warning it will be run this function
           THIS FUCNTION IS IMPORTANT ONE WHICH IS ALL PROCSESESS WILL RUNE FROM THIS FUCNTION!!!
           TOTAL_DATA2 = []
        '''
        array = []

        nam_ray=path.split("/")
        array_name=nam_ray[len(nam_ray)-1]
        array.append(array_name)
        with open(filename, "r") as ins:
            for line in ins:
                array.append(float(line))

        TOTAL_DATA2.append(array)

        data_root = Tk()
        data_root.wm_title("External Data")  ## creating root title
        data_root.geometry("400x400+200+200")  ## creating root geometry
        data_root.resizable(height=False, width=False)
        ## radios


        def clean(TOTAL_DATA2):
            TOTAL_DATA2=[]

        var11 = IntVar(data_root)
        var11.set(1)

        for leni1 in range(len(TOTAL_DATA2)):
            a = leni1 * 30
            Radiobutton(data_root, text=TOTAL_DATA2[leni1][0], indicatoron=0, variable=var11, value=leni1 + 1).place(x=10,
                                                                                                                  y=(
                                                                                                                  10 + a))

        var21 = IntVar(data_root)
        var21.set(2)
        for leni2 in range(len(TOTAL_DATA2)):
            a = leni2 * 30
            Radiobutton(data_root, text=TOTAL_DATA2[leni2][0], indicatoron=0, variable=var21, value=leni2 + 1).place(x=200,
                                                                                                                  y=(
                                                                                                                  10 + a))
        ##Buttons
        plot_one = Button(data_root, text="PLOT ONE DATA",
                          command=lambda: show_plot_one(TOTAL_DATA2[var11.get() - 1])).place(x=10, y=150)
        plot_hist = Button(data_root, text="HIST ONE DATA",
                           command=lambda: show_hist_one(TOTAL_DATA2[var11.get() - 1])).place(x=10, y=180)
        print_ = Button(data_root, text="PRINT DATA", command=lambda: print_data(TOTAL_DATA2[var11.get() - 1])).place(
            x=10, y=210)
        plot_both = Button(data_root, text="SCAT. BOTH DATAS",
                           command=lambda: show_plot_both(TOTAL_DATA2[var11.get() - 1],
                                                          TOTAL_DATA2[var21.get() - 1])).place(x=200, y=150)

        clean_data=Button(data_root,text="CLEAN DATA" ,command= lambda: clean(TOTAL_DATA2)).place(x=200,y=180)




    def test_plot(TOTALDATA1,TOTALDATA2):
        x = list(TOTALDATA1)
        name1 = x[0]
        x.pop(0)
        y = list(TOTALDATA2)
        name2 = y[0]
        y.pop(0)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title(name1 + " vs " + name2)
        plt.xlabel(name1)
        plt.ylabel(name2)

        ##finding the second smallest an d difference between first smallest
        def second_smallest(x):
            numbers=list(x)
            min_x=min(numbers)
            while(min(numbers)==min_x):
                numbers.remove(min_x)
            m2=min(numbers)
            difference=m2-min_x
            while (difference==1):
                while (min(numbers) == m2):
                    print("--optimizing data for plotting--")
                    numbers.remove(m2)
                m2=min(numbers)
                difference=m2-min_x

            return m2 ,difference


        ##first smallest of x
        min_x = min(x)
        ##second_smallest and diff of y
        min_x2,diff_x=second_smallest(x)
        ##first smallest of y
        min_y =min(y)
        ##second smallesr and diff of y
        min_y2,diff_y=second_smallest(y)
        ## max of x
        max_x=max(x)
        ## max of y
        max_y=max(y)
        '''
        usable_y=[]
        for a in range(len(y)):
            usable_y.append(y[a]/min_y)
        '''
        def create_usable_plot(x,y):
           usable_x=[]
           usable_y=[]
           for a in range(len(x)):
               usable_x.append(float(x[a]/diff_x))
           for a in range(len(y)):
               usable_y.append((int(y[a]/diff_y)))
           return usable_x,usable_y


        data1,data2=create_usable_plot(x,y)
        ax.scatter(data1,data2)
        plt.show()


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
        plt.title(name1+" vs "+name2)
        scale_x = min(x)
        scale_y = min(y)
        ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_x))
        ax.xaxis.set_major_formatter(ticks_x)
        ticks_y = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x / scale_y))
        ax.yaxis.set_major_formatter(ticks_y)
        ax.scatter(x, y)
        plt.show()




    def print_data(TOTAL):
        printable=list(TOTAL)

        print('-------------')
        print(printable[0])
        printable.pop(0)
        print(printable)

    def turn_to_txt2(TOTAL):
        TEXT=list(TOTAL)
        name=TEXT[0]
        TEXT.pop(0)

        rn = False
        try:
            f = open(name+ ".txt", 'w')
            rn = True
        except:
            tkMessageBox.showwarning("Textfile name error!!", "Text file name should be String type.")

        if rn==True:
            os.linesep

        for a in range(len(TEXT)):
            f.write(str(TEXT[a])+os.linesep)
        f.close()


    def turn_to_txt(TOTAL):

        rn = False
        try:
            textfile_name_1 = textfile_name.get()
            f = open(textfile_name_1 + ".txt", 'w')
            rn = True
        except:
            tkMessageBox.showwarning("Textfile name error!!", "Text file name should be String type.")

        if rn==True:
            os.linesep
            ##Writing headline
            ##Advisor: Prof.Dr. Ali Murat Guler
            str1 ="|====================================================================================|"
            str2 ="|                                                       *                            |"
            str3 ="|           N     N  EEEEEEE  U    U  TTTTTTT  RRRRR    I  N     N   OOOO            |"
            str4 ="|           N N   N  E        U    U     T     R    R   I  N N   N  O    O           |"
            str5 ="|           N  N  N  EEEEEEE  U    U     T     RRRRR    I  N  N  N  O    O           |"
            str6 ="|           N   N N  E        U    U     T     R    R   I  N   N N  O    O           |"
            str7 ="|           N     N  EEEEEEE   UUUU      T     R     R  I  N     N   OOOO            |"
            str8 ="|                                                                                    |"
            str9 ="|           QUASI-ELASTIC NEUTRINO SCATERRING (MONTE CARLO EVENT GENERATOR)          |"
            str10="|                                                                                    |"
            str11="|           VERSION: 1.00     Website: http://www.users.metu.edu.tr/e178422          |"
            str12="|                                                                                    |"
            str13="|           MIDDLE EAST TECHNICAL UNIVERSITY (METU) - DEPARTMENT OF PHYSICS          |"
            str14="|                                                                                    |"
            str15="|           Special Problems in Physics (Phys-400)                                   |"
            str16="|           Nijat Shukurov                                                           |"
            str17="|           Email: e178422@metu.edu.tr                                               |"
            str18="|           Advisor: Prof.Dr. Ali Murat Guler                                        |"
            str19="|                                                                                    |"
            str20="|====================================================================================|"
            f.write(os.linesep+str1 + os.linesep + str2 +os.linesep +str3+os.linesep+str4+os.linesep+str5+os.linesep+str6+os.linesep+str7+os.linesep+str8+os.linesep+str9+os.linesep+str10+os.linesep+str11+os.linesep+str12+os.linesep+str13+os.linesep+str14+os.linesep+str15+os.linesep+str16+os.linesep+str17+os.linesep+str18+os.linesep+str19+os.linesep+str20+os.linesep)
            ##end of header
            ## event info header
            strr1 = "|====================================================================================|"
            strr2 = "|                               EVENT INFORMATION:                                   |"
            if nucleon_type==1:
                strr3=  "|      v(bar) p  ---> e+   n                                                         |"
                strr4 = "|                                                                                    |"
                strr5=  "|      name        id                                                                |"
                strr6=  "|  A  (vbar)      -12                                                                |"
                strr7=  "|  B  (p+)        2212                                                               |"
                strr8=  "|  C  (n)         2112                                                               |"
                strr9=  "|  D  (e-)         11                                                                |"
            else:
                strr3 = "|      v      n  ---> e-   p+                                                        |"
                strr4=  "|                                                                                    |"
                strr5 = "|      name        id                                                                |"
                strr6 = "|  A  (v)          12                                                                |"
                strr7 = "|  B  (n)         2112                                                               |"
                strr8 = "|  C  (p+)        2212                                                               |"
                strr9 = "|  D  (e+)        -11                                                                |"
            strr10 = "|====================================================================================|"

            f.write(os.linesep + strr1 + os.linesep+strr2 +os.linesep +strr3 +os.linesep+strr4+os.linesep+strr5+os.linesep+strr6+os.linesep+strr7+os.linesep+strr8+os.linesep+strr9+os.linesep+strr10+os.linesep+os.linesep)
            ##event run
            strrr1 = "|====================================================================================|"
            strrr2 = "|                             EVENT LISTING                                          |"
            strrr3=  "#run  Neut.Energy      Neut. Cross sec.     Electr.Energy    Scat.Angle              |"
            f.write(os.linesep+strrr1+os.linesep+strrr2+os.linesep+strrr3+os.linesep+os.linesep)
            TEXT = []
            for ml in range(len(TOTAL)):
                TEXT.append(list(TOTAL[ml]))


            for a in range(len(TEXT)):
                TEXT[a].pop(0)

            for num in range(len(TEXT[0])):

                line=" "
                for b in range(len(TEXT)):
                    maxlen=15
                    freespace=" "
                    addscape=maxlen-len(str(TEXT[b][num]))
                    if addscape <=2:
                        addscape+=6
                    elif addscape <=5 and addscape>2:
                        addscape+=4
                    elif addscape <=8 and addscape>5:
                        addscape+=3
                    elif addscape <=14 and addscape > 8:
                        addscape-=3
                    else:
                        pass

                    for mik in range(addscape):
                        freespace+=" "
                    if b==3:
                        adding=str(repr(float(TEXT[b][num])))
                    else:
                        adding=str(float(TEXT[b][num]))
                    line+=adding+freespace;
                f.write(" #"+str(num)+"    "+line+os.linesep)

            f.close()

    ##Buttons
    stringo="----------------------------------------------------------------------------------------"
    Label(event_root,text=stringo).place(x=0,y=130)
    plot_one=Button(event_root,text="PLOT ONE DATA",command=lambda: show_plot_one(TOTAL_DATA[var1.get()-1])).place(x=10,y=150)
    plot_hist = Button(event_root, text="HIST ONE DATA", command=lambda: show_hist_one(TOTAL_DATA[var1.get()-1])).place(x=10, y=180)
    print_=Button(event_root,text="PRINT DATA", command=lambda: print_data(TOTAL_DATA[var1.get()-1])).place(x=10,y=210)
    plot_both1 = Button(event_root, text="OPTIMIZED PLOT BOTH",command=lambda: test_plot(TOTAL_DATA[var1.get() - 1], TOTAL_DATA[var2.get() - 1])).place(x=10,y=240)
    plot_both2 = Button(event_root, text="SCAT. BOTH DATAS", command=lambda: show_plot_both(TOTAL_DATA[var1.get()-1],TOTAL_DATA[var2.get()-1  ])).place(x=200,y=150)

    '''
    textfile_name=Entry(event_root, width=15)
    textfile_name.insert(END, "QE_excample")
    textfile_name.place(x=200, y=180)
    Label(event_root, text=".txt").place(x=295, y=180)
    textgenerator = Button(event_root, text="TEXT OUTPUT", command=lambda: turn_to_txt(TOTAL_DATA)).place(x=200, y=210)
    '''
    Label(event_root, text="-Text generator-").place(x=200, y=180)
    textfile_name = Entry(event_root, width=12)
    textfile_name.insert(END, "QE_example")
    textfile_name.place(x=295, y=210)
    Label(event_root, text=".txt").place(x=370, y=210)
    textgenerator = Button(event_root, text="TEXT OUTPUT", command=lambda: turn_to_txt(TOTAL_DATA)).place(x=200, y=210)

    textgenerator2 = Button(event_root, text="TEXT OUTPUT2", command=lambda: turn_to_txt2(TOTAL_DATA[var1.get()-1])).place(x=200, y=240)

    Label(event_root,text="Event information").place(x=10,y=300)
    range_of_energy='Neutrino energy range: '+str(inital_En)+"-"+str(final_En)+"Mev"
    Label(event_root,text=range_of_energy).place(x=10,y=320)

    run_num='#Run: '+str(rnumber)
    Label(event_root,text=run_num).place(x=10,y=340)
    nuke_text="Nucleon type: "+nucleon_name
    Label(event_root,text=nuke_text).place(x=10,y=360)



    event_root.resizable(height=False, width=False)
    menubar = Menu(event_root)  ##creating menu bar on root
    filemenu = Menu(menubar, tearoff=0)  ## creating filemenu variable
    filemenu.add_command(label="Open", command=lambda :open_file_test())
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
##both=Radiobutton(root,text="Both nucleons",variable=varia,value=3).place(x=10,y=160)
## input run Number
Label(root,text="Run number").place(x=10,y=190)
run_number=Entry(root,width=10)
run_number.place(x=100,y=190)
##press button
Button(root,text="RUN",command=test_input).place(x=10,y=220)
root.mainloop()## running main loop



