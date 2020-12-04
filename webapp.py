import streamlit as st 
from PIL import Image
import classify 
import numpy as np
import cv2
from keras.models import model_from_json
import pandas as pd
import SessionState
import os.path
import os
import streamlit as st



session = SessionState.get(loged=False)
# a = st.radio("Edit or show", ['Edit', 'Show'], 0)
# if a == 'Edit':
    # session.code = st.text_input('Edit code', session.code)
# else:
    # st.write(session.code)




abbreviation_dict = {12: 'Neutrophil (segmented)',
                     11: 'Neutrophil (band)',
                     2: 'Eosinophil',
                     0: 'Basophil',
                     8: 'Monocyte',
                     5: 'Lymphocyte (typical)',
                     4: 'Lymphocyte (atypical)',
                     3: 'Smudge Cell',
                     10: 'Myeloblast',
                     14: 'Promyelocyte',
                     9: 'Myelocyte',
                     6: 'Metamyelocyte',
                     7: 'Monoblast',
                     1: 'Erythroblast',
                     13: 'Promyelocyte (bilobed)'};


# np.array()

def login():
  st.title("Login")
  username = st.text_input("user name")
  password = st.text_input("password", type="password")
  if st.button("Login"):
    with open("DataBase.csv","r+") as f:
      myDataList = f.readlines()
      nameList = []
      passlist = []
      for line in myDataList:
        entry = line.split(",")
        if(len(entry) > 1):
          nameList.append(entry[0])
          passlist.append(entry[1])
      if username in nameList:
        if password == passlist[nameList.index(username)]:
          # global loged
          # loged = True
          st.write("Access granted to Predict")
          session.loged = True
          # change(True, 3,'Predict')
          # change(4,True)
        else:
          st.error("Invalid password")
      else:
        st.error("Invalid username") 



def logout():
  session.loged = False

def signup():
  st.title("Create an Account")
  username = st.text_input("username")
  Email = st.text_input("Email")
  password = st.text_input("Enter password", type="password")
    # if st.button("Already a user"):
    #   login() 
  if st.button("Sign Up"):
    with open("DataBase.csv","r+") as f:
      myDataList = f.readlines()
      nameList = []
      for line in myDataList:
        entry = line.split(",")
        nameList.append(entry[0])

      if username not in nameList:
        f.writelines(f'\n{username},{password},{Email}')
        # global loged
        # loged = True
        # change(True, 3,'Predict')
        session.loged = True
        # change_log()
        st.write("Access granted to Predict")
        # change(4,True)
      else:
        st.error("User already present") 




def mainframe():
  st.title("Welcome to Leukemia Cell Detection")
  if st.button("New User?"):
    signup()
  if st.button("Login"):
    login()




def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

def main():
  st.title("Luekemia Cell Detector")
  folder_path = '.\\New folder'
  filename = file_selector(folder_path=folder_path)
  st.write('You selected `%s`' % filename[13:])
  img_u = cv2.imread(filename)
  img = cv2.resize(img_u,(400,400))
  st.image(img, caption='Uploaded Image', use_column_width=True)
  if st.button('predict'):

    st.write("**Predicting the fate of Universe.....**")
    label = classify.predict(img)
    label = label.item()
    res = abbreviation_dict.get(label)
    st.markdown(res)
  # if session.loged == True:
  #   if st.button("Log Out"):
  #     logout()






def change(loged = False, next_clicked = 0, choice = 'Home'):#do chioce = 'Home'
  # create a button in the side bar that will move to the next page/radio button choice
  # next = st.sidebar.button('Next on list')

  # will use this list and next button to increment page, MUST BE in the SAME order
  # as the list passed to the radio button
  
  new_choice = ['Home','Login','New User','Predict','About']

  # This is what makes this work, check directory for a pickled file that contains
  # the index of the page you want displayed, if it exists, then you pick up where the
  #previous run through of your Streamlit Script left off,
  # if it's the first go it's just set to 0
  # if os.path.isfile('next.p'):
  #     next_clicked = pkle.load(open('next.p', 'rb'))
  #     # check if you are at the end of the list of pages
  #     if next_clicked == len(new_choice):
  #         next_clicked = 0 # go back to the beginning i.e. homepage
  # else:
  #     next_clicked = 0 #the start
  # next_clicked = 0
  # this is the second tricky bit, check to see if the person has clicked the
  # next button and increment our index tracker (next_clicked)
  # if next:
  #     #increment value to get to the next page
  #     next_clicked = next_clicked +1

  #     # check if you are at the end of the list of pages again
  #     if next_clicked == len(new_choice):
  #         next_clicked = 0 # go back to the beginning i.e. homepage

  # create your radio button with the index that we loaded
  # if(loged == False):
  # if next_clicked == 0 and loged == False:
  choice = st.sidebar.radio("",('Home','Login','New User','Predict','About'), index=next_clicked)
  # pkle.dump(new_choice.index(choice), open('next.p', 'wb'))


  # pickle the index associated with the value, to keep track if the radio button has been used
  # st.write(loged)

  # finally get to whats on each page
  if choice == 'Home':
    home()
      # st.write('this is home')
  elif choice == 'Login':
    if session.loged == True:
      st.title("Already Logged In")
      if st.button("Log Out"):
        logout()
    else:
      login()
  elif choice == 'New User':
    if session.loged == True:
      st.title("Already Logged In")
      if st.button("Log Out"):
        logout()
    else:
      signup()
  elif choice == 'About':
      About()
  elif choice == 'Predict':
    if(session.loged):
      main()
    else:
      st.title("Register or login to access this page")

#HOME
def home():
  st.write("<h1 style = 'text-align: center;'><u>Home</u></h1>",unsafe_allow_html = True)
  st.text("")
  st.header("What is Leukemia")
  st.write("<body style='text-align: justify;'>Leukemia is cancer that starts in\
  the tissue that forms blood. Most blood cells develop from cells in the\
  bone marrow called stem cells. In a person with leukemia, the bone marrow makes abnormal white blood cells. The \
  abnormal cells are leukemia cells. Unlike normal blood cells, leukemia cells don't die when they should. They may\
  crowd out normal white blood cells, red blood cells, and platelets. This makes it hard for normal blood cells to \
  do their work.</body>",unsafe_allow_html=True)
  
  df = pd.read_csv("HowCommon.csv").set_index('Common Types of Cancer')
  st.text("")
  # st.text("")

  st.header("How Common is this Cancer?")
  st.write("Compared to other cancers, leukemia is fairly common.")
  st.text("")
  # st.dataframe(df)
  # st.table(df.iloc)
  st.table(df) 
  st.text("")
  df1 = pd.read_excel("forBar.xlsx").set_index('Common Types of Cancer')

  # df2 = pd.DataFrame({
    # 'index': ['Cincinnati', 'San Francisco', 'Pittsburgh'],
    # 'sports_teams': [6, 8, 9],
# }).set_index('index')

  # df1.index = df['Common Types of Cancer']
  # st.write(df1.index)
  st.bar_chart(df1)
  st.text("")
  st.write("In 2020, it is estimated that there will be 60,530 new cases of leukemia and an\
  estimated 23,100 people will die of this disease.")
#   # 60530,23100

  # labels = ['Survive','Deaths'] 
  # sizes = [37430,23100] 
  # explode = (0.1,0)
  # plt.pie(sizes,explode = explode, labels = labels, shadow = True)
  # cols = st.beta_columns(4)
  # cols[0].pyplot(plt)
  st.header("Survivability")
  st.write("elative survival is an estimate of the percentage of patients who would be expected to survive the \
    effects of their cancer. It excludes the risk of dying from other causes. Because survival statistics are based\
    on large groups of people, they cannot be used to predict exactly what will happen to an individual patient. No \
    two patients are entirely alike, and treatment and responses to treatment can vary greatly.")
  show = Image.open("stats\\1.PNG")
  st.image(show,use_column_width = True)
  # st.header("")
  # original = Image.open("stats\\"+str(i)+".PNG")
  # st.image(original)
  df3 = pd.read_excel("forBar.xlsx",sheet_name = '02').set_index ('Year')
  # st.write(df3)
  st.subheader("Data over past years")
  st.line_chart(df3)

  # df4 = pd.read_excel("explorer_download.xlsx",sheet_name = 'Sheet3')#.set_index('Common Types of Cancer')
  # st.bar_chart(df4)

  st.subheader("Survival Relative Rate")
  df4 = pd.read_excel("forBar.xlsx",sheet_name = '01').set_index ('Year')
  st.line_chart(df4)
  st.write("SEER 9 5-Year Relative Survival Percent from 1975–2012, All Races, Both Sexes.\
  Modeled trend lines were calculated from the underlying rates using the Joinpoint Survival Model Software.")
  
  st.text("")
  st.text("")
  show = Image.open("stats\\5.PNG")
  st.image(show,use_column_width = True)
  
  st.text("")
  st.text("")
  show = Image.open("stats\\6.PNG")
  st.image(show,use_column_width = True)
  
  st.text("")
  st.text("")
  show = Image.open("stats\\7.PNG")
  st.image(show,use_column_width = True)
  
  st.text("")
  st.text("")
  show = Image.open("stats\\8.PNG")
  st.image(show,use_column_width = True)
  # show = Image.open("stats\\9.PNG")
  # st.image(show,use_column_width = True)
  # show = Image.open("stats\\11.PNG")
  # st.image(show,use_column_width = True)
  # show = Image.open("stats\\12.PNG")
  # st.image(show,use_column_width = True)













def About():
  st.header("About")
  st.subheader("About The Web Application")
  original = Image.open("UsedImages\\Streamlit.png")
  cols = st.beta_columns([1,2])
  cols[0].image(original,use_column_width = True)
  cols[1].markdown("<body style='text-align: justify;'>Streamlit is an open-source app framework for creating beautiful, performant\
    machine learning Web Apps</body>",unsafe_allow_html=True)
  cols[1].markdown("<body style='text-align: justify;'><i>Version : 0.71.0 </i></body>",unsafe_allow_html=True)

  

  st.subheader("About The Authors")
  # st.write("Nikhil Sharma\t")
  # NIKHIL SHARMA
  
  cols = st.beta_columns([1,3])
  cols[0].write("")
  cols[1].write("")
  cols = st.beta_columns([1,3])
  cols[0].write("")



  original = Image.open("Authors\\Sharma01.jpeg")
  cols = st.beta_columns([1,3])
  cols[0].image(original,use_column_width = True)
  cols[1].write("***Nikhil Sharma*** ")
  cols[1].markdown("<body style='text-align: justify;'> Nikhil Sharma is Currently \
    pursuing his Bachelors Degree in Electronics and Computer Engineering from \
    Electronics and Communication Departement, Thapar Institute of Engineering and Technology, Patiala. \
    His active interests include Computer Programming, Machine Learning and Researching in the field of \
    Image Processing and Data Science.</body>",unsafe_allow_html=True)
  # cols[1].markdown("<text style='text-align: justify; color: red;'>Some text</text>", unsafe_allow_html=True)
  # st.markdown("<h1 style='text-align: right; color: red;'>Some title</h1>", unsafe_allow_html=True)

  cols = st.beta_columns([1,3])
  cols[0].write("")
  cols[0].write("")

  # RAJANBIR SINGH GHUMAAN
  original = Image.open("Authors\\Rajan03.jpeg")
  cols = st.beta_columns([1,3])
  cols[0].image(original,use_column_width = True)
  cols[1].write("***Rajanbir Singh Ghumaan*** ")
  cols[1].markdown("<body style='text-align: justify;'> Rajanbir Singh Ghumaan is Currently \
    pursuing his Bachelors Degree in Electronics and Communication Engineering from \
    Electronics and Communication Departement, Thapar Institute of Engineering and Technology, Patiala. His skills and interests \
    include Comuputer Programming, Data Analysis and Research in noise removal algorithms. </body>",unsafe_allow_html=True)

  cols = st.beta_columns([1,3])
  cols[0].write("")
  cols[0].write("")

  # # PRATEEK JEET SINGH SOHI
  original = Image.open("Authors\\Sohi02.jpeg")
  cols = st.beta_columns([1,3])
  cols[0].image(original,use_column_width = True)
  cols[1].write("***Prateek Jeet Singh Sohi*** ")
  cols[1].markdown("<body style='text-align: justify;'> Prateek Jeet Singh Sohi is Currently \
    pursuing his Bachelors Degree in Electronics and Computer Engineering from \
    Electronics and Communication Departement, Thapar Institute of Engineering and Technology, Patiala. \
    His areas of interest are Data Analysis, Content Writing and Research in\
    Image Processing and related fields.</body>",unsafe_allow_html=True)


  cols = st.beta_columns([1,3])
  cols[0].write("")
  cols[0].write("")
  # # PIYUSH SATTI
  original = Image.open("Authors\\Satti03.jpg")
  cols = st.beta_columns([1,3])
  cols[0].image(original,use_column_width = True)
  cols[1].write("***Piyush Satti*** ")
  cols[1].markdown("<body style='text-align: justify;'> Piyush Satti is Currently \
    pursuing his Bachelors Degree in Electronics and Computer Engineering from \
    Electronics and Communication Departement, Thapar Institute of Engineering and Technology, Patiala. \
    His interests include research in Signal Processing, Noise Removal Algorithms and Machine Learning</body>",unsafe_allow_html=True)



  cols = st.beta_columns([1,3])
  cols[0].write("")
  cols[0].write("")
  # # ASST. PROF. BHARAT GARG
  original = Image.open("Authors\\Barat02.png")
  cols = st.beta_columns([1,3])
  cols[0].image(original,use_column_width = True)
  cols[1].write("***Dr. Bharat Garg*** ")
  cols[1].markdown("<body style='text-align: justify;'> Dr. Bharat Garg is working with ECED Department, \
    Thapar Institute of Engineering and Technology, Patiala since 2017. He has completed his PhD degree in \
    VLSI Circuits and Systems from ABV-IIITM Gwalior \
    in September 2017. His research interests include Low Power VLSI Design, Energy Efficient Architectures\
     for Image/Signal Processing and Hardware Security.</body>",unsafe_allow_html=True)
  

change()
