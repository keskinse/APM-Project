import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.model_selection import cross_val_score

# Confusion Matrix
def generate_confusion_matrix(y_true, y_pred, save_path):
    cm = confusion_matrix(y_true, y_pred)
    
    # Plotting the confusion matrix as a heatmap
    plt.imshow(cm, cmap = plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.xticks(np.arange(len(classes)), classes)
    plt.yticks(np.arange(len(classes)), classes)
    plt.colorbar()
    
    # Saving the plot as an image
    plt.savefig(save_path)
    plt.close()
    
# ROC Curve
def generate_roc_curve(y_true, y_score, save_path):
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    
    # Plot the ROC curve
    plt.plot(fpr, tpr, label = 'ROC curve (AUC = {:.2f})'.format(roc_auc))
    plt.title('Receiver Operating Characterstic (ROC)')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc = 'lower right')
    
    # Save the plot as an image
    plt.savefig(save_path)
    plt.close()
    
# Performing Cross Validation
def perform_cross_validation(clf, X, y, cv, scoring):
    score = cross_val_score(clf, X, y, cv = cv, scoring = scoring)
    print('Cross-Validation Scores: ', scores)
