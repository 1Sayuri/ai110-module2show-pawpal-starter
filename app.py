import streamlit as st
from pawpal_system import Owner, Pet, Task, Schedule

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_id="owner-001",
        name="Jordan",
        contact="",
        available_time=120,
        preferences={},
    )
    st.session_state.current_pet_id = None

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name

col1, col2 = st.columns(2)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet_id = f"pet-{len(st.session_state.owner.get_pets()) + 1:03}"
    new_pet = Pet(
        pet_id=pet_id,
        owner_id=st.session_state.owner.owner_id,
        name=pet_name,
        species=species,
    )
    st.session_state.owner.add_pet(new_pet)
    st.session_state.current_pet_id = pet_id
    st.success(f"Added pet: {new_pet.name}")

pets = st.session_state.owner.get_pets()
if pets:
    pet_options = {f"{pet.name} ({pet.species})": pet.pet_id for pet in pets}
    selected_label = list(pet_options.keys())[0]
    if st.session_state.current_pet_id is not None:
        selected_label = [label for label, pid in pet_options.items() if pid == st.session_state.current_pet_id][0]
    selected_pet_label = st.selectbox("Select a pet", list(pet_options.keys()), index=list(pet_options.keys()).index(selected_label))
    selected_pet_id = pet_options[selected_pet_label]
    st.session_state.current_pet_id = selected_pet_id
else:
    st.info("Add a pet first so you can attach tasks to it.")
    selected_pet_id = None

st.markdown("### Tasks")
st.caption("Add a task to the selected pet and build a schedule with your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if selected_pet_id is None:
        st.warning("Please add a pet first.")
    else:
        task_id = f"task-{sum(len(p.get_tasks()) for p in pets) + 1:03}"
        new_task = Task(
            task_id=task_id,
            pet_id=selected_pet_id,
            title=task_title,
            category="general",
            duration=int(duration),
            priority=priority,
        )
        pet = st.session_state.owner.get_pet_by_id(selected_pet_id)
        if pet is not None:
            pet.add_task(new_task)
            st.success(f"Added task '{new_task.title}' to {pet.name}")

if pets:
    all_tasks = []
    for pet in pets:
        for task in pet.get_tasks():
            all_tasks.append({
                "pet": pet.name,
                "title": task.title,
                "duration": task.duration,
                "priority": task.priority,
            })
    if all_tasks:
        st.write("Current tasks:")
        st.table(all_tasks)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("No pets available yet.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button now builds a schedule from the tasks attached to pets.")

if st.button("Generate schedule"):
    all_tasks = [task for pet in st.session_state.owner.get_pets() for task in pet.get_tasks()]
    if not all_tasks:
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = Schedule(owner=st.session_state.owner, tasks=all_tasks)
        schedule.generate_schedule()
        st.markdown("### Schedule")
        st.code(schedule.display_plan())
