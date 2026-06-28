import fastf1

# ----------------------------------------
# INITIAL SETUP
# ----------------------------------------

fastf1.Cache.enable_cache("cache")

YEAR = 2026

# Load the season schedule once
schedule = fastf1.get_event_schedule(YEAR)

# ----------------------------------------
# FUNCTIONS
# ----------------------------------------

def show_schedule():
    print("\n" + "=" * 90)
    print(f"FORMULA 1 {YEAR} SEASON SCHEDULE")
    print("=" * 90)

    print(f"{'Round':<8}{'Country':<20}{'Grand Prix':<40}{'Date'}")
    print("-" * 90)

    for _, race in schedule.iterrows():
        print(
            f"{race['RoundNumber']:<8}"
            f"{race['Country']:<20}"
            f"{race['EventName']:<40}"
            f"{race['EventDate'].date()}"
        )


def show_driver_lineup():

    try:
        round_number = int(input("\nEnter Round Number: "))

        event = schedule[schedule["RoundNumber"] == round_number].iloc[0]

    except:
        print("Invalid Round Number!")
        return

    print(f"\nLoading {event['EventName']}...")

    session = fastf1.get_session(
        YEAR,
        event["EventName"],
        "R"          # Race session
    )

    try:
        session.load()
    except Exception as e:
        print("Unable to load session.")
        print(e)
        return

    print("\n" + "=" * 70)
    print(f"{event['EventName']} DRIVER LINEUP")
    print("=" * 70)

    for code in session.drivers:

        driver = session.get_driver(code)

        print(f"\nDriver Name : {driver['BroadcastName']}")
        print(f"Code        : {code}")
        print(f"Number      : {driver['DriverNumber']}")
        print(f"Team        : {driver['TeamName']}")
        print(f"Team Color  : #{driver['TeamColor']}")


# ----------------------------------------
# MENU
# ----------------------------------------

while True:

    print("\n" + "=" * 45)
    print("       FORMULA 1 DATA VIEWER")
    print("=" * 45)
    print("1. View Full Season Schedule")
    print("2. View Driver Lineup")
    print("3. Exit")

    choice = input("\nSelect Option: ")

    if choice == "1":
        show_schedule()

    elif choice == "2":
        show_driver_lineup()

    elif choice == "3":
        print("\nThank you for using Formula 1 Data Viewer!")
        break

    else:
        print("Invalid option! Please try again.")