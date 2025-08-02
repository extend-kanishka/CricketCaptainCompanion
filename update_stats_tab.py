

from tkinter import ttk, Frame, Label, Entry
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox
import db_connection

conn = db_connection.connect_to_db()

def create_frame1(parent):
    frame = Frame(parent, bg="#404040")
    # Configure Treeview style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#d3d3d3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview',
              background=[('selected', "#1D1D1D")])
    
    # Create Treeview frame and scrollbar
    tree_frame = Frame(frame)
    tree_frame.place(relx=0.01, rely=0.016, relwidth=0.64, relheight=0.976)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack(fill=BOTH, expand=True)
    tree_scroll.config(command=my_tree.yview)
    my_tree['columns'] = ("MID","PlayerID", "Player", "Runs", "Balls", "Fours", "Sixes")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("MID", anchor=CENTER, width=50)
    my_tree.column("PlayerID", anchor=CENTER, width=50)  
    my_tree.column("Player", anchor=CENTER, width=150)
    my_tree.column("Runs", anchor=CENTER, width=50)
    my_tree.column("Balls", anchor=CENTER, width=50)
    my_tree.column("Fours", anchor=CENTER, width=50)
    my_tree.column("Sixes", anchor=CENTER, width=50)
    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("MID", text="MID", anchor=CENTER)
    my_tree.heading("PlayerID", text="PID", anchor=CENTER)
    my_tree.heading("Player", text="Player", anchor=CENTER)
    my_tree.heading("Runs", text="Runs", anchor=CENTER)
    my_tree.heading("Balls", text="Balls", anchor=CENTER)
    my_tree.heading("Fours", text="Fours", anchor=CENTER)
    my_tree.heading("Sixes", text="Sixes", anchor=CENTER)
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    datanbutton_frame = Frame(frame,bg="#404040")
    datanbutton_frame.place(relx=0.65, rely=0.0, relwidth=0.34, relheight=1)

    batsman_label = Label(datanbutton_frame,text="BATTING ENTRIES",font=('Arial', 16, 'bold'), fg="#FFFFFF", bg="#404040")
    batsman_label.place(x=40,y=15)
    
    runs_label = Label(datanbutton_frame, text="Runs",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    runs_label.grid(row=0, column=0,padx=35,pady=(70,20))
    runs_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    runs_entry.grid(row=0, column=1,padx=20,pady=(70,20))
    
    balls_label = Label(datanbutton_frame, text="Balls",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    balls_label.grid(row=1, column=0)
    balls_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    balls_entry.grid(row=1, column=1)
    
    fours_label = Label(datanbutton_frame, text="Fours",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    fours_label.grid(row=2, column=0,pady=20)
    fours_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    fours_entry.grid(row=2, column=1)
    
    sixes_label = Label(datanbutton_frame, text="Sixes",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    sixes_label.grid(row=3, column=0)
    sixes_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    sixes_entry.grid(row=3, column=1)
    
    
    



    def populate_treeview():
        # Clear Treeview
        for item in my_tree.get_children():
            my_tree.delete(item)

        cur = conn.cursor()
        cur.execute("""
            SELECT b.match_id, p.id, p.name, b.runs_scored, b.balls_faced, b.fours, b.sixes, b.dismissal
            FROM batting_stats b
            JOIN players p ON b.player_id = p.id
            ORDER BY b.match_id DESC
        """)
        rows = cur.fetchall()

        for idx, row in enumerate(rows):
            match_id, player_id, player_name, runs, balls, fours, sixes, dismissal = row

            # If not out, add *
            runs_display = f"{runs}*" if dismissal is False else str(runs)

            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            my_tree.insert("", "end", text="",
                        values=(match_id, player_id, player_name, runs_display, balls, fours, sixes),
                        tags=(tag,))

        cur.close()

    #populate_treeview()

    
    
    def clear_entries():
        runs_entry.delete(0,END)
        balls_entry.delete(0,END)
        sixes_entry.delete(0,END)
        fours_entry.delete(0,END)



    def select_record(e):

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        

        if not values or len(values) < 7:
            return  # Exit early

        clear_entries()

        ##selected = my_tree.focus()
        #values = my_tree.item(selected, 'values')
        
        runs_entry.insert(0, values[3])
        balls_entry.insert(0, values[4])
        fours_entry.insert(0, values[5])
        sixes_entry.insert(0, values[6])




        
    def remove_many():
        response = messagebox.askyesno(
            "Confirm Delete",
            "This will delete all selected batting records from the database.\nAre you sure?"
        )

        if response:
            selected = my_tree.selection()
            records_to_delete = []

            # Collect (match_id, player_id) pairs from Treeview
            for record in selected:
                match_id = my_tree.item(record, 'values')[0]
                player_id = my_tree.item(record, 'values')[1]
                records_to_delete.append((match_id, player_id))

            try:
                cur = conn.cursor()

                for match_id, player_id in records_to_delete:
                    cur.execute("""
                        DELETE FROM batting_stats
                        WHERE match_id = %s AND player_id = %s
                    """, (match_id, player_id))

                conn.commit()
                cur.close()

                # Remove visually from Treeview
                for record in selected:
                    my_tree.delete(record)

                clear_entries()
                messagebox.showinfo("Deleted", "Selected batting records deleted successfully.")

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to delete records.\n{e}")

    
    def update_record():
        selected = my_tree.focus()
        if not selected:
            messagebox.showerror("Error", "No record selected.")
            return

        # Get selected values from Treeview
        values = my_tree.item(selected, 'values')
        match_id = values[0]
        player_id = values[1]

        # Find the corresponding player_id via player name


            # Get updated data from entries
        runs_input = runs_entry.get().strip()
        balls = balls_entry.get().strip() or 0
        fours = fours_entry.get().strip() or 0
        sixes = sixes_entry.get().strip() or 0

        dismissal = True
        if runs_input.endswith('*'):
            dismissal = False
            runs_input = runs_input.rstrip('*')

        runs = int(runs_input) if runs_input else 0

        try:
            cur = conn.cursor()   # Update the database
            cur.execute("""
                UPDATE batting_stats
                SET runs_scored = %s,
                    balls_faced = %s,
                    fours = %s,
                    sixes = %s,
                    dismissal = %s
                WHERE match_id = %s AND player_id = %s
            """, (runs, balls, fours, sixes, dismissal, match_id, player_id))

            conn.commit()
            cur.close()

            populate_treeview()
            clear_entries()
            messagebox.showinfo("Success", "Record updated successfully.")
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update record.\n{e}")


     # Bind Treeview
    my_tree.bind("<ButtonRelease-1>", select_record)

    # Buttons
    update_btn = Button(datanbutton_frame, text="Update", width=15, bg="#2F66A1", fg="white", font=('Arial', 10, 'bold'), command=update_record)
    update_btn.grid(row=4, column=0, columnspan=2, pady=(30,7))

    delete_btn = Button(datanbutton_frame, text="Delete", width=15, bg="#823423", fg="white", font=('Arial', 10, 'bold'), command=remove_many)
    delete_btn.grid(row=5, column=0, columnspan=2, pady=7)

    clear_btn = Button(datanbutton_frame, text="Clear", width=15, bg="#3E7335", fg="white", font=('Arial', 10, 'bold'), command=clear_entries)
    clear_btn.grid(row=6, column=0, columnspan=2, pady=7)

    populate_treeview()

    
    return frame, populate_treeview




























def create_frame2(parent):
    frame = Frame(parent, bg="#404040")
    # Configure Treeview style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#d3d3d3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview',
              background=[('selected', "#1D1D1D")])
    
    # Create Treeview frame and scrollbar
    tree_frame = Frame(frame)
    tree_frame.place(relx=0.01, rely=0.01, relwidth=0.64, relheight=0.976)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack(fill=BOTH, expand=True)
    tree_scroll.config(command=my_tree.yview)
    my_tree['columns'] = ("MID","PlayerID", "Player", "Balls", "Runs", "Wickets", "Maidens")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("MID", anchor=CENTER, width=50)
    my_tree.column("PlayerID", anchor=CENTER, width=50)  
    my_tree.column("Player", anchor=CENTER, width=150)
    my_tree.column("Balls", anchor=CENTER, width=50)
    my_tree.column("Runs", anchor=CENTER, width=50)
    my_tree.column("Wickets", anchor=CENTER, width=50)
    my_tree.column("Maidens", anchor=CENTER, width=50)
    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("MID", text="MID", anchor=CENTER)
    my_tree.heading("PlayerID", text="PID", anchor=CENTER)
    my_tree.heading("Player", text="Player", anchor=CENTER)
    my_tree.heading("Balls", text="Balls", anchor=CENTER)
    my_tree.heading("Runs", text="Runs", anchor=CENTER)
    my_tree.heading("Wickets", text="Wickets", anchor=CENTER)
    my_tree.heading("Maidens", text="Maidens", anchor=CENTER)
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    datanbutton_frame = Frame(frame,bg="#404040")
    datanbutton_frame.place(relx=0.65, rely=0.0, relwidth=0.34, relheight=1)

    bowler_label = Label(datanbutton_frame,text="BOWLING ENTRIES",font=('Arial', 16, 'bold'), fg="#FFFFFF", bg="#404040")
    bowler_label.place(x=40,y=15)

    balls_label = Label(datanbutton_frame, text="Balls",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    balls_label.grid(row=0, column=0,padx=35,pady=(70,20))
    balls_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    balls_entry.grid(row=0, column=1,padx=20,pady=(70,20))
    
    runs_label = Label(datanbutton_frame, text="Runs",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    runs_label.grid(row=1, column=0)
    runs_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    runs_entry.grid(row=1, column=1)
    
    
    wickets_label = Label(datanbutton_frame, text="Wickets",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    wickets_label.grid(row=2, column=0,pady=20)
    wickets_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    wickets_entry.grid(row=2, column=1,pady=20)
    
    maidens_label = Label(datanbutton_frame, text="Sixes",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    maidens_label.grid(row=3, column=0)
    maidens_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    maidens_entry.grid(row=3, column=1)
    
    
    



    def populate_treeview():
        # Clear Treeview
        for item in my_tree.get_children():
            my_tree.delete(item)

        cur = conn.cursor()
        cur.execute("""
            SELECT b.match_id, p.id, p.name, b.balls_bowled, b.runs_conceded, b.wickets, b.maidens
            FROM bowling_stats b
            JOIN players p ON b.player_id = p.id
            ORDER BY b.match_id DESC
        """)
        rows = cur.fetchall()

        for idx, row in enumerate(rows):
            match_id, player_id, player_name, balls, runs, wickets, maidens = row

            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            my_tree.insert("", "end", text="",
                        values=(match_id, player_id, player_name, balls, runs, wickets, maidens),
                        tags=(tag,))

        cur.close()

    #populate_treeview()

    
    
    def clear_entries():
        balls_entry.delete(0,END)
        runs_entry.delete(0,END)
        wickets_entry.delete(0,END)
        maidens_entry.delete(0,END)


    


    def select_record(e):

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        

        if not values or len(values) < 7:
            return  # Exit early

        clear_entries()

        ##selected = my_tree.focus()
        #values = my_tree.item(selected, 'values')
        
        balls_entry.insert(0, values[3])
        runs_entry.insert(0, values[4])
        wickets_entry.insert(0, values[5])
        maidens_entry.insert(0, values[6])

    '''def select_record(e):
        clear_entries()

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        balls_entry.insert(0, values[3])
        runs_entry.insert(0, values[4])
        wickets_entry.insert(0, values[5])
        maidens_entry.insert(0, values[6])'''




        
    def remove_many():
        response = messagebox.askyesno(
            "Confirm Delete",
            "This will delete all selected batting records from the database.\nAre you sure?"
        )

        if response:
            selected = my_tree.selection()
            records_to_delete = []

            # Collect (match_id, player_id) pairs from Treeview
            for record in selected:
                match_id = my_tree.item(record, 'values')[0]
                player_id = my_tree.item(record, 'values')[1]
                records_to_delete.append((match_id, player_id))

            try:
                cur = conn.cursor()

                for match_id, player_id in records_to_delete:
                    cur.execute("""
                        DELETE FROM bowling_stats
                        WHERE match_id = %s AND player_id = %s
                    """, (match_id, player_id))

                conn.commit()
                cur.close()

                # Remove visually from Treeview
                for record in selected:
                    my_tree.delete(record)

                clear_entries()
                messagebox.showinfo("Deleted", "Selected bowling records deleted successfully.")

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to delete records.\n{e}")

    
    def update_record():
        selected = my_tree.focus()
        if not selected:
            messagebox.showerror("Error", "No record selected.")
            return

        # Get selected values from Treeview
        values = my_tree.item(selected, 'values')
        match_id = values[0]
        player_id = values[1]

        


            # Get updated data from entries
        
        balls = balls_entry.get().strip() or 0
        runs = runs_entry.get().strip() or 0
        wickets = wickets_entry.get().strip() or 0
        maidens = maidens_entry.get().strip() or 0

        

        try:
            cur = conn.cursor()   # Update the database
            cur.execute("""
                UPDATE bowling_stats
                SET balls_bowled = %s,
                    runs_conceded = %s,
                    wickets = %s,
                    maidens = %s
                
                WHERE match_id = %s AND player_id = %s
            """, (balls, runs, wickets, maidens, match_id, player_id))

            conn.commit()
            cur.close()

            populate_treeview()
            clear_entries()
            messagebox.showinfo("Success", "Record updated successfully.")
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update record.\n{e}")


     # Bind Treeview
    my_tree.bind("<ButtonRelease-1>", select_record)

    # Buttons
    update_btn = Button(datanbutton_frame, text="Update", width=15, bg="#2F66A1", fg="white", font=('Arial', 10, 'bold'), command=update_record)
    update_btn.grid(row=4, column=0, columnspan=2, pady=(30, 7))

    delete_btn = Button(datanbutton_frame, text="Delete", width=15, bg="#823423", fg="white", font=('Arial', 10, 'bold'), command=remove_many)
    delete_btn.grid(row=5, column=0, columnspan=2, pady=7)

    clear_btn = Button(datanbutton_frame, text="Clear", width=15, bg="#3E7335", fg="white", font=('Arial', 10, 'bold'), command=clear_entries)
    clear_btn.grid(row=6, column=0, columnspan=2, pady=7)

    populate_treeview()

    
    return frame, populate_treeview






























def create_frame3(parent):
    frame = Frame(parent, bg="#404040")
    # Configure Treeview style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#d3d3d3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview',
              background=[('selected', "#1D1D1D")])
    
    # Create Treeview frame and scrollbar
    tree_frame = Frame(frame)
    tree_frame.place(relx=0.01, rely=0.016, relwidth=0.64, relheight=0.976)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack(fill=BOTH, expand=True)
    tree_scroll.config(command=my_tree.yview)
    my_tree['columns'] = ("MID","PlayerID", "Player", "Catches", "Runouts", "Stumpings")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("MID", anchor=CENTER, width=50)
    my_tree.column("PlayerID", anchor=CENTER, width=50)  
    my_tree.column("Player", anchor=CENTER, width=150)
    my_tree.column("Catches", anchor=CENTER, width=50)
    my_tree.column("Runouts", anchor=CENTER, width=50)
    my_tree.column("Stumpings", anchor=CENTER, width=50)
    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("MID", text="MID", anchor=CENTER)
    my_tree.heading("PlayerID", text="PID", anchor=CENTER)
    my_tree.heading("Player", text="Player", anchor=CENTER)
    my_tree.heading("Catches", text="Catches", anchor=CENTER)
    my_tree.heading("Runouts", text="RunOuts", anchor=CENTER)
    my_tree.heading("Stumpings", text="Stumpings", anchor=CENTER)
    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    datanbutton_frame = Frame(frame,bg="#404040")
    datanbutton_frame.place(x=500, y=0, width=300, height=432)

    fielder_label = Label(datanbutton_frame,text="FIELDING ENTRIES",font=('Arial', 16, 'bold'), fg="#FFFFFF", bg="#404040")
    fielder_label.place(x=40,y=20)

    catches_label = Label(datanbutton_frame, text="Catches",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    catches_label.grid(row=0, column=0,padx=35,pady=(80,20))
    catches_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    catches_entry.grid(row=0, column=1,padx=5,pady=(80,20))
    
    runouts_label = Label(datanbutton_frame, text="RunOuts",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    runouts_label.grid(row=1, column=0)
    runouts_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    runouts_entry.grid(row=1, column=1)
    
    
    stumpings_label = Label(datanbutton_frame, text="Stumpings",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    stumpings_label.grid(row=2, column=0,pady=20)
    stumpings_entry = Entry(datanbutton_frame,width=10,font=('Arial', 12, 'bold'))
    stumpings_entry.grid(row=2, column=1,pady=20)
    

    
    
    



    def populate_treeview():
        # Clear Treeview
        for item in my_tree.get_children():
            my_tree.delete(item)

        cur = conn.cursor()
        cur.execute("""
            SELECT f.match_id, p.id, p.name, f.catches, f.run_outs, f.stumpings
            FROM fielding_stats f
            JOIN players p ON f.player_id = p.id
            ORDER BY f.match_id DESC
        """)
        rows = cur.fetchall()

        for idx, row in enumerate(rows):
            match_id, player_id, player_name, catches, runouts, stumpings = row

            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            my_tree.insert("", "end", text="",
                        values=(match_id, player_id, player_name, catches, runouts, stumpings),
                        tags=(tag,))

        cur.close()

    #populate_treeview()

    
    
    def clear_entries():
        catches_entry.delete(0,END)
        runouts_entry.delete(0,END)
        stumpings_entry.delete(0,END)


    


    def select_record(e):

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        

        if not values or len(values) < 6:
            return  # Exit early

        clear_entries()

        ##selected = my_tree.focus()
        #values = my_tree.item(selected, 'values')
        
        catches_entry.insert(0, values[3])
        runouts_entry.insert(0, values[4])
        stumpings_entry.insert(0, values[5])
        

    '''def select_record(e):
        clear_entries()

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        balls_entry.insert(0, values[3])
        runs_entry.insert(0, values[4])
        wickets_entry.insert(0, values[5])
        maidens_entry.insert(0, values[6])'''




        
    def remove_many():
        response = messagebox.askyesno(
            "Confirm Delete",
            "This will delete all selected fielding records from the database.\nAre you sure?"
        )

        if response:
            selected = my_tree.selection()
            records_to_delete = []

            # Collect (match_id, player_id) pairs from Treeview
            for record in selected:
                match_id = my_tree.item(record, 'values')[0]
                player_id = my_tree.item(record, 'values')[1]
                records_to_delete.append((match_id, player_id))

            try:
                cur = conn.cursor()

                for match_id, player_id in records_to_delete:
                    cur.execute("""
                        DELETE FROM fielding_stats
                        WHERE match_id = %s AND player_id = %s
                    """, (match_id, player_id))

                conn.commit()
                cur.close()

                # Remove visually from Treeview
                for record in selected:
                    my_tree.delete(record)

                clear_entries()
                messagebox.showinfo("Deleted", "Selected fielding records deleted successfully.")

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to delete records.\n{e}")

    
    def update_record():
        selected = my_tree.focus()
        if not selected:
            messagebox.showerror("Error", "No record selected.")
            return

        # Get selected values from Treeview
        values = my_tree.item(selected, 'values')
        match_id = values[0]
        player_id = values[1]

        


            # Get updated data from entries
        
        catches = catches_entry.get().strip() or 0
        runouts = runouts_entry.get().strip() or 0
        stumpings = stumpings_entry.get().strip() or 0
        

        

        try:
            cur = conn.cursor()   # Update the database
            cur.execute("""
                UPDATE fielding_stats
                SET catches = %s,
                    run_outs = %s,
                    stumpings = %s
                    
                
                WHERE match_id = %s AND player_id = %s
            """, (catches, runouts, stumpings,match_id,player_id))

            conn.commit()
            cur.close()

            populate_treeview()
            clear_entries()
            messagebox.showinfo("Success", "Record updated successfully.")
            
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update record.\n{e}")


     # Bind Treeview
    my_tree.bind("<ButtonRelease-1>", select_record)

    # Buttons
    update_btn = Button(datanbutton_frame, text="Update", width=15, bg="#2F66A1", fg="white", font=('Arial', 10, 'bold'), command=update_record)
    update_btn.grid(row=4, column=0, columnspan=2,padx=15, pady=(30, 10))

    delete_btn = Button(datanbutton_frame, text="Delete", width=15, bg="#823423", fg="white", font=('Arial', 10, 'bold'), command=remove_many)
    delete_btn.grid(row=5, column=0, columnspan=2,padx=15, pady=10)

    clear_btn = Button(datanbutton_frame, text="Clear", width=15, bg="#3E7335", fg="white", font=('Arial', 10, 'bold'), command=clear_entries)
    clear_btn.grid(row=6, column=0, columnspan=2,padx=15, pady=10)

    populate_treeview()

    
    return frame, populate_treeview










































def create_frame4(parent):
    frame = Frame(parent, bg="#404040")
    # Configure Treeview style
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#d3d3d3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview',
              background=[('selected', "#1D1D1D")])
    
    # Create Treeview frame and scrollbar
    tree_frame = Frame(frame)
    tree_frame.place(relx=0.01, rely=0.016, relwidth=0.64, relheight=0.976)
    tree_scroll = ttk.Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
    my_tree.pack(fill=BOTH, expand=True)
    tree_scroll.config(command=my_tree.yview)
    my_tree['columns'] = ("MID","Matchdate", "Opponent", "Location", "Matchtype")
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("MID", anchor=CENTER, width=50)
    my_tree.column("Matchdate", anchor=CENTER, width=100)  
    my_tree.column("Opponent", anchor=CENTER, width=100)
    my_tree.column("Location", anchor=CENTER, width=100)
    my_tree.column("Matchtype", anchor=CENTER, width=100)
    my_tree.heading("#0", text="", anchor=CENTER)
    my_tree.heading("MID", text="MID", anchor=CENTER)
    my_tree.heading("Matchdate", text="Match Date", anchor=CENTER)
    my_tree.heading("Opponent", text="Opponent", anchor=CENTER)
    my_tree.heading("Location", text="Location", anchor=CENTER)
    my_tree.heading("Matchtype", text="Match Type", anchor=CENTER)

    my_tree.tag_configure('oddrow', background="white")
    my_tree.tag_configure('evenrow', background="lightblue")
    
    datanbutton_frame = Frame(frame,bg="#404040")
    datanbutton_frame.place(relx=0.65, rely=00.0, relwidth=0.34, relheight=1)

    match_label = Label(datanbutton_frame,text="MATCH ENTRIES",font=('Arial', 16, 'bold'), fg="#FFFFFF", bg="#404040")
    match_label.place(x=50,y=15)

    matchdate_label = Label(datanbutton_frame, text="Mat_Date",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    matchdate_label.grid(row=0, column=0,padx=20,pady=(70,20))
    matchdate_entry = Entry(datanbutton_frame,width=13,font=('Arial', 12, 'bold'))
    matchdate_entry.grid(row=0, column=1,padx=0,pady=(70,20))
    
    opponent_label = Label(datanbutton_frame, text="Opponent",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    opponent_label.grid(row=1, column=0)
    opponent_entry = Entry(datanbutton_frame,width=13,font=('Arial', 12, 'bold'))
    opponent_entry.grid(row=1, column=1)
    
    
    location_label = Label(datanbutton_frame, text="Location",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    location_label.grid(row=2, column=0,pady=20)
    location_entry = Entry(datanbutton_frame,width=13,font=('Arial', 12, 'bold'))
    location_entry.grid(row=2, column=1,pady=20)

    matchtype_label = Label(datanbutton_frame, text="Mat_Type",font=('Arial', 12, 'bold'), fg="#FFFFFF", bg="#404040")
    matchtype_label.grid(row=3, column=0)
    matchtype_entry = Entry(datanbutton_frame,width=13,font=('Arial', 12, 'bold'))
    matchtype_entry.grid(row=3, column=1)
    
    

    
    
    



    def populate_treeview():
        # Clear Treeview
        for item in my_tree.get_children():
            my_tree.delete(item)

        cur = conn.cursor()
        cur.execute("""
            SELECT id, match_date, opponent, location, match_type
            FROM matches
            ORDER BY id DESC
        """)
        rows = cur.fetchall()

        for idx, row in enumerate(rows):
            id, match_date, opponent, location, match_type = row

            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            my_tree.insert("", "end", text="",
                        values=(id, match_date, opponent, location, match_type),
                        tags=(tag,))

        cur.close()

    #populate_treeview()

    
    
    def clear_entries():
        matchdate_entry.delete(0,END)
        opponent_entry.delete(0,END)
        location_entry.delete(0,END)
        matchtype_entry.delete(0,END)


    


    def select_record(e):

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')
        

        if not values or len(values) < 5:
            return  # Exit early

        clear_entries()

        ##selected = my_tree.focus()
        #values = my_tree.item(selected, 'values')
        
        matchdate_entry.insert(0, values[1])
        opponent_entry.insert(0, values[2])
        location_entry.insert(0, values[3])
        matchtype_entry.insert(0, values[4])
        

    '''def select_record(e):
        clear_entries()

        selected = my_tree.focus()
        values = my_tree.item(selected, 'values')

        balls_entry.insert(0, values[3])
        runs_entry.insert(0, values[4])
        wickets_entry.insert(0, values[5])
        maidens_entry.insert(0, values[6])'''
    



    def remove_many():
        response = messagebox.askyesno(
            "Confirm Delete",
            "This will delete all selected match records from the database.\nAre you sure?"
        )

        if response:
            selected = my_tree.selection()
            ids_to_delete = []

            for record in selected:
                match_id = my_tree.item(record, 'values')[0]
                ids_to_delete.append(match_id)

            try:
                cur = conn.cursor()

                for match_id in ids_to_delete:
                    cur.execute("""
                        DELETE FROM matches
                        WHERE id = %s
                    """, (match_id,))

                conn.commit()
                cur.close()

                # Remove visually from Treeview
                for record in selected:
                    my_tree.delete(record)

                clear_entries()
                messagebox.showinfo("Deleted", "Selected match records deleted successfully.")

            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Failed to delete records.\n{e}")




    def update_record():
        selected = my_tree.focus()
        if not selected:
            messagebox.showerror("Error", "No match selected.")
            return

        # Get selected values from Treeview
        values = my_tree.item(selected, 'values')
        match_id = values[0]  # Assuming match_id is the first column

        # Get updated data from Entry fields
        match_date = matchdate_entry.get().strip()
        opponent = opponent_entry.get().strip()
        location = location_entry.get().strip()
        match_type = matchtype_entry.get().strip()

        # Validate that all fields are filled
        if not all([match_date, opponent, location, match_type]):
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            cur = conn.cursor()
            cur.execute("""
                UPDATE matches
                SET match_date = %s,
                    opponent = %s,
                    location = %s,
                    match_type = %s
                WHERE id = %s
            """, (match_date, opponent, location, match_type, match_id))

            conn.commit()
            cur.close()

            populate_treeview()
            clear_entries()
            messagebox.showinfo("Success", "Match record updated successfully.")

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Failed to update match record.\n{e}")
        

    
    


     # Bind Treeview
    my_tree.bind("<ButtonRelease-1>", select_record)

    # Buttons
    update_btn = Button(datanbutton_frame, text="Update", width=15, bg="#2F66A1", fg="white", font=('Arial', 10, 'bold'), command=update_record)
    update_btn.grid(row=4, column=0, columnspan=2,padx=30, pady=(30, 7))

    delete_btn = Button(datanbutton_frame, text="Delete", width=15, bg="#823423", fg="white", font=('Arial', 10, 'bold'), command=remove_many)
    delete_btn.grid(row=5, column=0, columnspan=2,padx=30, pady=7)

    clear_btn = Button(datanbutton_frame, text="Clear", width=15, bg="#3E7335", fg="white", font=('Arial', 10, 'bold'), command=clear_entries)
    clear_btn.grid(row=6, column=0, columnspan=2,padx=30, pady=7)

    populate_treeview()

    
    return frame, populate_treeview






























def create_update_stats_tab(notebook):
    update_tab = Frame(notebook, bg="#404040")
    notebook.add(update_tab, text="UPDATE STATS")
    
    update_tab.grid_columnconfigure(0, weight=1)
    update_tab.grid_columnconfigure(1, weight=1)
    update_tab.grid_rowconfigure(0, weight=1)
    update_tab.grid_rowconfigure(1, weight=1)
    
    frame1, populate1 = create_frame1(update_tab)
    frame1.grid(row=0, column=0, sticky="nsew")# padx=5, pady=5)
    
    frame2, populate2 = create_frame2(update_tab)
    frame2.grid(row=0, column=1, sticky="nsew")# padx=5, pady=5)
    
    frame3, populate3 = create_frame3(update_tab)
    frame3.grid(row=1, column=0, sticky="nsew")# padx=5, pady=5)
    
    frame4, populate4 = create_frame4(update_tab)
    frame4.grid(row=1, column=1, sticky="nsew")# padx=5, pady=5)
    
    return update_tab, populate1, populate2, populate3, populate4


