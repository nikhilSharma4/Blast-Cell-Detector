mkdir -p ~/.matplotlib/
mkdir -p ~/.keras/
mkdir -p ~/.streamlit/
echo "\
[general]\n\
email = \"ghumaan1999@gmail.com\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
