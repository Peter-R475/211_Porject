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

        return self.current.title

    def remove(self, title):
        curr = self.head
        while curr is not None and curr.title != title:
            curr = curr.next

        if curr is None:
            return None

        if self.current == curr:
            if curr == self.tail:
                self.current = self.head if curr != self.head else None
            else:
                self.current = curr.next

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

        return "OK"

bucket = Playlist()
#เพิ่มเพลงเริ่มต้นเอาไว้สำหรับสาธิตการใช้งาน
bucket.add("Choosin' Texas")
bucket.add("Housewife")
bucket.add("Dracula")
bucket.add("Patient Zero")
cur = bucket.next_song()
print("Now playing:", cur, end="\n\n")

while True:
    print("add - เพิ่มเพลง, del - ลบเพลง, prev - เพลงก่อนหน้า, all - เพลงทั้งหมด, next - เพลงถัดไป\n")
    user_input = str(input("ตัวเลือก: "))
    if user_input == ("add"):
        song = input("โปรดใส่ชื่อเพลง: ")
        bucket.add(song)
        print("Added\n")
    elif user_input == ("del"):
        result = bucket.remove(cur)
    elif user_input == ("all"):
        print("Playlist: ")
        print(bucket.show_all())
    elif user_input == ("next"):
        print("Now playing:", bucket.next_song(), end="\n\n")
    elif user_input == ("prev"):
        print("Now playing:", bucket.prev_song(), end="\n\n")
        print("Removed")
    else:
        print("โปรดเลือกตัวเลือกที่ถูกต้อง")
    