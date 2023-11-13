import argparse
import datetime
import os
import pandas as pd
import plotly.graph_objects as go
import plotly_wrap as plwp
from plotly.subplots import make_subplots


def get_args():
    parser = argparse.ArgumentParser(
        description='Asset Visualization Generation')
    parser.add_argument('--title', '-t',
                        help='Graph title',
                        dest='title',
                        default='Assets',
                        type=str)
    return parser.parse_args()


def _main():

    # File location defaults
    current_working_dir = os.getcwd()
    data_dir = os.path.join(current_working_dir, "data")
    graphs_dir = os.path.join(current_working_dir, "graphs")
    plwp.init_dirs(data_dir, graphs_dir)

    # Output file timestamp
    dt_now = datetime.datetime.now()
    file_prefix = dt_now.strftime("%Y_%m_%d_%H%M%S_")

    args = get_args()
    print("\n Command line argument values: " + str(args) + "\n")

    # Dataframe parse
    df = pd.read_csv('assets.csv')
    print(df.to_string())

    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=(
            "Plot 1",
            "Plot 2",
            "Plot 3",
            "Plot 4"
        ),
        specs=[
            [{"type": "domain"}, {"type": "domain"}],
            [{"type": "domain"}, {"type": "domain"}]
        ],
    )

    fig.add_trace(
        go.Pie(
            labels=df['Asset'],
            values=df['Value'],
            textinfo='label+percent',
            hovertemplate="<br>".join([
                "Asset: %{label}",
                "Value: $%{value}",
            ]),
            name="",  # Stops 'trace0' from showing up on popup annotation
            legendgroup='asset',
            legendgrouptitle=dict(text='Asset'),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Pie(
            labels=df['Class'],
            values=df['Value'],
            textinfo='label+percent',
            hovertemplate="<br>".join([
                "Class: {label}",
                "Value: $%{value}",
            ]),
            name="",  # Stops 'trace0' from showing up on popup annotation
            legendgroup='class',
            legendgrouptitle=dict(text='Class'),
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Pie(
            labels=df['Resource'],
            values=df['Value'],
            textinfo='label+percent',
            hovertemplate="<br>".join([
                "Resource: {label}",
                "Value: $%{value}",
            ]),
            name="",  # Stops 'trace0' from showing up on popup annotation
            legendgroup='resource',
            legendgrouptitle=dict(text='Resource'),
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        title_text=args.title,
    )

    plwp.default(fig)
    plwp.save_html(fig, file_prefix + args.title, graphs_dir, auto_open=True)


if __name__ == "__main__":
    _main()
