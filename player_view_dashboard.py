
import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from db_connection import connect_to_db
conn = connect_to_db()
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg











def create(notebook):


    tab = tk.Frame(notebook, bg="#333333")
    notebook.add(tab, text="PLAYER INTERFACE ||> DASHBOARD")


    zero   = tk.Frame(tab, bg="#333333", bd=1)
    one   = tk.Frame(tab, bg="#333333", bd=1)
    two   = tk.Frame(tab, bg="#333333", bd=1)
    three = tk.Frame(tab, bg="#333333", bd=1)
    four  = tk.Frame(tab, bg="#333333", bd=1)
    five  = tk.Frame(tab, bg="#333333", bd=1)
    six   = tk.Frame(tab, bg="#333333", bd=1)

    # Layout using grid (can switch to pack/place if needed)
    #tab.grid_rowconfigure((0, 1), weight=0)
    #tab.grid_columnconfigure((0, 1, 2), weight=0)
    zero.place(relx=0.0, rely=0.0, relwidth=0.30, relheight=0.15)
    one.place(relx=0.0, rely=0.15, relwidth=0.30, relheight=0.40)
    two.place(relx=0.30, rely=0.0, relwidth=0.35, relheight=0.55)
    three.place(relx=0.65, rely=0.0, relwidth=0.35, relheight=0.55)

    four.place(relx=0.0, rely=0.55, relwidth=0.33, relheight=0.45)
    five.place(relx=0.33, rely=0.55, relwidth=0.33, relheight=0.45)
    six.place(relx=0.66, rely=0.55, relwidth=0.34, relheight=0.45)




    # Title
    title = tk.Label(zero, text="View Dashboard of:",
                     font=("Arial", 16, "bold"), bg="#333333", fg="white")
    title.place(x=25,y=25)

    # Combobox
    combo = ttk.Combobox(zero, font=("Arial", 13,"bold"), width=20, state="readonly")
    combo.place(x=25,y=75)

    cur = conn.cursor()
    cur.execute("SELECT id, name FROM players ORDER BY name")
    players = cur.fetchall()
    cur.close()
    combo['values'] = [f"{name} ({pid})" for pid, name in players]

    # Frame container for stats (initially empty)


    def extract_player_id():
        selected = combo.get()
        if "(" in selected and ")" in selected:
            try:
                return int(selected.split("(")[-1].split(")")[0])
            except:
                return None
        return None

    def on_submit():
        player_id = extract_player_id()
        if player_id:
            create_player_main_tab(tab, player_id, one, two, three, four, five, six)
        else:
            messagebox.showerror("Error", "Please select a valid player.")

    submit_btn = tk.Button(zero, text="Submit", command=on_submit,
                           bg="green", fg="white", font=("Arial", 12, "bold"))
    submit_btn.place(x=250,y=71)

    





def create_player_main_tab(tab, player_id, one, two, three, four, five, six):

    for widget in one.winfo_children():
        widget.destroy()
    
    # Create the main tab
   

    # Define 6 internal frames
    
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







    # Player Details
    info_text = (
        f"Player ID  :    {player_info['id']}\n\n"
        f"Name        :    {player_info['name']}\n\n"
        f"Age           :    {player_info['age']}\n\n"
        f"Role          :    {player_info['type']}"
    )

    info_label = tk.Label(one, text=info_text, font=("Arial", 15,"bold"), bg="#333333", fg="white", justify="left", anchor="w")
    info_label.pack(padx=37,pady=40, fill="x")

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





    


