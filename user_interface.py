
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from db_connection import connect_to_db
conn = connect_to_db()
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def create_player_dashboard_tab(notebook, player_id):

    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview',
              background=[('selected', "#1d1d1d")])


    tab = tk.Frame(notebook, bg="#333333")
    notebook.add(tab, text="MATCH BY MATCH STATS")



    cur = conn.cursor()
    try:
        cur.execute("SELECT name FROM players WHERE id = %s", (player_id,))
        result = cur.fetchone()
        player_name = result[0] if result else "Player"
    except Exception as e:
        print("Error fetching player name:", e)
        player_name = "Player"
    finally:
        cur.close()

    ######################  Title Row  ########################
    title = tk.Label(tab, text=f"Hello, {player_name}, here are your match-by-match stats!", 
                 font=("Arial", 16, "bold"), bg="#333333", fg="white")
    #title = tk.Label(tab, text="PLAYER MATCH-BY-MATCH STATS", 
                     #font=("Arial", 16, "bold"), bg="#333333", fg="white")
    title.pack(pady=10)

    ######################  Table Frame  ######################
    table_frame = tk.Frame(tab, bg="#333333")
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = (
        "Date", "Opponent", "Location", "Matchtype",
        "R_scored","Dismissal", "B_Faced", "4s", "6s",
        "B_bowled", "R_conceded", "Wickets", "Maidens",
        "Catches", "Stumpings", "RunOuts"
    )

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16, selectmode="extended")

    # Set each heading and width manually
    tree.heading("Date", text="Date")
    tree.column("Date", width=100, anchor="center")

    tree.heading("Opponent", text="Opponent")
    tree.column("Opponent", width=100, anchor="center")

    tree.heading("Location", text="Location")
    tree.column("Location", width=100, anchor="center")

    tree.heading("Matchtype", text="Matchtype")
    tree.column("Matchtype",width=100, anchor="center")

    for col in columns[4:]:
        tree.heading(col, text=col)
        tree.column(col, width=80, anchor="center")

    tree.tag_configure('evenrow', background="lightblue")
    tree.tag_configure('oddrow', background="white")
    tree.pack(side="left", fill="both", expand=True)

#--------------------------------------------------------------------------------------------------------
    # Scrollbars
    yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side="right", fill="y")

    ######################  Fetch & Populate  ######################
    cur = conn.cursor()

    query = '''
        SELECT m.match_date, m.opponent, m.location, m.match_type,
        COALESCE(bs.runs_scored,0),
        COALESCE(bs.dismissal,TRUE) AS dismissal_info,
        COALESCE(bs.balls_faced,0), COALESCE(bs.fours,0), COALESCE(bs.sixes,0),
        COALESCE(bos.balls_bowled,0), COALESCE(bos.runs_conceded,0),
        COALESCE(bos.wickets,0), COALESCE(bos.maidens,0),
        COALESCE(fs.catches,0), COALESCE(fs.stumpings,0), COALESCE(fs.run_outs,0)
        FROM matches m
        JOIN (
            SELECT DISTINCT match_id FROM batting_stats WHERE player_id = %s
            UNION
            SELECT DISTINCT match_id FROM bowling_stats WHERE player_id = %s
            UNION
            SELECT DISTINCT match_id FROM fielding_stats WHERE player_id = %s
        ) played_matches ON m.id = played_matches.match_id
        LEFT JOIN batting_stats bs ON m.id = bs.match_id AND bs.player_id = %s
        LEFT JOIN bowling_stats bos ON m.id = bos.match_id AND bos.player_id = %s
        LEFT JOIN fielding_stats fs ON m.id = fs.match_id AND fs.player_id = %s
        ORDER BY m.match_date DESC
    '''
    cur.execute(query, (player_id, player_id, player_id, player_id, player_id, player_id))
    rows = cur.fetchall()

    total = [0] * 11  # We have 11 numeric fields to sum

# Mapping: [R_scored, B_Faced, 4s, 6s, B_bowled, R_conceded, Wickets, Maidens, Catches, Stumpings, RunOuts]
    for row in rows:
        tag = 'evenrow' if rows.index(row) % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=row, tags=(tag,))
        
        total[0] += row[4]   # R_scored
        total[1] += row[6]   # B_Faced
        total[2] += row[7]   # 4s
        total[3] += row[8]   # 6s
        total[4] += row[9]   # B_bowled
        total[5] += row[10]  # R_conceded
        total[6] += row[11]  # Wickets
        total[7] += row[12]  # Maidens
        total[8] += row[13]  # Catches
        total[9] += row[14]  # Stumpings
        total[10] += row[15] # RunOuts
    total_matches = len(rows)

    def safe_div(n, d): return round(n / d, 2) if d else 0

    dismissals = 0

    for row in rows:
        if bool(row[5]):
            dismissals += 1

    total_wickets = total[6]


    bat_avg = "∞" if dismissals == 0 else round(total[0] / dismissals, 2)
    bat_sr  = safe_div(total[0] * 100, total[1])
    bowl_avg = "∞" if total_wickets == 0 else round(total[5] / total_wickets, 2)
    bowl_sr  = safe_div(total[4], total[6])
    economy  = safe_div(total[5] * 6, total[4])

    ######################  Bottom Frame Split ######################
    bottom_frame = tk.Frame(tab, bg="#333333")
    bottom_frame.pack(fill="x", padx=10, pady=10)

    left_frame = tk.Frame(bottom_frame, bg="#333333")
    left_frame.pack(side="left", fill="both", expand=True,padx=(0,5))

    right_frame = tk.Frame(bottom_frame, bg="#333333")
    right_frame.pack(side="right", fill="both", expand=True,padx=(5,0))

    ######################  Averages Section (Left) ######################
    tk.Label(left_frame, text="Averages", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(0, 5))

    avg_columns = ("Bat Avg", "Bat SR", "Bowl Avg", "Bowl SR", "Economy")
    avg_tree = ttk.Treeview(left_frame, columns=avg_columns, show="headings", height=1)
    avg_tree.tag_configure("highlight", background="#2C3157",foreground="white")

    for col in avg_columns:
        avg_tree.heading(col, text=col)
        avg_tree.column(col, width=100, anchor="center")

    avg_tree.insert("", "end", values=(bat_avg, bat_sr, bowl_avg, bowl_sr, economy), tags=("highlight",))
    avg_tree.pack(fill="x")

    ######################  Totals Section (Right) ######################
    tk.Label(right_frame, text="Totals", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(0, 5))

    total_columns = (
        "R_scored", "B_Faced", "4s", "6s",
        "B_bowled", "R_conceded", "Wickets", "Maidens",
        "Catches", "Stumpings", "RunOuts"
    )
    total_tree = ttk.Treeview(right_frame, columns=total_columns, show="headings", height=1)
    total_tree.tag_configure( "highlight",background="#2C3157",foreground="white")

    for col in total_columns:
        total_tree.heading(col, text=col)
        total_tree.column(col, width=80, anchor="center")

    # Populate total row
    total_row = [total[0], total[1], total[2], total[3],
                 total[4], total[5], total[6], total[7],
                 total[8], total[9], total[10]]
    total_tree.insert("", "end", values=total_row, tags=("highlight",))
    total_tree.pack(fill="x")

    cur.close()






def show_player_gui(player_id):
    root = tk.Tk()
    root.state('zoomed')
    root.title("Player Dashboard")
    root.configure(bg="#333333")

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)
    create_player_main_tab(notebook,player_id)
    create_player_dashboard_tab(notebook, player_id)
    

    root.mainloop()




def create_player_main_tab(notebook,player_id):
    
    # Create the main tab
    tab = tk.Frame(notebook, bg="#333333")
    notebook.add(tab, text="PLAYER DASHBOARD")

    # Define 6 internal frames
    one   = tk.Frame(tab, bg="#333333", bd=1)
    two   = tk.Frame(tab, bg="#333333", bd=1)
    three = tk.Frame(tab, bg="#333333", bd=1)
    four  = tk.Frame(tab, bg="#333333", bd=1)
    five  = tk.Frame(tab, bg="#333333", bd=1)
    six   = tk.Frame(tab, bg="#333333", bd=1)

    # Layout using grid (can switch to pack/place if needed)
    tab.grid_rowconfigure((0, 1), weight=0)
    tab.grid_columnconfigure((0, 1, 2), weight=0)

    one.place(relx=0.0, rely=0.0, relwidth=0.30, relheight=0.55)
    two.place(relx=0.30, rely=0.0, relwidth=0.35, relheight=0.55)
    three.place(relx=0.65, rely=0.0, relwidth=0.35, relheight=0.55)

    four.place(relx=0.0, rely=0.55, relwidth=0.33, relheight=0.45)
    five.place(relx=0.33, rely=0.55, relwidth=0.33, relheight=0.45)
    six.place(relx=0.66, rely=0.55, relwidth=0.34, relheight=0.45)
    # You can use these frames now to insert charts, info, and tables
    # Example:
    # plot_batting_progression(player_id, one)
    # plot_bowling_progression(player_id, two)
    # add_summary_labels(player_id, three) etc.

    

################################################################           FIRST            ##############################################



    cur = conn.cursor()
    try:
        cur.execute("SELECT id, name, age, type FROM players WHERE id = %s", (player_id,))
        result = cur.fetchone()
        if result:
            player_id_db, player_name, player_age, player_type = result
        else:
            player_id_db, player_name, player_age, player_type = player_id, "Unknown", 0, "Unknown"
    except Exception as e:
        print("Error fetching player info:", e)
        player_id_db, player_name, player_age, player_type = player_id, "Unknown", 0, "Unknown"
    finally:
        cur.close()



    player_info = {
        "id": player_id_db,
        "name": player_name,
        "age": player_age,
        "type": player_type
    }

        # --- Get user credentials ---
    cur = conn.cursor()
    try:
        cur.execute("SELECT username, password FROM users WHERE player_id = %s", (player_id,))
        user_data = cur.fetchone()
        if user_data:
            current_username, current_password = user_data
        else:
            current_username, current_password = "N/A", "N/A"
    except Exception as e:
        print("Error fetching credentials:", e)
        current_username, current_password = "N/A", "N/A"
    finally:
        cur.close()

    # --- Credential Frame ---
    credential_frame = tk.Frame(one, bg="#333333")
    credential_frame.pack(pady=(10, 5))

    # Username Row
    tk.Label(credential_frame, text="Username:", font=("Arial", 12,'bold'), bg="#333333", fg="white").grid(row=0, column=0, sticky="e", padx=5, pady=5)

    username_var = tk.StringVar(value=current_username)
    username_entry = tk.Entry(credential_frame, textvariable=username_var, font=("Arial", 12), width=14)
    username_entry.grid(row=0, column=1, padx=5, pady=15)

    def update_username():
        new_username = username_var.get().strip()
        if new_username and new_username != current_username:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to update username to '{new_username}'?")
            if confirm:
                try:
                    cur = conn.cursor()
                    cur.execute("UPDATE users SET username = %s WHERE player_id = %s", (new_username, player_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Username updated successfully.")
                except Exception as e:
                    print("Username update error:", e)
                    messagebox.showerror("Error", "Could not update username.")
                finally:
                    cur.close()













    def show_password_popup():
        try:
            cur = conn.cursor()
            cur.execute("SELECT password FROM users WHERE player_id = %s", (player_id,))
            result = cur.fetchone()
            if result:                    
                password = result[0]
            else:
                password = "Not found"
        except Exception as e:
            print("Password fetch error:", e)
            password = "Error fetching password"
        finally:
            cur.close()

        popup = tk.Toplevel()
        popup.title("Your Password")
        popup.configure(bg="#333333")
        popup.geometry("300x150")

        label = tk.Label(popup, text=password, font=("Arial", 18, "bold"), fg="white", bg="#333333")
        label.pack(expand=True, pady=40)








    def update_password_popup():
        def submit_password_update():
            old_pwd = current_pwd_entry.get().strip()
            new_pwd = new_pwd_entry.get().strip()

            if not old_pwd or not new_pwd:
                messagebox.showwarning("Missing", "Please fill in both fields.")
                return

            try:
                cur = conn.cursor()
                cur.execute("SELECT password FROM users WHERE player_id = %s", (player_id,))
                result = cur.fetchone()
                if not result:
                    messagebox.showerror("Error", "User not found.")
                    return

                db_password = result[0]
                if old_pwd != db_password:
                    messagebox.showerror("Error", "Current password is incorrect.")
                    return

                confirm = messagebox.askyesno("Confirm", "Are you sure you want to update your password?")
                if confirm:
                    cur.execute("UPDATE users SET password = %s WHERE player_id = %s", (new_pwd, player_id))
                    conn.commit()
                    messagebox.showinfo("Success", "Password updated successfully.")
                    win.destroy()
            except Exception as e:
                print("Password update error:", e)
                messagebox.showerror("Error", "Could not update password.")
            finally:
                cur.close()

        # --- Create Styled Update Window ---
        win = tk.Toplevel()
        win.title("Change Password")
        win.configure(bg="#333333")
        win.geometry("450x350")

        frame = tk.Frame(win, bg="#333333")
        frame.pack(pady=20)

        login_label = tk.Label(frame, text="Change Password", bg="#333333", fg="#FF3399", font=("Arial", 30))
        login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=30)

        current_label = tk.Label(frame, text="Current Password", bg="#333333", fg="white", font=("Arial", 16))
        current_label.grid(row=1, column=0)
        current_pwd_entry = tk.Entry(frame, show="*", font=("Arial", 16))
        current_pwd_entry.grid(row=1, column=1, pady=20)

        new_label = tk.Label(frame, text="New Password", bg="#333333", fg="white", font=("Arial", 16))
        new_label.grid(row=2, column=0)
        new_pwd_entry = tk.Entry(frame, show="*", font=("Arial", 16))
        new_pwd_entry.grid(row=2, column=1, pady=20)

        submit_button = tk.Button(
            frame, text="Submit", bg="#FF3399", fg="white", font=("Arial", 16),
            command=submit_password_update
        )
        submit_button.grid(row=3, column=1, pady=20, sticky="e")

        win.bind('<Return>', lambda event: submit_button.invoke())












    




    tk.Button(credential_frame, text="Update", width=15, bg="#2F66A1", fg="white", font=('Arial', 10, 'bold'), command=update_username).grid(row=0, column=2, padx=5)

    # Password Row
    tk.Label(credential_frame, text="Password:", font=("Arial", 12,'bold'), bg="#333333", fg="white").grid(row=1, column=0, sticky="e", padx=5, pady=5)

    tk.Button(credential_frame, text="Show",  width=15, bg="#2FA16A", fg="white", font=('Arial', 10, 'bold'),command=show_password_popup).grid(row=1, column=1, padx=5)
    tk.Button(credential_frame, text="Update",  width=15, bg="#2F66A1", fg="white", font=('Arial', 10, 'bold'),command=update_password_popup).grid(row=1, column=2, padx=5)


























        # Player Information Title
    title_label = tk.Label(one, text="PLAYER INFORMATION", font=("Arial", 16, "bold"), bg="#333333", fg="white",justify="left",anchor="w")
    title_label.pack(padx=40,pady=(60, 40),fill="x")

    # Player Details
    info_text = (
        f"Player ID  :    {player_info['id']}\n\n"
        f"Name        :    {player_info['name']}\n\n"
        f"Age           :    {player_info['age']}\n\n"
        f"Role          :    {player_info['type']}"
    )

    info_label = tk.Label(one, text=info_text, font=("Arial", 15,"bold"), bg="#333333", fg="white", justify="left", anchor="w")
    info_label.pack(padx=40, fill="x")

########################################################################################################################################


    def plot_batting_progression(player_id, frame):
      
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT runs_scored FROM batting_stats
                WHERE player_id = %s
                ORDER BY match_id
            """, (player_id,))
            scores = [row[0] for row in cur.fetchall()]
        except Exception as e:
            print("Error fetching batting progression:", e)
            scores = []
        finally:
            cur.close()

        # Create figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color("#D1D1D1")
        
        if scores:
            ax.bar(range(1, len(scores)+1), scores, width=0.95, color='#00c853')  # Green bars
            ax.set_xticks(range(1, len(scores)+1)) 
            ax.set_title("Batting Progression", fontsize=14, weight='bold',color = 'white')
            ax.set_xlabel("Innings",color = 'white')
            ax.set_ylabel("Runs Scored",color = 'white')
            ax.grid(True, linestyle="--", alpha=0.4)
        else:
            ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)

        # Embed plot in tkinter frame
        for widget in frame.winfo_children():
            widget.destroy()  # Clear old plot if any

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#######################################################################################################################################

    def plot_boundaries_pie(player_id, frame):
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT COALESCE(SUM(fours), 0), COALESCE(SUM(sixes), 0)
                FROM batting_stats
                WHERE player_id = %s
            """, (player_id,))
            fours, sixes = cur.fetchone()
        except Exception as e:
            print("Error fetching boundaries data:", e)
            fours, sixes = 0, 0
        finally:
            cur.close()

        # Edge case: if both are 0, fake 50-50
        if fours == 0 and sixes == 0:
            data = [1, 1]
            labels = ['Fours (0)', 'Sixes (0)']
        else:
            data = [fours, sixes]
            labels = [f'Fours ({fours})', f'Sixes ({sixes})']

        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Create the pie chart
        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        colors = ['#fdd835', '#ff1744']  # Yellow for 4s, Red for 6s
        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')

        _, texts, _ = ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        for text in texts:
            text.set_color("white")
            text.set_fontsize(10)

        ax.set_title("Boundary Breakdown", fontsize=14, weight='bold',color = 'white')

        # Embed it in the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)




#######################################################################################################################################

    def plot_bowling_progression(player_id, frame):
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT wickets FROM bowling_stats
                WHERE player_id = %s
                ORDER BY match_id
            """, (player_id,))
            wickets = [row[0] for row in cur.fetchall()]
        except Exception as e:
            print("Error fetching bowling progression:", e)
            wickets = []
        finally:
            cur.close()

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color("#D1D1D1")

        if wickets:
            innings = list(range(1, len(wickets)+1))
            ax.bar(innings, wickets, width=0.95, color='#2962ff', align='center')  # Blue bars
            ax.set_title("Bowling Progression", fontsize=14, weight='bold',color = 'white')
            ax.set_xlabel("Innings",color = 'white')
            ax.set_ylabel("Wickets Taken",color = 'white')
            ax.set_xticks(innings)
            ax.set_xticks(range(1, len(wickets)+1))
            ax.set_xlim(0.5, len(wickets) + 0.5)
            ax.grid(True, linestyle="--", alpha=0.4)
        else:
            ax.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=14)

        # Embed plot in tkinter frame
        for widget in frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


###############################################################################################################################################################

    def plot_fielding_pie(player_id, frame):
        cur = conn.cursor()
        try:
            cur.execute("""
                SELECT COALESCE(SUM(catches), 0), COALESCE(SUM(run_outs), 0)
                FROM fielding_stats
                WHERE player_id = %s
            """, (player_id,))
            catches, run_outs = cur.fetchone()
        except Exception as e:
            print("Error fetching fielding data:", e)
            catches, run_outs = 0, 0
        finally:
            cur.close()

        # Handle case where both are 0
        if catches == 0 and run_outs == 0:
            data = [1, 1]
            labels = ['Catches (0)', 'Run Outs (0)']
        else:
            data = [catches, run_outs]
            labels = [f'Catches ({catches})', f'Run Outs ({run_outs})']

        # Clear the frame before plotting
        for widget in frame.winfo_children():
            widget.destroy()

        # Create the pie chart
        fig = Figure(figsize=(4, 4), dpi=100)
        ax = fig.add_subplot(111)
        colors = ['#00e676', '#2979ff']  # Green for catches, Blue for run outs

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')


        _, texts, _ =ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)

        
        for text in texts:
            text.set_color("white")
            text.set_fontsize(10)

        ax.set_title("Fielding Breakdown", fontsize=14, weight='bold',color = 'white')

        # Embed in Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



#########################################################################################################################################################





    def create_radar_chart(player_id,frame):
        cur= conn.cursor()


        # --- Get Team Totals ---
        cur.execute("SELECT SUM(runs_scored) FROM batting_stats")
        total_runs = cur.fetchone()[0] or 1

        cur.execute("SELECT SUM(wickets) FROM bowling_stats")
        total_wickets = cur.fetchone()[0] or 1

        cur.execute("SELECT SUM(catches + run_outs + stumpings) FROM fielding_stats")
        total_fielding = cur.fetchone()[0] or 1

        # --- Get Player Totals ---
        cur.execute("SELECT SUM(runs_scored) FROM batting_stats WHERE player_id = %s", (player_id,))
        player_runs = cur.fetchone()[0] or 0

        cur.execute("SELECT SUM(wickets) FROM bowling_stats WHERE player_id = %s", (player_id,))
        player_wickets = cur.fetchone()[0] or 0

        cur.execute("SELECT SUM(catches + run_outs + stumpings) FROM fielding_stats WHERE player_id = %s", (player_id,))
        player_fielding = cur.fetchone()[0] or 0

        # --- Calculate % Contributions ---
        batting_percent = (player_runs / total_runs) * 100
        bowling_percent = (player_wickets / total_wickets) * 100
        fielding_percent = (player_fielding / total_fielding) * 100

        # --- Radar Data ---
        labels = ['Batting', 'Bowling', 'Fielding']
        values = [batting_percent, bowling_percent, fielding_percent]

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]

        # --- Plotting ---
        
        fig, ax = plt.subplots(figsize=(3.25, 3.25), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='deepskyblue', linewidth=2)
        ax.fill(angles, values, color='deepskyblue', alpha=0.4)
        ax.set_title("Contribution", fontsize=14, weight='bold', color = 'white',y=1.08)
        fig.tight_layout(pad=1.1)
        

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, color='white', fontsize=10)

        # Hide radial ticks
        ax.set_yticklabels([])
        ax.set_yticks([])
        ax.spines['polar'].set_color('white')
        ax.grid(color='gray', linestyle='dotted', linewidth=0.7)

        fig.patch.set_facecolor('#333333')
        ax.set_facecolor('#333333')

        # Embed in Tkinter frame
        for widget in frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.1, anchor='n')









    plot_batting_progression(player_id, two)

    plot_boundaries_pie(player_id,four)

    plot_bowling_progression(player_id, three)

    plot_fielding_pie(player_id, six)

    create_radar_chart(player_id,five)

    # You can return them if needed for reference
    return one, two, three, four, five, six





    


