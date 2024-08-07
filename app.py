import numpy as np
import pickle
import streamlit as st

loaded_model=pickle.load(open("D:/Desktop/Crawl/train_model.sav","rb"))

def price_recommend(input_data):

    input_data_as_numpy_array=np.asarray(input_data)

    input_data_reshaped=input_data_as_numpy_array.reshape(1,-1)

    prediction=loaded_model.predict(input_data_reshaped)
    return prediction

def main():
    st.title("Price Recommendation Web App on Booking.Com")
    distance_from_center = st.text_input("Distance from City Center (in km)")
    number_of_guests = st.text_input("Number of Guests")  # Text input for guest count
    number_of_bedrooms = st.text_input("Number of Bedrooms")
    room_size = st.text_input("Size of Room (in m)")
    sea_view = st.checkbox("Sea View") 
    mountain_view = st.checkbox("Mountain View ")
    city_view = st.checkbox("City View (Optional)")
    private_bathroom = st.checkbox("Private Bathroom")
    private_pool = st.checkbox("Private Pool")
    rooftop_pool = st.checkbox("Rooftop Pool")
    minibar = st.checkbox("Minibar")
    barbecue = st.checkbox("Barbecue")
    soundproofing = st.checkbox("Soundproofing")
    sauna = st.checkbox("Sauna")
    spa_bath = st.checkbox("Spa Bath")
    garden_view = st.checkbox("Garden View")
    
    
    distance_from_center = float(distance_from_center)
    number_of_guests = int(number_of_guests)
    number_of_bedrooms = float(number_of_bedrooms)
    room_size = float(room_size)
    sea_view = 1 if sea_view else 0
    mountain_view = 1 if mountain_view else 0
    city_view = 1 if city_view else 0
    private_bathroom = 1 if private_bathroom else 0
    private_pool = 1 if private_pool else 0
    rooftop_pool = 1 if rooftop_pool else 0
    minibar = 1 if minibar else 0
    barbecue = 1 if barbecue else 0
    soundproofing = 1 if soundproofing else 0
    sauna = 1 if sauna else 0
    spa_bath = 1 if spa_bath else 0
    garden_view = 1 if garden_view else 0
    
    result=0
    
    if st.button("Recommended Price: "):
        result=price_recommend([distance_from_center,room_size,sea_view,mountain_view,
            city_view,number_of_guests,private_bathroom,private_pool,rooftop_pool,
            minibar,barbecue,soundproofing,sauna,spa_bath,garden_view,number_of_bedrooms])
        
        
        
    st.success(result)
    
if __name__ == '__main__':
    main()