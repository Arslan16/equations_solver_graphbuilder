from re import compile, split
from sympy import Symbol, solve

# Алгоритм, приводящий уравнение в корректный вид
def reform(expression):
    "Enternal method to reform the equation to correct view"
    global expression_reform, num
    num = [str(i) for i in range(0, 10)]
    signs = ['+', '-', '*', '/','(', ')', '^', '=']
    expression_reform = [] # Заготовка для корректного уравнения
    # Если в уравнении есть "=", тогда найти индекс =, иначе индекс 100
    border = expression.index('=') if '=' in expression else 1000
    for i in range(0, len(expression)): # Перебор по индексам в строке
        if expression[i] in num: # Если элемент - число
            # Если число стоит не первым, и перед ним какой либо знак
            if i != 0 and expression[i-1] in signs:
                if i < border: # Если число стоит до знака "="
                    expression_reform.append(expression[i]) # Добавить число без изменений
                else: # Иначе число стоит после знака "=", значит перед числом знак минус
                    # Если перед числом знак степени, то добавить без изменений
                    if expression[i-1] == '^' or bracket: 
                        expression_reform.append(expression[i])
                    # Если перед число =, то добавить минус, затем число
                    elif expression[i-1] == '=':
                        expression_reform.append(f"-")
                        expression_reform.append(expression[i])
                    else:
                        #expression_reform.append(f"-")
                        expression_reform.append(expression[i])
            else: 
                expression_reform.append(expression[i])

        if expression[i] == 'x': # Если элемент х и он не в начале
            if i == 0:
                expression_reform.append('1*x')
            elif i != 0:
                if expression[i-1] in num or expression[i] == ')': # Если перед "х" число(множитель) или скобка то сначала 
                    expression_reform.append('*x') # добавить знак умножения, атем добавить "х"
                elif expression[i-1] == '*': # Если пользователь сам ввел знак умножения перед "х"
                    expression_reform.append('x') # То добавить просто х
                else: # Если перед "х" нет множителя и знака умножения, значит множитиель "1"
                    if i < border:
                        expression_reform.append('1*x') # Добавить "1*х"
                    else:
                        expression_reform.append('-1*x')

        if expression[i] in signs: # Если элемент - знак
            if expression[i] == '(': # Если элемент - это левая скобка
                bracket = True
                if i != 0: # Если скобка не стоит первая в уравнении (избежание IndexError)
                    if expression[i-1] == ')' or expression[i-1] in num or expression[i-1] == 'x': 
                        # Если перед скобкой другая скобка или число, то добавить знак *
                        expression_reform.append('*(')
                    elif expression[i-1] == '*':
                        expression_reform.append('(')
                    elif expression[i-1] == '+' or expression[i-1] == '-':
                        expression_reform.append('1*(')
                    elif expression[i-1] == '=':
                        expression_reform.append('-1*(')
                else: # Если левая скобка стоит первая
                    expression_reform.append('1*(')

            elif expression[i] == ')': # Если скобка правая
                bracket = False
                if i != len(expression)-1: # Если скобка не стоит последняя (избежание IndexError)
                    if expression[i+1] in num: # Если перед скобкой число, то добавить *
                        expression_reform.append(')*')
                    else: 
                        expression_reform.append(')')
                else: # Если скобка стоит последней.
                    expression_reform.append(')')

            elif expression[i] == '^':
                expression_reform.append('**')
            elif expression[i] == '=':
                continue
            else: # Если любой другой знак
                if ((expression[i] == '+') or(expression[i] == '-')) and (i > border) and (bracket == False): 
                    if expression[i] == '+':
                        expression_reform.append('-')
                    elif expression[i] == '-':
                        expression_reform.append('+')
                elif expression[i] != '/' and i > border and bracket == True: 
                    expression_reform.append(expression[i])  
                elif expression[i] == '/':
                    expression_reform.append('/')
                else:
                    expression_reform.append(expression[i])

    expression_reform = ''.join(expression_reform) # Соединение всех элементов в строку
    return expression_reform 


# Алгоритм, разделяющий уравнение на составные части для производной
def devision(expression):
    global num, list_of_parts
    i = 0
    list_of_parts = []  # набор составных частей уравнения
    part = '' # Одна состовная часть выражения
    bracket = False # Показатель того, что элемент находиться или не находится в скобке
    while True:
        # Если элемент не последний
        if i != len(expression): 
            # Если элемент не знак
            if expression[i] not in ('(', ')', '+', '-', '*'):
                part += expression[i] # К прошлому выражению добавить новый элемент  

            elif expression[i] == '*':
                # Если началась следующая часть выражения, значит нынешнюю часть добавить
                # Начать новую, отдельно добавить знак умножения
                if expression[i+1] == '(' and expression[i-1] == ')':
                    list_of_parts.append(part)
                    part = ''
                    list_of_parts.append(str(expression[i]))
                    bracket = False
                # Если знак умножения находится внутри скобки или связывает множитель скобки и скобку
                else: 
                    part += expression[i]  

            # Если началась часть внутри скобки, то добавить скобку
            elif expression[i] == '(':
                bracket = True
                part += expression[i]
            # Если скобка закончилась, то добавить скобку, 
            elif expression[i] == ')':
                part += expression[i]
                bracket = False
            # элемент это знак + или -
            elif expression[i] in ('+', '-'):
                # Если зак находится внутри скобки, то добавить к старому выражению
                # и создание выражения не прекращать
                if bracket:
                    part += expression[i]
                else:
                    # Если длина части не нулевая
                    if len(part) != 0:
                        # Готовую часть добавить в список
                        list_of_parts.append(part)
                        part = '' # Часть начать снова
                    # элемент + - добавить отдельно
                    list_of_parts.append(str(expression[i]))
                    bracket = False     
            i += 1
        else:
            if len(part) != 0:
                list_of_parts.append(part)
            break

# Функция для нахождения производной. Кнопка "Производная"
def derivate(expression):
    global deriv, sign, i_sign, expression_reform, num
    def return_derivate(value, part_in_brackets=None, is_part_in_brackets=None): 
        global deriv, sign, i_sign, num
        num = [str(i) for i in range(0, 10)]
        # Для удобства восприятия возвращается знак ^
        value = str(value).replace('**', '^')
        Fx_new = None
        if (str(value[-1]) == 'x'): # если х в первой степени
            Fx_new = str(value).replace('*x','') # Удаление х # Добавление только множителя; (7х)' = 7
        elif '^' in value:
            value = split('[* ^]+', value) # разделение на части
            if int(value[0]) != 1: # если множитель не единица
                if int(value[2])-1 == 1: # если производная степень = 1, то не показывать
                    Fx_new = f'{int(value[0])*int(value[2])}{value[1]}' # (множитель*степень)х
                else: 
                    # Нахождение производной; (множитель*степень)х^(степень-1)
                    Fx_new = f'{int(value[0])*int(value[2])}{value[1]}^{int(value[2])-1}' 
            elif int(value[0]) == 1: # если множитель 1
                if int(value[2])-1 == 1: # если производная степень = 1, то не показывать
                    Fx_new = f'{value[2]}{value[1]}'
                else:
                    # Нахождение производной; (Степень)*х^(Степень-1)
                    Fx_new = f'{int(value[2])}{value[1]}^{int(value[2])-1}'

        if Fx_new:
            if is_part_in_brackets == 'all': # 0 если производная степени скобки
                part_in_brackets = str(part_in_brackets).replace('**', '^').replace('*x', 'x')
                deriv.append(Fx_new.replace('x', part_in_brackets)) 

            elif is_part_in_brackets == 'first': # Если первая часть скобки
                deriv.append('*(') # то добавить *( и первое слагаемое в скобках 
                deriv.append(Fx_new)                 
                if len(sipob) != 0:
                    deriv.append(str(sipob[0])) # Добавление знака 
                    sipob.pop(0)
            elif is_part_in_brackets == 'middle': # Если это не первая и не конечная часть скобки
                deriv.append(Fx_new) # то добавить как есть 
                if len(sipob) != 0:
                    deriv.append(str(sipob[0])) # добавить знак для скобки 
                    sipob.pop(0)
            elif is_part_in_brackets == 'end': # Если конечная часть скобки
                deriv.append(Fx_new) # то в конце добавить закрывающую скобку  
                deriv.append(')') 
            else: # Если это слагаемое не относится ни к какой скобке
                deriv.append(Fx_new) # добавить производное и знак 
                if len(sign) != 0:
                    deriv.append(str(sign[0])) # Добавление знака 
                    sign.pop(0)
 
        else: # Если слагаемое не прошло никаких преобразований 
            if is_part_in_brackets == 'first':
                if deriv[-1] == ('+' or '-'): # Если в производной лишний знак
                    deriv.pop()   # то его удалить, добавить *( 
                deriv.append('*(') 
            if is_part_in_brackets == 'middle':
                sipob.pop(0) # Если слагаемое в скобке в середине, то удалить не нужный знак в скобке
            if is_part_in_brackets == 'end': # если в конце остается лишний знак в производной
                if deriv[-1] == ('+' or '-'): # он удаляется, добавляется )
                    deriv.pop() 
                deriv.append(")") 
                if len(sign) != 0: # Если знаки еще есть, то после скобки добавить
                    deriv.append(str(sign[0])) 
                    sign.pop(0)
            elif len(sign) != 0: # Если слагаемое не из скобки не прошло никаких преобразований, то удалить
                sign.pop(0) # неиспользованный знак         

    sign = [] # заготовка для знаков исходного уравнения
    deriv = [] # заготовка для производной уравнения
    i_sign = 0 # счетчик индекса знака

    expression = reform(expression) # Преобразвание уравнения
    devision(expression) # разделение на части для дальнейшего нахождения производной

    for i in list_of_parts: # Последовательное добавление знаков из исходного уравнения
        if i == '+':
            sign.append('+')
            list_of_parts.remove(i)
        elif i == '-':
            if list_of_parts.index(i) == 0: # Если в уравнении первый х или число отрицательное, 
                deriv.append('-') # то оно сразу идет в производную
                list_of_parts.remove(i)
            else:
                sign.append('-')
                list_of_parts.remove(i)

    if len(sign) == 0: # Если знака нет, добавить знак, чтобы не возникла IndexError
        sign.append('+')
    # Разделение уравнения на составлные части по знакам

    for part in list_of_parts: # Работа с каждой частью отдельно
        # Если слагаемое сложное, то есть есть скобки
        if ('(' and ')') in part:
            start_index = part.find('(')
            end_index = part.find(')') # Найти местоположение скобок по индексам
            part_in_brackets = part[start_index+1:end_index] # Выделить часть в скобках
            expression = str(part).replace(part_in_brackets, 'x') # В исхоном выражении заменить на х
            # Найти производную степенной скобки как для обычного х
            return_derivate(expression, part_in_brackets, is_part_in_brackets='all') 
            sipob = [] # отдельное хранилище для знаков внутри скобок
            # заполнение хранилища знаков внутри скобки
            for i in range(0, len(part)): 
                if part[i] == '+':
                    sipob.append('+')
                elif part[i] == '-':
                    sipob.append('-')
            # разделение части в скобках по знакам на отдельные составляющие  
            part_in_brackets = split("[+ -]+", part_in_brackets) 
            for k in range(0, len(part_in_brackets)):
                if k == 0: # Если элемент первый, отправить с флажком "first" для добавления в производную " *( "
                    return_derivate(part_in_brackets[k], is_part_in_brackets='first') 
                # Если элемент не первый и не оследний, отправить с флажком "middle"
                elif k != 0 and k != len(part_in_brackets)-1: 
                    return_derivate(part_in_brackets[k], is_part_in_brackets='middle')
                # Если элемент последний, отправить с флажком end для добавления в производную " ) "
                elif k == len(part_in_brackets)-1:
                    return_derivate(part_in_brackets[k], is_part_in_brackets='end')
        # Если слагаемое простое, то отправить на преобразование сразу
        else:
            return_derivate(part)

    # Если после преобразований остается лишний знак, то он удаляется
    if deriv[-1] == '+' or deriv[-1] == '-':
        deriv.pop()

    # Соединение в одну строку
    deriv = ''.join(deriv)
    return (deriv, 'derivation_output')

def solve_equation(expression):
    global solution, expression_reform
    # Полученние уравнения из поля ввода
    x = Symbol('x') # Символ, относительно которого будет решаться уравнение
    symbols = "^[a-wyzA-WYZА-ЧШ-Яа-чш-яёЁ]+$" # Все символы кроме х
    pattern = compile(symbols) 
    if len(expression) == 0: # Проверка на ввод
        return ('Ошибка! Введите уравнение!', 'solution_output')
    elif pattern.search(expression) is not None:  
        # Проверка, если будут найдены какие либо символы помимо "х", то выдать ошибку
        return ('Ошибка! Введите уравнение! Не строку!', 'solution_output') # 
    else: expression_reform = reform(expression)

    # обработка ошибок
    try:
        # метод библиотеки Python - solve для решения уравнений
        # возвращает список из корней
        solution = solve(expression_reform, x)
    except:
        # В случае ошибки прекращение выполнения функции и вывод ошибки пользователю
        return ('Ошибка! Неверный формат ввода!', 'solution_output') 

    # Последовательное добавление в отформатированую строку
    # для удобного отображения. Пример "х1=2" "х2=4"
    solution_string = []
    for i in range(0, len(solution)):
        solution_string.append(f'x{i+1}={solution[i]}; \n')   
    # преврращение в единую строку
    solution_string = ''.join(solution_string)
    # замена символов компьютера более понятными для человека аналогами
    # I заменяется на √(-1); замена 'sqrt' на '√'
    solution_string = solution_string.replace('I', '√(-1)').replace('sqrt', '√')
    return (solution_string, 'solution_output')
   
# Кнопка "График уравнения"
def show_equation_graph(expression, x_min_value, x_max_value):
    global y_list, expression_reform
    expression_reform = reform(expression) # Преобразование уравнения
    # Передача в функцию для создания графика
    output_data = show_graph(expression_reform, x_min_value, x_max_value)
    return output_data

# Кнопка "График производной"
def show_deriv_graph(x_min_value, x_max_value):
    global deriv, deriv_graph
    try:
        deriv_graph = reform(deriv) # Если производная найдена, то привести ее к корректному виду
    except NameError: # Если производной нет, то просьба найти ее
        return ('Ошибка! Найдите производную!', 'solution_output')
    output_data = show_graph(deriv_graph, x_min_value, x_max_value) # Передача в функцию для создания графика
    return output_data

# Функция отрисовки графика
def show_graph(expression, x_min_value, x_max_value):
    global y_list

    x_list = [] 
    y_list = []

    i = x_min_value # Перекидывание значения x_min чтобы не изменять глобального значения 
    while i <= x_max_value: 
        x_list.append(i) 
        i += 0.25 # Нахождение всех х в заданном диапазоне с шагом 0.25
        # for не используется, так как он работает только с целыми значениями

    for x in x_list:
        # Нахождение значения функции в каждой точке х
        y_list.append(eval(expression)) 
        
    # Добавление графика
    return (x_list, y_list, 'graph_output')