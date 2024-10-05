from pydantic import BaseModel
import streamlit as st

class BaseView(BaseModel):
  status: str

  def render(self):
    st.write(self.status)

