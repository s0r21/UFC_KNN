# KNN Model
from Data_Processing import X_train, X_test, y_train, y_test, real_test_set, export_dataframe
from Packages import *

Model_Accuracy = []

# n_neighbor = 109 with test size of 0.3 (0.564134)
# n_neighbor = 126 with test size of 0.2 (0.572163)

for i in range(1, 100):
     Model = KNeighborsClassifier(n_neighbors=i, algorithm='kd_tree').fit(X_train, y_train.values.ravel())
     Predicting_y = Model.predict(X_test)
     print("We're at #" + str(i))
     Model_Accuracy.append([i,metrics.accuracy_score(y_test, Predicting_y)])

Model_accuracy_df = pd.DataFrame(Model_Accuracy)
Model_accuracy_df = Model_accuracy_df.rename(columns= {0:"N_Neighbor", 1:"Accuracy"})\
    .sort_values(by='Accuracy', ascending=False)

print(Model_accuracy_df.iloc[0])

Official_Model = KNeighborsClassifier(n_neighbors=Model_accuracy_df['N_Neighbor'].iloc[0],
                                      algorithm=Model.algorithm).fit(X_train, y_train.values.ravel())
Official_Model_Prediction = Official_Model.predict(real_test_set)
Official_Model_Prediction = pd.DataFrame(np.transpose(Official_Model_Prediction))
Official_Model_Prediction.columns = ['Predicition']

# Last step is to put the results in a DF with the names of the people in the event.

excel_output = export_dataframe.join(Official_Model_Prediction).dropna()

excel_output.to_excel('C:/Users/t0ys0r/OneDrive/Desktop/UFC Model/Latest_Event.xlsx',
                      sheet_name='Latest Event')

# print(score_array)

# print("Accuracy of model at K=7 is",metrics.accuracy_score(y_test, Predicting_y))
