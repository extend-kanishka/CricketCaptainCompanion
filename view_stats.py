from tkinter import *
from tkinter import ttk
import db_connection
import psycopg2
from tkinter import messagebox
from datetime import datetime
from tkinter import Frame, Label, Entry, StringVar, Radiobutton, Button, ttk
conn = db_connection.connect_to_db()
cur = conn.cursor()
upper_tree = None
lower_tree = None
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#It grabs all the stuff from Tkinter so we can make GUI with windows, buttons, and all that jazz.
#It pulls in ttk from Tkinter for some slick-looking widgets, like fancy buttons or tables.
#It brings in a custom file called db_connection.py that’s got the code to hook up to a database.
#It gets psycopg2 to let us mess with a PostgreSQL database.
#It takes messagebox from Tkinter to pop up little alerts, like “yo, something went wrong” or “all good!”
#It grabs datetime to deal with dates and times in the code.
#It pulls in specific Tkinter bits like Frame, Label, Entry, and a few others to build the GUI.
#It calls a function from db_connection.py to link up with the database and keeps that connection in a thing called conn.
#It makes a cursor thingy from the database connection so we can run SQL queries.
#It sets up a variable called upper_tree for a table-like thing (Treeview) and leaves it empty (None) for now.
#It sets up another variable called lower_tree for another table-like thing, also empty (None) to start.

##################################################################################################################################################################


def create_view_stats_tab(notebook):
    global upper_tree, lower_tree

    frame = Frame(notebook, bg="#404040")
    notebook.add(frame, text="STATS ||> FIELDING OVERVIEW")

    # Treeview styling
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    

    style.map('Treeview',background=[('selected', "#1D1D1D")])

    # ------------ UPPER TABLE: MOST CATCHES ------------


    button_frame = Frame(frame, bg="#404040", padx=10, pady=10)
    button_frame.place(relx=0.7, rely=0, relwidth=0.3, relheight=0.5)
    upper_frame = Frame(frame, bg="#404040", padx=10, pady=10)
    upper_frame.place(relx=0.7, rely=0.05, relwidth=0.3, relheight=0.7)



    upper_label = Label(upper_frame, text="BEST FIELDERS", font=('Arial', 14, 'bold'),
                        bg="#404040", fg="white")
    upper_label.pack(pady=(0, 5))

    upper_scroll = Scrollbar(upper_frame)
    upper_scroll.pack(side=RIGHT, fill=Y)

    upper_tree = ttk.Treeview(upper_frame, yscrollcommand=upper_scroll.set, selectmode="extended")
    upper_tree.pack(fill=BOTH, expand=True)
    upper_scroll.config(command=upper_tree.yview)

    upper_tree['columns'] = ("PlayerID", "Name", "Catches", "RunOuts")
    upper_tree.column("#0", width=0, stretch=NO)
    upper_tree.column("PlayerID", anchor=CENTER, width=40)
    upper_tree.column("Name", anchor=CENTER, width=150)
    upper_tree.column("Catches", anchor=CENTER, width=75)
    upper_tree.column("RunOuts", anchor=CENTER, width=75)
    for col in upper_tree['columns']:
        upper_tree.heading(col, text=col, anchor=CENTER)

    upper_tree.tag_configure('oddrow', background="white")
    upper_tree.tag_configure('evenrow', background="lightblue")











    lower_frame = Frame(frame, bg="#404040", padx=10, pady=10)
    lower_frame.place(relx=0.7, rely=0.75, relwidth=0.3, relheight=0.25)

    lower_label = Label(lower_frame, text="BEST KEEPERS", font=('Arial', 14, 'bold'),
                        bg="#404040", fg="white")
    lower_label.pack(pady=(0, 5))

    lower_scroll = Scrollbar(lower_frame)
    lower_scroll.pack(side=RIGHT, fill=Y)

    lower_tree = ttk.Treeview(lower_frame, yscrollcommand=lower_scroll.set, selectmode="extended")
    lower_tree.pack(fill=BOTH, expand=True)
    lower_scroll.config(command=lower_tree.yview)

    lower_tree['columns'] = ("PlayerID", "Name", "Catches", "Stumpings", "RunOuts")
    lower_tree.column("#0", width=0, stretch=NO)
    lower_tree.column("PlayerID", anchor=CENTER, width=40)
    lower_tree.column("Name", anchor=CENTER, width=150)
    lower_tree.column("Catches", anchor=CENTER, width=60)
    lower_tree.column("Stumpings", anchor=CENTER, width=70)
    lower_tree.column("RunOuts", anchor=CENTER, width=70)
    for col in lower_tree['columns']:
        lower_tree.heading(col, text=col, anchor=CENTER)

    lower_tree.tag_configure('oddrow', background="white")
    lower_tree.tag_configure('evenrow', background="lightblue")



    def plot_fielding_stats(parent_frame):

        for widget in fielding_chart_frame.winfo_children():
            widget.destroy()

        try:
            cur = conn.cursor()
            # Get top 5 players by catches
            query = '''
                SELECT p.name, SUM(f.catches) AS total_catches
                FROM fielding_stats f
                JOIN players p ON p.id = f.player_id
                GROUP BY p.name
                ORDER BY total_catches DESC
                LIMIT 5
            '''
            cur.execute(query)
            data = cur.fetchall()
            if not data:
                messagebox.showinfo("No Data", "No fielding data found.")
                return

            names = [row[0] for row in data]
            catches = [row[1] for row in data]

            # Plotting
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.barh(names, catches, color='skyblue')
            ax.set_xlabel('Catches')
            ax.set_title('Top 5 Fielders by Catches')
            ax.invert_yaxis()  # Highest first

            # Display in Tkinter

            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        except psycopg2.Error as e:
            conn.rollback()
            messagebox.showerror("Database Error", str(e))


    

    def plot_catches_progression(parent_frame):
        try:
            cur = conn.cursor()
            cur.execute('''
                SELECT m.id, SUM(f.catches) AS total_catches
                FROM fielding_stats f
                JOIN matches m ON f.match_id = m.id
                GROUP BY m.id
                ORDER BY m.id
            ''')
            data = cur.fetchall()
            if not data:
                messagebox.showinfo("No Data", "No match fielding data found.")
                return

            # Instead of using match_date, we label x-axis as Match 1, Match 2, etc.
            match_labels = [f"Match {i+1}" for i in range(len(data))]
            totals = [row[1] for row in data]

            fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
            ax.plot(match_labels, totals, marker='o', color='orange')
            ax.set_title('Total Catches by Matches')
            ax.set_ylabel("Number of Catches")
            ax.tick_params(axis='x')
            canvas = FigureCanvasTkAgg(fig, master=parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        except psycopg2.Error as e:
            conn.rollback()
            messagebox.showerror("DB Error", str(e))


    def plot_both_fielding_charts(btn):
        plot_fielding_stats(fielding_chart_frame)
        plot_catches_progression(progression_chart_frame)
        btn.config(state="disabled")



    fielding_chart_frame = Frame(frame, bg="#404040")
    fielding_chart_frame.place(relx=0.015, rely=0.025, relwidth=0.674, relheight=0.46)

    progression_chart_frame = Frame(frame, bg="#404040")
    progression_chart_frame.place(relx=0.015, rely=0.515, relwidth=0.674, relheight=0.46)




    
        
    # Refresh Button
    plot_btn = Button(button_frame, text="Plot Statistics",
                    bg="#4169E1", fg="white", padx=10)
    plot_btn.grid(row=0, column=0, padx=5, pady=5)
    plot_btn.config(command=lambda: plot_both_fielding_charts(plot_btn))

    # Refresh Button
    refresh_btn = Button(button_frame, text="Refresh Tables",
                        command=refresh_view_stats,
                        bg="#228B22", fg="white", padx=10)
    refresh_btn.grid(row=0, column=1, padx=5, pady=5)






    refresh_view_stats()
    



    
    





    return frame









def refresh_view_stats():
    global upper_tree, lower_tree
    if not upper_tree or not lower_tree:
        return

    try:
        # Clear tables
        upper_tree.delete(*upper_tree.get_children())
        lower_tree.delete(*lower_tree.get_children())

        # UPPER TABLE: Most Catches + RunOuts
        query1 = '''
            SELECT p.id, p.name, SUM(f.catches) as total_catches, SUM(f.run_outs) as total_run_outs
            FROM fielding_stats f
            JOIN players p ON f.player_id = p.id
            GROUP BY p.id
            ORDER BY (SUM(f.catches) + SUM(f.run_outs)) DESC
        '''
        cur.execute(query1)
        results1 = cur.fetchall()
        for idx, row in enumerate(results1):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            upper_tree.insert("", "end", values=row, tags=(tag,))

        # LOWER TABLE: Only Wicketkeepers
        query2 = '''
            SELECT p.id, p.name, SUM(f.catches), SUM(f.stumpings), SUM(f.run_outs)
            FROM fielding_stats f
            JOIN players p ON f.player_id = p.id
            WHERE LOWER(p.type) = 'wicketkeeper'
            GROUP BY p.id
        '''
        cur.execute(query2)
        results2 = cur.fetchall()
        for idx, row in enumerate(results2):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            lower_tree.insert("", "end", values=row, tags=(tag,))

    except psycopg2.Error as e:
        conn.rollback()
        print("Database error:", e)





