from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import StringVar
from tkinter.ttk import Combobox
import db_connection
conn = db_connection.connect_to_db()
import datetime
import update_stats_tab
populate_functions = {}
import view_stats
import os

import bowler_stats_recentmatches
import bowler_stats_timeframe
import batsman_stats_recentmatches
import batsman_stats_timeframe
import player_view_dashboard
import player_view_match_by_match

x = datetime.datetime.now()
date_string = f"{x.year}/{x.month:02d}/{x.day:02d}"



mainphoto = None  
addbutton = None
clearbutton = None
updatebutton = None
deletebutton = None





def create_user_manager_tab(notebook):

    
    ##############################################################            TREEVIEW AND FRAME          #############################################

    tab = Frame(notebook, bg="#404040")
    notebook.add(tab, text='USER MANAGER')
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground = "#D3D3D3")
    style.map('Treeview',
              background=[('selected',"#1d1d1d")])
    tree_frame =  Frame(tab)
    tree_frame.place(relx=0.009,rely=0.016,relwidth=0.6255,relheight=0.968)
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT,fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set,selectmode="extended")
    my_tree.pack(fill=BOTH , expand=True)
    tree_scroll.config(command=my_tree.yview)
    my_tree['columns']=("ID","PID","Name","Age","Type","Username","Password","Role")
    my_tree.column("#0",width=0,stretch=NO)
    my_tree.column("ID", width=0, stretch=NO) 
    my_tree.column("PID", anchor=CENTER , width=50)
    my_tree.column("Name",anchor=CENTER,width=150)
    my_tree.column("Age",anchor=CENTER,width=80)
    my_tree.column("Type",anchor=CENTER,width=140)
    my_tree.column("Username",anchor=CENTER,width=140)
    my_tree.column("Password",anchor=CENTER,width=140)
    my_tree.column("Role",anchor=CENTER,width=120)
    my_tree.heading("#0",text="",anchor=CENTER)
    my_tree.heading("ID", text="", anchor=CENTER) 
    my_tree.heading("PID", text="PID", anchor=CENTER)
    my_tree.heading("Name",text="Name",anchor=CENTER)
    my_tree.heading("Age",text="Age",anchor=CENTER)
    my_tree.heading("Type",text="Type",anchor=CENTER)
    my_tree.heading("Username",text="Username",anchor=CENTER)
    my_tree.heading("Password",text="Password",anchor=CENTER)
    my_tree.heading("Role",text="Role",anchor=CENTER)
    my_tree.tag_configure('oddrow',background="white")
    my_tree.tag_configure('evenrow',background="lightblue")

    
#######################################################################       DATA SELECTION        #######################################################

    data_frame = LabelFrame(tab,text="Data")
    data_frame.place(x=985,y=425,width=550,height=205)

    name_label = Label(data_frame,text="Name")
    name_label.grid(row=0,column=0,padx=(35,30),pady=30)
    name_entry=Entry(data_frame)
    name_entry.grid(row=0,column=1,padx=10,pady=20)

    age_label = Label(data_frame,text="Age")
    age_label.grid(row=0,column=2,padx=50,pady=20)
    age_entry=Entry(data_frame)
    age_entry.grid(row=0,column=3,pady=30)

    username_label = Label(data_frame,text="Username")
    username_label.grid(row=1,column=0)
    username_entry=Entry(data_frame)
    username_entry.grid(row=1,column=1)

    password_label = Label(data_frame,text="Password")
    password_label.grid(row=1,column=2)
    password_entry=Entry(data_frame)
    password_entry.grid(row=1,column=3)

    type_label = Label(data_frame,text="Type")
    type_label.grid(row=2,column=0,pady=30)
    type_entry=Entry(data_frame)
    type_entry.grid(row=2,column=1)

    role_label = Label(data_frame,text="Role")
    role_label.grid(row=2,column=2)
    role_entry=Entry(data_frame)
    role_entry.grid(row=2,column=3)

    
######################################################################         FUNCTIONS         ########################################################

    def populate_treeview():
    # Clear the existing Treeview first
        for item in my_tree.get_children():
            my_tree.delete(item)
        cur = conn.cursor()
        # We join players and users because the data is split
        cur.execute("""
            SELECT u.id,p.id, p.name, p.age, p.type, u.username, u.password, u.role
            FROM users u
            JOIN players p ON u.player_id = p.id
            ORDER BY u.id
        """)
        rows = cur.fetchall()
        # Re-populate the Treeview
        for idx, row in enumerate(rows):
            user_id, player_id, name, age, type_, username, password, role = row
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            my_tree.insert("", "end", iid=user_id, text="",
                        values=(user_id, player_id, name, age, type_, username, password, role),
                        tags=(tag,))

        cur.close()





    def add_record():
        name = name_entry.get()
        age = age_entry.get()
        player_type = type_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        role = role_entry.get()

        user_id = db_connection.add_user_and_player(
            conn, name, age, player_type, username, password, role
        )

        if user_id:
            # Insert into treeview too
            '''global count
            if user_id % 2 == 0:
                my_tree.insert("", "end", iid=user_id, text="", 
                    values=(user_id, player_id, name, age, player_type, username, password, role), tags=('evenrow',))
            else:
                my_tree.insert("", "end", iid=user_id, text="", 
                    values=(user_id, player_id, name, age, player_type, username, password, role), tags=('oddrow',))
            count += 1
            clear_entries()
            messagebox.showinfo("Success", "Record added successfully.")'''
            populate_treeview()
            clear_entries()
        refresh_combobox_options()
        
        


    
    

    
    def select_record(e):
        name_entry.delete(0,END)
        age_entry.delete(0,END)
        type_entry.delete(0,END)
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        role_entry.delete(0,END)

        #grab record number
        selected = my_tree.focus()
        #grab record values
        values = my_tree.item(selected,'values')
        #outputs to entryboxes
        
        if not values or len(values) < 8:
            return
        name_entry.insert(0,values[2])
        age_entry.insert(0,values[3])
        type_entry.insert(0,values[4])
        username_entry.insert(0,values[5])
        password_entry.insert(0,values[6])
        role_entry.insert(0,values[7])


    def clear_entries():
        name_entry.delete(0,END)
        age_entry.delete(0,END)
        type_entry.delete(0,END)
        username_entry.delete(0,END)
        password_entry.delete(0,END)
        role_entry.delete(0,END)

        
    def remove_many():
        response = messagebox.askyesno(
            "Confirm Delete",
            "This will delete all selected records from the database.\nAre you sure?"
        )

        if response:
            selected = my_tree.selection()
            user_ids_to_delete = []

            # Collect user_ids from Treeview
            for record in selected:
                user_id = my_tree.item(record, 'values')[0]
                user_ids_to_delete.append(user_id)

            try:
                cur = conn.cursor()

                # Delete related players via player_id
                # First delete users, then players (or handle with CASCADE if foreign key allows)
                for user_id in user_ids_to_delete:

                    cur.execute("SELECT player_id FROM users WHERE id = %s", (user_id,))
                    result = cur.fetchone()
                    player_id = result[0] if result else None
                    # Delete user first
                    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))

                    # Optionally delete player too
                    if player_id:
                        cur.execute("DELETE FROM players WHERE id = %s", (player_id,))

                conn.commit()
                cur.close()

                # Remove from Treeview
                for record in selected:
                    my_tree.delete(record)

                clear_entries()
                messagebox.showinfo("Deleted", "Selected records deleted successfully.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to delete records.\n{e}")
        refresh_combobox_options()

    
    def update_record():
        selected = my_tree.focus()
        if not selected:
            messagebox.showerror("Error", "No data selected.")
            return

        # Fetch user_id from Treeview (first column)
        user_id = my_tree.item(selected, 'values')[0]

        # Get updated data from Entry fields
        name = name_entry.get()
        age = age_entry.get()
        type_ = type_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        role = role_entry.get()

        try:
            cur = conn.cursor()

            # Update players table (linked through player_id foreign key)
            cur.execute("""
                UPDATE players
                SET name = %s, age = %s, type = %s
                WHERE id = (SELECT player_id FROM users WHERE id = %s)
            """, (name, age, type_, user_id))

            # Update users table
            cur.execute("""
                UPDATE users
                SET username = %s, password = %s, role = %s
                WHERE id = %s
            """, (username, password, role, user_id))

            conn.commit()
            cur.close()

            # Refresh the Treeview
            populate_treeview()
            clear_entries()
            messagebox.showinfo("Success", "Record updated successfully.")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update record.\n{e}")

        refresh_combobox_options()
        

    ########################################################################       IMAGES        ########################################################

    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    global mainphoto
    global addbutton
    global clearbutton
    global updatebutton
    global deletebutton
    
    mainphoto = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "bitmap.png"))
    addbutton = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "button1.png"))
    updatebutton = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "button2.png"))
    clearbutton = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "button3.png"))
    deletebutton = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "button4.png"))

    label = Label(tab,image = mainphoto)
    label.place(x=985,y=0)

############################################################################       BUTTONS        #######################################################

    button_frame = LabelFrame(tab,text="Commands")
    button_frame.place(x=985,y=631,width=550,height=140)

    add_button = Button(button_frame,image=addbutton,command=add_record)
    add_button.grid(row=0,column=0,padx=45,pady=20)
    
    clear_button = Button(button_frame,image=clearbutton,command=clear_entries)
    clear_button.grid(row=0,column=1)

    update_button = Button(button_frame,image=updatebutton,command = update_record)
    update_button.grid(row=0,column=2,padx=45)

    remove_one_selected = Button(button_frame,image=deletebutton,command=remove_many)
    remove_one_selected.grid(row=0,column=3)

    
    ########################################################################        OTHERS         ############################################################

    #Bind the treeview
    my_tree.bind("<ButtonRelease-1>",select_record)
    my_tree.bind("<Return>", select_record)
    populate_treeview()

    return tab















player_vars = []  # Store StringVars to retrieve selection later
player_comboboxes = []  # Store Comboboxes themselves if needed
player_options = []  # Initialize this early




def refresh_combobox_options():
    # Fetch fresh player options from database
    cur = conn.cursor()
    cur.execute("SELECT name || ' (' || id || ')' FROM players ORDER BY name")
    global player_options
    player_options = [row[0] for row in cur.fetchall()]
    cur.close()

    # Set full player list to all comboboxes
    for combo in player_comboboxes:
        combo['values'] = player_options


























def create_enter_stats_tab(notebook):
    tab = Frame(notebook, bg="#404040")
    notebook.add(tab, text='ENTER STATS')
    x = datetime.datetime.now()
    date_string = f"{x.year}/{x.month:02d}/{x.day:02d}"

    
    ##################################################################################     TOP ENTRIES      ###########################################################
    
    

   
    matchdate_label = Label(tab, text="Match Date", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    matchdate_label.grid(row=1, column=1, padx=(80, 5), pady=35)  

    matchdate_entry = Entry(tab, font=('Arial', 12, 'bold'))
    matchdate_entry.grid(row=1, column=2, padx=(5, 40), pady=35)  
    matchdate_entry.insert(0, date_string)

   
    opponent_label = Label(tab, text="Opponent", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    opponent_label.grid(row=1, column=3, padx=(40, 5), pady=35)


    opponent_entry = Entry(tab, font=('Arial', 12, 'bold'))  
    opponent_entry.grid(row=1, column=4, padx=(5, 40), pady=35)

    
    location_label = Label(tab, text="Location", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    location_label.grid(row=1, column=5, padx=(40, 5), pady=35)

    location_entry = Entry(tab, font=('Arial', 12, 'bold'))
    location_entry.grid(row=1, column=6, padx=(5, 40), pady=35)

    
    matchtype_label = Label(tab, text="Match Type", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    matchtype_label.grid(row=1, column=7, padx=(40, 5), pady=35)

    matchtype_entry =Entry(tab, font=('Arial', 12, 'bold'))
    matchtype_entry.grid(row=1, column=8, padx=(5, 40), pady=35)

    #######################################################################################    FUNCTIONS      #################################################

    def move_to_next_entry(event, current_index, entries, grid_size):
        """Move focus to the next Entry widget when Enter is pressed."""
        next_index = (current_index + 1) % len(entries)  # Wrap to 0 after last entry
        entries[next_index].focus_set()
        return "break"  # Prevent default Enter behavior (like adding newlines)

    

    def clear_entries():
    # Clear top entries
        matchdate_entry.delete(0, END)
        opponent_entry.delete(0, END)
        location_entry.delete(0, END)
        matchtype_entry.delete(0, END)

        # Refill date
        x = datetime.datetime.now()
        matchdate_entry.insert(0, f"{x.year}/{x.month:02d}/{x.day:02d}")

        # Clear grid entries
        for entry in my_entries:
            entry.delete(0, END)

        # Clear comboboxes
        for combo in player_comboboxes:
            combo.set('')
        refresh_combobox_options()


    def submit_stats():
        try:
            cur = conn.cursor()

            # Insert into matches
            match_date = matchdate_entry.get()
            opponent = opponent_entry.get()
            location = location_entry.get()
            match_type = matchtype_entry.get()

            cur.execute("""
                INSERT INTO matches (match_date, opponent, location, match_type)
                VALUES (%s, %s, %s, %s) RETURNING id
            """, (match_date, opponent, location, match_type))
            match_id = cur.fetchone()[0]

            combo_values = [combo.get() for combo in player_comboboxes]


            if any(val.strip() == "No match found" for val in combo_values):
                messagebox.showerror("Invalid Selection", "One or more player selections are invalid ('No match found'). Please correct them before submitting.")
                return

            # Filter valid selections
            selected_players = [val for val in combo_values if val and 'No match' not in val]
            unique_players = set(selected_players)

            if len(selected_players) != len(unique_players):
                messagebox.showerror("Error", "Duplicate players selected! Each player must be unique.")
                conn.rollback()
                return

            # For as many players as selected
            for row_index, combo in enumerate(player_comboboxes):
                selected = combo.get()
                if not selected or 'No match' in selected:
                    continue
                
                player_id = int(selected.split('(')[-1].strip(')'))

                row_entries = my_entries[row_index*11 : (row_index+1)*11]
                values = [(entry.get().strip() or '0') for entry in row_entries]

                # Batting
                runs_input = values[0]
                dismissal = True
                if runs_input.endswith('*'):
                    dismissal = False
                    runs_input = runs_input.rstrip('*')
                runs_scored = int(runs_input or 0)
                balls_faced, fours, sixes = map(int, values[1:4])

                cur.execute("""
                    INSERT INTO batting_stats (player_id, match_id, runs_scored, balls_faced, fours, sixes, dismissal)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (player_id, match_id, runs_scored, balls_faced, fours, sixes, dismissal))

                # Bowling
                balls_bowled, runs_conceded, wickets, maidens = map(int, values[4:8])
                cur.execute("""
                    INSERT INTO bowling_stats (player_id, match_id, balls_bowled, runs_conceded, wickets, maidens)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (player_id, match_id, balls_bowled, runs_conceded, wickets, maidens))

                # Fielding
                catches, run_outs, stumpings = map(int, values[8:11])
                cur.execute("""
                    INSERT INTO fielding_stats (player_id, match_id, catches, run_outs, stumpings)
                    VALUES (%s, %s, %s, %s, %s)
                """, (player_id, match_id, catches, run_outs, stumpings))

            conn.commit()
            cur.close()
            populate_functions['frame1']()
            populate_functions['frame2']()
            populate_functions['frame3']()
            populate_functions['frame4']()
            messagebox.showinfo("Success", "Match and stats saved successfully.")

            # Clear the entries after success
            for combo in player_comboboxes:
                combo.set('')
            for entry in my_entries:
                entry.delete(0, END)

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Failed", f"Failed to submit stats:\n{e}")

        #######################################################################################    MAIN ENTRYBOXES      #################################################

    entry_frame = LabelFrame(tab ,bg="#404040")
    entry_frame.place(x=250,y=120,width=1260,height=592)
        

    my_entries = []

    for y in range(11):
        for x in range(11):
            my_entry = Entry(entry_frame, width=10, font=('Arial', 12, 'bold'))
            my_entry.grid(row = y , column = x , padx = 10 , pady = 15)
            my_entry.bind("<Return>", lambda event, idx=len(my_entries): move_to_next_entry(event, idx, my_entries, 11))
            my_entries.append(my_entry)

        

    tableplayername = Label(tab, text="PLAYER NAME", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablerunsscored = Label(tab, text="Runs\nScored", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tableballsfaced = Label(tab, text="Balls\nFaced", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablefours = Label(tab, text="Fours\nHit", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablesixes = Label(tab, text="Sixes\nHit", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tableballsbowled = Label(tab, text="Balls\nBowled", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablerunsconceded = Label(tab, text="Runs\nConceded", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablewicketstaken = Label(tab, text="Wickets\nTaken", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablemaidens = Label(tab, text="Maiden\nOvers", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablecatchestaken = Label(tab, text="Catches\nTaken", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablerunouts = Label(tab, text="Run\nOuts", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tablestumpings = Label(tab, text="Stumping\nDone", font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    tableplayername.place(x=60,y=100)
    tablerunsscored.place(x=280,y=90)
    tableballsfaced.place(x=395,y=90)
    tablefours.place(x=510,y=90)
    tablesixes.place(x=625,y=90)
    tableballsbowled.place(x=734,y=90)
    tablerunsconceded.place(x=838,y=90)
    tablewicketstaken.place(x=958,y=90)
    tablemaidens.place(x=1074,y=90)
    tablecatchestaken.place(x=1186,y=90)
    tablerunouts.place(x=1310,y=90)
    tablestumpings.place(x=1405,y=90)


    submit_button = Button(tab, text="Submit Stats", font=('Arial', 12, 'bold'),bg="#48EDA6", command=submit_stats)
    submit_button.place(x=1400, y=725)  # Adjust placement as needed



    ##########################################################         COMBOBOXES           #################################################          


          
    

    

    

    last_key_was_enter = {'flag': False}
    def filter_combobox(event, combo, var):
    # Ignore navigation keys
        if event.keysym in ('Up', 'Down', 'Left', 'Right', 'Tab'):
            return
        
        typed = var.get().lower()

        if typed == '':
            refresh_combobox_options()  # Show all options again
        else:
            filtered = [option for option in player_options if typed in option.lower()]
            combo['values'] = filtered if filtered else ['No match found']

        if event.keysym == 'Return':
            if not last_key_was_enter['flag']:
                combo.event_generate('<Down>')
                last_key_was_enter['flag'] = True
            else:
                last_key_was_enter['flag'] = False
                focus_next_combobox(combo)  # Focus away from combobox (any widget)
            return  # Stop extra Enter behavior
        last_key_was_enter['flag'] = False
        combo.icursor(END)

    
    def focus_next_combobox(current_combo):
        try:
            idx = player_comboboxes.index(current_combo)
            next_combo = player_comboboxes[(idx + 1) % len(player_comboboxes)]
            next_combo.focus_set()
        except ValueError:
            pass


    refresh_combobox_options()
    for i in range(11):
        var = StringVar()#StringVar() is a tkinter variable class used to store and manage the selected value of the Combobox
        player_vars.append(var)
        combo = Combobox(tab, textvariable=var, values=player_options, width=20, font=('Arial', 12, 'bold'))
        combo.place(x=20, y=137 + i * 53)  # Adjust x/y as per your design
        combo.bind('<KeyRelease>', lambda event, c=combo, v=var: filter_combobox(event, c, v))
        player_comboboxes.append(combo)

    


    


    #update when user updates content
    def on_combo_cleared(event, combo):
        if not combo.get().strip():
            refresh_combobox_options()

    
        

    #update after selection
    def on_combo_selected(event):
        refresh_combobox_options()

    for combo in player_comboboxes:
        combo.bind('<FocusOut>', lambda e, c=combo: on_combo_cleared(e, c))
        combo.bind('<<ComboboxSelected>>', on_combo_selected)


    return tab











































def create_view_stats_tab(notebook):
    tab = Frame(notebook, bg="#404040")
    notebook.add(tab, text='VIEW STATS')
    # Widgets go here
    return tab

def show_admin_gui():
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    window = Tk()
    window.state('zoomed')
    window.title("Cricket Captain Companion")
    window.geometry('1920x1080')
    window.configure(bg='#333333')
    icon = PhotoImage(file=os.path.join(BASE_DIR, "Assets", "path6.png"))
    #icon = PhotoImage(file='C:\\Users\\ACER\\Desktop\\Project\\Assets\\path6.png')
    window.iconphoto(True, icon)

    notebook = ttk.Notebook(window)
    notebook.pack(expand=True, fill="both")

    
    create_user_manager_tab(notebook)
    create_enter_stats_tab(notebook)

    update_tab, populate1, populate2, populate3, populate4 = update_stats_tab.create_update_stats_tab(notebook)
    populate_functions['frame1'] = populate1
    populate_functions['frame2'] = populate2
    populate_functions['frame3'] = populate3
    populate_functions['frame4'] = populate4
    view_stats.create_view_stats_tab(notebook)
    batsman_stats_timeframe.create_view_stats_tab(notebook)
    batsman_stats_recentmatches.create_view_stats_tab(notebook)
    bowler_stats_timeframe.create_view_stats_tab(notebook)
    bowler_stats_recentmatches.create_view_stats_tab(notebook)
    player_view_dashboard.create(notebook)
    player_view_match_by_match.create(notebook)
    
    
    


    window.mainloop()

