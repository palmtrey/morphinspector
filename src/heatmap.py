import os
import pandas
import plotly.express as px
from tqdm import tqdm

def get_distances_from_df(df: pandas.DataFrame) -> list[float]:
  '''Gets sorted distances from a NearFace dump dataframe.

  Sorts a given dataframe by morph, and then returns a list of
  float distance values in that order. NearFace dump files are
  automatically sorted by descending distance - this won't work
  for a heatmap. Sorting these distances by morph allows the
  distances to be matched up exactly when potting.

  Args:
    df: pandas DataFrame containing NearFace dump data (can be
      either cosine or L2 metric data).
  '''

  df.sort_values(by='identity', inplace=True)

  if 'VGG-Face_cosine' in df.columns:
    return df['VGG-Face_cosine'].tolist()
  elif 'VGG-Face_euclidean_l2' in df.columns:
    return df['VGG-Face_euclidean_l2'].tolist()
  else:
    return None


def plot_heatmap(cosine_dir: str, l2_dir: str) -> None:
  '''Plots a heatmap of cosine distances versus L2 distances.

  Uses plotly.express to plot a heatmap of a morph dataset given
  NearFace dump directories for the dataset's cosine and l2
  folders. NearFace backend must be VGG-Face.

  Args:
    cosine_dir: path to a directory containg NearFace dump csv
      files using the cosine distance metric.
    l2_dir: path to a directory containing NearFace dump csv
      files using the Euclidean L2 distance metric.
  '''
  # df = px.data.tips()
  x = []
  y = []
  for cosine_morph in tqdm(os.listdir(cosine_dir)):
    with open(cosine_dir + '/' + cosine_morph) as f:
      df = pandas.read_csv(f, delimiter='\t')
      x += get_distances_from_df(df)

  for l2_morph in tqdm(os.listdir(l2_dir)):
    with open(l2_dir + '/' + l2_morph) as f:
      df = pandas.read_csv(f, delimiter='\t')
      y += get_distances_from_df(df)

  df = pandas.DataFrame()
  df['x'] = x
  df['y'] = y

  fig = px.density_contour(df, x='x', y='y')
  fig.update_traces(contours_coloring="fill", contours_showlabels=True)
  fig.show()


if __name__ == '__main__':
  plot_heatmap('../data/nearface_out/morphs/clarkson_morphs_cosine', '../data/nearface_out/morphs/clarkson_morphs_l2')
  # with open('../data/nearface_out/morphs/clarkson_morphs_cosine/00_0-01_0.png.csv') as f:
  #   df = pandas.read_csv(f, delimiter='\t')
  #   l = get_distances_from_df(df)
  #   print(l)

