import streamlit as st
import json
import os

# =========================
# Load / Init Data
# =========================
if "tasks" not in st.session_state:
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []

if "edit_index" not in st.session_state:
    st.session_state.edit_index = None


# =========================
# Save Function
# =========================
def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(st.session_state.tasks, f)


# =========================
# UI Header
# =========================
st.title("🗂️ Team Planning System")

# =========================
# Dashboard
# =========================
total = len(st.session_state.tasks)
done = len([t for t in st.session_state.tasks if t["status"] == "Done"])
todo = total - done

col1, col2, col3 = st.columns(3)
col1.metric("Total Tasks", total)
col2.metric("Done", done)
col3.metric("Todo", todo)

# =========================
# Sidebar Menu
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Task", "View Tasks"]
)

# =========================
# ADD TASK
# =========================
if menu == "Add Task":
    st.subheader("➕ Add New Task")

    title = st.text_input("Task Title")
    member = st.text_input("Assigned To")
    deadline = st.date_input("Deadline")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    if st.button("Add Task"):
        if title.strip() == "":
            st.error("Task title cannot be empty")
        else:
            task = {
                "title": title,
                "member": member,
                "deadline": str(deadline),
                "priority": priority,
                "status": "Todo"
            }

            st.session_state.tasks.append(task)
            save_tasks()
            st.success("Task added successfully!")

# =========================
# VIEW TASKS
# =========================
elif menu == "View Tasks":
    st.subheader("📋 All Tasks")

    # Filter
    priority_filter = st.selectbox(
        "Filter by Priority",
        ["All", "High", "Medium", "Low"]
    )

    # Edit Mode
    if st.session_state.edit_index is not None:
        i = st.session_state.edit_index
        task = st.session_state.tasks[i]

        st.subheader("✏️ Edit Task")

        new_title = st.text_input("Title", task["title"])
        new_member = st.text_input("Member", task["member"])
        new_priority = st.selectbox(
            "Priority",
            ["High", "Medium", "Low"],
            index=["High", "Medium", "Low"].index(task["priority"])
        )
        new_status = st.selectbox(
            "Status",
            ["Todo", "Done"],
            index=["Todo", "Done"].index(task["status"])
        )

        if st.button("Save Changes"):
            st.session_state.tasks[i]["title"] = new_title
            st.session_state.tasks[i]["member"] = new_member
            st.session_state.tasks[i]["priority"] = new_priority
            st.session_state.tasks[i]["status"] = new_status

            save_tasks()
            st.session_state.edit_index = None
            st.rerun()

    # Tasks List
    if len(st.session_state.tasks) == 0:
        st.info("No tasks yet.")
    else:
        for i, task in enumerate(st.session_state.tasks):

            if priority_filter != "All" and task["priority"] != priority_filter:
                continue

            with st.container():
                st.markdown(f"### Task {i+1}")
                st.write(f"**Title:** {task['title']}")
                st.write(f"**Member:** {task['member']}")
                st.write(f"**Deadline:** {task['deadline']}")
                st.write(f"**Priority:** {task['priority']}")
                st.write(f"**Status:** {task['status']}")

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(f"✅ Done {i}"):
                        st.session_state.tasks[i]["status"] = "Done"