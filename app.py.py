import json
from pathlib import Path
import streamlit as st

TASKS_FILE = Path(__file__).with_name("my_routine.json")
DEFAULT_TASKS = ["Wake up early", "Freshen up", "Gym", "Breakfast", "Coding"]

def load_tasks():
    if not TASKS_FILE.exists():
        return DEFAULT_TASKS.copy()
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        return tasks if isinstance(tasks, list) else DEFAULT_TASKS.copy()
    except (json.JSONDecodeError, OSError):
        return DEFAULT_TASKS.copy()

def save_tasks(tasks):
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)

st.set_page_config(page_title="Personal Task Manager", page_icon="✅")
st.title("✅ Personal Task Manager")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

with st.form("add_task", clear_on_submit=True):
    new_task = st.text_input("Add a task")
    submitted = st.form_submit_button("Add task")
    if submitted:
        task = new_task.strip()
        if task:
            st.session_state.tasks.append(task)
            save_tasks(st.session_state.tasks)
            st.rerun()
        else:
            st.warning("Please enter a task.")

st.subheader(f"Your tasks ({len(st.session_state.tasks)})")
for index, task in enumerate(st.session_state.tasks):
    left, right = st.columns([5, 1])
    left.write(f"{index + 1}. {task}")
    if right.button("Delete", key=f"delete_{index}"):
        st.session_state.tasks.pop(index)
        save_tasks(st.session_state.tasks)
        st.rerun()
