import tkinter as tk
import json

# Title of window
root = tk.Tk()
root.title("To-Do List")

# Title Icon
titleImage = tk.PhotoImage(file="image/title.png")
root.iconphoto(False, titleImage)

# Main Window
root.geometry("350x500+400+100")
root.configure(bg="black")
root.resizable(False, False)

# Top Bar
topImage = tk.PhotoImage(file="image/bar.png")
tk.Label(root, image=topImage, bg="#32405b").pack()

current_popup = None

# Create an empty list
tasks = []


# Listbox for displaying all the output/tasks
frame = tk.Frame(root, bd=3, width=700, height=300, bg="#32405b")
frame.pack(pady=(0, 0))

listBox = tk.Listbox(frame,
                     font=('arial', 21),
                     width=20,
                     height=12,
                     bg="#32405b",
                     fg="white",
                     selectbackground="#5a95ff")

listBox.pack(side="left", fill="both", padx=2)
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side="right", fill="both")

listBox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listBox.yview)


# Functions
def update_listbox():
    clear_listbox()
    for task in tasks:
        listBox.insert("end", f"{task['Task']} [{task['Category']}]")


# Save and Load buttons
save_button = tk.Button(root, text="Save", command=lambda: save_tasks)
save_button.pack(side="left", fill="both")

load_button = tk.Button(root, text="Load", command=lambda: load_tasks)
load_button.pack(side="left", fill="both")


# Save function
def save_tasks(event):
    with open("tasks.json", 'w') as file:
        json.dump(tasks, file)


# Load function
def load_tasks(event):
    global tasks
    try:
        with open("tasks.json", 'r') as file:
            tasks = json.load(file)
        update_listbox()
    except FileNotFoundError:
        return "No saved tasks found"


def clear_listbox():
    listBox.delete(0, "end")


def remove_task():
    # Get the text of the currently selected task
    task = listBox.curselection()
    # Confirm it is in the listbox
    if task:
        tasks.pop(task[0])
        # Update the listbox
        update_listbox()


# Close other popups
def close_popup():
    global current_popup
    if current_popup is not None:
        current_popup.destroy()
        current_popup = None


# Popup
def show_popup(title, icon):
    global current_popup
    close_popup()

    popup = tk.Toplevel(root)
    current_popup = popup
    popup.title(title)

    icon = tk.PhotoImage(file=f"image/{icon}")
    popup.iconphoto(False, icon)

    root.update_idletasks()
    root_width, root_height, root_x, root_y = [root.winfo_width(), root.winfo_height(), root.winfo_rootx(),
                                               root.winfo_rooty()]

    popup_width, popup_height, popup_x, popup_y = root_width, root_height // 2, root_x, root_y + root_height // 2

    popup.geometry(f"{popup_width}x{popup_height}+{popup_x}+{popup_y}")


# Category Popup
def category_popup():
    show_popup("Categories", "category1.png")

    # Create a listbox that will show all categories
    category_listbox = tk.Listbox(current_popup, font=('Arial', 15))
    category_listbox.pack()

    # Add "All" option to show all categories
    category_listbox.insert(tk.END, "All")

    button_asc = tk.Button(current_popup, text="Sort the categories in ascending order", command=lambda: sort_task(ascending=True))
    button_asc.pack()

    button_desc = tk.Button(current_popup, text="Sort the categories in descending order", command=lambda: sort_task(ascending=False))
    button_desc.pack()

    # Populate the listbox with all categories that exist
    for task in tasks:
        category = task.get('Category')
        if category not in category_listbox.get(0, tk.END):
            category_listbox.insert(tk.END, category)

    # Functions to filter tasks based on selected category
    def filter_by_category(event):
        global filtered_tasks
        selected_category = category_listbox.get(category_listbox.curselection())
        if selected_category == "All":
            filtered_update_listbox(tasks)
        else:
            filtered_tasks = [task for task in tasks if task['Category'] == selected_category]
            filtered_update_listbox(filtered_tasks)

    category_listbox.bind('<ButtonRelease-1>', filter_by_category)


def filtered_update_listbox(filtered_tasks):
    clear_listbox()
    for task in filtered_tasks:
        listBox.insert("end", f"{task['Task']} [{task['Category']}]")


def sort_task(ascending=True):
    global tasks
    tasks = sorted(tasks, key=lambda category: category['Category'], reverse=not ascending)
    update_listbox()


# Category Icon
categoryImage = tk.PhotoImage(file="image/category.png")
categoryLabel = tk.Label(root, image=categoryImage, bg="#000000")
categoryLabel.place(x=20, y=14)
categoryLabel.bind("<Button-1>", lambda event: category_popup())


# Add Popup
def add_popup():
    global entry_task
    global display_task
    global entry_category
    global display_category
    show_popup("Add Task", "add1.png")

    display_task = tk.Label(current_popup, text="")
    display_task.pack()

    entry_task = tk.Entry(current_popup)
    entry_task.pack()

    display_category = tk.Label(current_popup, text="")
    display_category.pack()

    entry_category = tk.Entry(current_popup)
    entry_category.pack()

    button_submit = tk.Button(current_popup, text="Submit", command=add_input)
    button_submit.pack()

    button_close = tk.Button(current_popup, text="Close", command=current_popup.destroy)
    button_close.pack()


# Main function for taking the input of the user
def add_input():
    task = entry_task.get()
    category = entry_category.get()

    if task and category != "":
        tasks.append({"Task": task, "Category": category})
        update_listbox()
    else:
        display_task["text"] = "Please enter a task"
        display_category["text"] = "Please enter a category"
    entry_task.delete(0, "end")
    entry_category.delete(0, "end")


# Add Icon
addImage = tk.PhotoImage(file="image/add.png")
addLabel = tk.Label(root, image=addImage, bg="#000000")
addLabel.place(x=110, y=15)
addLabel.bind("<Button-1>", lambda event: add_popup())


# Edit Popup
def edit_popup():
    global selected_index
    global entry_task
    global display_task
    global entry_category
    global display_category

    show_popup("Edit Task", "edit1.png")
    selected_index = listBox.curselection()
    if selected_index:
        selected_task = tasks[selected_index[0]]

        display_task = tk.Label(current_popup, text=f"Task selected: {selected_task['Task']}")
        display_task.pack()

        entry_task = tk.Entry(current_popup)
        entry_task.insert(0, selected_task['Task'])
        entry_task.pack()

        display_category = tk.Label(current_popup, text=f"Category selected: [{selected_task['Category']}]")
        display_category.pack()

        entry_category = tk.Entry(current_popup)
        entry_category.insert(0, selected_task['Category'])
        entry_category.pack()

        button_update = tk.Button(current_popup, text="Update the list", command=lambda: updated_input(selected_index[0]))
        button_update.pack()


def updated_input(selected_index):
    task = entry_task.get()
    category = entry_category.get()

    if task and category != "":
        tasks[selected_index] = {"Task": task, "Category": category}
        update_listbox()
        current_popup.destroy()
    else:
        display_task["text"] = "Please enter a task"
        display_category["text"] = "Please enter a category"


# Edit Icon
editImage = tk.PhotoImage(file="image/edit.png")
editLabel = tk.Label(root, image=editImage, bg="#000000")
editLabel.place(x=205, y=20)
editLabel.bind("<Button-1>", lambda event: edit_popup())

# Remove Icon
removeImage = tk.PhotoImage(file="image/remove.png")
removeLabel = tk.Label(root, image=removeImage, bg="#000000")
removeLabel.place(x=290, y=20)
removeLabel.bind("<Button-1>", lambda event: remove_task())

root.mainloop()
