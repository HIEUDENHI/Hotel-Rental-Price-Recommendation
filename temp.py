import numpy as np
import pickle


loaded_model=pickle.load(open("D:/Desktop/Crawl/train_model.sav","rb"))

input_data=(5.3,400.0,1.0,1.0,1.0,14,1.0,1.0,0.0,1.0,1.0,0.0,0.0,0.0,1.0,6.0)

input_data_as_numpy_array=np.asarray(input_data)

input_data_reshaped=input_data_as_numpy_array.reshape(1,-1)

prediction=loaded_model.predict(input_data_reshaped)
print(f"Recommended_price: {prediction}")