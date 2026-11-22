"use strict";

class Stack {
  constructor() {
    this.items = [];
  }
  push(x) {
    this.items.push(x);
  }
  isEmpty() {
    return this.items.length === 0;
  }
  getAll() {
    if (this.isEmpty()) return null;
    return [...this.items].reverse();
  }
}

class Song {
  constructor(title) {
    this.title = title;
    this.prev = null;
    this.next = null;
    this.count = 0;
  }
}

// Circular doubly linked list

class Playlist {
  constructor() {
    this.head = null;
    this.tail = null;
    this.current = null;
    this.history = new Stack();
  }

  add(title) {
    const node = new Song(title);
    if (this.head === null) {
      this.head = node;
      this.tail = node;
      node.next = node;
      node.prev = node;
    } else {
      node.prev = this.tail;
      node.next = this.head;
      this.tail.next = node;
      this.head.prev = node;
      this.tail = node;
    }
  }

  showAll() {
    if (this.head === null) return [];
    let node = this.head;
    const songs = [];
    while (true) {
      songs.push([node.title, node === this.current]);
      node = node.next;
      if (node === this.head) break;
    }
    return songs;
  }

  nextSong() {
    if (this.head === null) return [null, null];
    this.current = this.current === null ? this.head : this.current.next;
    this.history.push(this.current.title);
    this.current.count += 1;
    return [this.current.title, this.current.count];
  }

  prevSong() {
    if (this.tail === null) return [null, null];
    this.current = this.current === null ? this.tail : this.current.prev;
    this.history.push(this.current.title);
    this.current.count += 1;
    return [this.current.title, this.current.count];
  }

  remove(title) {
    if (this.head === null) return null;

    let curr = this.head;
    while (curr.title !== title) {
      curr = curr.next;
      if (curr === this.head) return null;
    }

    if (curr === this.head && curr === this.tail) {
      this.head = null;
      this.tail = null;
      this.current = null;
      return "Deleted";
    }

    if (this.current === curr) this.current = curr.next;

    curr.prev.next = curr.next;
    curr.next.prev = curr.prev;

    if (curr === this.head) this.head = curr.next;
    if (curr === this.tail) this.tail = curr.prev;

    if (this.current !== null) this.current.count += 1;

    return "Deleted";
  }

  playHistory() {
    return this.history.getAll();
  }

  random() {
    if (this.head === null) return [null, null];

    const hst = this.history.items;
    let cur = this.head;
    const unplayed = [];

    while (true) {
      if (!hst.includes(cur.title)) unplayed.push(cur);
      cur = cur.next;
      if (cur === this.head) break;
    }

    if (unplayed.length === 0) return [null, null];

    const index = hst.length % unplayed.length;
    this.current = unplayed[index];
    this.current.count += 1;
    this.history.push(this.current.title);

    return [this.current.title, this.current.count];
  }

  insert(title) {
    const node = new Song(title);
    if (this.head === null) {
      this.head = node;
      this.tail = node;
      this.current = node;
      node.next = node;
      node.prev = node;
      return;
    }

    if (this.current === null) this.current = this.tail;

    node.next = this.current.next;
    node.prev = this.current;
    this.current.next.prev = node;
    this.current.next = node;

    if (this.current === this.tail) this.tail = node;
  }
}

// FOR HTML CALLING
const bucket = new Playlist();
["Choosin' Texas", "Housewife", "Dracula", "Patient Zero"].forEach((t) =>
  bucket.add(t)
);

const $ = (id) => document.getElementById(id);
let toastTimer = null;

function flash(kind, text) {
  const el = $("message");
  el.textContent = text;
  el.className = `message ${kind}`;
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (el.hidden = true), 4000);
}

function clearFlash() {
  $("message").hidden = true;
}

function doNext() {
  if (bucket.nextSong()[0] === null) flash("warning", "Playlist is empty.");
  else clearFlash();
  render();
}

function doPrev() {
  if (bucket.prevSong()[0] === null) flash("warning", "Playlist is empty.");
  else clearFlash();
  render();
}

function doRandom() {
  const [title] = bucket.random();
  if (title === null)
    flash("warning", "No unplayed songs left to randomize (or playlist is empty).");
  else clearFlash();
  render();
}

function doDelete() {
  if (bucket.current === null) {
    flash("warning", "Please select a song (play one) before deleting.");
    return render();
  }
  const title = bucket.current.title;
  bucket.remove(title);
  flash("success", `Deleted: ${title}`);
  render();
}

function submitSong(mode) {
  const input = $("song-title");
  const name = input.value.trim();
  if (!name) {
    flash("warning", "Please enter a song title.");
    return input.focus();
  }
  if (mode === "add") {
    bucket.add(name);
    flash("success", `Added: ${name}`);
  } else {
    bucket.insert(name);
    flash("success", `Inserted after current: ${name}`);
  }
  input.value = "";
  render();
}

function renderList(listEl, emptyEl, rows) {
  listEl.replaceChildren();
  emptyEl.hidden = rows.length > 0;
  rows.forEach(({ text, current }) => {
    const li = document.createElement("li");
    if (current) li.classList.add("current");
    const marker = document.createElement("span");
    marker.className = "marker";
    marker.textContent = current ? "▶️" : "";
    const label = document.createElement("span");
    label.textContent = text;
    li.append(marker, label);
    listEl.append(li);
  });
}

function render() {
  const cur = bucket.current;
  $("now-title").textContent = `Now playing: ${cur ? cur.title : "—"}`;
  $("now-sub").textContent = cur
    ? `Play count: ${cur.count}`
    : "Press Next, Previous or Random to start.";

  renderList(
    $("playlist"),
    $("playlist-empty"),
    bucket.showAll().map(([title, current], i) => ({
      text: `${i + 1}. ${title}`,
      current,
    }))
  );

  const hist = bucket.playHistory();
  renderList(
    $("history"),
    $("history-empty"),
    (hist || []).map((s, i) => ({ text: `${i + 1}. ${s}`, current: false }))
  );
}


$("song-form").addEventListener("submit", (e) => {
  e.preventDefault();
  submitSong("add"); // Enter key = "Add to end"
});
$("btn-add").addEventListener("click", () => submitSong("add"));
$("btn-insert").addEventListener("click", () => submitSong("insert"));
$("btn-delete").addEventListener("click", doDelete);
$("btn-prev").addEventListener("click", doPrev);
$("btn-next").addEventListener("click", doNext);
$("btn-random").addEventListener("click", doRandom);

render();
