import datetime
import streamlit as st
import extra_streamlit_components as stx
import time
st.write("# Cookie Manager")

#@st.fragment
def get_manager():
    return stx.CookieManager()

cookie_manager = get_manager()


def retry_until(max_elapsed_time=5, dt=0.01):
    total_elapsed_time = 0.
    values = cookie_manager.get_all(key='retry')
    while (values is None) and (total_elapsed_time < max_elapsed_time):
        total_elapsed_time+=dt
        time.sleep(dt)
    return total_elapsed_time

st.subheader("All Cookies:")
cookies = cookie_manager.get_all()
st.write(cookies)

c1, c2, c3 = st.columns(3)
    

with c1:
    st.subheader("Get Cookie:")
    cookie = st.text_input("Cookie", key="0")
    clicked = st.button("Get")
    if clicked:
        elapsed = retry_until()
        value = cookie_manager.get(cookie=cookie)
        st.write(value)
        st.markdown(elapsed)
        print(elapsed)
        
with c2:
    st.subheader("Set Cookie:")
    cookie = st.text_input("Cookie", key="1")
    val = st.text_input("Value")
    if st.button("Add"):
        cookie_manager.set(cookie, val) # Expires in a day by default
        elapsed = retry_until()
        st.write(f"Cookie set! Time taken: {elapsed} seconds")
        print(elapsed)
    
with c3:
    st.subheader("Delete Cookie:")
    cookie = st.text_input("Cookie", key="2")
    dt = 0.
    if st.button("Delete"):
        cookie_manager.delete(cookie)
        elapsed = retry_until()
        st.write(f"Cookie deleted! Time taken: {elapsed} seconds")
        print(elapsed)
