# 🏏 Cricket Captain Companion

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![language](https://img.shields.io/badge/language-python-3670A0)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![OS](https://img.shields.io/badge/OS-windows-0078D4)
![CPU](https://img.shields.io/badge/CPU-x64-FF8C00)
[![GitHub release](https://img.shields.io/github/v/release/prasannaexe/CricketCaptainCompanion)](#)
[![GitHub release date](https://img.shields.io/github/release-date/prasannaexe/CricketCaptainCompanion)](#)
[![GitHub last commit](https://img.shields.io/github/last-commit/prasannaexe/CricketCaptainCompanion)](#)



[![Share](https://img.shields.io/badge/share-000000?logo=x&logoColor=white)](https://x.com/intent/tweet?text=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/prasannaexe/CricketCaptainCompanion)
[![Share](https://img.shields.io/badge/share-1877F2?logo=facebook&logoColor=white)](https://www.facebook.com/sharer/sharer.php?u=https://github.com/prasannaexe/CricketCaptainCompanion)
[![Share](https://img.shields.io/badge/share-FF4500?logo=reddit&logoColor=white)](https://www.reddit.com/submit?title=Check%20out%20this%20project%20on%20GitHub:%20https://github.com/prasannaexe/CricketCaptainCompanion)
[![Share](https://img.shields.io/badge/share-0088CC?logo=telegram&logoColor=white)](https://t.me/share/url?url=https://github.com/prasannaexe/CricketCaptainCompanion)





## 📃 Table of Contents
- [About](#-about)
- [Features](#-features) 
- [Tech Stack](#-tech-stack)
- [Database Schema](#database-schema)
- 
- 
- [Certification](#-certification)
- [How to Build](#-how-to-build)
- [Documentation](#-documentation)
- [Feedback and Contributions](#-feedback-and-contributions)
- [License](#-license)




## 📌 Features

- 🔐 **Role-Based Login**: Separate interfaces for captains and players.
- 👤 **Player Management**: Add/edit player profiles and credentials.
- 🏟️ **Match Management**: Store date, location, opponent, and type of match.
- 📊 **Performance Entry**: Add batting, bowling, and fielding stats per player per match.
- 📈 **Form Analysis**: View player performance over last N matches or custom date range.
- 🖥️ **Clean GUI**: Built with Tkinter and Treeview for a polished interface.



## 🧠 Tech Stack



| Layer         | Tech Used                                 |
|---------------|-------------------------------------------|
| 🖥️ Frontend   | `Tkinter`                                 |
| ⚙️ Logic      | `Python 3.13.5`                            |
| 🔌 Connector  | `psycopg2`          |
| 🗄️ Database Host  |  `Supabase`         |
| 🧑‍💻 Code Editor  | `Visual Studio Code`   |
| ☁️ Code Hosting  | `GitHub`              |
| 🛠️ Packaging     | `PyInstaller`         |



## 🧱 Database Schema

🧍‍♂️ players Table
| Column | Type        | Constraints |
| ------ | ----------- | ----------- |
| `id`   | SERIAL      | PRIMARY KEY |
| `name` | VARCHAR(40) | NOT NULL    |
| `age`  | INT         | NOT NULL    |
| `type` | VARCHAR(40) | —           |

👤 users Table
| Column      | Type        | Constraints          |
| ----------- | ----------- | ------------------- |
| `id`        | SERIAL      | PRIMARY KEY          |
| `username`  | VARCHAR(40) | NOT NULL, UNIQUE     |
| `password`  | VARCHAR(40) | NOT NULL            |
| `role`      | VARCHAR(20) | NOT NULL            |
| `player_id` | INT         | UNIQUE, FOREIGN KEY|

🏏 matches Table
| Column       | Type        | Constraints   |
| ------------ | ----------- | --------------|
| `id`         | SERIAL      | PRIMARY KEY  |
| `match_date` | DATE        | NOT NULL |
| `opponent`   | VARCHAR(20) | —           |
| `location`   | VARCHAR(20) | —             |
| `match_type` | VARCHAR(20) | —            |

🪖 batting_stats Table
| Column        | Type    | Constraints                 |
| ------------- | ------- | --------------------------- |
| `id`          | SERIAL  | PRIMARY KEY                 |
| `player_id`   | INT     | FOREIGN KEY |
| `match_id`    | INT     | FOREIGN KEY |
| `runs_scored` | INT     | DEFAULT 0                   |
| `balls_faced` | INT     | DEFAULT 0                   |
| `fours`       | INT     | DEFAULT 0                   |
| `sixes`       | INT     | DEFAULT 0                   |
| `dismissal`   | BOOLEAN | DEFAULT FALSE               |

🎯 bowling_stats Table
| Column          | Type   | Constraints                 |
| --------------- | ------ | --------------------------- |
| `id`            | SERIAL | PRIMARY KEY                 |
| `player_id`     | INT    | FOREIGN KEY  |
| `match_id`      | INT    | FOREIGN KEY  |
| `balls_bowled`  | INT    | DEFAULT 0                   |
| `runs_conceded` | INT    | DEFAULT 0                   |
| `wickets`       | INT    | DEFAULT 0                   |
| `maidens`       | INT    | DEFAULT 0                   |

🧤 fielding_stats Table
| Column      | Type   | Constraints  |
| ----------- | ------ | ------------- |
| `id`        | SERIAL | PRIMARY KEY   |
| `player_id` | INT    | FOREIGN KEY |
| `match_id`  | INT    | FOREIGN KEY  |
| `catches`   | INT    | DEFAULT 0   |
| `run_outs`  | INT    | DEFAULT 0    |
| `stumpings` | INT    | DEFAULT 0   |


---


## 🚀 Getting Started

### Prerequisites

- Python 3.13.5
- PostgreSQL
- `psycopg2` installed
- Tkinter (comes with Python)

### Clone and Run

```bash
git clone https://github.com/yourusername/CricketCaptainCompanion.git
cd CricketCaptainCompanion
python main.py
```

## Directory Structure
```
Cricket-Captain-Companion
├─ Assets
│  ├─ bitmap.png
│  ├─ button1.png
│  ├─ button2.png
│  ├─ button3.png
│  ├─ button4.png
│  └─ path6.png
├─ dist
│  └─ main.exe
├─ .gitignore
├─ admin_interface.py
├─ batsman_stats_recentmatches.py
├─ batsman_stats_timeframe.py
├─ bowler_stats_recentmatches.py
├─ bowler_stats_timeframe.py
├─ config.ini
├─ db_connection.py
├─ LICENSE
├─ main.py
├─ main.spec
├─ player_view_dashboard.py
├─ player_view_match_by_match.py
├─ README.md
├─ requirements.txt
├─ update_stats_tab.py
├─ user_interface.py
└─ view_stats.py
```
## 🛠️ Issues Encountered

- **Supabase Lag**: Integrating Supabase slowed down queries due to online latency. We optimized by caching and restructuring our DB calls.

- **PyInstaller Packaging**: Some image and config file paths broke when building `.exe`. Fixed by restructuring `Assets/` and using relative paths.

- **Tkinter Layout on Full HD**: Getting consistent layout across 1920x1080 resolution required pixel-perfect geometry tuning.

- **Cursor Already Closed Errors**: Fixed by using separate cursors per DB operation in `psycopg2`.

---

## 🧠 Lessons Learned

- Learned real-world use of SQL joins, aggregation, and complex filters for stats queries.

- Improved Python GUI design using `Tkinter`, `ttk.Treeview`, and `matplotlib`.

- Understood the trade-offs between local databases vs. cloud-hosted services (Supabase/PostgreSQL).

- Understood the challenge of balancing UI design with backend performance.

---

## 🎯 Future Enhancements

- Add player vs player comparisons in visual graphs.

- Build a cloud dashboard version for teams with login and role access.

- Add PDF export for stats and charts.

- Build a mobile version with Flutter or React Native.

- Implement dark mode for better UX.

---

## 🧑‍💻 Contributing

Contributions are welcome! Please open issues or submit pull requests for new stat types, UI improvements, or bug fixes.

Please ensure your pull request adheres to the following guidelines:

- Alphabetize your entry.
- Search for previous suggestions before making a new one, as yours may be a duplicate.
- Suggested READMEs should be beautiful or stand out in some way.
- Make an individual pull request for each suggestion.
- New categories or improvements to the existing categorization are welcome.
- Keep descriptions short and simple, but descriptive.
- Start the description with a capital and end with a full stop/period.
- Check your spelling and grammar.
- Make sure your text editor is set to remove trailing whitespace.
- Use the `#readme` anchor for GitHub READMEs to link them directly.

Thank you for your suggestions!
### Steps:


---

## 🤝 Acknowledgements

Respected Er. Rajad Shakya – for providing guidance throughout the project.

Open-source communities, YouTube educators & documentation authors.

All contributors and developers behind Python, PostgreSQL, and open tools.


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Prasanna Paudel

079BEI023 – Thapathali Campus, IOE, TU

🔗 GitHub


  
