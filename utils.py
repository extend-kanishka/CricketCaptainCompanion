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


#It grabs all the stuff from Tkinter so we can make a cool GUI with windows, buttons, and all that jazz.
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
    notebook.add(frame, text="VIEW STATS")

    # Treeview styling
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview', background=[('selected', "#337488")])

    # ------------ UPPER TABLE: MOST CATCHES ------------
    upper_frame = Frame(frame, bg="#404040", padx=10, pady=10)
    upper_frame.place(relx=0.7, rely=0, relwidth=0.3, relheight=0.75)

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






    view_frame = Frame(frame, bg="#404040")
    view_frame.place(
        relx=0, rely=0,
        relwidth=0.7,
        relheight=1,
        x=10, y=10,  # left and top padding
        height=-20,  # top + bottom
        width=-11    # left + right
    )


    main_scroll = Scrollbar(view_frame, orient="vertical")
    main_scroll.grid(row=7, column=3, sticky="ns")


    stat_type = StringVar(value="batsman")
    rb1 = Radiobutton(view_frame, text="Batsman", variable=stat_type, value="batsman", bg="#404040", fg="white",
                      command=lambda: update_main_view(stat_type.get(), widgets=view_frame_widgets))
    rb2 = Radiobutton(view_frame, text="Bowler", variable=stat_type, value="bowler", bg="#404040", fg="white",
                      command=lambda: update_main_view(stat_type.get(), widgets=view_frame_widgets))
    rb1.grid(row=0, column=0, sticky="w")
    rb2.grid(row=0, column=1, sticky="w")



    Label(view_frame, text="Sort By:", bg="#404040", fg="white").grid(row=0, column=2, sticky="w")
    sort_by_cb = ttk.Combobox(view_frame, values=[
        "Name", "Runs", "Average", "Strike Rate", "100s", "Best",  # For batsmen
        "Wickets", "Economy", "Maidens", "Best", "Bowling Average"  # For bowlers
    ])
    sort_by_cb.set("Name")  # default
    sort_by_cb.grid(row=0, column=3, sticky="w")




    # Date Range
    Label(view_frame, text="From (YYYY-MM-DD):", bg="#404040", fg="white").grid(row=1, column=0, sticky="w")
    from_date_entry = Entry(view_frame)
    from_date_entry.grid(row=1, column=1)

    Label(view_frame, text="To (YYYY-MM-DD):", bg="#404040", fg="white").grid(row=2, column=0, sticky="w")
    to_date_entry = Entry(view_frame)
    to_date_entry.insert(0, datetime.now().date().isoformat())
    to_date_entry.grid(row=2, column=1)

    # Recent Matches
    Label(view_frame, text="Recent Matches (N):", bg="#404040", fg="white").grid(row=3, column=0, sticky="w")
    recent_entry = Entry(view_frame)
    recent_entry.grid(row=3, column=1)

    # Match Filters (Comboboxes)
    Label(view_frame, text="Opponent:", bg="#404040", fg="white").grid(row=4, column=0, sticky="w")
    opponent_cb = ttk.Combobox(view_frame, state="readonly")
    opponent_cb.grid(row=4, column=1)

    Label(view_frame, text="Location:", bg="#404040", fg="white").grid(row=5, column=0, sticky="w")
    location_cb = ttk.Combobox(view_frame, state="readonly")
    location_cb.grid(row=5, column=1)

    Label(view_frame, text="Match Type:", bg="#404040", fg="white").grid(row=6, column=0, sticky="w")
    type_cb = ttk.Combobox(view_frame, state="readonly")
    type_cb.grid(row=6, column=1)

    # Stats Treeview
    stats_tree = ttk.Treeview(view_frame, selectmode="extended", yscrollcommand=main_scroll.set)
    stats_tree.grid(row=7, column=0, columnspan=3, sticky="nsew")
    main_scroll.config(command=stats_tree.yview)
    view_frame.grid_rowconfigure(7, weight=1)
    view_frame.grid_columnconfigure(2, weight=1)

    # Refresh Button
    refresh_btn = Button(view_frame, text="Refresh",
                     command=lambda: on_refresh(stat_type.get(), view_frame_widgets),
                     bg="#228B22", fg="white", padx=10)
    refresh_btn.grid(row=0, column=2)

    # Save widget references for use in update_main_view
    view_frame_widgets = {
        'from_date': from_date_entry,
        'to_date': to_date_entry,
        'recent_n': recent_entry,
        'opponent': opponent_cb,
        'location': location_cb,
        'match_type': type_cb,
        'tree': stats_tree,
        'sort_by': sort_by_cb 
    }
    def on_refresh(stat_type, widgets):
        refresh_view_stats()
        populate_comboboxes(widgets)
        update_main_view(stat_type, widgets)

    populate_comboboxes(view_frame_widgets)
    update_main_view(stat_type.get(), widgets=view_frame_widgets)

    # Initialize Comboboxes and Trees
    refresh_view_stats()  # Updates best fielders/wicketkeepers
    populate_comboboxes(view_frame_widgets)  # Fills opponent/location/type filters
    update_main_view(stat_type.get(), widgets=view_frame_widgets) 







    
    return frame





def on_refresh(stat_type, widgets):
    refresh_view_stats()
    
    update_main_view(stat_type, widgets)








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















def populate_comboboxes(widgets):
    try:
        cur.execute("SELECT DISTINCT opponent FROM matches ORDER BY opponent")
        opponents = [row[0] for row in cur.fetchall()]
        widgets['opponent']['values'] = ["All"] + opponents
        widgets['opponent'].set("All")

        cur.execute("SELECT DISTINCT location FROM matches ORDER BY location")
        locations = [row[0] for row in cur.fetchall()]
        widgets['location']['values'] = ["All"] + locations
        widgets['location'].set("All")

        cur.execute("SELECT DISTINCT match_type FROM matches ORDER BY match_type")
        match_types = [row[0] for row in cur.fetchall()]
        widgets['match_type']['values'] = ["All"] + match_types
        widgets['match_type'].set("All")
    except psycopg2.Error as e:
        conn.rollback()
        print("Combo fetch error:", e)




def update_main_view(stat_type, widgets):
    from tkinter import NO, CENTER
    import psycopg2

    cur = conn.cursor()

    tree = widgets['tree']
    tree.delete(*tree.get_children())

    # Set up Treeview columns
    if stat_type == "batsman":
        columns = ("PlayerID", "Name", "Innings", "Runs", "Balls", "Average", "StrikeRate", "Fours", "Sixes", "100s", "Best")
    else:
        columns = ("PlayerID", "Name", "Innings", "Balls", "Wickets", "Runs", "Average", "StrikeRate", "Economy", "Maidens", "Best")

    tree['columns'] = columns
    tree.column("#0", width=0, stretch=NO)
    for col in columns:
        tree.column(col, anchor=CENTER, width=90)
        tree.heading(col, text=col, anchor=CENTER)

    # --- Filters ---
    filters = []
    params = []

    from_date = widgets['from_date'].get().strip()
    to_date = widgets['to_date'].get().strip()

    if from_date:
        filters.append("m.match_date >= %s")
        params.append(from_date)
    if to_date:
        filters.append("m.match_date <= %s")
        params.append(to_date)

    opponent = widgets['opponent'].get().strip()
    location = widgets['location'].get().strip()
    match_type = widgets['match_type'].get().strip()

    if opponent != "All":
        filters.append("LOWER(m.opponent) = LOWER(%s)")
        params.append(opponent)

    if location != "All":
        filters.append("LOWER(m.location) = LOWER(%s)")
        params.append(location)

    if match_type != "All":
        filters.append("LOWER(m.match_type) = LOWER(%s)")
        params.append(match_type)

    where_clause = "WHERE " + " AND ".join(filters) if filters else ""

    # Sorting and Recent Filters
    selected_sort = widgets['sort_by'].get().strip()
    recent_n = widgets['recent_n'].get().strip()

    valid_sort_columns = {
        'Name': 'name',
        'Runs': 'runs',
        'Average': 'average',
        'Strike Rate': 'strike_rate',
        'Innings': 'innings',
        'Wickets': 'wickets',
        'Economy': 'economy'
    }

    sort_column = valid_sort_columns.get(selected_sort, None)
    sort_clause = f"ORDER BY {sort_column} DESC" if sort_column else ""
    recent_clause = f"ORDER BY latest_match DESC LIMIT {recent_n}" if recent_n.isdigit() else ""

    try:
        if stat_type == "batsman":
            query = f'''
                SELECT *
                FROM (
                    SELECT 
                        p.id,
                        p.name,
                        COUNT(CASE WHEN bs.balls_faced > 0 THEN 1 END) AS innings,
                        SUM(bs.runs_scored) AS runs,
                        SUM(bs.balls_faced) AS balls,
                        ROUND(NULLIF(SUM(bs.runs_scored)::decimal / NULLIF(COUNT(*) FILTER (WHERE bs.dismissal = TRUE), 0), 0), 2) AS average,
                        ROUND(NULLIF(SUM(bs.runs_scored)::decimal * 100 / NULLIF(SUM(bs.balls_faced), 0), 0), 2) AS strike_rate,
                        SUM(bs.fours) AS fours,
                        SUM(bs.sixes) AS sixes,
                        SUM(CASE WHEN bs.runs_scored >= 100 THEN 1 ELSE 0 END) AS hundreds,
                        (
                            SELECT 
                                bs2.runs_scored || CASE WHEN bs2.dismissal = FALSE THEN '*' ELSE '' END
                            FROM batting_stats bs2
                            JOIN matches m2 ON bs2.match_id = m2.id
                            WHERE bs2.player_id = p.id
                            ORDER BY bs2.runs_scored DESC
                            LIMIT 1
                        ) AS best,
                        MAX(m.match_date) AS latest_match
                    FROM batting_stats bs
                    JOIN players p ON bs.player_id = p.id
                    JOIN matches m ON bs.match_id = m.id
                    {where_clause}
                    GROUP BY p.id, p.name
                ) sub
                {recent_clause if recent_clause else sort_clause}
            '''

        else:  # bowler
            query = f'''
                SELECT *
                FROM (
                    SELECT 
                        p.id,
                        p.name,
                        COUNT(CASE WHEN bs.balls_bowled > 0 THEN 1 END) AS innings,
                        SUM(bs.balls_bowled) AS balls,
                        SUM(bs.wickets) AS wickets,
                        SUM(bs.runs_conceded) AS runs,
                        ROUND(NULLIF(SUM(bs.runs_conceded)::decimal / NULLIF(SUM(bs.wickets), 0), 0), 2) AS average,
                        ROUND(NULLIF(SUM(bs.balls_bowled)::decimal / NULLIF(SUM(bs.wickets), 0), 0), 2) AS strike_rate,
                        ROUND(NULLIF(SUM(bs.runs_conceded)::decimal * 6 / NULLIF(SUM(bs.balls_bowled), 0), 0), 2) AS economy,
                        SUM(bs.maidens) AS maidens,
                        (
                            SELECT 
                                bs2.wickets || '/' || bs2.runs_conceded
                            FROM bowling_stats bs2
                            JOIN matches m2 ON bs2.match_id = m2.id
                            WHERE bs2.player_id = p.id
                            ORDER BY bs2.wickets DESC, bs2.runs_conceded ASC
                            LIMIT 1
                        ) AS best,
                        MAX(m.match_date) AS latest_match
                    FROM bowling_stats bs
                    JOIN players p ON bs.player_id = p.id
                    JOIN matches m ON bs.match_id = m.id
                    {where_clause}
                    GROUP BY p.id, p.name
                ) sub
                {recent_clause if recent_clause else sort_clause}
            '''

        cur.execute(query, tuple(params))
        results = cur.fetchall()

        for idx, row in enumerate(results):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row, tags=(tag,))

    except psycopg2.Error as e:
        conn.rollback()
        print("Main stats fetch error:", e)