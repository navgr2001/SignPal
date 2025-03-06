import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, LabelBinarizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc, f1_score
import joblib
import glob
import os


# Load all data
def load_data():
    dataframes = []
    # Use glob to get all CSV files that match the pattern
    for file in glob.glob("collect_csv/data_*.csv"):
        df = pd.read_csv(file, header=None)
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)

# Pre-process data
def preprocess_data(data):
    data = data.drop_duplicates().dropna()
    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    scaler = MinMaxScaler()
    X = pd.DataFrame(scaler.fit_transform(X))
    return X, y

# Plot metrics
def plot_metrics(y_test, y_pred, y_test_bin, y_pred_proba, class_names, train_acc, test_acc):
    # Confusion Matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.ylabel("Actual")
    plt.xlabel("Predicted")
    plt.show()

    # Classification Report
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # ROC Curve and AUC
    plt.figure(figsize=(10, 7))
    for i, class_name in enumerate(class_names):
        fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_pred_proba[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{class_name} (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend()
    plt.grid()
    plt.show()

    # Accuracy Chart
    plt.figure(figsize=(10, 5))
    epochs = range(1, len(train_acc) + 1)
    plt.plot(epochs, train_acc, label="Training Accuracy", marker="o")
    plt.plot(epochs, test_acc, label="Testing Accuracy", marker="o")
    plt.title("Training and Testing Accuracy over Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid()
    plt.show()

# Train the model with hyperparameter tuning
def train_model(X, y):
    y = y.astype(str)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    # Best model from GridSearchCV
    best_model = grid_search.best_estimator_
    print(f"Best Parameters: {grid_search.best_params_}")

    # Accuracy tracking
    train_acc = []
    test_acc = []


    # Simulate epochs for RandomForest (not inherently epoch-based)
    for _ in range(10):  # Simulate 10 training iterations
        best_model.fit(X_train, y_train)
        train_acc.append(accuracy_score(y_train, best_model.predict(X_train)))
        test_acc.append(accuracy_score(y_test, best_model.predict(X_test)))

    # Final prediction and probability for ROC
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)

    # Accuracy and F1 Score
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average="weighted")
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print(f"F1 Score: {f1:.2f}")

    # Prepare for ROC curve (binarize labels)
    lb = LabelBinarizer()
    y_test_bin = lb.fit_transform(y_test)
    class_names = lb.classes_

    # Save the trained model
    joblib.dump(best_model, 'sign_language_model.pkl')
    print("Model trained and saved as 'sign_language_model.pkl'.")

    # Plot metrics: confusion matrix, ROC, and accuracy chart
    plot_metrics(y_test, y_pred, y_test_bin, y_pred_proba, class_names, train_acc, test_acc)

if __name__ == '__main__':
    # Load raw data
    data = load_data()

    # Pre-process the data
    X, y = preprocess_data(data)

    # Train the model with preprocessed data
    train_model(X, y)
