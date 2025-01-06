from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = Button("Complete", hx_get=f'/toggle/{todo.id}', target_id = tid)
    delete = Button("Delete", hx_delete=f'/{todo.id}', hx_swap = 'outerHTML', target_id = tid)
    return Li(toggle,'  ',delete,'  ',todo.title,' || ', todo.body, ' || ' , todo.c_date,' || ' , todo.d_date,' || ' ,  todo.tag , " " +  ('Completed' if todo.is_completed else ''),id=tid )

app,rt,todos,Todo = fast_app('todos.db',render=render,id=int, title=str,
                    body=str,c_date = str,
                    d_date = str, tag = str,
                    is_completed = bool,pk = 'id')


@rt('/')
def get():   

    frm = Form(Input(name='title', placeholder ="Enter your Task Title"),
                    Input(name='body', placeholder ="Enter your Task"),
                    Input(name='c_date', type= 'date' ),
                    Input(name='d_date', type= 'date'),
                    #Tags for the task had 4 different types 'dt' for DailyTask, 'pert' for PersonalTask, 'colt' for CollegeTask and 'wt' for WorkTask
                    Input(name='tag', placeholder ="Enter your Task Tag"),
                     Button('Add'),hx_post='/', target_id = "todo-list", 
                     hx_swap = 'beforeend')

    tdlist = Ul(*todos(),id = "todo-list")
    sort = Button(A('List',href='/lt'))
    return Titled("TODO LIST", Card(tdlist,header=frm ), sort)

@rt('/{tid}')
def delete(tid:int):
    todos.delete(tid)  


@rt('/')
def post(title: str, body: str, c_date: str, d_date: str, tag: str):
    new_todo = Todo(
        title=title,
        body=body,
        c_date=c_date,
        d_date=d_date,
        tag = tag,
        is_completed=False
    )
    return todos.insert(new_todo)

@rt('/toggle/{tid}')
def get(tid:int): 
    todo = todos[tid]
    todo.is_completed = not todo.is_completed
    todos.update(todo)
    return render(todo)

@rt('/lt')
def get():
    back = Button(A('DashBoard',href='/'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd'))
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("TODO LIST ITEMS", back ,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                    Ul(*todos(),id = "todo-list"))

@rt('/ct')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt'))   
    return Titled("Completed TASKS",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*[todo for todo in todos() if todo.is_completed],id = "todo-list"))

@rt('/pt')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("Pending TASKS",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags:  ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*[todo for todo in todos() if not todo.is_completed ],id = "todo-list"))

@rt('/scd')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("SORTED BY CREATED DATE",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*todos(order_by = 'c_date'),id = "todo-list"))

@rt('/sdd')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("SORTED BY CREATED DATE",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*[todo for todo in todos(order_by = 'd_date') if todo.d_date],id = "todo-list"))

@rt('/dt')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("SORTED BY CREATED DATE",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*todos(where="tag='dt'"),id = "todo-list"))

@rt('/pert')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("SORTED BY CREATED DATE",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*todos(where="tag='pert'"),id = "todo-list"))

@rt('/colt')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("SORTED BY CREATED DATE",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*todos(where="tag='colt'"),id = "todo-list"))

@rt('/wt')
def get():
    back = Button(A('Full List',href='/lt'))
    ct = Button(A('Completed Task',href='/ct')) 
    pt = Button(A('Pending Task',href='/pt')) 
    scd = Button(A('Sort By Creating Date',href='/scd')) 
    sdd = Button(A('Sort By Due Date',href='/sdd')) 
    dt = Button(A('DailyTask',href='/dt')) 
    pert = Button(A('PersonalTask',href='/pert')) 
    colt = Button(A('CollegeTask',href='/colt')) 
    wt = Button(A('WorkTask',href='/wt')) 
    return Titled("SORTED BY CREATED DATE",back,
                  Card(ct,' ',pt,' ',scd,' ',sdd,' | Tags: ' ,dt,' ',pert,' ',colt,' ',wt), 
                  Ul(*todos(where="tag='wt'"),id = "todo-list"))




serve()
