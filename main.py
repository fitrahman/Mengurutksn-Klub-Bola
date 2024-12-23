import streamlit as st
import matplotlib.pyplot as plt

def recursive_sort(data):
    """Sorts the data by points using recursion (ascending order)."""
    if len(data) <= 1:
        return data
    pivot = data[0]
    less_than_pivot = [x for x in data[1:] if x['points'] <= pivot['points']]
    greater_than_pivot = [x for x in data[1:] if x['points'] > pivot['points']]
    return recursive_sort(less_than_pivot) + [pivot] + recursive_sort(greater_than_pivot)

def iterative_sort(data):
    """Sorts the data by points using iteration (descending order)."""
    n = len(data)
    for i in range(n):
        for j in range(0, n-i-1):
            if data[j]['points'] < data[j+1]['points']:
                data[j], data[j+1] = data[j+1], data[j]
    return data

def calculate_points(won, drawn):
    """Calculate points based on wins and draws."""
    return won * 3 + drawn

def plot_team_pie_chart(team):
    """Plots a pie chart for a team's statistics."""
    labels = ['Won', 'Drawn', 'Lost']
    sizes = [team['won'], team['draw'], team['lost']]
    colors = ['#4CAF50', '#FFC107', '#F44336']
    explode = (0.1, 0, 0)  # Highlight the 'Won' section

    fig, ax = plt.subplots()
    ax.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, explode=explode
    )
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    st.pyplot(fig)

def main():
    st.title("Football League Table Sorting")

    # Input table data
    st.write("Enter team data below:")
    input_data = st.text_area(
        "Input format: Team, Won, Drawn, Lost", 
        "Liverpool,12,3,1\nChelsea,10,5,2\nArsenal,9,6,2"
    )

    if input_data:
        try:
            # Parse input data
            teams = [None]  # Placeholder to start index from 1
            for line in input_data.splitlines():
                parts = line.split(",")
                won = int(parts[1].strip())
                drawn = int(parts[2].strip())
                lost = int(parts[3].strip())
                team_data = {
                    'team': parts[0].strip(),
                    'points': calculate_points(won, drawn),
                    'played': won + drawn + lost,
                    'won': won,
                    'draw': drawn,
                    'lost': lost
                }
                teams.append(team_data)

            # Check if data exceeds 20 teams
            if len(teams) - 1 > 20:
                st.error("Maximum input limit is 20 teams. Please reduce the input data.")
                return

            # Sort order
            order = st.radio("Sort by points in order:", ("Descending", "Ascending"))

            # Sort teams
            if order == "Ascending":
                sorted_teams = recursive_sort(teams[1:])
                # Assign rank in reverse order (higher points -> lower rank number)
                for idx, team in enumerate(sorted_teams, start=1):
                    team['rank'] = len(sorted_teams) - idx + 1
            else:
                sorted_teams = iterative_sort(teams[1:])
                # Assign rank normally
                for idx, team in enumerate(sorted_teams, start=1):
                    team['rank'] = idx

            # Display sorted table
            st.write("### Sorted Table")
            st.table(sorted_teams)

            # Select team for pie chart
            team_names = [team['team'] for team in sorted_teams]
            selected_team_name = st.selectbox("Select a team to display its statistics:", team_names)

            # Find selected team and plot pie chart
            for team in sorted_teams:
                if team['team'] == selected_team_name:
                    st.write(f"### Statistics for {team['team']}")
                    plot_team_pie_chart(team)
                    break

        except Exception as e:
            st.error(f"Error parsing input: {e}")

if __name__ == "__main__":
    main()
