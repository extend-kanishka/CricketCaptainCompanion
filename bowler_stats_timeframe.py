from tkinter import *
from tkinter import ttk
import db_connection
import psycopg2
from tkinter import messagebox
from datetime import datetime
from tkinter import Frame, Label, Entry, StringVar, Radiobutton, Button, ttk
conn = db_connection.connect_to_db()
cur = conn.cursor()




def create_view_stats_tab(notebook):

    frame = Frame(notebook, bg="#404040")
    notebook.add(frame, text="BOWLERS -BY TIMEFRAME")

    # Treeview styling
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="#D3D3D3",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#D3D3D3")
    style.map('Treeview', background=[('selected', "#1d1d1d")])

    


    view_frame = Frame(frame, bg="#404040")
    view_frame.place(
        relx=0, rely=0,
        relwidth=1,
        relheight=1,
       
    )


    


    stat_type = StringVar(value="bowler")




    Label(view_frame, text="Sort By:", bg="#404040", fg="white",font=("Arial", 12, "bold")).grid(row=0, column=4, padx=(50,15),pady=20)
    sort_by_cb = ttk.Combobox(view_frame,font=('Arial',12,'bold') ,values=[
        "Name","Wickets", "Balls", "Average", "Strike Rate", "Economy", "Best",  # For batsmen
        #"Wickets", "Economy", "Maidens", "Best", "Bowling Average"  # For bowlers
    ])
    sort_by_cb.set("Name")  # default
    sort_by_cb.grid(row=0, column=5, padx=(15,243),pady=20)




    # Date Range
    Label(view_frame, text="From (YYYY-MM-DD):", bg="#404040", fg="white",font=("Arial", 12, "bold")
          ).grid(row=0, column=0, padx=(50,15),pady=20)
    from_date_entry = Entry(view_frame,font=('Arial', 12, 'bold'))
    from_date_entry.grid(row=0, column=1,padx=(15,50),pady=20)

    Label(view_frame, text="To (YYYY-MM-DD):", bg="#404040", fg="white",font=("Arial", 12, "bold")
          ).grid(row=0, column=2, padx=(50,15),pady=20)
    to_date_entry = Entry(view_frame,font=('Arial', 12, 'bold'))
    to_date_entry.insert(0, datetime.now().date().isoformat())
    to_date_entry.grid(row=0, column=3,padx=(15,50),pady=20)

    '''Recent Matches
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
    type_cb.grid(row=6, column=1)'''

    # Stats Treeview
    tree_container = Frame(view_frame)
    tree_container.grid(row=7, column=0, columnspan=7, sticky="nsew", padx=10, pady=(60,10))

    stats_tree = ttk.Treeview(tree_container, selectmode="extended")
    stats_tree.pack(side="left", fill="both", expand=True)


    stats_tree.tag_configure('oddrow',background="white")
    stats_tree.tag_configure('evenrow',background="lightblue")

    main_scroll = Scrollbar(tree_container, orient="vertical", command=stats_tree.yview)
    main_scroll.pack(side="right", fill="y")

    stats_tree.configure(yscrollcommand=main_scroll.set)
    view_frame.grid_rowconfigure(7, weight=1)
    view_frame.grid_columnconfigure(2, weight=1)

    # Refresh Button
    refresh_btn = Button(view_frame, text="Refresh",font=("Arial",12, "bold"),
                     command=lambda: on_refresh(stat_type.get(), view_frame_widgets),
                     bg="#228B22", fg="white", padx=10)
    refresh_btn.place(x=1360,y=47)


    Label(view_frame, text="MATCH TYPE:", bg="#404040", fg="white", font=("Arial", 12, "bold")).place(x=100,y=80)
    match_type_cb = ttk.Combobox(view_frame, font=('Arial', 12, 'bold'))
    match_type_cb.place(x=245,y=80)

    # Opponent
    Label(view_frame, text="OPPONENT:", bg="#404040", fg="white", font=("Arial", 12, "bold")).place(x=575,y=80)
    opponent_cb = ttk.Combobox(view_frame, font=('Arial', 12, 'bold'))
    opponent_cb.place(x=710,y=80)

    # Location
    Label(view_frame, text="LOCATION:", bg="#404040", fg="white", font=("Arial", 12, "bold")).place(x=970,y=80)
    location_cb = ttk.Combobox(view_frame, font=('Arial', 12, 'bold'))
    location_cb.place(x=1093,y=80)



    # Save widget references for use in update_main_view
    view_frame_widgets = {
        'from_date': from_date_entry,
        'to_date': to_date_entry,
        #'recent_n': recent_entry,
        'opponent': opponent_cb,
        'location': location_cb,
        'match_type': match_type_cb,
        'tree': stats_tree,
        'sort_by': sort_by_cb 
    }
    def on_refresh(stat_type, widgets):
        #populate_comboboxes(widgets)
        update_main_view(stat_type, widgets)

    #populate_comboboxes(view_frame_widgets)
    update_main_view(stat_type.get(), widgets=view_frame_widgets)

    # Initialize Comboboxes and Trees
    #populate_comboboxes(view_frame_widgets)  # Fills opponent/location/type filters
    #update_main_view(stat_type.get(), widgets=view_frame_widgets) 



    return frame

def on_refresh(stat_type, widgets):
    
    update_main_view(stat_type, widgets)







'''def populate_comboboxes(widgets):
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
'''



'''def update_main_view(stat_type, widgets):
    from tkinter import NO, CENTER
    import psycopg2

    cur = conn.cursor()

    tree = widgets['tree']
    tree.delete(*tree.get_children())

    # Set up Treeview columns
    
    #if stat_type == "batsman":
    columns = ("PlayerID", "Name", "Innings", "Runs", "Balls", "Average", "StrikeRate", "Fours", "Sixes", "100s", "Best")
    #else:
    #columns = ("PlayerID", "Name", "Innings", "Balls", "Wickets", "Runs", "Average", "StrikeRate", "Economy", "Maidens", "Best")

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

    #opponent = widgets['opponent'].get().strip()
    #location = widgets['location'].get().strip()
    #match_type = widgets['match_type'].get().strip()

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
        #'Wickets': 'wickets',
        #'Economy': 'economy'
    }

    sort_column = valid_sort_columns.get(selected_sort, None)
    sort_clause = f"ORDER BY {sort_column} DESC" if sort_column else ""
    recent_clause = f"ORDER BY latest_match DESC LIMIT {recent_n}" if recent_n.isdigit() else ""

    try:
        if stat_type == "batsman":
            query = f
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
            

        else:  # bowler
            query = f
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
            

        cur.execute(query, tuple(params))
        results = cur.fetchall()

        for idx, row in enumerate(results):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row, tags=(tag,))

    except psycopg2.Error as e:
        conn.rollback()
        print("Main stats fetch error:", e)

'''



def update_main_view(stat_type, widgets):
    from tkinter import NO, CENTER
    import psycopg2
    from datetime import datetime

    cur = conn.cursor()
    tree = widgets['tree']
    tree.delete(*tree.get_children())

    columns = ("PlayerID", "Name", "Innings", "Balls", "Wickets", "Runs", "Average", "StrikeRate","Economy", "Maidens", "Best")
    tree['columns'] = columns
    tree.column("#0", width=0, stretch=NO)
    for col in columns:
        tree.column(col, anchor=CENTER, width=90)
        tree.heading(col, text=col, anchor=CENTER)


    def populate_combobox_options():
        try:
            cur.execute("SELECT DISTINCT match_type FROM matches")
            match_types = [row[0] for row in cur.fetchall()]
            widgets['match_type']['values'] = [''] + match_types  # allow empty selection

            cur.execute("SELECT DISTINCT opponent FROM matches")
            opponents = [row[0] for row in cur.fetchall()]
            widgets['opponent']['values'] = [''] + opponents

            cur.execute("SELECT DISTINCT location FROM matches")
            locations = [row[0] for row in cur.fetchall()]
            widgets['location']['values'] = [''] + locations

        except psycopg2.Error as e:
            print("Error populating comboboxes:", e)


    populate_combobox_options()

    # Get filters
    filters = []
    params = []

    from_date = widgets['from_date'].get().strip()
    to_date = widgets['to_date'].get().strip()

    # If not provided, fallback to full range
    if not from_date:
        cur.execute("SELECT MIN(match_date) FROM matches")
        earliest = cur.fetchone()[0]
        from_date = earliest.strftime('%Y-%m-%d') if earliest else '2000-01-01'

    if not to_date:
        to_date = datetime.now().date().isoformat()


    filters.append("m.match_date BETWEEN %s AND %s")
    params.extend([from_date, to_date])



    match_type = widgets['match_type'].get().strip()
    if match_type:
        filters.append("m.match_type = %s")
        params.append(match_type)

    opponent = widgets['opponent'].get().strip()
    if opponent:
        filters.append("m.opponent = %s")
        params.append(opponent)

    location = widgets['location'].get().strip()
    if location:
        filters.append("m.location = %s")
        params.append(location)









    where_clause = where_clause = f"WHERE {' AND '.join(filters)}" if filters else ""

    selected_sort = widgets['sort_by'].get().strip()

    sort_column = None
    sort_order = "DESC"  # default

    valid_sort_columns = {
        'Name': ('name', 'ASC'),
        'Wickets': ('wickets', 'DESC'),
        'Balls': ('balls', 'DESC'),
        'Average': ('average', 'ASC'),
        'Strike Rate': ('strike_rate', 'ASC'),
        'Economy': ('economy', 'ASC'),
        'Best': ('best_sort_key', 'DESC'),
    }



    selected_sort = widgets['sort_by'].get().strip()
    if selected_sort in valid_sort_columns:
        sort_column, sort_order = valid_sort_columns[selected_sort]
        if sort_order == "ASC":
            sort_clause = f"ORDER BY {sort_column} ASC NULLS LAST"
        else:
            sort_clause = f"ORDER BY {sort_column} DESC"
    else:
        sort_clause = ""

    #sort_column = valid_sort_columns.get(selected_sort, None)
    #sort_clause = f"ORDER BY {sort_column} DESC" if sort_column else ""

    try:
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

                    -- For sorting best: combine wickets and negative runs
                    (
                        SELECT 
                            bs2.wickets * 1000 - bs2.runs_conceded
                        FROM bowling_stats bs2
                        WHERE bs2.player_id = p.id
                        ORDER BY bs2.wickets DESC, bs2.runs_conceded ASC
                        LIMIT 1
                    ) AS best_sort_key
                    
                FROM bowling_stats bs
                JOIN players p ON bs.player_id = p.id
                JOIN matches m ON bs.match_id = m.id
                {where_clause}
                GROUP BY p.id, p.name
            ) sub
            {sort_clause}
        '''

        cur.execute(query, tuple(params))
        results = cur.fetchall()

        for idx, row in enumerate(results):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            tree.insert("", "end", values=row, tags=(tag,))

    except psycopg2.Error as e:
        conn.rollback()
        print("Main stats fetch error:", e)