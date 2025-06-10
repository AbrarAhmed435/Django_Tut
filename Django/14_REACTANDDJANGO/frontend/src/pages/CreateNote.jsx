import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { Link } from "react-router-dom";

export default function CreateNote() {
  const navigate = useNavigate();

  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const createNote = (e) => {
    e.preventDefault();
    if (!title.trim() || !content.trim()) return;
    api
      .post("/api/notes/", { content, title })
      .then((res) => {
        if (res.status === 201) {
          alert("Note Created");
        } else {
          alert("Failed to create note");
        }
      })
      .catch((err) => alert(err));

    setContent("");
    setTitle("");
    navigate("/notes");
  };
  return (
    <div>
      <h2 style={{ textAlign: "center" }}>Create a Note👇</h2>
      <form onSubmit={createNote} className="create-form">
        <label htmlFor="title">Title</label>
        <br />
        <input
          type="text"
          id="title"
          required
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <br />
        <br />
        <label htmlFor="content">Content</label>
        <br />
        <textarea
          id="content"
          name="content"
          required
          value={content}
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
        <br />
        <br />
        <button>Submit</button>
        <p style={{marginTop:'20px'}}><Link to ='/notes'>See Posts</Link></p>
      </form>
    </div>
  );
}
