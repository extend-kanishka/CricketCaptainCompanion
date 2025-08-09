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
- [About](#ℹ️-about)
- [Features](#-features) 
- [Tech Stack](#-tech-stack)
- [Prerequisite](#-prerequisite)
- [Installation](#-installation)
- [App Interface](#-app-interface)
- [Database Schema](#-database-schema)
- [Directory Structure](#-directory-structure)
- [Issues Encountered](#-issues-encountered)
- [Future Enhancements](#-future-enhancements)
- [Lessons Learnt](#-lessons-learnt)
- [Acknowledgements](#-acknowledgements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

  

## ℹ️ About
<img src="https://private-user-images.githubusercontent.com/123853733/475893474-bb2d59cd-8275-437d-b5f4-a8e9ba3c5d07.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NTQ3MTE3MTcsIm5iZiI6MTc1NDcxMTQxNywicGF0aCI6Ii8xMjM4NTM3MzMvNDc1ODkzNDc0LWJiMmQ1OWNkLTgyNzUtNDM3ZC1iNWY0LWE4ZTliYTNjNWQwNy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwODA5JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDgwOVQwMzUwMTdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT04MTk1YzEwYjIwM2I2OTU5YjY5MDlhYmQxYmE3NzdmNWJlNTY5YWMxMDA2YTg0ZTFmMWQ0ZjI1OWNkODEwMTMxJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.P_-Pbey2vjmevWrzu9XqCHAG93IA-kKUwiBFF6iV7Gk" align="right" alt="Cricket Captain Companion screenshot" width="350" style="margin-left: 15px; margin-bottom: 15px;">
Cricket Captain Companion is a Windows-based desktop application designed to assist cricket team captains in player selection by allowing them to view their players performance over a certain time frame or range of matches. The application offers a user-friendly interface built with python's built in gui library tkinter. Captains can record each player’s batting, bowling, and fielding statistics per match. It features role-based access, allowing captains full data access with advanced analysis tools while players can view only their own recent performances. This design helps prevent players from comparing themselves with teammates, which can sometimes lead to overconfidence or unnecessary pressure - factors that can otherwise affect their performance on the field. Captains can filter and sort data by parameters such as total runs, batting average, or wickets taken within a given timeframe or a fixed number of recent matches. Using capable PostgreSQL database it’s ideal for domestic tournaments lacking advanced analysis tools and for school/college matches to record performances and select award-winning players.





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



## ⚙ Prerequisite

dfsfd
## ⬇ Installation

sdfsdf
## 🖥 App Interface

sdfsdf


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

## 📁 Directory Structure
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


## 🛠 Issues Encountered

### Slow Startup in Cloud Edition
The initial startup of app loads around 10 interface pages with data fetched directly from the database , which caused around 30 seconds delay. Additionally, basic operations like adding, editing, or deleting players/matches/stats took ~2 seconds each due to online query latency.

### Foreign Key Deletion Restrictions
Users linked to other tables ( batting or bowling stats) could not be deleted without first removing all associated records, due to foreign key constraints.

### Resolution-Specific Layout Challenges
While the main layout was dynamic, some pages had too many widgets to scale cleanly, resulting in layouts optimized mainly for 1920×1080 ± 200px resolutions. Certain elements had to be hardcoded for proper alignment.

### No Data Isolation in Demo Cloud Version
To keep the demo version simple and avoid further slowdowns, all users shared a single public database in the cloud build. This allowed quick testing, but meant captains could view all players, not just those on their team. So the cloud version is there for demonstration only.



## 🎯 Future Enhancements

- Implement search feature in the update stats tab for quickly updating the filtered statistics.

- Use indexing on frequently queried columns to speed up database operations.

- Mechanism to export the graphs made using matplotlib to pdf formats .

- Allow user deletion without requiring manual removal of all related stats.

- Merge the current 4 search pages to a single search page with all possible filters.


## 🧠 Lessons Learnt


- Learned real world use of SQL joins, aggregation, and complex filters for stats queries.

- Learned Python GUI design using `Tkinter`, `ttk.Treeview`, and `matplotlib`.

- Understood the trade-offs between local databases vs. cloud-hosted ones (speed vs convenience)

- Understood the challenges of making an interface capable of running in a variety of resolutions.

- Understood the challenges optimizing database performance through the use of indices.



## 🤝 Acknowledgements

Respected Sir 🙏🙏 Er. Rajad Shakya👑– for providing us the opportunity and guidance.

Open-source communities, Subreddits & documentation authors.

All contributors and developers of Python, PostgreSQL, and psycopg2.

Youtube channels (Codemy.com , M Prashant Tech, techTFQ, Code first with Hala)

AI (Chat gpt , Grok and Gemini) for thier recommendations and ideas.


## 🧑‍💻 Contributing

Contributions are welcome! Please open issues or submit pull requests for new features, UI improvements, or bug fixes.

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



## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.



## 👤 Author

Prasanna Paudel

Department of Electronics and Computer Engineering

Thapathali Campus, IOE, TU

🔗 GitHub


  
