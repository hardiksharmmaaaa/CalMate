import streamlit as st

page_bg_floating = '''
<style>
@keyframes floatUpDown {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}

.floating-element {
    position: absolute;
    top: 20%;
    left: 30%;
    width: 100px;
    height: 100px;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    animation: floatUpDown 5s ease-in-out infinite;
}

.floating-element-2 {
    position: absolute;
    top: 60%;
    left: 70%;
    width: 150px;
    height: 150px;
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    animation: floatUpDown 8s ease-in-out infinite;
}
</style>

<div class="floating-element"></div>
<div class="floating-element-2"></div>
'''

st.markdown(page_bg_floating, unsafe_allow_html=True)


page_bg_gradient = '''
<style>
@keyframes moveGradient {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(270deg, #ff9a9e, #fad0c4, #fad0c4, #ff9a9e);
    background-size: 800% 800%;
    animation: moveGradient 12s ease infinite;
}
</style>
'''

st.markdown(page_bg_gradient, unsafe_allow_html=True)
