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
- [Requirements](#-requirements)
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
Cricket Captain Companion is a Windows-based desktop application designed to assist cricket team captains in player selection by allowing them to view their players performance over a certain time frame or range of matches. The application offers a user-friendly interface built with python's built in gui library tkinter. Captains can record each player’s batting, bowling, and fielding statistics per match. It features role-based access, allowing captains(admin) full data access with advanced analysis tools while players(user) can view only their own recent performances. This design helps prevent players from comparing themselves with teammates, which can sometimes lead to overconfidence or unnecessary pressure - factors that can affect their performance on the field. Captains can filter and sort data by parameters such as total runs, batting average, or wickets taken within a given timeframe or a fixed number of recent matches. Using capable PostgreSQL database it’s ideal for domestic tournaments lacking advanced analysis tools and for school/college matches to record performances and select award-winning players. 

---

There are two versions of the application downloadable CCC-Cloud with supabase hosting its database. Acts as a demo version as it doesnt need any dependencies ( Just install and run ). The main version CCC-Standalone needs PostgreSQL downloaded and it needs to be setup for the connection with app. Procedures are shown in  [Prerequisite](#-prerequisite) section.





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



## ⚙ Requirements

### CCC Cloud
- Display Resolution: require a display resolution around Full HD (1920×1080 ± 200px) for optimal layout and usability.
- Internet Connection: requires a stable internet connection to access the Supabase-hosted database.
- Patience: requires around 30 seconds time for starting up because ~10 pages need to be filled with data fetched from supabase at startup.

[Video Tutorial](https://www.youtube.com/watch?v=py6F1E-n-8c)

### CCC Standalone
- Display Resolution: require a display resolution around Full HD (1920×1080 ± 200px) for optimal layout and usability.
- Database: requires postgreSQL to be installed in the device locally and a database named cricket be created via pgadmin or psql.
- Config.ini : edit the config.ini file to match its contents with the credentials of the database cricket which you created.

[Video Tutorial](https://www.youtube.com/watch?v=6-lGYn0ZKbw) 
  
---
(Both versions are bundled with Python and required libraries, so no external dependencies are needed.
If running source code directly, install Python 3.13+ and dependencies listed in requirements.txt file)


## ⬇ Installation
Please make sure you have read and fulfilled all requirements☝️☝️ before installing and running the application.
### 📦 Download Releases

You can download the pre-built executable versions from the Releases section by following these steps:

- Download the desired ZIP file from the links above.

- Extract/unzip the folder to your preferred location.

- Run the executable inside (ccc-cloud.exe or ccc-standalone.exe).

[Video Tutorial to downlaod CCC-Standalone](https://www.youtube.com/watch?v=6-lGYn0ZKbw&t=144s)

[Video Tutorial to download CCC-Cloud](https://www.youtube.com/watch?v=py6F1E-n-8c&t=32s)


### 💻 Using Source Code

If you want to use the source code instead of pre-built executables:

#### Option 1: Download ZIP

- Click the Code button on the GitHub repository page.

- Select Download ZIP.

- Extract the ZIP file to your computer.

- Make sure you have Python 3.13+ installed.

- Open a terminal (Command Prompt or PowerShell) and navigate to the extracted folder.

- Install dependencies with:

      pip install -r requirements.txt
- Run the app:

      python main.py




#### Option 2: Clone the repository (Recommended for developers)

- Install Git if you don’t have it already.

- Open a terminal and run:

      git clone https://github.com/prasannaexe/CricketCaptainCompanion.git

- Navigate into the cloned folder:

      cd CricketCaptainCompanion

- Install dependencies:

      pip install -r requirements.txt

- Run the app:

      python main.py



## 🖥 App Interface
Here is a showcase of how the application looks and what functionality it offers from the perspective of the Admin and Users:

- Login Page
<img src="https://github.com/user-attachments/assets/64f4a842-10f3-437b-9255-179342cf34ab" >

The login page lets admins login and signup (only possible when there is no 'first admin' once the 'first admin' is create he can create other users or admins and provide them credentials which they can change later) 

### Admin Interface
- User Manager Page
<img src="https://github.com/user-attachments/assets/e11ba007-3368-4287-99ee-450185384d95" />

The user manager page lets the admin create new users with the Name , Age , username , password , role and type attributes. The admin can also delete and update any entries he wants. Beside The table in the upper part is a brillinat matsterpiece of a poster with a black batsman ready to smash the incoming ball in a klien blue background with the big letters showcasing the app name in full glory.

- Enter stats Page
<img src="https://github.com/user-attachments/assets/cd456225-dd6e-4553-b49b-2d9cb6ee3dcd" />

The enter stats page lets the admin enter the statistics of players choosen from the list which contains all players form user manager tab . You can enter any no. of player's stats at a time 1-11) and then choose the match details. The statistics attributes default to 0 and can be traversed easily with Enter key.

- Update stats Page
<img src="https://github.com/user-attachments/assets/eabff061-aaf6-42a7-845a-5ec4fed2d3e9" />

The update stats page contains 4 tables about the recent entries and lets you easily update and delete stats and match details. The stats tables are separated into batting bowling and fielding stats to make the search more quickly

- Fielding overview Page
<img src="https://github.com/user-attachments/assets/577f1608-0fed-49dc-9ab6-aa3ec7776ab8" />

The fielding overview page shows two tables on the right separating the priveleged wicketkeepers from the fielders and showing thier rankings on their fielding performance . Click the plot statistics button and see the magical graphs pop out from nowhere showing efforts of each fielders and the team as a whole.

- Batsmen by timeframe
<img src="https://github.com/user-attachments/assets/1d1e3c6d-c6e8-4ee7-825e-eee1f9167c27" />

The batsmen by timeframe page lets you see which batsman was most prolific in a given timeframe or if you want sort them by averages,strike rates and many more. You can also filter thier performance against a particular opponent

- Batsmen by recent matches
<img src="https://github.com/user-attachments/assets/2d5128f1-c8cf-4872-901f-288db444df4a" />

Batsmen by recnet matches page lets you see which batsman is the most in-form and performed great in recent matches. This is the ultimate capatins wish come true and lets them choose thier best players.

- Bowlers by timeframe

<img  src="https://github.com/user-attachments/assets/caa924d6-e5e0-40e0-9308-f501f5e9a7e7" />

The bowler by timeframe page lets you see who was the gun bowler in their time. More good news! you can also filter them against particular opponents , on a particular ground , in a particular format along with wide range of sorting options.

- Bowlers by recent matches
<img src="https://github.com/user-attachments/assets/8c498885-259d-43cc-84c6-681999fecdd6" />

The bowlers by recent matches lets you select young pacers with better stamina and tougher attitude . Those ageing medium pacers in the name of fast bowlers getting chances on their past fantasies have nowhere to hide now.

- Dashboard
<img src="https://github.com/user-attachments/assets/b6c06695-a553-4e1b-bd26-bc50b422985c" />

Combining personal info along with cool graphs this page lets the admin see their users view . Select any one of you players and see thier batting progression , bowling progression and other cool graphs.

- Match by Match stats
<img src="https://github.com/user-attachments/assets/0233ce1e-ab8f-49ee-8537-79c6d6e4400d" />

All these tabs and still not satisfied , the last resort is a table that takes you down the memory lane to olden times when the player started and how his career shaped . A topping to the cake would be small tables showing averages and aggregates

### User Interface

Everyone views the world differently - I took that saying and implemented it here so that every player sees only their stuffs and not be distracted, overconfident or feel low comparing their stats with other players

- Dashboard

<img src="https://github.com/user-attachments/assets/0d942950-1329-4abb-b6a8-31062152b419" />

Have seen this before ? No check again this time theres no player selector and you can only see your stats. (for users) . Also you can change username and password if you dont like what the admin gave you or some other player found out your secret keys.

- Change password
<img src="https://github.com/user-attachments/assets/1741f707-7d39-44f4-8b53-e01754b0bafa" />

This interface lets users change password if they have current password . If you dont you need to see your admin (captain).

- Match by match stats
<img src="https://github.com/user-attachments/assets/1153ca0a-22d6-40ca-9be5-529d00ac10ea" />

Same but different . Different because this time there is that kind hearted welcome message showing the apps hospitable side . Along with that is your whole career in one page like it or not.


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


  
