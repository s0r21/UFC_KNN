# KNN Model
from Data_processing_and_webscrape.Data_Processing import X_train, X_test, y_train, y_test, real_test_set, export_dataframe
from Utils import *
def create_directory(directory_name, file_name):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, directory_name)
    filename = os.path.join(path, file_name)
    if not os.path.exists(path):
        os.mkdir(path)
    return(filename)
def official_model_function():
    Official_Model = KNeighborsClassifier(n_neighbors=Model_accuracy_df['N_Neighbor'].iloc[0],
                                          algorithm=Model.algorithm).fit(X_train, y_train.values.ravel())
    Official_Model_Prediction = Official_Model.predict(real_test_set)
    Official_Model_Prediction = pd.DataFrame(np.transpose(Official_Model_Prediction))
    Official_Model_Prediction.columns = ['Predicition']
    return Official_Model_Prediction
def model_accuracy_function():
    Model_accuracy_df = pd.DataFrame(Model_Accuracy)
    Model_accuracy_df = Model_accuracy_df.rename(columns= {0:"N_Neighbor", 1:"Accuracy"})\
        .sort_values(by='Accuracy', ascending=False)
    return Model_accuracy_df
Model_Accuracy = []

# Building the KNN Model. Iterates through 99 values to see which one provides the highest accuracy.
for i in range(1, 1000):
     Model = KNeighborsClassifier(n_neighbors=i, algorithm='kd_tree', metric='chebyshev').fit(X_train, y_train.values.ravel())
     Predicting_y = Model.predict(X_test)
     print("We're at #" + str(i))
     Model_Accuracy.append([i,metrics.accuracy_score(y_test, Predicting_y)])

# Making the array into a dataframe and sorting the values in DESC order
Model_accuracy_df = model_accuracy_function()

# Prints the n_neighbor with the highest accuracy based on the test set
print(Model_accuracy_df.iloc[0])

# Putting the results in a DF with the names of the people in the event and exporting it to an XLSX file on my computer
excel_output = export_dataframe.join(official_model_function()).dropna()
file_name = create_directory('Output', 'todays_ufc_event.xlsx')
excel_output.to_excel(file_name)