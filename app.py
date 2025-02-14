import numpy as np
import pickle
import streamlit as st

# Nạp mô hình đã được huấn luyện (đảm bảo đường dẫn đúng)
loaded_model = pickle.load(open("/Users/macbook/Desktop/Crawl/train_model.sav", "rb"))

def price_recommend(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return prediction

def main():
    st.title("Price Recommendation Web App on Booking.Com")

    distance_from_center = st.text_input("Distance from City Center (in km)")
    number_of_guests = st.text_input("Number of Guests")
    number_of_bedrooms = st.text_input("Number of Bedrooms")
    room_size = st.text_input("Size of Room (in m)")

    sea_view = st.checkbox("Sea View")
    mountain_view = st.checkbox("Mountain View")
    city_view = st.checkbox("City View")
    private_bathroom = st.checkbox("Private Bathroom")
    private_pool = st.checkbox("Private Pool")
    rooftop_pool = st.checkbox("Rooftop Pool")
    minibar = st.checkbox("Minibar")
    barbecue = st.checkbox("Barbecue")
    soundproofing = st.checkbox("Soundproofing")
    sauna = st.checkbox("Sauna")
    spa_bath = st.checkbox("Spa Bath")
    garden_view = st.checkbox("Garden View")
    
    if distance_from_center and number_of_guests and number_of_bedrooms and room_size:
        try:
            distance_val = float(distance_from_center)
            guests_val = int(number_of_guests)
            bedrooms_val = float(number_of_bedrooms)
            room_size_val = float(room_size)
        except Exception as e:
            st.error("Vui lòng nhập đúng định dạng số!")
            return

        input_features = [
            distance_val,
            room_size_val,
            1 if sea_view else 0,
            1 if mountain_view else 0,
            1 if city_view else 0,
            guests_val,
            1 if private_bathroom else 0,
            1 if private_pool else 0,
            1 if rooftop_pool else 0,
            1 if minibar else 0,
            1 if barbecue else 0,
            1 if soundproofing else 0,
            1 if sauna else 0,
            1 if spa_bath else 0,
            1 if garden_view else 0,
            bedrooms_val
        ]

        if st.button("Recommended Price"):
            result = price_recommend(input_features)
            st.success(f"Recommended Price: {result[0]}")
    else:
        st.info("Vui lòng nhập đầy đủ thông tin.")

if __name__ == '__main__':
    main()
