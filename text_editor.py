# I will make a project that is a simple text editor and explanation of its function
# mengimport semua class tkinter
from tkinter import *
from tkinter import messagebox # mengimport class messgebox dari tkinter
from tkinter.filedialog   import asksaveasfilename # mengimport 'askopenfilename' dari class 'filedialog' tkinter
from tkinter import filedialog # mengimport class file dialog dari library tkinter
import os, webbrowser # (import os)mengimport class python yaitu os, (import webbroser) untuk pergi ke website atau situs yang dituju
from tkinter.messagebox import askokcancel # mengimport messegebox sebagi 'askokcancel'
from tkinter import messagebox as mbox # mengimport messagebox ke mbox
# membuat class 'SImpleEditor' dengan inheritence class 'Frame' (di tkinter)
class SimpleEditor(Frame):
    def __init__(self, parent=None, file=None):
        Frame.__init__(self, parent)
        self.frm = Frame(parent)
        self.frm.pack(fill=X)
        self.buatJudul()
        self.parent = parent 
        self.parent.title('Text Editor Sederhana Dengan Tkinter | Ahmad Bujai Rimi 20190801217')
        self.buatTombol()
        self.kolomTeksUtama()
        self.settext(text='',file=file)
        self.kolomTeks.config(font=('DejaVu Sans Mono', 10))
        self.path = ''
        self.indeks = '0.9' # inisialisasi variabel 'indeks' sebagai penentu lokasi pencarian
        self.buatCari()
        self.buatMenuBar()
    # fungsi 'buatTombol'
    def buatTombol(self): 
        Button(self.frm, text='Open',relief='flat',  command=self.bukaFile).pack(side=LEFT)
        Button(self.frm, text='Save',relief='flat',  command=self.perintahSimpan).pack(side=LEFT)
        Button(self.frm, text='Copy', relief='flat', command=self.perintahCopy).pack(side=LEFT)
        Button(self.frm, text='Cut', relief='flat',   command=self.perintahCut).pack(side=LEFT)
        Button(self.frm, text='Paste', relief='flat', command=self.perintahPaste).pack(side=LEFT)
        Button(self.frm, text='Undo', relief='flat',   command=self.perintahUndo).pack(side=LEFT)
        Button(self.frm, text='Redo', relief='flat', command=self.perintahRedo).pack(side=LEFT)
        Button(self.frm, text='Keluar', relief='flat', command=self.perintahKeluar).pack(side=LEFT)
    # fungsi 'kolomTeksUtama'
    def kolomTeksUtama(self):
        scroll = Scrollbar(self)
        kolomTeks = Text(self, relief=SUNKEN, undo=True)
        scroll.config(command=kolomTeks.yview)
        kolomTeks.config(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        kolomTeks.pack(side=LEFT, expand=YES, fill=BOTH)
        self.kolomTeks = kolomTeks
        self.pack(expand=YES, fill=BOTH)
    # fungsi 'buatMenuBar'
    def buatMenuBar(self):
        self.menubar = Menu(self.parent,bd=0)
        self.fileMenu = Menu(self.parent, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.bukaFile)
        self.fileMenu.add_command(label="Save", command=self.perintahSimpan)
        self.fileMenu.add_command(label="Exit", command=self.perintahKeluar)
        self.menubar.add_cascade(label="File", menu=self.fileMenu)

        self.menuEdit = Menu(self.parent, tearoff=0)
        self.menuEdit.add_command(label="Undo", command=self.perintahUndo)
        self.menuEdit.add_command(label="Redo", command=self.perintahRedo)
        self.menuEdit.add_separator() # menambah garis atau separator
        self.menuEdit.add_command(label="Copy", command=self.perintahCopy)
        self.menuEdit.add_command(label="Cut", command=self.perintahCut)
        self.menuEdit.add_command(label="Paste", command=self.perintahPaste)
        self.menubar.add_cascade(label="Edit", menu=self.menuEdit)

        self.menuWebGithub = Menu(self.parent, tearoff=0)
        self.menuWebGithub.add_command(label="MyGithub", command=self.pergikeGithub)
        self.menubar.add_cascade(label="Github", menu=self.menuWebGithub)

        self.menuAbout = Menu(self.parent, tearoff=0)
        self.menuAbout.add_command(label="about my application", command=self.about)
        self.menubar.add_cascade(label="About", menu=self.menuAbout)

        self.parent.config(menu=self.menubar) # memasukkan menubar ke window
        self.pack() # memasukkan aplikasi ke window
    # fungsi 'perintahSimpan'
    def perintahSimpan(self):
        print(self.path) 
        if self.path:
            alltext = self.gettext()
            open(self.path, 'w').write(alltext)
            messagebox.showinfo('Berhasil', 'Selamat File telah tersimpan ! ')
        else:
            tipeFile = [('Text file', '*.txt'), ('Python file', '*asdf.py'), ('All files', '.*')] # membuka tipe yang di cari  di file dialog untuk menyimpan file
            filename = asksaveasfilename(filetypes=(tipeFile), initialfile=self.kolomJudul.get()) # menampilkan file dialog dan mendapatkan lokasi tempat menyimpan file yang di pilih user
            if filename:
                alltext = self.gettext()
                open(filename, 'w').write(alltext)
                self.path = filename
    # fungsi 'perintahCopy'
    def perintahCopy(self):
        try:
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
            self.kolomTeks.selection_clear()
        except:
            pass
    # fungsi 'perintahCut'
    def perintahCut(self):
        try :
            text = self.kolomTeks.get(SEL_FIRST, SEL_LAST)
            self.kolomTeks.delete(SEL_FIRST, SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(text)
        except:
            pass
    # fungsi 'perintahPaste'
    def perintahPaste(self):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.kolomTeks.insert(INSERT, text)
        except TclError:
            pass
    # fungsi 'perintahFind'
    def perintahFind(self):
        target = self.kolomCari.get() # mendapatkan teks dari kolom cari (teks yang akan di cari)
        if target:
            self.indeks = self.kolomTeks.search(target, str(float(self.indeks)+0.1), stopindex=END) # mencari file
            if self.indeks:
                pastit = self.indeks + ('+%dc' % len(target)) # mendapatkan jumlah karakter
                self.kolomTeks.tag_remove(SEL, '1.0', END)
                self.kolomTeks.tag_add(SEL, self.indeks, pastit)
                self.kolomTeks.mark_set(INSERT, pastit)
                self.kolomTeks.see(INSERT)
                self.kolomTeks.focus()
            else:
                self.indeks = '0.9' # mengubah nilai 'self.indeks' menjadi 0.9
    # fungsi 'perintahKeluar'
    def perintahKeluar(self):
        ans = askokcancel('Keluar', "anda yakin ingin keluar?") # menampilkan kotak konfirmasi
        if ans: Frame.quit(self)
    # fungsi 'settext'
    def settext(self, text='', file=None):
        if file:
            text = open(file, 'r').read()
        self.kolomTeks.delete('1.0', END)
        self.kolomTeks.insert('1.0', text)
        self.kolomTeks.mark_set(INSERT, '1.0')
        self.kolomTeks.focus()
    # fungsi 'getText'
    def gettext(self):
        return self.kolomTeks.get('1.0', END+'-1c') # mendapatkan semua teks di kolom utama
    # fungsi 'buatJudul'
    def buatJudul(self):
        top = Frame(root)
        top.pack(fill=BOTH, padx=17, pady=5)
        judul = Label(top, text="Judul : ")
        judul.pack(side="left")
        self.kolomJudul = Entry(top)
        self.kolomJudul.pack(side="left")
    # fungsi 'buatCari'
    def buatCari(self):
        Button(self.frm, text='Cari', command=self.perintahFind).pack(side="right")
        self.kolomCari = Entry(self.frm)
        self.kolomCari.pack(side="right")
    # fungsi 'bukaFile'
    def bukaFile(self):
        extensiFile = [ ('All files', '*'), ('Text files', '*.txt'),('Python files', '*.py')] # insialisasi tipe file
        buka = filedialog.askopenfilename(filetypes = extensiFile) # membuka file dialog untuk memilih file untuk di buka
        if buka != '':
            text = self.readFile(buka) # mendapatkan semua teks (menjalankan metode 'readFIle'
            if text:
                self.path = buka
                nama = os.path.basename(buka)
                self.kolomJudul.delete(0, END)
                self.kolomJudul.insert(END, nama)
                self.kolomTeks.delete('0.1',END)
                self.kolomTeks.insert(END, text)
    # fungsi 'readFile'
    def readFile(self, filename):
        try:
            f = open(filename, "r")
            text = f.read()
            return text
        except:
            messagebox.showerror("Error!!","Maaf file tidak dapat dibuka ! :) \nsabar ya..") # menampilkan pesan dialog error
            return None
    # fungsi 'about'
    def about(self):
        mbox.showinfo("about my application", "aplikasi text editor sederhana dengan modul tkinter(Tk).\n\n"
                                              "aplikasi ini berdasarkan materi python dasar \ndan OOP (Object Oriented Programming)\n\n"
                                              "aplikasi ini bisa digunakan sebagai untuk membuat file teks dan juga file python\n\n"
                                              "\t\tcreated by ahmad bujai rimi - 20190801217") # code disamping ini untuk menampilkan pesan dialog
    # fungsi 'pergikeGithub'
    def pergikeGithub(self):
        webbrowser.open_new(r"https://github.com/bujay/Design-Analisis-Algoitma") # pergi ke Github saya
    # fungsi 'perintahUndo'
    def perintahUndo(self):
        try:
            self.kolomTeks.edit_undo() # melakukan undo
        except:
            pass
    # fungsi 'perintahRedo'
    def perintahRedo(self):
        try:
            self.kolomTeks.edit_redo() # melakukan redo
        except:
            pass
root = Tk() # menampilkan window Tkinter
SimpleEditor(root) # menjalankan metode 'SimpleEditor'
mainloop() # agar window tidak langsung close saat di jalankan