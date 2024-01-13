import argparse
import os
import pandas as pd
import plotly.graph_objects as go
import plotly_wrap as plwp
from plotly.subplots import make_subplots


def get_args():
    parser = argparse.ArgumentParser(
        description='IMDb Heatmap Generator')
    parser.add_argument('--title', '-t',
                        help='Graph title',
                        dest='title',
                        default='SHOW',
                        type=str)
    return parser.parse_args()


def _main():

    # File location defaults
    current_working_dir = os.getcwd()
    data_dir = os.path.join(current_working_dir, "data")
    graphs_dir = os.path.join(current_working_dir, "graphs")
    plwp.init_dirs(data_dir, graphs_dir)

    args = get_args()
    print("\n Command line argument values: " + str(args) + "\n")

    # Dataframe parse
    df = pd.read_csv('data/imdb_breaking_bad.csv')
    print(df.to_string())

    fig = go.Figure(data=go.Heatmap(
        z=[
            [1, 20, 30],
            [20, 1, 60],
            [30, 60, 1],
        ],
    ))

    fig.update_layout(
        title_text=args.title,
    )

    plwp.default(fig)

    # fig.show()
    plwp.save_html(fig, args.title, graphs_dir, auto_open=True)


if __name__ == "__main__":
    _main()
