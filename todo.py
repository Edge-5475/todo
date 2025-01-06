from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = Button("Complete", hx_get=f'/toggle/{todo.id}', target_id = tid)
    return Li(toggle,todo.title,' || ', todo.body, ' || ' , todo.c_date,' || ' , todo.d_date + " " + ('Completed' if todo.is_completed else ''),id=tid )

app,rt,todos,Todo = fast_app('todos.db',render=render,id=int, title=str,
                    body=str,c_date = str,
                    d_date = str, 
                    is_completed = bool )


@rt('/')
def get():   
    
    frm = Form(Input(name='title', placeholder ="Enter your Task Title"),
                    Input(name='body', placeholder ="Enter your Task"),
                    Input(name='c_date', type= 'date' ),
                    Input(name='d_date', type= 'date'),
                     Button('Add'),hx_post='/', target_id = "todo-list", 
                     hx_swap = 'beforeend')

    tdlist = Ul(*todos())
    
    return Titled("TODO LIST", frm ,tdlist)

@rt('/')
def post(title:str):
    return title  

@rt('/toggle/{tid}')
def get(tid:int): 
    todo = todos[tid]
    todo.is_completed = not todo.is_completed
    todos.update(todo)
    return render(todo)

serve()