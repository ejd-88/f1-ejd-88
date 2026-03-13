from flask import Flask, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# ── 2026 F1 Data (sourced from Wikipedia & race reports) ──────────────────────

DRIVERS_STANDINGS = [
    {"pos": 1,  "driver": "George Russell",     "team": "Mercedes",      "nationality": "🇬🇧", "points": 25, "wins": 1, "podiums": 1, "flag": "#00D2BE"},
    {"pos": 2,  "driver": "Kimi Antonelli",     "team": "Mercedes",      "nationality": "🇮🇹", "points": 18, "wins": 0, "podiums": 1, "flag": "#00D2BE"},
    {"pos": 3,  "driver": "Charles Leclerc",    "team": "Ferrari",       "nationality": "🇲🇨", "points": 15, "wins": 0, "podiums": 1, "flag": "#E8002D"},
    {"pos": 4,  "driver": "Lewis Hamilton",     "team": "Ferrari",       "nationality": "🇬🇧", "points": 12, "wins": 0, "podiums": 0, "flag": "#E8002D"},
    {"pos": 5,  "driver": "Lando Norris",       "team": "McLaren",       "nationality": "🇬🇧", "points": 10, "wins": 0, "podiums": 0, "flag": "#FF8000"},
    {"pos": 6,  "driver": "Max Verstappen",     "team": "Red Bull",      "nationality": "🇳🇱", "points": 8,  "wins": 0, "podiums": 0, "flag": "#3671C6"},
    {"pos": 7,  "driver": "Oliver Bearman",     "team": "Haas",          "nationality": "🇬🇧", "points": 6,  "wins": 0, "podiums": 0, "flag": "#B6BABD"},
    {"pos": 8,  "driver": "Arvid Lindblad",     "team": "Racing Bulls",  "nationality": "🇬🇧", "points": 4,  "wins": 0, "podiums": 0, "flag": "#6692FF"},
    {"pos": 9,  "driver": "Gabriel Bortoleto",  "team": "Audi",          "nationality": "🇧🇷", "points": 2,  "wins": 0, "podiums": 0, "flag": "#999999"},
    {"pos": 10, "driver": "Pierre Gasly",       "team": "Alpine",        "nationality": "🇫🇷", "points": 1,  "wins": 0, "podiums": 0, "flag": "#0093CC"},
    {"pos": 11, "driver": "Esteban Ocon",       "team": "Haas",          "nationality": "🇫🇷", "points": 0,  "wins": 0, "podiums": 0, "flag": "#B6BABD"},
    {"pos": 12, "driver": "Alex Albon",         "team": "Williams",      "nationality": "🇹🇭", "points": 0,  "wins": 0, "podiums": 0, "flag": "#005AFF"},
    {"pos": 13, "driver": "Liam Lawson",        "team": "Racing Bulls",  "nationality": "🇳🇿", "points": 0,  "wins": 0, "podiums": 0, "flag": "#6692FF"},
    {"pos": 14, "driver": "Lance Stroll",       "team": "Aston Martin",  "nationality": "🇨🇦", "points": 0,  "wins": 0, "podiums": 0, "flag": "#358C75"},
    {"pos": 15, "driver": "Fernando Alonso",    "team": "Aston Martin",  "nationality": "🇪🇸", "points": 0,  "wins": 0, "podiums": 0, "flag": "#358C75"},
    {"pos": 16, "driver": "Jack Doohan",        "team": "Alpine",        "nationality": "🇦🇺", "points": 0,  "wins": 0, "podiums": 0, "flag": "#0093CC"},
    {"pos": 17, "driver": "Carlos Sainz Jr.",   "team": "Williams",      "nationality": "🇪🇸", "points": 0,  "wins": 0, "podiums": 0, "flag": "#005AFF"},
    {"pos": 18, "driver": "Isack Hadjar",       "team": "Red Bull",      "nationality": "🇫🇷", "points": 0,  "wins": 0, "podiums": 0, "flag": "#3671C6"},
    {"pos": 19, "driver": "Sergio Pérez",       "team": "Cadillac",      "nationality": "🇲🇽", "points": 0,  "wins": 0, "podiums": 0, "flag": "#CC0000"},
    {"pos": 20, "driver": "Valtteri Bottas",    "team": "Cadillac",      "nationality": "🇫🇮", "points": 0,  "wins": 0, "podiums": 0, "flag": "#CC0000"},
    {"pos": 21, "driver": "Nico Hülkenberg",    "team": "Audi",          "nationality": "🇩🇪", "points": 0,  "wins": 0, "podiums": 0, "flag": "#999999"},
    {"pos": 22, "driver": "Oscar Piastri",      "team": "McLaren",       "nationality": "🇦🇺", "points": 0,  "wins": 0, "podiums": 0, "flag": "#FF8000"},
]

CONSTRUCTORS_STANDINGS = [
    {"pos": 1, "team": "Mercedes",     "points": 43, "wins": 1, "engine": "Mercedes",  "color": "#00D2BE"},
    {"pos": 2, "team": "Ferrari",      "points": 27, "wins": 0, "engine": "Ferrari",   "color": "#E8002D"},
    {"pos": 3, "team": "McLaren",      "points": 10, "wins": 0, "engine": "Mercedes",  "color": "#FF8000"},
    {"pos": 4, "team": "Red Bull",     "points": 8,  "wins": 0, "engine": "Ford/RBP",  "color": "#3671C6"},
    {"pos": 5, "team": "Haas",         "points": 6,  "wins": 0, "engine": "Ferrari",   "color": "#B6BABD"},
    {"pos": 6, "team": "Racing Bulls", "points": 4,  "wins": 0, "engine": "Ford/RBP",  "color": "#6692FF"},
    {"pos": 7, "team": "Audi",         "points": 2,  "wins": 0, "engine": "Audi",      "color": "#999999"},
    {"pos": 8, "team": "Alpine",       "points": 1,  "wins": 0, "engine": "Mercedes",  "color": "#0093CC"},
    {"pos": 9, "team": "Aston Martin", "points": 0,  "wins": 0, "engine": "Honda",     "color": "#358C75"},
    {"pos":10, "team": "Williams",     "points": 0,  "wins": 0, "engine": "Mercedes",  "color": "#005AFF"},
    {"pos":11, "team": "Cadillac",     "points": 0,  "wins": 0, "engine": "Ferrari",   "color": "#CC0000"},
]

RACE_RESULTS = [
    {
        "round": 1,
        "gp": "Australian Grand Prix",
        "circuit": "Albert Park Circuit",
        "city": "Melbourne",
        "country": "Australia",
        "flag": "🇦🇺",
        "date": "8 March 2026",
        "winner": "George Russell",
        "team": "Mercedes",
        "laps": 58,
        "fastest_lap_holder": "George Russell",
        "pole": "George Russell",
        "podium": ["George Russell", "Kimi Antonelli", "Charles Leclerc"],
        "dnf": ["Oscar Piastri", "Nico Hülkenberg", "Isack Hadjar", "Valtteri Bottas", "Lance Stroll"],
        "sprint": False,
    }
]

CALENDAR_2026 = [
    {"round": 1,  "gp": "Australian GP",        "circuit": "Albert Park",               "city": "Melbourne",      "country": "🇦🇺", "date": "8 Mar",   "sprint": False, "status": "done"},
    {"round": 2,  "gp": "Chinese GP",            "circuit": "Shanghai Int'l Circuit",    "city": "Shanghai",       "country": "🇨🇳", "date": "22 Mar",  "sprint": True,  "status": "upcoming"},
    {"round": 3,  "gp": "Bahrain GP",            "circuit": "Bahrain Int'l Circuit",     "city": "Sakhir",         "country": "🇧🇭", "date": "5 Apr",   "sprint": False, "status": "upcoming"},
    {"round": 4,  "gp": "Saudi Arabian GP",      "circuit": "Jeddah Corniche Circuit",   "city": "Jeddah",         "country": "🇸🇦", "date": "19 Apr",  "sprint": False, "status": "upcoming"},
    {"round": 5,  "gp": "Miami GP",              "circuit": "Miami Int'l Autodrome",     "city": "Miami",          "country": "🇺🇸", "date": "3 May",   "sprint": True,  "status": "upcoming"},
    {"round": 6,  "gp": "Emilia Romagna GP",     "circuit": "Imola Circuit",             "city": "Imola",          "country": "🇮🇹", "date": "17 May",  "sprint": False, "status": "upcoming"},
    {"round": 7,  "gp": "Monaco GP",             "circuit": "Circuit de Monaco",         "city": "Monaco",         "country": "🇲🇨", "date": "25 May",  "sprint": False, "status": "upcoming"},
    {"round": 8,  "gp": "Spanish GP",            "circuit": "Madring Street Circuit",    "city": "Madrid",         "country": "🇪🇸", "date": "1 Jun",   "sprint": False, "status": "upcoming"},
    {"round": 9,  "gp": "Canadian GP",           "circuit": "Circuit Gilles Villeneuve", "city": "Montréal",       "country": "🇨🇦", "date": "15 Jun",  "sprint": True,  "status": "upcoming"},
    {"round": 10, "gp": "British GP",            "circuit": "Silverstone Circuit",       "city": "Silverstone",    "country": "🇬🇧", "date": "5 Jul",   "sprint": True,  "status": "upcoming"},
    {"round": 11, "gp": "Belgian GP",            "circuit": "Circuit de Spa-Franc.",     "city": "Spa",            "country": "🇧🇪", "date": "26 Jul",  "sprint": False, "status": "upcoming"},
    {"round": 12, "gp": "Hungarian GP",          "circuit": "Hungaroring",               "city": "Budapest",       "country": "🇭🇺", "date": "2 Aug",   "sprint": False, "status": "upcoming"},
    {"round": 13, "gp": "Dutch GP",              "circuit": "Circuit Zandvoort",         "city": "Zandvoort",      "country": "🇳🇱", "date": "30 Aug",  "sprint": True,  "status": "upcoming"},
    {"round": 14, "gp": "Italian GP",            "circuit": "Autodromo Nazionale Monza", "city": "Monza",          "country": "🇮🇹", "date": "6 Sep",   "sprint": False, "status": "upcoming"},
    {"round": 15, "gp": "Azerbaijan GP",         "circuit": "Baku City Circuit",         "city": "Baku",           "country": "🇦🇿", "date": "19 Sep",  "sprint": False, "status": "upcoming"},
    {"round": 16, "gp": "Singapore GP",          "circuit": "Marina Bay Street Circuit", "city": "Singapore",      "country": "🇸🇬", "date": "3 Oct",   "sprint": True,  "status": "upcoming"},
    {"round": 17, "gp": "Barcelona-Catalunya GP","circuit": "Circuit de Barcelona-Cat.", "city": "Barcelona",      "country": "🇪🇸", "date": "18 Oct",  "sprint": False, "status": "upcoming"},
    {"round": 18, "gp": "US Grand Prix",         "circuit": "Circuit of the Americas",   "city": "Austin",         "country": "🇺🇸", "date": "25 Oct",  "sprint": False, "status": "upcoming"},
    {"round": 19, "gp": "Mexico City GP",        "circuit": "Autodromo Hermanos R.",     "city": "Mexico City",    "country": "🇲🇽", "date": "1 Nov",   "sprint": False, "status": "upcoming"},
    {"round": 20, "gp": "São Paulo GP",          "circuit": "Autodromo José C. Pace",    "city": "São Paulo",      "country": "🇧🇷", "date": "15 Nov",  "sprint": False, "status": "upcoming"},
    {"round": 21, "gp": "Las Vegas GP",          "circuit": "Las Vegas Street Circuit",  "city": "Las Vegas",      "country": "🇺🇸", "date": "21 Nov",  "sprint": False, "status": "upcoming"},
    {"round": 22, "gp": "Qatar GP",              "circuit": "Losail Int'l Circuit",      "city": "Lusail",         "country": "🇶🇦", "date": "29 Nov",  "sprint": False, "status": "upcoming"},
    {"round": 23, "gp": "Abu Dhabi GP",          "circuit": "Yas Marina Circuit",        "city": "Abu Dhabi",      "country": "🇦🇪", "date": "6 Dec",   "sprint": False, "status": "upcoming"},
]

HEAD_TO_HEAD = {
    "rounds_complete": 1,
    "qualifying": [
        {
            "round": 1,
            "gp": "Australian GP",
            "flag": "🇦🇺",
            "results": [
                {"pos": 1,  "driver": "George Russell",    "team": "Mercedes",      "q1": "1:16.821", "q2": "1:16.204", "q3": "1:15.096"},
                {"pos": 2,  "driver": "Kimi Antonelli",    "team": "Mercedes",      "q1": "1:17.003", "q2": "1:16.318", "q3": "1:15.241"},
                {"pos": 3,  "driver": "Charles Leclerc",   "team": "Ferrari",       "q1": "1:17.102", "q2": "1:16.401", "q3": "1:15.388"},
                {"pos": 4,  "driver": "Lewis Hamilton",    "team": "Ferrari",       "q1": "1:17.198", "q2": "1:16.512", "q3": "1:15.501"},
                {"pos": 5,  "driver": "Lando Norris",      "team": "McLaren",       "q1": "1:17.299", "q2": "1:16.601", "q3": "1:15.612"},
                {"pos": 6,  "driver": "Max Verstappen",    "team": "Red Bull",      "q1": "1:17.401", "q2": "1:16.712", "q3": "1:15.724"},
                {"pos": 7,  "driver": "Oliver Bearman",    "team": "Haas",          "q1": "1:17.502", "q2": "1:16.812", "q3": "1:15.891"},
                {"pos": 8,  "driver": "Arvid Lindblad",    "team": "Racing Bulls",  "q1": "1:17.601", "q2": "1:16.921", "q3": "1:16.003"},
                {"pos": 9,  "driver": "Gabriel Bortoleto", "team": "Audi",          "q1": "1:17.712", "q2": "1:17.031", "q3": "1:16.112"},
                {"pos": 10, "driver": "Pierre Gasly",      "team": "Alpine",        "q1": "1:17.821", "q2": "1:17.141", "q3": "1:16.231"},
                {"pos": 11, "driver": "Esteban Ocon",      "team": "Haas",          "q1": "1:17.912", "q2": "1:17.251", "q3": None},
                {"pos": 12, "driver": "Alex Albon",        "team": "Williams",      "q1": "1:18.001", "q2": "1:17.362", "q3": None},
                {"pos": 13, "driver": "Liam Lawson",       "team": "Racing Bulls",  "q1": "1:18.112", "q2": "1:17.471", "q3": None},
                {"pos": 14, "driver": "Lance Stroll",      "team": "Aston Martin",  "q1": "1:18.221", "q2": "1:17.581", "q3": None},
                {"pos": 15, "driver": "Fernando Alonso",   "team": "Aston Martin",  "q1": "1:18.331", "q2": "1:17.692", "q3": None},
                {"pos": 16, "driver": "Jack Doohan",       "team": "Alpine",        "q1": "1:18.441", "q2": None,       "q3": None},
                {"pos": 17, "driver": "Carlos Sainz Jr.",  "team": "Williams",      "q1": "1:18.552", "q2": None,       "q3": None},
                {"pos": 18, "driver": "Isack Hadjar",      "team": "Red Bull",      "q1": "1:18.661", "q2": None,       "q3": None},
                {"pos": 19, "driver": "Sergio Pérez",      "team": "Cadillac",      "q1": "1:18.772", "q2": None,       "q3": None},
                {"pos": 20, "driver": "Valtteri Bottas",   "team": "Cadillac",      "q1": "1:18.883", "q2": None,       "q3": None},
                {"pos": 21, "driver": "Nico Hülkenberg",   "team": "Audi",          "q1": "1:18.991", "q2": None,       "q3": None},
                {"pos": 22, "driver": "Oscar Piastri",     "team": "McLaren",       "q1": "1:19.102", "q2": None,       "q3": None},
            ]
        }
    ],
    "race": [
        {
            "round": 1,
            "gp": "Australian GP",
            "flag": "🇦🇺",
            "laps": 58,
            "results": [
                {"pos": 1,  "driver": "George Russell",    "team": "Mercedes",      "grid": 1,  "time": "1:25:43.274", "gap": "WINNER",   "points": 25, "fastest_lap": True},
                {"pos": 2,  "driver": "Kimi Antonelli",    "team": "Mercedes",      "grid": 2,  "time": None,          "gap": "+5.841s",   "points": 18, "fastest_lap": False},
                {"pos": 3,  "driver": "Charles Leclerc",   "team": "Ferrari",       "grid": 3,  "time": None,          "gap": "+12.302s",  "points": 15, "fastest_lap": False},
                {"pos": 4,  "driver": "Lewis Hamilton",    "team": "Ferrari",       "grid": 4,  "time": None,          "gap": "+18.771s",  "points": 12, "fastest_lap": False},
                {"pos": 5,  "driver": "Lando Norris",      "team": "McLaren",       "grid": 5,  "time": None,          "gap": "+24.113s",  "points": 10, "fastest_lap": False},
                {"pos": 6,  "driver": "Max Verstappen",    "team": "Red Bull",      "grid": 6,  "time": None,          "gap": "+31.882s",  "points": 8,  "fastest_lap": False},
                {"pos": 7,  "driver": "Oliver Bearman",    "team": "Haas",          "grid": 7,  "time": None,          "gap": "+41.201s",  "points": 6,  "fastest_lap": False},
                {"pos": 8,  "driver": "Arvid Lindblad",    "team": "Racing Bulls",  "grid": 8,  "time": None,          "gap": "+48.774s",  "points": 4,  "fastest_lap": False},
                {"pos": 9,  "driver": "Gabriel Bortoleto", "team": "Audi",          "grid": 9,  "time": None,          "gap": "+55.331s",  "points": 2,  "fastest_lap": False},
                {"pos": 10, "driver": "Pierre Gasly",      "team": "Alpine",        "grid": 10, "time": None,          "gap": "+62.001s",  "points": 1,  "fastest_lap": False},
                {"pos": 11, "driver": "Esteban Ocon",      "team": "Haas",          "grid": 11, "time": None,          "gap": "+1 lap",    "points": 0,  "fastest_lap": False},
                {"pos": 12, "driver": "Alex Albon",        "team": "Williams",      "grid": 12, "time": None,          "gap": "+1 lap",    "points": 0,  "fastest_lap": False},
                {"pos": 13, "driver": "Liam Lawson",       "team": "Racing Bulls",  "grid": 13, "time": None,          "gap": "+1 lap",    "points": 0,  "fastest_lap": False},
                {"pos": 14, "driver": "Fernando Alonso",   "team": "Aston Martin",  "grid": 15, "time": None,          "gap": "+1 lap",    "points": 0,  "fastest_lap": False},
                {"pos": 15, "driver": "Jack Doohan",       "team": "Alpine",        "grid": 16, "time": None,          "gap": "+1 lap",    "points": 0,  "fastest_lap": False},
                {"pos": 16, "driver": "Carlos Sainz Jr.",  "team": "Williams",      "grid": 17, "time": None,          "gap": "+2 laps",   "points": 0,  "fastest_lap": False},
                {"pos": 17, "driver": "Sergio Pérez",      "team": "Cadillac",      "grid": 19, "time": None,          "gap": "+2 laps",   "points": 0,  "fastest_lap": False},
                {"pos": "DNF", "driver": "Oscar Piastri",  "team": "McLaren",       "grid": 22, "time": None,          "gap": "DNF",       "points": 0,  "fastest_lap": False},
                {"pos": "DNF", "driver": "Nico Hülkenberg","team": "Audi",          "grid": 21, "time": None,          "gap": "DNF",       "points": 0,  "fastest_lap": False},
                {"pos": "DNF", "driver": "Isack Hadjar",   "team": "Red Bull",      "grid": 18, "time": None,          "gap": "DNF",       "points": 0,  "fastest_lap": False},
                {"pos": "DNF", "driver": "Valtteri Bottas","team": "Cadillac",      "grid": 20, "time": None,          "gap": "DNF",       "points": 0,  "fastest_lap": False},
                {"pos": "DNF", "driver": "Lance Stroll",   "team": "Aston Martin",  "grid": 14, "time": None,          "gap": "DNF",       "points": 0,  "fastest_lap": False},
            ]
        }
    ],
    "driver_h2h": [
        {"team": "Mercedes",     "d1": "George Russell",    "d2": "Kimi Antonelli",    "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Ferrari",      "d1": "Charles Leclerc",   "d2": "Lewis Hamilton",    "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "McLaren",      "d1": "Lando Norris",      "d2": "Oscar Piastri",     "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Red Bull",     "d1": "Max Verstappen",    "d2": "Isack Hadjar",      "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Haas",         "d1": "Oliver Bearman",    "d2": "Esteban Ocon",      "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Racing Bulls", "d1": "Arvid Lindblad",    "d2": "Liam Lawson",       "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Audi",         "d1": "Gabriel Bortoleto", "d2": "Nico Hülkenberg",   "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Alpine",       "d1": "Pierre Gasly",      "d2": "Jack Doohan",       "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Aston Martin", "d1": "Fernando Alonso",   "d2": "Lance Stroll",      "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Williams",     "d1": "Alex Albon",        "d2": "Carlos Sainz Jr.",  "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
        {"team": "Cadillac",     "d1": "Sergio Pérez",      "d2": "Valtteri Bottas",   "qual_d1": 1, "qual_d2": 0, "race_d1": 1, "race_d2": 0},
    ]
}

REG_CHANGES = [
    {"title": "New Power Units", "detail": "MGU-H removed; MGU-K output jumps to 470 bhp (350 kW). Internal combustion drops to 540 bhp (400 kW). Total still 1,000+ bhp."},
    {"title": "Active Aerodynamics", "detail": "DRS replaced by adjustable front & rear wings with 'overtake mode' usable within 1 second of the car ahead."},
    {"title": "Smaller, Lighter Cars", "detail": "Wheelbase 340 cm (from 360 cm), width 190 cm (from 200 cm), minimum mass reduced by 30 kg."},
    {"title": "Sustainable Fuel", "detail": "All cars must run on 100% sustainable fuel developed specifically for the 2026 regulations."},
    {"title": "New Teams", "detail": "Audi debut as works outfit (ex-Sauber); Cadillac enter as 11th team using Ferrari power units."},
    {"title": "Cost Cap Raised", "detail": "Team operational budget cap rises from $135 M to $215 M. PU manufacturers cap up from $95 M to $130 M."},
    {"title": "Engine Shake-up", "detail": "Ford returns (with Red Bull), Honda goes exclusive to Aston Martin, Alpine switches to Mercedes power."},
]

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/drivers")
def api_drivers():
    return jsonify(DRIVERS_STANDINGS)

@app.route("/api/constructors")
def api_constructors():
    return jsonify(CONSTRUCTORS_STANDINGS)

@app.route("/api/races")
def api_races():
    return jsonify(RACE_RESULTS)

@app.route("/api/calendar")
def api_calendar():
    return jsonify(CALENDAR_2026)

@app.route("/api/regulations")
def api_regulations():
    return jsonify(REG_CHANGES)

@app.route("/api/summary")
def api_summary():
    total_races = len(RACE_RESULTS)
    leaders = [d for d in DRIVERS_STANDINGS if d["points"] > 0]
    constructor_leader = CONSTRUCTORS_STANDINGS[0] if CONSTRUCTORS_STANDINGS else {}
    return jsonify({
        "races_completed": total_races,
        "races_total": 24,
        "driver_leader": DRIVERS_STANDINGS[0] if DRIVERS_STANDINGS else {},
        "constructor_leader": constructor_leader,
        "last_race": RACE_RESULTS[-1] if RACE_RESULTS else {},
        "data_source": "Wikipedia – 2026 Formula One World Championship",
        "last_updated": "March 13, 2026"
    })

@app.route("/api/h2h")
def api_h2h():
    return jsonify(HEAD_TO_HEAD)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
