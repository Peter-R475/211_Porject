class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self, i):
        if self.is_empty():
            return None
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def get_all(self):
        return list(reversed(self.items))

class Song:
    def __init__(self, title):
        self.title = title
        self.prev = None
        self.next = None

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
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def show_all(self):
        current = self.head
        while current is not None:
            print(current.title, end=' ')
            current = current.next
            if current is not None:
                print('<-> ', end='')
        print('')

    def show_reverse(self):
        current = self.tail
        while current is not None:
            print(current.title, end=' ')
            current = current.prev
            if current is not None:
                print('<-> ', end='')
        print('')

    def next_song(self):
        if self.head is None:
            return None

        if self.current is None:
            self.current = self.head
        elif self.current.next is not None:
            self.current = self.current.next
        else:
            self.current = self.head
        
        self.history.push(self.current.title)
        return self.current.title

    def prev_song(self):
        if self.tail is None:
            return None

        if self.current is None:
            self.current = self.tail
        elif self.current.prev is not None:
            self.current = self.current.prev
        else:
            self.current = self.tail

        self.history.push(self.current.title)
        return self.current.title

    def remove(self, title):
        curr = self.head
        while curr is not None and curr.title != title:
            curr = curr.next

        if curr is None:
            return None

        if self.current == curr:
            if curr.next is not None:
                self.current = curr.next
            elif curr.prev is not None:#
                self.current = self.head
            else:
                self.current = None
        
        if curr == self.head:
            self.head = curr.next
            if self.head is not None:
                self.head.prev = None
        else:
            curr.prev.next = curr.next

        if curr == self.tail:
            self.tail = curr.prev
            if self.tail is not None:
                self.tail.next = None
        else:
            curr.next.prev = curr.prev
        
        if self.head is None:
          self.tail = None
          self.current = None

        return "Deleted"

    def Play_history(self):
        return self.history.get_all()

    def random(self):
        hst = self.history.items
        cur = self.head
        n = 0
        found = False
        while cur is not None:
            if cur.title not in hst:
                n += 1
                print(n, ":", cur.title)
                found = True
            cur = cur.next
        if found: 
            return "Total Played:", n
        return "Out of items"

    def insert(self, title):
        node = Song(title)
        if self.head is None:
            self.head = node
            self.tail = node
            self.current = node
            return 
        
        if self.current.next is None:
            self.current.next = node
            node.prev = self.current
            self.tail = node

        else:
            node.next = self.current.next
            node.prev = self.current
            self.current.next.prev = node
            self.current.next = node

bucket = Playlist()
#เพิ่มเพลงเริ่มต้นเอาไว้สำหรับสาธิตการใช้งาน
bucket.add("Choosin' Texas")
bucket.add("Housewife")
bucket.add("Dracula")
bucket.add("Patient Zero")
bucket.current = bucket.head
print("Now playing:", bucket.current.title, end="\n\n")

while True:
    print("add - เพิ่มเพลง, del - ลบเพลง, prev - เพลงก่อนหน้า, all - เพลงทั้งหมด, next - เพลงถัดไป, history - ประวัติการเล่น, random - สุ่มเพลง, insert - แทรกเพลง\n")
    user_input = str(input("ตัวเลือก: "))
    if user_input == ("add"):
        song = input("โปรดใส่ชื่อเพลง: ")
        bucket.add(song)
        print("Added\n")
    if user_input == ("del"):
        if bucket.current is None:
            print("Playlist is empty\n")
            continue
        titles = bucket.current.title
        if bucket.current is not None:
            bucket.remove(titles)
            if bucket.current is not None:
                print("Deleted")
                print("Now playing: ", bucket.current.title, end="\n")
            else:
                print("Playlist is empty", end="\n")

    if user_input == ("all"):
        print("Playlist: ")
        bucket.show_all()
        print("\n")

    if user_input == ("next"):
        print("Now playing:", bucket.next_song(), end="\n\n")

    if user_input == ("prev"):
        print("Now playing:", bucket.prev_song(), end="\n\n")

    if user_input == ("history"):
        print("History:", bucket.Play_history(), end="\n\n")

    if user_input == ("random"):
        print("Result:\n")
        print(bucket.random(), end="\n\n")

    if user_input == ("insert"):
        song = input("โปรดใส่ชื่อเพลง: ")
        bucket.insert(song)
        print("Inserted\n")

    