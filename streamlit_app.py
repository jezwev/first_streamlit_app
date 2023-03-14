import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents healthly diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#add a pick list
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruit:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

#createa function
def get_fruityvice_data(fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # Normalize semi-structured JSON data into a flat table.
    return pandas.json_normalize(fruityvice_response.json())



#user input for fruit

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get some info")
    else:    
        # Display in streamlit table strucutre
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()

#dont run past here
#streamlit.stop()


streamlit.header("The fruit load list contains:")
def get_fruit_load_list(my_cnx):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()


#add a button
if streamlit.button('Get fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list(my_cnx)
    streamlit.dataframe(my_data_row)

#allow end user to add fruit to list
def insert_row(new_fruit):
     with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('fromstreamlit')")
        return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?','')
streamlit.text('The user entered '+ insert_row(add_my_fruit))