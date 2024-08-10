import json
import os
import pandas as pd
from tqdm import tqdm

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, RepeatVector

import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Load dependent and independent data
dependent_data = pd.read_csv("merged_data_filled.csv")
independent_data = pd.read_csv("sentiment_data.csv")

X = independent_data.drop(columns=['Date'])
y = dependent_data.drop(columns=['Date'])

X = X.astype('float32')
y = y.astype('float32')

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape input data for LSTM model (samples, time steps, features)
X_train = X_train.values.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.values.reshape(X_test.shape[0], X_test.shape[1], 1)

print("Shape of X_train:", X_train.shape)
print("Shape of X_test:", X_test.shape)
print("Shape of y_train:", y_train.shape)
print("Shape of y_test:", y_test.shape)


# Define the LSTM model
model = Sequential([
    LSTM(units=128, input_shape=(X_train.shape[1], 1)),
    RepeatVector(y_train.shape[1]),  # Repeat the LSTM output for each feature in y_train
    LSTM(64, return_sequences=True),  #  number of neurons in the Dense layer
    Dense(1)  # Output layer with one neuron for regression task
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=150, batch_size=32, validation_split=0.1)

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print("Test Loss:", loss)

# Make predictions
predictions = model.predict(X_test)

print("Shape of y_test:", y_test.shape)
print("Shape of predictions:", predictions.shape)


# Calculate error
# Flatten y_test and predictions to 1D arrays
y_test_flat = y_test.to_numpy().flatten()
predictions_flat = predictions.flatten()
y_t2 = y_test.to_numpy()
predictions_2d = np.reshape(predictions, (predictions.shape[0], -1))
predictions_df = pd.DataFrame(predictions_2d, columns=y_test.columns)
actual_df = pd.DataFrame(y_t2, columns=y_test.columns)
# Save DataFrame to a CSV file
predictions_df.to_csv('predicted_data.csv', index=False)
actual_df.to_csv('actual_data.csv', index=False)

# Calculate mean squared error
mse = mean_squared_error(y_test_flat, predictions_flat)
print("Mean Squared Error:", mse)

# Reshape predictions to match the shape of y_test
predictions_reshaped = predictions.squeeze()  # Remove the extra dimension

# Visualize results
plt.figure(figsize=(10, 6))
plt.plot(y_test, label='Actual')
plt.plot(predictions_reshaped, label='Predicted')
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Actual vs Predicted')
plt.legend()
plt.savefig('actual_vs_predicted.png')
# plt.show()

mse_groups = [[] for _ in range(6)]  # List to store mean squared errors for each group
group_size = 438  # Number of features in each group
for i in range(y_test.shape[1]):
    group_index = i % 6  # Calculate cyclic group index
    y_test_group = y_test.iloc[:, i]
    predictions_group = predictions[:, i]
    mse_group = mean_squared_error(y_test_group, predictions_group)
    mse_groups[group_index].append(mse_group)

# Optionally, compute the average of mean squared errors for all groups
avg_mse_groups = [sum(mse_group) / len(mse_group) for mse_group in mse_groups]
avg_mse = sum(avg_mse_groups) / len(avg_mse_groups)
print("Average Mean Squared Error for each cyclic group:", avg_mse_groups)
print("Overall Average Mean Squared Error:", avg_mse)