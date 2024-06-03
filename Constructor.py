import customtkinter as ctk
import matplotlib.pyplot as plt
import Controller_module as Ctrl

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk


commands_controller = Ctrl.Transmitter()
ctk.set_appearance_mode('Light')


class Button_Constructor(ctk.CTkButton):
    """Создает кнопку, при наджатии команда передается 
    в контроллер или исполняется сразу """
    def __init__(self, command, *args, **kwargs):
        if callable(command) or type(command) is None:
            super().__init__(command=command, *args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
            self.configure(command=self.press)
            self.command = command
    
    def press(self):
        commands_controller.execute_command(self.command)
    

class Graphic_Window_Constructor:
    def __init__(self, win, column:int, row:int, rowspan:int=1, columnspan:int=1):
        self.win = win
        self.column = column
        self.row = row
        self.rowspan =rowspan
        self.columnspan = columnspan

    def build_matplotlib_figure(self):
        #global canvas, fig, ax, canvas_widget, toolbar_frame
        self.fig = plt.figure(figsize=[8, 4], dpi=100) # более темный Заготовка для будущего окна
        self.ax = self.fig.add_subplot(111) # добавление осей
        self.ax.grid() # добавление сетки координат
        
        canvas = FigureCanvasTkAgg(self.fig, master = self.win) # Совмещение двух модулей Python
        canvas.draw() # Добавление окна графика в заготовку
        self.canvas_widget=canvas.get_tk_widget() # Преобразование окна в элемент интрефейса
        self.canvas_widget.grid(row=0, column=0, columnspan=4, sticky='nswe') # Размещение в приложении

        self.toolbar_frame = ctk.CTkFrame(master=self.win, width=1) # Создание контейнера, свободного пространства
        self.toolbar_frame.rowconfigure(0, minsize=15)
        self.toolbar_frame.columnconfigure(0, minsize=549)
        self.toolbar = NavigationToolbar2Tk(canvas, self.toolbar_frame) # Добавление самой панели навигации 
        self.toolbar_frame.grid(column=0, row=1, columnspan=self.columnspan, rowspan=self.rowspan, sticky='nswe', padx=1, pady=2) # лоя панели навигации 
        

class About_programm_window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__set_sizes()
        self.title('О программе')
        header = ctk.CTkLabel(self, anchor=ctk.CENTER, font=ctk.CTkFont('Calibri', size=30, weight='bold'), text='О программе')
        main_label = ctk.CTkLabel(self, justify=ctk.LEFT, font=ctk.CTkFont('Calibri', size=24), text='''
        Программа создана в рамках индивидуального проекта: 
        «Кубические уравнения и мнимые числа, история открытия решения,
        применение в реальной жизни»

        Уфимский колледж радиоэлектронки, телекоммуникации и безопасности
        Студент: Шайдулин Арслан 
        Группа: 9ИСП-11-22
        Преподаватель по математике: Идрисова Гульчачак Равиловна
        Преподаватель по информатике: Павленко Наталья Сергеевна

        Программа написана на языке Python
        Использованные модули:
        customtkinter
        re
        matplotlib
        sympy 
        ''')

        header.grid(column=0, row=0, columnspan=2, sticky='we') # Размещение надписи "О программе"
        main_label.grid(column=0, row=1, columnspan=2, sticky='w') # Размещене текста
        exit_btn = ctk.CTkButton(self, text='Выход', font=ctk.CTkFont(family='Calibri', size=22), command=self.destroy) # Создание кнопки выхода
        exit_btn.grid(row=2, column=1, sticky='nwse', padx=10, pady=10) # Размещение кнопки выхода

    def __set_sizes(self):
        self.geometry("825x630+1400+500")
        self.columnconfigure(0, minsize=250)
        self.columnconfigure(1, minsize=50)

        self.rowconfigure(0, minsize=50)
        self.rowconfigure(1, minsize=350)
        self.rowconfigure(2, minsize=50)
        
    def show(self):
        self.mainloop()


class Settings_window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.__set_sizes()
        self.title("Настройки")
        ctk.CTkLabel(self, text="Настройки\nДиапазон графика\nМин: -150; Макс: 150", font=ctk.CTkFont('Calibri', size=28)).grid(row=0, column=0, columnspan=4)
        ctk.CTkLabel(self, text='x мин:', font=ctk.CTkFont('Calibri', size=24)).grid(row=1, column=0) # Размещение
        ctk.CTkLabel(master=self, text='x макс:', font=ctk.CTkFont('Calibri', size=24)).grid(row=1, column=2)

        x_min = ctk.CTkEntry(self, font=ctk.CTkFont('Calibri', size=26))
        x_min.insert(0, '-5.0')
        x_min.grid(row=1, column=1, sticky='nswe') # Размещение

        x_max = ctk.CTkEntry(self, font=ctk.CTkFont('Calibri', size=26)) # Создание поля ввода для х макс
        x_max.insert(0, '5.0')
        x_max.grid(row=1, column=3, sticky='nswe') # Размещение

        Button_Constructor(master=self, text='Принять', command='set_settings',
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=2, column=0, columnspan=3, sticky='nswe', pady=20)

        x_min_controller = Ctrl.Input_controller('x_min', x_min)
        x_max_controller = Ctrl.Input_controller('x_max', x_max)

        ctk.CTkButton(self, text='Выход', command=self.destroy, font=ctk.CTkFont(family='Calibri', size=22)).grid(row=2, column=3, sticky='nswe', pady=20)

        example_1 = "Примеры\nx^3+2x^2+3x+6;\n"
        example_2 = "x^3-4x^2-16x+64;\n"
        example_3 = "8x^4+x^3+64x+8;\n"
        examples = [example_1, example_2, example_3]
        examples = ''.join(examples)

        ctk.CTkLabel(self, text=examples, font=ctk.CTkFont('Calibri', size=28), anchor='nw', padx=5).grid(row=0, column=4, sticky='nswe', columnspan=2)
        self.mainloop()

    def __set_sizes(self):
        self.geometry('660x335+1200+500')
        self.rows = [155, 50, 120]
        self.columns = [36, 86, 36, 86, 250]

        for i in range(len(self.rows)): self.rowconfigure(i, minsize=self.rows[i])
        for i in range(len(self.columns)): self.columnconfigure(i, minsize=self.columns[i])

    def show(self):
        self.mainloop()


class App(ctk.CTk):
    global x_min, x_max
    def __init__(self: ctk.CTk):
        super().__init__()
        self.__set_sizes()
        self.title("График и рcшение уравнений")
        
        Button_Constructor(master=self, text='Настройки', 
                          command=self.show_settings_win, 
                          font=ctk.CTkFont(family='Calibri', size=22)).grid(row=1, column=2, sticky='nswe')
        
        Button_Constructor(master=self, text='График уравнения',   
                           command='show_equation_graph', 
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=2, column=2,  sticky='nswe', padx=1, pady=2)
        
        Button_Constructor(master=self, text='График производной', 
                           command='show_deriv_graph', 
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=3, column=2,  sticky='nswe', padx=1, pady=2)
        
        Button_Constructor(master=self, text='Решить уравнение',   
                           command='solve_equation', 
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=4, column=2, sticky='nswe', padx=1, pady=2)
        
        Button_Constructor(master=self, text='Производная',        
                           command='derivation', 
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=5, column=2, sticky='nswe', padx=1, pady=2)
        
        Button_Constructor(master=self, text='О программе',        
                           command=self.show_about_program_window, 
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=6, column=0, sticky='nswe', padx=1, pady=2)
        
        Button_Constructor(master=self, text='Очистить',
                           command='clear_all', 
                           font=ctk.CTkFont(family='Calibri', size=22)).grid(row=6, column=1, sticky='nswe', padx=2, pady=2)
        
        ctk.CTkButton(master=self, text='Выход', 
                      command=self.quit,
                      font=ctk.CTkFont(family='Calibri', size=22)).grid(row=6, column=2, sticky='nswe', pady=2)

        ctk.CTkLabel(master=self, text='Уравнение:', font=ctk.CTkFont(family='Calibri', size=26)).grid(row=2, column=0)
        ctk.CTkLabel(master=self, text='Производная:', font=ctk.CTkFont(family='Calibri', size=26)).grid(row=3, column=0)
        ctk.CTkLabel(master=self, text='Корни\nуравнения:',font=ctk.CTkFont(family='Calibri', size=26)).grid(row=4, column=0, rowspan=2, sticky='nswe')
        
        self.deriv_output_frame = ctk.CTkFrame(master=self)
        self.deriv_output_frame.columnconfigure(0, minsize=391)
        self.deriv_output_frame.rowconfigure(0, minsize=15)

        self.output_frame = ctk.CTkScrollableFrame(master=self, width=391, height=20)
        self.output_frame.columnconfigure(0, minsize=391)
        self.output_frame.rowconfigure(0, minsize=15)
        self.output_frame.rowconfigure(1, minsize=15)

        self.deriv_output_frame.grid(row=3, column=1, sticky='nswe', pady=5)
        self.output_frame.grid(row=4, column=1, sticky='nswe', rowspan=2, pady=5)
    
        self.output = ctk.CTkLabel(master=self.output_frame, height=30,
                              text='Пример ввода:\n5x^3+15x^2-4x-12\nx^3-x^2-4x-6', 
                              font=ctk.CTkFont(family='Calibri', size=26),
                              anchor=ctk.CENTER) 
                              
    
        self.deriv_output = ctk.CTkLabel(master=self.deriv_output_frame, 
                                         text='', anchor=ctk.CENTER, 
                                         font=ctk.CTkFont(family='Calibri', size=26))

        self.output.grid(row=0, column=0, rowspan=2, sticky='nswe', padx=2)
        self.deriv_output.grid(row=0, column=0, sticky='nswe', padx=2)

        entry = ctk.CTkEntry(self, width=2, font=ctk.CTkFont(family='Calibri', size=34))
        entry.grid(row=2, column=1, sticky='nswe', padx=3, pady=2)

        main_input_controller = Ctrl.Input_controller(name='equation', win=entry)
        self.set_graphic_window(0, 0, 1, 2)

    def __set_sizes(self):
        self.geometry("800x960")
        self.resizable(True, True)
        self.columns = [160, 391, 180]
        self.rows = [475, 15, 15, 78, 78, 78, 78]

        for i in range(len(self.rows)): self.rowconfigure(i, minsize=self.rows[i], weight=0)

        for i in range(len(self.columns)): self.columnconfigure(i, minsize=self.columns[i], weight=0)
    
    def set_graphic_window(self, column:int, row:int, rowspan:int=1, columnspan:int=1):
        """Создает окно графика в заданном окне на заданном месте"""
        self.graph_win = Graphic_Window_Constructor(self, column, row, rowspan, columnspan)
        self.graph_win.build_matplotlib_figure()
        output_controller = Ctrl.Output_Controller(solution_output=self.output, derivation_output=self.deriv_output, graph_output=self.graph_win)

    def show_about_program_window(self):
        self.about_program_window = About_programm_window()
        self.about_program_window.mainloop()

    def show_settings_win(self):
        self.settings_win = Settings_window()
        self.settings_win.mainloop()


if __name__ == '__main__':
    try:
        app = App()
        app.mainloop()
    except Exception:
        exit()