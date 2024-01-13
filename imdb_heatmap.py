import argparse
import logging
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
                        default='Breaking Bad',
                        type=str)
    return parser.parse_args()


def _main():

    logging.basicConfig(
        format='%(levelname)s %(asctime)s %(message)s',
        level=logging.DEBUG,
        datefmt='%Y_%m_%d %I:%M:%S %p'
    )

    # File location defaults
    current_working_dir = os.getcwd()
    data_dir = os.path.join(current_working_dir, "data")
    graphs_dir = os.path.join(current_working_dir, "graphs")
    plwp.init_dirs(data_dir, graphs_dir)

    args = get_args()
    logging.info("Command line argument values: %s", str(args))

    # Dataframe parse
    df = pd.read_csv('data/imdb_breaking_bad.csv', index_col=0)
    # print(df.to_string())

    # Determine heatmap dimensions
    season_episode_num_max = df['season_episode_num'].max()
    logging.info("season_episode_num_max: %d", season_episode_num_max)
    season_num_max = df['season_num'].max()
    logging.info("season_num_max: %d", season_num_max)

    heatmap_data = []
    for i in range(season_episode_num_max):
        current_season_episode_num = i + 1
        logging.info("current_season_episode_num: %d", current_season_episode_num)
        season_df = df[df['season_episode_num'] == current_season_episode_num]
        season_ratings = season_df['rating'].tolist()
        if len(season_ratings) != season_num_max:
            seasons_without_episode = season_num_max - len(season_ratings)
            for j in range(seasons_without_episode):
                season_ratings.insert(0, 0)
                # season_ratings.insert(0,None)
        logging.info("season_ratings: %s", season_ratings)
        heatmap_data.append(season_ratings)
    # print(heatmap_data)

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        text=heatmap_data,
        x=list(range(1, season_num_max)),
        y=list(range(1, season_episode_num_max)),
        colorscale=[[0.000, "rgb(0,0,0)"],
                    [0.699, "rgb(0,0,0)"],
                    [0.699, "rgb(255,0,0)"],
                    [0.700, "rgb(255,0,0)"],
                    [0.700, "rgb(255,109,0)"],
                    [0.800, "rgb(255,109,0)"],
                    [0.800, "rgb(255,255,0)"],
                    [0.900, "rgb(255,255,0)"],
                    [0.900, "rgb(150,200,150)"],
                    [0.950, "rgb(150,200,150)"],
                    [0.950, "rgb(0,225,0)"],
                    [1.000, "rgb(0,225,0)"],
                    ]
    ))

    plwp.default_font(fig)
    plwp.default_template(fig)
    fig.update_xaxes(side="top")
    fig.update_layout(
        title_text=args.title,
        height=750,
        width=750,
    )
    fig['layout']['yaxis']['autorange'] = "reversed"

    # fig.show()
    plwp.save_html(fig, args.title, graphs_dir, auto_open=True)


if __name__ == "__main__":
    _main()
