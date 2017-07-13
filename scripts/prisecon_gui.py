import tkinter as tk
from tkinter import ttk


def main():
    select = tk.Tk()

    new_menu_button = tk.Menubutton(select, text="New", relief="raised")
    new_menu = tk.Menu(new_menu_button)
    new_menu.add_command(label="Experiment", command=new_experiment)
    new_menu.add_command(label="Economy", command=new_economy)
    new_menu.add_command(label="Prototype", command=new_prototype)

    edit_menu_button = tk.MenuButton(select)
    edit_menu = tk.Menu(edit_menu_button, text="Edit", relief="raised")
    edit_menu.add_command(label="Experiment", command=edit_experiment)
    edit_menu.add_command(label="Economy", command=edit_economy)
    edit_menu.add_command(label="Prototype", command=edit_prototype)

    simulate_menu_button = tk.Menubutton(
        select, text="Simulate", relief="raised")
    simulate_menu = tk.Menubutton(simulate_menu_button)
    simulate_menu.add_command(label="Experiment", relief="raised")
    simulate_menu.add_command(label="Economy", relief="raised")

    analyze_menu_button = tk.Menubutton(
        select, text="Analyze", relief="raised")
    analyze_menu = tk.Menu(analyze_menu_button)
    analyze_menu.add_command(label="Experiment", command=analyze_experiment)
    analyze_menu.add_command(label="Economy", command=analyze_economy)

    new_menu_button.pack()
    edit_menu_button.pack()
    simulate_menu_button.pack()
    analyze_menu_button.pack()
