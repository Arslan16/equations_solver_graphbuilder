import Handlers_module
import customtkinter as ctk


class Input_controller:
    """Отвечает за все поля ввода, чтобы брать данные для передатчика"""
    instances = {
        "equation": None,
        "x_max": None,
        "x_min": None
    }

    def __new__(cls, name, win):
        if cls.instances[name] == None:
            cls.instances[name] = super().__new__(cls)
        return cls.instances[name]
    
    def __init__(self, name, win):
        self.name = name
        self.win = win

    def get_input(self):
        return self.win.get()

    @classmethod
    def get_instance(cls, name):
        return cls.instances[name]
    

class Output_Controller:
    """Отвечает за вывод информации в соответствующее окно вывода, после
    получение данных от обработчика"""
    instance = None
    def __new__(cls, solution_output, derivation_output, graph_output):
        if cls.instance == None:
            cls.instance = super().__new__(cls) 
        return cls.instance

    def __init__(self, solution_output, derivation_output, graph_output):
        self.outputs = {
            'solution_output': solution_output,
            'derivation_output': derivation_output,
            'graph_output': graph_output
        }

    def output(self, output_data):
        """Осуществляет вывод полученных данных пользователю"""
        output_window:ctk.CTkLabel = self.outputs[output_data[-1]]

        if len(output_data) == 2:
            output_window.configure(text=output_data[0], font=ctk.CTkFont('Calibri', size=34), anchor=(ctk.CENTER), text_color='black')

        elif len(output_data) == 3:
            def get_data_to_axes(arr):
                arr_of_zeros = [0 for i in range( int(round(min(arr), 5)), int(round(max(arr), 5))+1)]
                sequence_arr = [i for i in range(int(round(min(arr), 5)), int(round(max(arr), 5))+1)]
                return arr_of_zeros, sequence_arr

            output_window.canvas_widget.destroy()
            output_window.toolbar_frame.destroy()
            output_window.build_matplotlib_figure()
            x_zeros, x_sequence = get_data_to_axes(arr=output_data[0])
            y_zeros, y_sequence = get_data_to_axes(arr=output_data[1])
            output_window.ax.plot(x_sequence, x_zeros, color='black')
            output_window.ax.plot(y_zeros, y_sequence, color='black') # ось у
            output_window.ax.plot(output_data[0], output_data[1]) # x=output_data[0] y=output_data[1]

    @classmethod
    def get_instance(cls):
        return cls.instance

# class Transmitter:
#     """Отвечает за обработку команды кнопок, принятие данных от контроллера полей ввода данных
#     Передачу данных обработчикам 
#     Принятие данных от обработчиков 
#     за вывод данных обработчика пользователю, через контроллер полей вывода"""
#     def __init__(self):
#         global x_max_input, x_min_input, x_max_value, x_min_value
#         self.solvers = {
#         'solve_equation':Handlers_module.solve_equation,
#         'derivation':Handlers_module.derivate}

#         self.graphics = {
#             'show_equation_graph':Handlers_module.show_equation_graph,
#             'show_deriv_graph':Handlers_module.show_deriv_graph}     

#         self.equation_input = (Input_controller.get_instance("equation"))
#         self.expression = self.equation_input.get_input()

#     def execute_command(self, command):
#         global x_min_value, x_max_value
#         output_window = Output_Controller.get_instance()
#         self.x_max_input = Input_controller.get_instance('x_max')
#         self.x_min_input = Input_controller.get_instance('x_min')

#         if command == 'set_settings':
#             self.x_max_input = Input_controller.get_instance('x_max')
#             self.x_min_input = Input_controller.get_instance('x_min')
#             x_max_value = float(self.x_max_input.get_input()) 
#             x_min_value = float(self.x_min_input.get_input()) 

#         if (self.x_max_input == None or self.x_min_input == None):
#             x_max_value = 5.0
#             x_min_value = -5.0
        
#         if command in self.solvers.keys():
#             command = self.solvers[command]
#             output_data = command(self.expression)
#             output_window.output(output_data) 

#         if command in self.graphics.keys():
#             if command == 'show_equation_graph':
#                 command = self.graphics[command]  
#                 output_data = command(self.expression, x_min_value, x_max_value) 
#                 output_window.output(output_data) 
#             elif command == 'show_deriv_graph':
#                 command = self.graphics[command] 
#                 output_data = command(x_min_value, x_max_value) 
#                 output_window.output(output_data) 

#         if command == 'clear_all':
#             graph_window = output_window.outputs['graph_output'] 

#             self.equation_input.win.delete(0, ctk.END)                        

#             output_data = () # Очистка сохранённых данных

#             # Очистка всех полей ввода/вывода
#             output_window.outputs['solution_output'].configure(text='') 
#             output_window.outputs['derivation_output'].configure(text='') 

#             graph_window.canvas_widget.destroy()
#             graph_window.toolbar_frame.destroy()
#             graph_window.build_matplotlib_figure()


class Transmitter:
    """Отвечает за обработку команды кнопок, принятие данных от контроллера полей ввода данных
    Передачу данных обработчикам 
    Принятие данных от обработчиков 
    за вывод данных обработчика пользователю, через контроллер полей вывода"""
    global x_max_input, x_min_input, x_max_value, x_min_value
    solvers = {
    'solve_equation':Handlers_module.solve_equation,
    'derivation':Handlers_module.derivate
    }

    graphics = {
        'show_equation_graph':Handlers_module.show_equation_graph,
        'show_deriv_graph':Handlers_module.show_deriv_graph
    }


    def execute_command(self, command):
        global x_min_value, x_max_value
        output_window = Output_Controller.get_instance()
        self.x_max_input = Input_controller.get_instance('x_max')
        self.x_min_input = Input_controller.get_instance('x_min')

        if command == 'set_settings':
            self.x_max_input = Input_controller.get_instance('x_max')
            self.x_min_input = Input_controller.get_instance('x_min')
            x_max_value = float(self.x_max_input.get_input()) 
            x_min_value = float(self.x_min_input.get_input()) 

        if (self.x_max_input == None or self.x_min_input == None):
            x_max_value = 5.0
            x_min_value = -5.0

        equation_input = Input_controller.get_instance("equation")
        if command in self.solvers.keys():
            command = self.solvers[command]
            expression = equation_input.get_input() 
            output_data = command(expression)
            output_window.output(output_data) 

        if command in self.graphics.keys():
            expression = equation_input.get_input() 
            if command == 'show_equation_graph':
                command = self.graphics[command]  
                output_data = command(expression, x_min_value, x_max_value) 
                output_window.output(output_data) 
            elif command == 'show_deriv_graph':
                command = self.graphics[command] 
                output_data = command(x_min_value, x_max_value) 
                output_window.output(output_data) 

        if command == 'clear_all':
            graph_window = output_window.outputs['graph_output'] 

            equation_input = Input_controller.get_instance("equation")
            equation_input.win.delete(0, ctk.END)                        

            output_data = () # Очистка сохранённых данных

            # Очистка всех полей ввода/вывода
            output_window.outputs['solution_output'].configure(text='') 
            output_window.outputs['derivation_output'].configure(text='') 

            graph_window.canvas_widget.destroy()
            graph_window.toolbar_frame.destroy()
            graph_window.build_matplotlib_figure()

