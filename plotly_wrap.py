import datetime
import os


# Standardized defaults for figure sizing
FIG_HEIGHT = 810
FIG_WIDTH = 1440

# Standardized defaults for alignment anchors
DEFAULT_ALIGNMENT = "left"
DEFAULT_XREF = "paper"
DEFAULT_YREF = "paper"

# Standardized defaults for fonts
PLOTLY_FONTS = dict(
    family="Arial",
    size=18,
    color="#7f7f7f",
)

# Standardized defaults templare
PLOTLY_TEMPLATE = "plotly_dark"


def init_dirs(data_dir, graphs_dir):
    # Create directories if nonexistant
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    if not os.path.exists(graphs_dir):
        os.mkdir(graphs_dir)


def default_font(fig):
    # Apply default fonts to figure
    fig.update_layout(
        font=PLOTLY_FONTS,
    )


def default_template(fig):
    # Apply default template to figure
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
    )


def default_size(fig):
    # Apply default size to figure
    fig.update_layout(
        height=FIG_HEIGHT,
        width=FIG_WIDTH,
    )


def default(fig):
    default_font(fig)
    default_template(fig)
    default_size(fig)


def annotate(
    fig,
    annotation,
    align=DEFAULT_ALIGNMENT,
    xref=DEFAULT_XREF,
    yref=DEFAULT_YREF,
    x=0,
    y=0.96875,
    showarrow=False,
):
    # Apply text annotation using default alignment and location
    fig.add_annotation(
        text=annotation,
        align=align,
        xref=xref,
        yref=yref,
        x=x,
        y=y,
        showarrow=showarrow,
    )


def save_html(fig, title, graphs_dir, auto_open=True):
    # Save figure to graphs directory with title as filename
    dt_now = datetime.datetime.now()
    file_prefix = dt_now.strftime("%Y_%m_%d_%H%M%S_")
    filename = file_prefix + title.strip().replace(" ", "_") + ".html"
    filepath = os.path.join(graphs_dir, filename)
    fig.write_html(filepath, auto_open=auto_open)
