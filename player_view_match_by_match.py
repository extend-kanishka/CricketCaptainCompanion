import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from psycopg2 import sql
from db_connection import connect_to_db

conn = connect_to_db()

def create_stats_frame(container , player_id):
    # Delete old stats frame contents
    for widget in container.winfo_children():
        widget.destroy()

    ######################  Table Frame  ######################
    table_frame = tk.Frame(container, bg="#333333")
    table_frame.pack(fill="both", expand=True, padx=0, pady=0)

    columns = (
        "Date", "Opponent", "Location", "Matchtype",
        "R_scored", "Dismissal", "B_Faced", "4s", "6s",
        "B_bowled", "R_conceded", "Wickets", "Maidens",
        "Catches", "Stumpings", "RunOuts"
    )

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=16, selectmode="extended")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col in columns[:4] else 80, anchor="center")

    tree.tag_configure('evenrow', background="lightblue")
    tree.tag_configure('oddrow', background="white")
    tree.pack(side="left", fill="both", expand=True)

    yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side="right", fill="y")

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
    cur.execute(query, (player_id,) * 6)
    rows = cur.fetchall()
    cur.close()

    total = [0] * 11
    for i, row in enumerate(rows):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
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

    def safe_div(n, d): return round(n / d, 2) if d else 0

    total_wickets = total[6]
    dismissals = sum(bool(row[5]) for row in rows)
    bat_avg = "∞" if dismissals == 0 else round(total[0] / dismissals, 2)
    bat_sr  = safe_div(total[0] * 100, total[1])
    bowl_avg = "∞" if total_wickets == 0 else round(total[5] / total_wickets, 2)
    bowl_sr  = safe_div(total[4], total[6])
    economy  = safe_div(total[5] * 6, total[4])

    ######################  Bottom Frame ######################
    bottom_frame = tk.Frame(container, bg="#333333")
    bottom_frame.pack(fill="x", pady=10)

    left_frame = tk.Frame(bottom_frame, bg="#333333")
    left_frame.pack(side="left", fill="both", expand=True,padx=(0,5))

    right_frame = tk.Frame(bottom_frame, bg="#333333")
    right_frame.pack(side="right", fill="both", expand=True,padx=(5,0))

    # Averages
    tk.Label(left_frame, text="Averages", font=("Arial", 12, "bold"), bg="#333333", fg="white").pack(pady=(0, 5))
    avg_columns = ("Bat Avg", "Bat SR", "Bowl Avg", "Bowl SR", "Economy")
    avg_tree = ttk.Treeview(left_frame, columns=avg_columns, show="headings", height=1)
    avg_tree.tag_configure("highlight", background="#2C3157",foreground="white")
    for col in avg_columns:
        avg_tree.heading(col, text=col)
        avg_tree.column(col, width=100, anchor="center")
    avg_tree.insert("", "end", values=(bat_avg, bat_sr, bowl_avg, bowl_sr, economy), tags=("highlight",))
    avg_tree.pack(fill="x")

    # Totals
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
    total_tree.insert("", "end", values=total, tags=("highlight",))
    total_tree.pack(fill="x")


def create(notebook):

    frame = tk.Frame(notebook, bg="#333333")
    notebook.add(frame, text="MATCH BY MATCH STATS")


    # Title
    title = tk.Label(frame, text="Choose the player to see their interface:",
                     font=("Arial", 16, "bold"), bg="#333333", fg="white")
    title.grid(row=0,column=0,padx=(300,10),pady=10)

    # Combobox
    combo = ttk.Combobox(frame, font=("Arial", 13,"bold"), width=20, state="readonly")
    combo.grid(row=0,column=1,padx=(10,100),pady=10)

    cur = conn.cursor()
    cur.execute("SELECT id, name FROM players ORDER BY name")
    players = cur.fetchall()
    cur.close()
    combo['values'] = [f"{name} ({pid})" for pid, name in players]

    # Frame container for stats (initially empty)
    stats_container = tk.Frame(frame, bg="#333333")
    stats_container.grid(row=1,columnspan=3,sticky="nsew",padx=10,pady=0)

    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)

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
            create_stats_frame(stats_container, player_id)
        else:
            messagebox.showerror("Error", "Please select a valid player.")

    submit_btn = tk.Button(frame, text="Submit", command=on_submit,
                           bg="green", fg="white", font=("Arial", 12, "bold"))
    submit_btn.grid(row=0,column=2,padx=(150,270),pady=20)

    


