import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

fastf1.Cache.enable_cache('cache')

#==========================================Track Database=========================================
TRACKS = {
    1: {"country": "Australia", "city": "Melbourne", "name": "Albert Park"},
    2: {"country": "China", "city": "Shanghai", "name": "Shanghai International Circuit"},
    3: {"country": "Japan", "city": "Suzuka", "name": "Suzuka"},
    4: {"country": "Miami", "city": "USA", "name": "Miami International Autodrome"},
    5: {"country": "Canada", "city": "Montreal", "name": "Circuit Gilles Villeneuve"},
    6: {"country": "Monaco", "city": "Monaco", "name": "Monaco"},
    7: {"country": "Spain", "city": "Barcelona", "name": "Circuit de Catalunya"},
    8: {"country": "Austria", "city": "Spielberg", "name": "Red Bull Ring"},
    9: {"country": "Great Britain", "city": "Silverstone", "name": "Silverstone"},
    10: {"country": "Belgium", "city": "Spa-Francorchamps", "name": "Spa-Francorchamps"},
    11: {"country": "Hungary", "city": "Budapest", "name": "Hungaroring"},
    12: {"country": "Netherlands", "city": "Zandvoort", "name": "Zandvoort"},
    13: {"country": "Italy", "city": "Monza", "name": "Monza"},
    14: {"country": "Spain", "city": "Madrid", "name": "Madring"},
    15: {"country": "Azerbaijan", "city": "Baku", "name": "Baku"},
    16: {"country": "Singapore", "city": "Singapore", "name": "Singapore"},
    17: {"country": "USA", "city": "Austin", "name": "Circuit of the Americas"},
    18: {"country": "Mexico", "city": "Mexico City", "name": "Mexico City"},
    19: {"country": "Brazil", "city": "São Paulo", "name": "Interlagos"},
    20: {"country": "USA", "city": "Las Vegas", "name": "Las Vegas Strip Circuit"},
    21: {"country": "Qatar", "city": "Lusail", "name": "Lusail"},
    22: {"country": "Abu Dhabi", "city": "Yas Marina", "name": "Yas Marina"}
}

#==========================================Menu Functions=========================================
def display_track_menu():
    print("\n" + "=" * 60)
    print("SELECT A TRACK")
    print("=" * 60)
    for num, track in TRACKS.items():
        print(f"{num:>2}. {track['country']:<15} - {track['city']:<15} ({track['name']})")
    print("=" * 60)

def get_year():
    while True:
        try:
            year = int(input("\nEnter year (e.g., 2024): "))
            if 2018 <= year <= 2030:
                return year
            print("Please enter a valid year (2018-2030)")
        except ValueError:
            print("Please enter a valid number")

def get_track_selection():
    display_track_menu()
    while True:
        try:
            choice = int(input("\nEnter track number (1-22): "))
            if 1 <= choice <= 22:
                return TRACKS[choice]
            print("Please enter a number between 1 and 22")
        except ValueError:
            print("Please enter a valid number")

#==========================================Main Program=========================================
def main():
    print("\n" + "=" * 60)
    print("F1 QUALIFYING SESSION TRACK VISUALIZATION")
    print("=" * 60)
    
    year = get_year()
    track = get_track_selection()
    
    print(f"\nLoading: {year} {track['country']} GP - Qualifying Session")
    print("This may take a moment...")
    
    # Load Qualifying session ('Q')
    session = fastf1.get_session(year, track['country'], 'Q')
    session.load()
    
    laps = session.laps
    print(f"\nTotal laps recorded in session: {len(laps)}\n")
    print("=" * 60)
    print(f"{'Driver':<8} {'Team':<15} {'Fastest Lap':<12} {'Lap #':<6}")
    print("=" * 60)
    
    all_drivers = laps['Driver'].unique()
    fig, ax = plt.subplots(figsize=(12, 9))
    cmap = plt.get_cmap('tab20')
    
    legend_entries = []
    
    for i, driver_code in enumerate(all_drivers):
        driver_laps = laps.pick_driver(driver_code)
        
        if driver_laps.empty:
            continue
        fastest_lap = driver_laps.pick_fastest()
        
        if fastest_lap is None or pd.isna(fastest_lap.get('LapTime')):
            print(f"{driver_code:<8} {'---':<15} {'No valid lap':<12} {'---':<6}")
            continue
        
        driver_info = session.get_driver(driver_code)
        team_name = driver_info.get('TeamName', 'Unknown')
        team_color = driver_info.get('TeamColor', None)
        
        if team_color and isinstance(team_color, str) and team_color != '':
            color = f"#{team_color}"
        else:
            color = cmap(i / len(all_drivers))
        
        lap_time_str = str(fastest_lap['LapTime'])
        lap_number = fastest_lap.get('LapNumber', '?')
        print(f"{driver_code:<8} {team_name:<15} {lap_time_str:<12} {lap_number:<6}")
        
        telemetry = fastest_lap.get_telemetry()
        if telemetry.empty:
            continue
        
        line, = ax.plot(telemetry['X'], telemetry['Y'],
                        color=color,
                        linewidth=1.5,
                        alpha=0.85,
                        label=f"{driver_code} ({lap_time_str})")
        legend_entries.append(line)
    
    print("=" * 60)
    
    ax.set_aspect('equal')
    ax.set_title(f"All Drivers' Fastest Laps - {year} {track['country']} GP Qualifying",
                 fontsize=14, fontweight='bold')
    ax.axis('off')
    
    if legend_entries:
        sorted_pairs = sorted(
            zip(legend_entries, [e.get_label() for e in legend_entries]),
            key=lambda p: p[1].split('(')[-1].rstrip(')')
        )
        ax.legend(
            handles=[p[0] for p in sorted_pairs],
            labels=[p[1] for p in sorted_pairs],
            loc='best',
            fontsize=8,
            framealpha=0.9,
            title="Driver (Fastest Lap)",
            title_fontsize=10
        )
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()