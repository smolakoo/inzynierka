import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import requests
import pandas as pd
import matplotlib.pyplot as plt


def download_file(url, filename=''):
    try:
        req = requests.get(url)
        if filename:
            pass
        else:
            filename = req.url[req.url.rfind('/')+1:]

        with req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
        return None

def openFromPC():
    filename=filedialog.askopenfilename(initialdir="C:\\Users\\Wojtek\\PycharmProjects\\projekt_gui",
                                        title="Wybierz plik do otwarcia",
                                        filetypes=(("xlsx files", "*.xlsx"), ("All files", "*.*")))
    label_Filepath["text"] = filename
    return None

def Load_excel_data():
    root.withdraw()
    top2= Toplevel()
    top2.title("Podgląd pliku")
    top2.geometry("700x850")
    file_path = label_Filepath["text"]

    x_var = tkinter.StringVar(top2)
    y_var = tkinter.StringVar(top2)
    plot_var = tkinter.StringVar(top2)
    plot_var.set('Wykres liniowy')
    listOfPlots = ['Wykres liniowy', 'Wykres słupkowy', 'Wykres punktowy', 'Histogram']

    try:
        excel_filename = r"{}".format(file_path)
        if excel_filename[-4:] == ".csv":
            df = pd.read_csv(excel_filename)

        else:
            df = pd.read_excel(excel_filename, skiprows=4)

    except ValueError:
        top2.withdraw()
        messagebox.showerror("Błąd", "Plik który wybrałeś jest niepoprawny")

        return None
    except FileNotFoundError:
        top2.withdraw()
        messagebox.showerror("Błąd", f" {file_path}")
        root.deiconify()

        return None
    frame = LabelFrame(top2, text="Excel Data")
    frame.place(height=600, width=700)
    tv2 = ttk.Treeview(frame)
    tv2.place(relheight=1, relwidth=1)
    tscrolly = Scrollbar(frame, orient="vertical", command=tv2.yview)
    tscrollx = Scrollbar(frame, orient="horizontal", command=tv2.xview)
    tv2.configure(xscrollcommand=tscrollx.set, yscrollcommand=tscrolly.set)
    tscrollx.pack(side="bottom", fill="x")
    tscrolly.pack(side="right", fill="y")
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    df.fillna(value=0, axis=1, inplace=True)
    df.rename(columns={'Unnamed: 0': 'Data'}, inplace=True)

    def select_column(event):
        col = tv2.identify_column(event.x)
        print("Wybrana kolumna:", col)
        column_name = tv2.heading(col)["text"]
        myLabel2.config(text=f"Wybrana kolumna: {column_name}")

    frame2=LabelFrame(top2, text="Opcje")
    frame2.place(height=250, width= 700, y=600)

    myLabel2 = Label(frame2)
    myLabel2.pack(side="bottom")
    tv2.bind("<Button-1>", select_column)

    tv2["column"] = list(df.columns.str.replace('\n', ' '))
    tv2["show"] = "headings"
    for column in tv2["columns"]:
        tv2.heading(column, text=column)

    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        tv2.insert("", "end", values=row)

    def plot_data():
        x=x_var.get()
        y=y_var.get()
        try:
            plot_type=plot_var.get()
            if plot_type =='Wykres punktowy':
                plt.scatter(pd.to_numeric(df[x], errors='coerce'), pd.to_numeric(df[y], errors='coerce'))
                plt.xlabel(x)
                plt.ylabel(y)
                plt.show()
            elif plot_type=='Wykres liniowy':
                plt.plot(pd.to_numeric(df[x], errors='coerce'), pd.to_numeric(df[y], errors='coerce'))
                plt.xlabel(x)
                plt.ylabel(y)
                plt.show()
            elif plot_type =='Wykres słupkowy':
                plt.bar(pd.to_numeric(df[x], errors='coerce'), pd.to_numeric(df[y], errors='coerce'))
                plt.xlabel(x)
                plt.ylabel(y)
                plt.show()
            elif plot_type =='Histogram':

                plt.hist(pd.to_numeric(df[x], errors='coerce'))
                plt.xlabel(x)
                plt.show()

        except KeyError:
            root.withdraw()
            messagebox.showerror("Błąd", "Nie wybrano kolumn")
            return None


    def dane_statystyczne():
        top1= Toplevel()
        top1.title('Dane Statystyczne')
        top1.geometry("500x500")
        x= x_var.get()
        y= y_var.get()
        try:

            daneX=df[x].describe()
            daneY=df[y].describe()

        except KeyError:
            root.withdraw()
            top1.withdraw()
            messagebox.showerror("Błąd", "Nie wybrano kolumn.")
            return None
        label5 = Label(top1, text='')
        label6= Label(top1, text='')
        try:
            label5.config(text=f"Dane statystyczne dla kolumny:   {x}  {daneX}")
            label6.config(text=f"Dane stastystyczne dla kolumny:  {y}  {daneY}")
        except UnboundLocalError:
            return None
        label5.pack(side="top")
        label6.pack(side="bottom")

    def closeWindow():
        top2.withdraw()
        root.deiconify()

    def mergeColumns():
        x= x_var.get()
        y= y_var.get()
        nazwa=entryNazwaPliku.get()
        columnsMerged= [x,y]
        try:
            df[columnsMerged].to_excel(nazwa + '.xlsx', index= False)
            messagebox.showinfo("Sukces", "Zapisano nowy plik.")
        except KeyError:
            messagebox.showerror("Błąd", "Nie wybrano kolumn do zapisu.")
        except ValueError:
            messagebox.showerror("Błąd", "Nie wpisano nazwy pliku.")



    label10 = Label(frame2, text="Wybierz kolumnę do osi X wykresu:").place(x=5, y=5)
    label11 = Label(frame2, text="Wybierz kolumnę do osi Y wykresu:").place(x=5, y=110)
    buttonAxisX = OptionMenu(frame2, x_var, *df.columns).place(x=30, y=20)
    buttonAxisY = OptionMenu(frame2, y_var, *df.columns).place(x=30, y=135)
    buttonPlotType = OptionMenu(frame2, plot_var, *listOfPlots).place(x=520, y=5, width=165)
    buttonWykres = Button(frame2, text="Narysuj wykres.", command=plot_data).place(x=520, y=45, width=165)
    buttonDaneStatystczne = Button(frame2, text="Wygeneruj dane statystyczne", command=dane_statystyczne).place(x=520, y=80, width=165)
    buttonEscape= Button(frame2, text="Powrót do menu głównego", command=closeWindow).place(x=520, y=200, width=165)
    labelZapis=Label(frame2, text="Wpisz nazwę pliku do zapisu:").place(x=520, y=110)
    buttonZapisz= Button(frame2, text="Zapisz nowy plik.", command=mergeColumns).place(x=520, y=165, width=165)
    entryNazwaPliku= Entry(frame2, width=27)
    entryNazwaPliku.place(x=520, y=130)




def openData():
    top= Toplevel()
    top.title('Podgląd pliku')
    top.geometry("700x850")
    try:
        downloadUrl = entry.get()
        filename = download_file(downloadUrl)
        readfile = pd.read_excel(filename, skiprows=4)

        if filename is None :
            top.withdraw()
            messagebox.showerror("Błąd", "Nie wybrano pliku do pobrania.")

    except ValueError:
            top.withdraw()
            messagebox.showerror("Błąd", "Nie wybrano pliku do pobrania.")
            return None

    readfile.to_csv(filename+".csv", index = None, header = True)
    df = pd.DataFrame(pd.read_csv(filename+".csv"))
    df.dropna(axis=1, how='all', inplace=True)
    df.dropna(axis=0, how='all', inplace=True)
    df.fillna(value=0, axis=1, inplace=True)
    df.replace("-", "0", inplace=True, regex=True)
    df.rename(columns={'Unnamed: 0': 'Data'}, inplace=True)






    frame= LabelFrame(top, text="Excel Data")
    frame.place(height=600, width=700)
    tv1= ttk.Treeview(frame)
    tv1.place(relheight= 1, relwidth= 1)
    tscrolly= Scrollbar(frame, orient="vertical", command= tv1.yview)
    tscrollx= Scrollbar(frame, orient="horizontal", command= tv1.xview)
    tv1.configure(xscrollcommand=tscrollx.set, yscrollcommand= tscrolly.set)
    tscrollx.pack(side="bottom", fill="x")
    tscrolly.pack(side="right", fill="y")
    tv1["column"]=list(df.columns.str.replace('\n', ' '))
    tv1["show"]="headings"
    print(tv1["column"])

    for column in tv1["columns"]:
        tv1.heading(column, text=column, anchor=CENTER)

    df_rows = df.to_numpy().tolist()

    for row in df_rows:
        tv1.insert("", "end", values=row)

    frame2 = LabelFrame(top, text="Opcje")
    frame2.place(height=250, width=700, y=600)

    def select_column(event):
        col = tv1.identify_column(event.x)
        print("Wybrana kolumna:", col)
        column_name = tv1.heading(col)["text"]
        myLabel2.config(text=f"Wybrana kolumna: {column_name}")

    myLabel2 = Label(top)
    myLabel2.pack(side="bottom")
    tv1.bind("<Button-1>", select_column)

    def closeWindow():
        top.withdraw()
        root.deiconify()

    def plot_data():
        x=x_var.get()
        y=y_var.get()
        try:
            plot_type=plot_var.get()
            if plot_type =='Wykres punktowy':
                plt.scatter(pd.to_numeric(df[x], errors='coerce'), pd.to_numeric(df[y], errors='coerce'))
                plt.xlabel(x)
                plt.ylabel(y)
                plt.show()
            elif plot_type=='Wykres liniowy':
                plt.plot(pd.to_numeric(df[x], errors='coerce'), pd.to_numeric(df[y], errors='coerce'))
                plt.xlabel(x)
                plt.ylabel(y)
                plt.show()
            elif plot_type =='Wykres słupkowy':
                plt.bar(pd.to_numeric(df[x], errors='coerce'), pd.to_numeric(df[y], errors='coerce'))
                plt.xlabel(x)
                plt.ylabel(y)
                plt.show()
            elif plot_type =='Histogram':

                plt.hist(pd.to_numeric(df[x], errors='coerce'))
                plt.xlabel(x)
                plt.show()

        except KeyError:
            root.withdraw()
            messagebox.showerror("Błąd", "Nie wybrano kolumn")
            return None

    def dane_statystyczne():

        top1= Toplevel()
        top1.title('Dane Statystyczne')
        top1.geometry("500x500")
        x= x_var.get()
        y= y_var.get()
        try:
            daneX=df[x].describe()
            daneY=df[y].describe()
        except KeyError:
            top1.withdraw()
            messagebox.showerror("Błąd", "Nie wybrano kolumn.")
        label5 = Label(top1, text='')
        label6= Label(top1, text='')
        try:
            label5.config(text=f"Dane statystyczne dla kolumny:  \n {x} \n \n{daneX}")
            label6.config(text=f"Dane stastystyczne dla kolumny: \n {y} \n \n{daneY}")
        except UnboundLocalError:
            return None
        label5.pack(side="top")
        label6.pack(side="bottom")

    def mergeColumns():
        x= x_var.get()
        y= y_var.get()
        nazwa=entryNazwaPliku.get()
        columnsMerged= [x,y]
        try:
            df[columnsMerged].to_excel(nazwa + '.xlsx', index= False)
            messagebox.showinfo("Sukces", "Zapisano nowy plik.")
        except KeyError:
            messagebox.showerror("Błąd", "Nie wybrano kolumn do zapisu.")
        except ValueError:
            messagebox.showerror("Błąd", "Nie wpisano nazwy pliku.")

    x_var= tkinter.StringVar(top)
    y_var= tkinter.StringVar(top)
    plot_var= tkinter.StringVar(top)
    plot_var.set('Wykres liniowy')
    listOfPlots= ['Wykres liniowy', 'Wykres słupkowy', 'Wykres punktowy', 'Histogram']

    label10 = Label(frame2, text="Wybierz kolumnę do osi X wykresu:").place(x=5, y=5)
    label11 = Label(frame2, text="Wybierz kolumnę do osi Y wykresu:").place(x=5, y=110)
    buttonAxisX = OptionMenu(frame2, x_var, *df.columns).place(x=30, y=20)
    buttonAxisY = OptionMenu(frame2, y_var, *df.columns).place(x=30, y=135)
    buttonPlotType = OptionMenu(frame2, plot_var, *listOfPlots).place(x=520, y=5, width=165)
    buttonWykres = Button(frame2, text="Narysuj wykres.", command=plot_data).place(x=520, y=45, width=165)
    buttonDaneStatystczne = Button(frame2, text="Wygeneruj dane statystyczne", command=dane_statystyczne).place(x=520, y=80, width=165)
    buttonEscape = Button(frame2, text="Powrót do menu głównego", command=closeWindow).place(x=520, y=200, width=165)
    labelZapis = Label(frame2, text="Wpisz nazwę pliku do zapisu:").place(x=520, y=110)
    buttonZapisz = Button(frame2, text="Zapisz nowy plik.", command=mergeColumns).place(x=520, y=165, width=165)
    entryNazwaPliku = Entry(frame2, width=27)
    entryNazwaPliku.place(x=520, y=130)



    root.withdraw()



root = Tk()
root.title("Projekt GUI")
root.geometry("450x250")

downloadFrame= LabelFrame(root, text="Pobierz plik z internetu").place(height=100, width=400, relx=0, rely=0)
entry = Entry(downloadFrame, width=45)
entry.place(x=10, y=40)


def downloadButton():
    downloadUrl= entry.get()
    filename=download_file(downloadUrl)
    ifSuccess=download_file(downloadUrl, filename)
    if ifSuccess:
        messagebox.showinfo("Informacja", "Pobrano plik")
    else:
        messagebox.showerror("Błąd","Nie pobrano żadnego pliku")

myLabel = Label(downloadFrame, text="Wklej link do danych:").place(x=10 ,y=20 )
buttonDownload = Button(downloadFrame, text="Pobierz dane", command= downloadButton).place(x=300 , y=25)
buttonOpen = Button(downloadFrame, text="Otwórz plik", command=openData).place(x=300 , y=55 )



file_frame = LabelFrame(root, text="Otwórz plik z plików dostępnych na komputerze")
file_frame.place(height=100, width=400, rely=0.35, relx=0)
buttonBrowse = Button(file_frame, text="Przeglądaj", command=lambda: openFromPC())
buttonBrowse.place(rely=0.65, relx=0.50)
buttonLoad = Button(file_frame, text="Otwórz plik", command=lambda: Load_excel_data())
buttonLoad.place(rely=0.65, relx=0.30)
label_Filepath = ttk.Label(file_frame, text="Nie wybrano żadnego pliku")
label_Filepath.place(rely=0, relx=0)

buttonQuit = Button(root, text="Wyjście", command= root.quit).place(x=200, y= 300)

root.mainloop()