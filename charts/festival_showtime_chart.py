import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


class FestivalShowTimeChart:
    def __init__(self, show_data):
        # Convert show data to a DataFrame for Gantt chart
        df = pd.DataFrame(show_data, columns=['Show', 'Start', 'Finish', 'Stage'])

        # Group shows by stage
        grouped_shows = df.groupby('Stage')

        # Create a figure and axes
        self.fig, ax = plt.subplots(figsize=(20, 0.5 * (len(grouped_shows) + 1)))

        # Plot the Gantt chart
        for i, (_, group) in enumerate(grouped_shows):
            for _, row in group.iterrows():
                start_time = datetime.strptime(row['Start'], '%I:%M %p').time()
                end_time = datetime.strptime(row['Finish'], '%I:%M %p').time()

                dummy_date = datetime.today().date()

                if start_time.strftime('%p') == 'AM':
                    tomorrow_date = datetime.today().date() + timedelta(days=1)
                    start = datetime.combine(tomorrow_date, start_time)
                else:
                    start = datetime.combine(dummy_date, start_time)

                if end_time.strftime('%p') == 'AM':
                    tomorrow_date = datetime.today().date() + timedelta(days=1)
                    end = datetime.combine(tomorrow_date, end_time)
                else:
                    end = datetime.combine(dummy_date, end_time)

                midpoint = start + (end - start) / 2
                bar_width = (end - start).total_seconds() / 60  # Width in minutes

                ax.barh(i, bar_width, left=start, height=1, align='center', color='blue', alpha=0.8)

                #ax.barh(i, end - start, left=start, height=1, align='center', color='blue', alpha=0.8)
                ax.text(midpoint, i, row['Show'], ha='center', va='center', color='white')

        # Configure the chart layout
        ax.set_xlim(datetime.combine(dummy_date, datetime.strptime('07:00 PM', '%I:%M %p').time()),
                    datetime.combine(dummy_date + timedelta(days=1), datetime.strptime('05:30 AM', '%I:%M %p').time()))
        ax.set_ylim(-0.5, len(grouped_shows) - 0.5)
        ax.set_xlabel('Time')
        ax.set_yticks(range(len(grouped_shows)))
        ax.set_yticklabels(grouped_shows.groups.keys())
        ax.set_title('Show Schedule')

        # Add stage labels for rows
        ax2 = ax.twinx()
        ax2.set_ylim(ax.get_ylim())
        ax2.set_yticks(range(len(grouped_shows)))
        ax2.set_yticklabels(grouped_shows.groups.keys())
        ax2.tick_params(left=False, labelleft=True, right=False, labelright=False)

        # Add time intervals at the bottom
        start_time = datetime.strptime('07:00 PM', '%I:%M %p').time()
        end_time = datetime.strptime('05:30 AM', '%I:%M %p').time()
        time_intervals = pd.date_range(datetime.combine(dummy_date, start_time),
                                       datetime.combine(dummy_date + timedelta(days=1), end_time),
                                       freq='30min')
        time_labels = [t.strftime('%I:%M %p') for t in time_intervals]
        ax.set_xticks(time_intervals)
        ax.set_xticklabels(time_labels, rotation=45, ha='right')
        ax.margins(x=0.2)

        # Remove spines and ticks
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(left=False, labelleft=False, bottom=False)
