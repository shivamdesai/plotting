import argparse
import logging
import os
import pandas as pd
import plotly.graph_objects as go
import plotly_wrap as plwp
from plotly.subplots import make_subplots


def get_args():
    parser = argparse.ArgumentParser(
        description="IMDb Heatmap Generator \n python imdb_heatmap.py -t 'IMDb Heatmap SHOW' --loglevel=20")
    parser.add_argument('--title', '-t',
                        help='Figure title',
                        dest='title',
                        default='Figure Title',
                        type=str)
    parser.add_argument('--loglevel',
                        help='Level of logging to output',
                        dest='loglevel',
                        default=logging.INFO,
                        type=int)
    return parser.parse_args()


def _main():

    # Inputs and config
    args = get_args()
    logging.basicConfig(
        format='%(levelname)s %(asctime)s %(message)s',
        level=args.loglevel,
        datefmt='%Y_%m_%d %I:%M:%S %p'
    )
    logging.debug("Command line argument values: %s", str(args))

    # File location defaults
    current_working_dir = os.getcwd()
    data_dir = os.path.join(current_working_dir, "data")
    graphs_dir = os.path.join(current_working_dir, "graphs")
    plwp.init_dirs(data_dir, graphs_dir)

    # Dataframe parse
    df = pd.read_csv('data/imdb_breaking_bad.csv', index_col=0)
    # df = pd.read_csv('data/imdb_tinker.csv', index_col=0)
    # print(df.to_string())
    df_description = df.describe()
    logging.debug("Dataframe description: %s", df_description)

    # Determine heatmap dimensions
    season_episode_num_max = df['season_episode_num'].max()
    logging.info("season_episode_num_max: %d", season_episode_num_max)
    season_num_max = df['season_num'].max()
    logging.info("season_num_max: %d", season_num_max)

    heatmap_data = []
    logging.debug("beginning heatmap data generation")
    for i in range(season_episode_num_max):
        current_season_episode_num = i + 1
        logging.debug("current_season_episode_num: %d", current_season_episode_num)
        season_df = df[df['season_episode_num'] == current_season_episode_num]
        season_ratings = season_df['rating'].tolist()
        if len(season_ratings) != season_num_max:
            seasons_without_episode = season_num_max - len(season_ratings)
            for j in range(seasons_without_episode):
                season_ratings.insert(0, 0)
                # season_ratings.insert(0,None)
        logging.debug("season_ratings: %s", season_ratings)
        heatmap_data.append(season_ratings)
    logging.debug("ending heatmap data generation")
    logging.debug("heatmap data: %s", heatmap_data)
    # print(heatmap_data)

    x_vals = list(range(1, season_num_max + 1))
    y_vals = list(range(1, season_episode_num_max + 1))
    logging.debug("x axis labels: %s", x_vals)
    logging.debug("y axis labels: %s", y_vals)

    fig = go.Figure(data=go.Heatmap(
        x=x_vals,
        y=y_vals,
        z=heatmap_data,
        text=heatmap_data,
        texttemplate="%{text}",
        textfont={"size": 12},
        zmin=0,
        zmax=100,
        colorscale=[
            # 00-50 plotly_dark paper_bgcolor
            # 50-70 Red
            # 70-80 Orange
            # 80-90 Yellow
            # 90-95 Light Green
            # 95-100 Bright Green
            [0.00, "rgb(17,17,17)"],
            [0.60, "rgb(255,0,0)"],
            [0.70, "rgb(255,128,0)"],
            [0.80, "rgb(255,255,0)"],
            [0.90, "rgb(0,255,0)"],
            [1.00, "rgb(0,128,0)"],
        ],
    ))

    plwp.default_font(fig)
    plwp.default_template(fig)
    # TODO - reformat these to have a semblance of conformity
    fig.layout.yaxis.type = 'category'
    fig.update_layout(
        title_text=args.title,
        xaxis_title="Season",
        yaxis_title="Episode",
        height=875,
        width=500,
    )
    fig.update_xaxes(side="top", ticktext=x_vals)
    fig.update_yaxes(ticktext=y_vals)
    fig['layout']['yaxis']['autorange'] = "reversed"

    # fig.show()
    plwp.save_html(fig, args.title, graphs_dir, auto_open=True)


if __name__ == "__main__":
    _main()
