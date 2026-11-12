import streamlit as st
st.set_page_config(page_title="Music Playlist", page_icon=":musical_note:", layout="wide")
class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def is_empty(self):
        return len(self.items) == 0

    def get_all(self):
        if self.is_empty(): 
            return None
        return self.items[::-1]

class Song:
    def __init__(self, title):
        self.title = title
        self.prev = None
        self.next = None
        self.count = 0

class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.history = Stack()

    def add(self, title):
        node = Song(title)
        if self.head is None:
            self.head = node
            self.tail = node
            node.next = node
            node.prev = node
        else:
            node.prev = self.tail
            node.next = self.head
            self.tail.next = node
            self.head.prev = node
            self.tail = node

    def show_all(self):
        if self.head is None:
            return []
        if self.current is not None:
            start = self.current 
        else:
            start = self.head
        current = start
        songs = []
        while True:
            # print(current.title, end=' ')
            songs.append(current.title)
            current = current.next
            if current == start:
                break
            # print('<-> ', end='')
        return songs

    def next_song(self):
        if self.head is None:
            return None, None

        if self.current is None:
            self.current = self.head
        else:
            self.current = self.current.next
        
        self.history.push(self.current.title)
        self.current.count += 1
        return self.current.title, self.current.count

    def prev_song(self):
        if self.tail is None:
            return None, None

        if self.current is None:
            self.current = self.tail
        else:
            self.current = self.current.prev

        self.history.push(self.current.title)
        self.current.count += 1
        return self.current.title, self.current.count

    def remove(self, title):
        if self.head is None:
            return None

        curr = self.head
        while curr.title != title:
            curr = curr.next
            if curr == self.head:
                return None

        if curr == self.head and curr == self.tail:
            self.head = None
            self.tail = None
            self.current = None
            return "Deleted"

        if self.current == curr:
            self.current = curr.next

        curr.prev.next = curr.next
        curr.next.prev = curr.prev

        if curr == self.head:
            self.head = curr.next
        if curr == self.tail:
            self.tail = curr.prev

        if self.current is not None:
            self.current.count += 1

        return "Deleted"

    def Play_history(self):
        return self.history.get_all()

    def random(self):
        if self.head is None:
            return None, None

        hst = self.history.items
        cur = self.head
        n_hst = []

        while True:
            if cur.title not in hst:
                n_hst.append(cur)
            cur = cur.next
            if cur == self.head:
                break

        if not n_hst:
            return None, None

        index = len(self.history.items) % len(n_hst)
        chosen = n_hst[index]

        self.current = chosen
        self.current.count += 1
        self.history.push(self.current.title)

        return self.current.title, self.current.count

    def insert(self, title):
        node = Song(title)
        if self.head is None:
            self.head = node
            self.tail = node
            self.current = node
            node.next = node
            node.prev = node
            return

        if self.current is None:
            self.current = self.tail

        node.next = self.current.next
        node.prev = self.current
        self.current.next.prev = node
        self.current.next = node

        if self.current == self.tail:
            self.tail = node
if "bucket" not in st.session_state:
    b = Playlist()
    for t in ["Choosin' Texas", "Housewife", "Dracula", "Patient Zero"]:
        b.add(t)
    st.session_state.bucket = b
    st.session_state.msg = None

bucket = st.session_state.bucket


def flash(kind, text):
    st.session_state.msg = (kind, text)


def do_next():
    if bucket.next_song()[0] is None:
        flash("warning", "Playlist is empty.")


def do_prev():
    if bucket.prev_song()[0] is None:
        flash("warning", "Playlist is empty.")


def do_random():
    title, _ = bucket.random()
    if title is None:
        flash("warning", "No unplayed songs left to randomize (or playlist is empty).")


def do_delete():
    if bucket.current is None:
        flash("warning", "Please select a song (play one) before deleting.")
        return
    title = bucket.current.title
    bucket.remove(title)
    flash("success", f"Deleted: {title}")


st.title("🎵 Music Playlist")
with st.sidebar:
    st.header("Manage songs")
    with st.form("song_form", clear_on_submit=True):
        name = st.text_input("Song title")
        c1, c2 = st.columns(2)
        add_btn = c1.form_submit_button("Add to end", use_container_width=True)
        ins_btn = c2.form_submit_button("Insert next", use_container_width=True)
    if (add_btn or ins_btn) and not name.strip():
        flash("warning", "Please enter a song title.")
    elif add_btn:
        bucket.add(name.strip())
        flash("success", f"Added: {name.strip()}")
    elif ins_btn:
        bucket.insert(name.strip())
        flash("success", f"Inserted after current: {name.strip()}")

    st.button("🗑️ Delete current song", on_click=do_delete, use_container_width=True)
if st.session_state.msg:
    kind, text = st.session_state.msg
    getattr(st, kind)(text)
    st.session_state.msg = None

if bucket.current is not None:
    st.subheader(f"Now playing: {bucket.current.title}")
    st.caption(f"Play count: {bucket.current.count}")
else:
    st.subheader("Now playing: —")
    st.caption("Press Next, Previous or Random to start.")

b1, b2, b3 = st.columns(3)
b1.button("⏮️ Previous", on_click=do_prev, use_container_width=True)
b2.button("⏭️ Next", on_click=do_next, use_container_width=True)
b3.button("🔀 Random", on_click=do_random, use_container_width=True)

st.divider()
left, right = st.columns(2)

with left:
    st.subheader("Playlist")
    # Walk from head so the order stays fixed; just put a pointer before the current song
    node = bucket.head
    if node is None:
        st.info("Playlist is empty. Add a song from the sidebar.")
    else:
        i = 1
        while True:
            if node is bucket.current:
                st.markdown(f"▶️ **{i}. {node.title}**")
            else:
                st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{i}. {node.title}")
            node = node.next
            i += 1
            if node is bucket.head:
                break

with right:
    st.subheader("Play history")
    hist = bucket.Play_history()
    if hist is None:
        st.info("Nothing played yet.")
    else:
        for i, s in enumerate(hist, 1):
            st.markdown(f"{i}. {s}")

# while True:
#     print("add - เพิ่มเพลง, del - ลบเพลง, prev - เพลงก่อนหน้า, all - เพลงทั้งหมด, next - เพลงถัดไป, history - ประวัติการเล่น, random - สุ่มเพลง, insert - แทรกเพลง\n")
#     user_input = str(input("ตัวเลือก: "))
#     if user_input == ("add"):
#         song = input("โปรดใส่ชื่อเพลง: ")
#         bucket.add(song)
#         print("Added\n")
#     if user_input == ("del"):
#         if bucket.current is None:
#             print("Please select your song to delete!\n")
#             continue
#         titles = bucket.current.title
#         if bucket.current is not None:
#             bucket.remove(titles)
#             if bucket.current is not None:
#                 print("Deleted")
#                 print("Now playing: ", bucket.current.title, end="\n")
#             else:
#                 print("Playlist is empty", end="\n")

#     if user_input == ("all"):
#         print("Playlist: ")
#         bucket.show_all()
#         print("\n")

#     if user_input == ("next"):
#         title, count = bucket.next_song()
#         print("Now playing:", title, "COUNT:", count, end="\n\n")

#     if user_input == ("prev"):
#         title, count = bucket.prev_song()
#         print("Now playing:", title, "COUNT:", count, end="\n\n")

#     if user_input == ("history"):
#         print("History:", bucket.Play_history(), end="\n\n")

#     if user_input == ("random"):
#         title, count = bucket.random()
#         print("Now playing:", title, "COUNT:", count, end="\n\n")

#     if user_input == ("insert"):
#         song = input("โปรดใส่ชื่อเพลง: ")
#         bucket.insert(song)
#         print("Inserted\n")