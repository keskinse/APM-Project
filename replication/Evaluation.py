import numpy as np
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import cross_val_score

# Confusion matrix
def generate_confusion_matrix(y_true, y_pred, classes, use_case, pattern):
    
    # Creating the heatmap
    cm = confusion_matrix(y_true, y_pred)
    fig = go.Figure(data = go.Heatmap(z = cm, colorscale = 'Blues'))
    
    # Adding labels and formatting to the figure
    fig.update_layout(title = f'Confusion Matrix - {use_case} - {pattern}:',
                      xaxis = dict(title = 'Predicted Label', ticktext = classes, tickvals = np.arange(len(classes))),
                      yaxis = dict(title = 'True Label', ticktext = classes, tickvals = np.arange(len(classes))),
                      coloraxis_colorbar = dict(title = 'Counts'))
    
    # Saving figure into image folder
    save_path = f'images/ConfusionMatrix-{use_case}-{pattern}.png'
    fig.write_image(save_path)