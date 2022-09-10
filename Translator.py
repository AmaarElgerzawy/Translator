import os
from random import random
import re
from shutil import move, rmtree
from googletrans import Translator, constants
import tkinter as Tk
from tkinter import *
from tkinter import ttk

class translation():
  def __init__(self) -> None:
    self.main = Tk()
    self.main.geometry('400x120+500+250')
    self.main.resizable(False, False)
    self.main.title('Translate translation files'.title())

    prime_path = StringVar()
    move_path = StringVar()
    lan_from = StringVar()
    lan_to = StringVar()

    global translator
    translator = Translator()

    self.prime_path_lapel = Label(self.main, text="Prime Path  ")
    self.prime_path_lapel.place(x=10, y=20)
    self.prime_path_entry = Entry(self.main, width=45, textvariable=prime_path)
    self.prime_path_entry.place(x=90, y=20)

    self.BackUp_path_lapel = Label(self.main, text="Back Up Path  ")
    self.BackUp_path_lapel.place(x=10, y=50)
    self.BackUp_path_entry = Entry(self.main, width=45 , textvariable=move_path)
    self.BackUp_path_entry.place(x=90, y=50)

    self.from_lab = Label(self.main , text="From: ")
    self.from_lab.place(x = 15 , y = 80)
    self.Box_From = ttk.Combobox(self.main, values=tuple(constants.LANGUAGES.keys()), textvariable=lan_from , width=5)
    self.Box_From.place(x= 50 , y = 80)

    self.To_lab = Label(self.main, text="To: ")
    self.To_lab.place(x=290, y=80)
    self.Box_to = ttk.Combobox(self.main, values=tuple(constants.LANGUAGES.keys()), textvariable=lan_to , width=5)
    self.Box_to.place(x=310, y=80)

    self.lab_pricent = Label(self.main , text=f"Progres: {0}%" , fg="green")

    the_rand = int(random()*1000000)

    def get_srt(name):
        return re.search(".+srt", name)
    
    def move_files():
      prime_list = os.listdir(prime_path.get())
      if move_path.get():
        for i in prime_list:
          try:
            os.mkdir(fr"{move_path.get()}/{i}")
          finally:
            for j in os.listdir(rf"{prime_path.get()}/{i}"):
              if re.search(".+srt", j):
                move(f"{prime_path.get()}/{i}/{j}", fr"{move_path.get()}/{i}/{j}")
      else:
        for i in prime_list:
          try:
              os.mkdir(fr"{prime_path.get()}/{i}/backUp")
          finally:
            for j in os.listdir(rf"{prime_path.get()}/{i}"):
              if re.search(".+srt", j):               
                move(f"{prime_path.get()}/{i}/{j}", fr"{prime_path.get()}/{i}/backUp/{j}")
      
      try:
        for i in os.listdir(fr"C:/the_Translated{the_rand}"):
          for j in os.listdir(fr"C:/the_Translated{the_rand}/{i}"):
            move(fr"C:/the_Translated{the_rand}/{i}/{j}", fr"{prime_path.get()}/{i}/{j}")
      finally:
        rmtree(f"C:/the_Translated{the_rand}", ignore_errors=True)

    def progress(n):
      progress_var['value'] += n
      self.lab_pricent.config(text=f"Progres: {round(progress_var['value'] , 2)}%")

    def the_core(lanFrom , lanTo):
      # function that return srt file name but with bug that if no files will return none in the list 
      try:
        os.mkdir(fr"C:/the_Translated{the_rand}")
      except:pass
      
      prime_path_ls = os.listdir(rf"{prime_path.get()}")
      the_number_of_files = 0
      #the starter folder path
      for beta_path in prime_path_ls:
        
        path = rf"{prime_path.get()}/{beta_path}"
        the_files = os.listdir(path)
        the_number_of_files += len(list(filter(get_srt, the_files)))
      
      self.main.update()
      self.main.update_idletasks()
      the_number_of_files = 100/the_number_of_files
      #the starter folder path
      for beta_path in prime_path_ls:
        path = rf"{prime_path.get()}/{beta_path}"
        the_files = os.listdir(path)
        try:
          os.mkdir(fr"C:/the_Translated{the_rand}/{beta_path}")
        except:pass
        self.main.update()
        self.main.update_idletasks()
        #the list and loop fot remove none from list that contain srt name files
        the_filterd_list = list(filter(get_srt, the_files))

        counter = 0
        while counter < len(the_filterd_list):
          #reading english line from files and concatnate multible lines
          the_lines = []
          the_ints = []


          for j in open(path+"/"+the_filterd_list[counter], "r", encoding="utf8").readlines():
              try:
                int(j[4])
                the_ints.append(j)
              except:
                try:
                  int(j[0])
                except:
                  the_lines.append(j)
         

          self.main.update()
          self.main.update_idletasks()

          #removing \n from list and from every line
          i = 0
          while i < the_lines.count("\n"):
            the_lines.remove("\n")
          for v in the_lines:
            the_lines[the_lines.index(v)] = v[:-1]

          final_file = open(fr"C:/the_Translated{the_rand}/{beta_path}/{the_filterd_list[counter]}", "a", encoding="utf16")

          #final step inserting translation into file
          i, vb = 0, 0
          while i < len(the_lines):
            if not the_lines[i].endswith("."):
              try:
                x = the_ints[vb].index(">")
                y = the_ints[vb+1].index(">")
                final_file.write(the_ints[vb][:x] + the_ints[vb+1][y:])
              except:
                final_file.write("00:00:00,000 --> 00:00:00,000\n")
              try:
                temp = the_lines[i+1]
                the_lines.remove(the_lines[i+1])
              except:
                temp = ""
              tar = the_lines[i] + temp
              global translator
              try:
                self.main.update()
                self.main.update_idletasks()
                translated_text = translator.translate(tar, dest=lanTo, src=lanFrom)
              except:
                new_translator = Translator()
                translator = new_translator
                translated_text = new_translator.translate(tar, dest=lanTo, src=lanFrom)

              final_file.write(translated_text.text+"\n")
              final_file.write("\n")

              i += 1
              vb += 2

              self.main.update()
              self.main.update_idletasks()
            else:
              final_file.write(the_ints[vb])

              try:
                self.main.update()
                self.main.update_idletasks()
                translated_text = translator.translate(the_lines[i], dest=lanTo, src=lanFrom)
              except:
                new_translator = Translator()
                translator = new_translator
                translated_text = translator.translate(the_lines[i], dest=lanTo, src=lanFrom)

              final_file.write(translated_text.text+"\n")
              final_file.write("\n")

              i += 1
              vb += 1

              self.main.update()
              self.main.update_idletasks()

          final_file.close()
          counter += 1
          progress(the_number_of_files)

    def clear_then_core():
      lanFrom = lan_from.get() if lan_from.get() else "en"
      lanTo = lan_to.get() if lan_to.get() else "ar"

      self.prime_path_entry.destroy()
      self.prime_path_lapel.destroy()
      self.BackUp_path_entry.destroy()
      self.BackUp_path_lapel.destroy()
      self.translate_button.destroy()

      self.from_lab.destroy()
      self.Box_From.destroy()
      self.To_lab.destroy()
      self.Box_to.destroy()

      progress_var.pack(pady=30)
      self.lab_pricent.place(x=150 , y = 50)

      self.main.update()
      self.main.update_idletasks()
      try:
        the_core(lanFrom, lanTo)
        self.main.update()
        self.main.update_idletasks()
        move_files()
      except:
        self.lab_pricent.config(text=f"Progres: Down" , fg="brown")
        err = Label(self.main, text="There Is An Error Thrown Please Check Your Internet Connection.\n Or Make Sure That Folders Is In The Right Pattern", fg="red")
        err.pack()
      else:
        self.lab_pricent.destroy()
        progress_var.destroy()

      Label(self.main, text="Done!!", font=("Courier", 25, "bold"), fg="green").pack(pady=30)
    
    progress_var = ttk.Progressbar(self.main, orient=HORIZONTAL, length=300, mode='determinate')
    
    self.translate_button = Button(self.main, text="Start Translate", command=clear_then_core)
    self.translate_button.place(x = 160 , y = 85)

    self.main.mainloop()

my_program1 = translation()
