from LZWCore import LZWCore

from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import filedialog as fd

import os.path
import time


def select_file(mode: bool, e_input_file: ttk.Entry)  -> None:
    '''
    Depending on the mode (compress / decompress) open the file 
    selection window (All files / .lzw) and write the resulting 
    path to entry "e_input_file".
    
    '''

    if mode:
        # Decompress
        file_name = fd.askopenfilename(filetypes = (("LZW files", "*.lzw"),))
        
    else:   
        # Compress
        file_name = fd.askopenfilename(filetypes = (("All fiels", "*.*"),))

    e_input_file.delete(0, END)
    e_input_file.insert(0, file_name)


def select_save_directory(e_output_dir: ttk.Entry) -> None:
    ''' 
    Open the folder selection window and write the resulting path to 
    entry "e_output_dir".
    
    '''

    e_output_dir.delete(0, END)
    folder_selected = fd.askdirectory()
    e_output_dir.insert(0, folder_selected)


def comress_or_decompress_file(core: LZWCore,
                               mode: bool, 
                               input_file: str, 
                               output_dir: str, 
                               txt_output: Text) -> None:
    '''
    Depending on the mode, compress or decompress "input_file" 
    and place it in the "output_dir" directory.
    
    '''

    if (output_dir == None) or (os.path.isfile(output_dir)) or (not(os.path.exists(output_dir))):
        # By default, save the file next to the executable.
        output_dir = '.\\'
    else:
        output_dir = output_dir + '/'

    if mode:
        # Decompress
        try:
            lead_time = time.time()
            core.decompress(input_file, output_dir, time_flag = False)
            lead_time = time.time() - lead_time
            output_text = 'Decompress - Success!\nLead time: '
            output_text += str(lead_time) + 's.'
        except:
            output_text = 'Decompress error!'
        core.reset_decoder()
        
    else:   
        # Compress
        try:
            lead_time = time.time()
            core.compress(input_file, output_dir, time_flag = False)
            lead_time = time.time() - lead_time
            output_text = 'Compress - Success!\nLead time: '
            output_text += str(lead_time) + 's.'
        except:
            output_text = 'Compress error!'
        core.reset_encoder()

    txt_output.delete(1.0, END)
    txt_output.insert(1.0, output_text)


def main():

    theme_bg_color = '#464646'
    theme_text_color = '#bebebe'
    theme_txt_bg_color = '#373737'

    core = LZWCore()

    #------------------------- Main Window ---------------------------#
    root = ThemedTk(theme = "equilux")
    root.title("LZW-Compressor")
    root.resizable(False, False) 
    root['bg'] = theme_bg_color
    root.geometry('450x300')


    #-------------------------- Input File ---------------------------#
    l_input_file = Label(root, 
                      text = 'Input File:', 
                      bg = theme_bg_color, 
                      fg = theme_text_color)

    e_input_file = ttk.Entry(root, width = 40)

    #--------------------------- Output Dir ---------------------------#
    l_output_dir = Label(root, 
                      text = 'Save Directory:', 
                      bg = theme_bg_color, 
                      fg = theme_text_color)

    e_output_dir = ttk.Entry(root, width = 40)    


    #------------------------- Output Text ---------------------------#
    f_txt_output = ttk.LabelFrame(root, text = 'Output')
    
    txt_output = Text(f_txt_output, 
                     width = 34, 
                     height = 6, 
                     bg = theme_txt_bg_color, 
                     fg = theme_text_color)

    txt_output.pack(side = 'left')
 
    scroll = ttk.Scrollbar(f_txt_output, command = txt_output.yview)
    scroll.pack(side = 'left', fill = 'y')
 
    txt_output.config(yscrollcommand = scroll.set)

    #----------------------------- Mode ------------------------------#
    f_mode = ttk.LabelFrame(root, text = 'Mode')
    r_var = BooleanVar()
    r_var.set(0)
    r_compress = ttk.Radiobutton(f_mode, 
                               text = 'Compress   ', 
                               variable = r_var, 
                               value = 0)

    r_decompress = ttk.Radiobutton(f_mode, 
                               text = 'Decompress', 
                               variable = r_var, 
                               value = 1)

    # Сlearing "e_input_file" on mode change.
    def delete_text_input_entry(*arg) -> None:
        e_input_file.delete(0, END)
    r_var.trace('w', delete_text_input_entry)

    r_compress.pack()
    r_decompress.pack()

    #----------------------------- Start -----------------------------#
    b_start = ttk.Button(root, text = "start", width = 13)
    b_start.config(command = lambda: comress_or_decompress_file(core,
                                                                int(r_var.get()),
                                                                str(e_input_file.get()),
                                                                str(e_output_dir.get()),
                                                                txt_output))

    #---------------------------- Select -----------------------------#
    b_select_file = ttk.Button(root, text = "...", width = 2)
    b_select_file.config(command = lambda: select_file(int(r_var.get()),
                                                           e_input_file))

    b_select_output_dir = ttk.Button(root, text = "...", width = 2)
    b_select_output_dir.config(command = lambda: select_save_directory(e_output_dir))

    #----------------------------- Pack ------------------------------#
    l_input_file.place(x = 20, y = 20)
    e_input_file.place(x = 20, y = 40)
    b_select_file.place(x = 270, y = 36)

    l_output_dir.place(x = 20, y = 80)
    e_output_dir.place(x = 20, y = 100)
    b_select_output_dir.place(x = 270, y = 96)

    f_txt_output.place(x = 20, y = 140)

    f_mode.place(x = 330, y = 30)

    b_start.place(x = 330, y = 145)

    
    root.mainloop()



if __name__ == '__main__':
    main()