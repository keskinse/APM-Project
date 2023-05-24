import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import cross_val_score

# Confusion matrix
def generate_confusion_matrix(y_true, y_pred, classes, use_case, pattern):
    
    # Creating the confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Convert classes to list
    classes = classes.tolist()
    
    # Create annotations
    z_text = [[str(value) for value in row] for row in cm]
    
    # Set up figure
    fig = ff.create_annotated_heatmap(
        cm,
        x = classes,
        y = classes,
        annotation_text = z_text,
        colorscale = 'Viridis'
    )
    
    # Add title
    fig.update_layout(
        title = '<i><b>Confusion Matrix - {} - {}</b></i>'.format(use_case, pattern),
        xaxis = dict(title = 'Predicted Labels', ticktext = classes, tickvals = np.arange(len(classes))),
        yaxis = dict(title = 'True Labels', ticktext = classes, tickvals = np.arange(len(classes)), autorange='reversed')
        )
    
    # Adding custom xaxis title
    fig.add_annotation(
        dict(
            font = dict(color = "black", size = 14),
            x = 0.5,
            y = -0.15,
            showarrow = False,
            text = "Predicted value",
            xref = "paper",
            yref = "paper"
        )
    )
    
    # Adjust margins to make room for yaxis title
    fig.update_layout(margin = dict(t = 50, l = 200))
    
    # Save the figure as an image
    save_path = f'images/ConfusionMatrix-{use_case}-{pattern}.png'
    fig.write_image(save_path)
    
# Roc Curve
def generate_roc_curve(y_true, y_score, use_case, pattern):
    
    fpr, tpr, threshould = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    # Creting a scatter plot for the ROC Curve
    fig = go.Figure(data = go.Scatter(
        x = fpr,
        y = tpr,
        mode = 'lines',
        name = f'ROC Curve (AUC = {roc_auc:.2f})'
    ))
    
    # Adding labels and formatting to the figure
    fig.update_layout(title = f'Receiver Operating Characteristic (ROC) - {use_case} - {pattern}',
                      xaxis = dict(title = 'False Positive Rate'),
                      yaxis = dict(title = 'True Positive Rate'),
                      legend = dict(x = .5, y = .5, orientation = 'h'))
    
    # Saving figure
    fig.write_image(f'images/ROC-Curve-{use_case}-{pattern}.png')