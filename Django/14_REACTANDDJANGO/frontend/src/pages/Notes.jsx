import { useState, useEffect } from "react";
import api from "../api";
import { Link } from "react-router-dom";
import { IoIosAddCircleOutline } from "react-icons/io";

export default function Notes() {
  const [notes, setNotes] = useState([]);

  useEffect(() => {
    getNotes();
  }, []);

  const getNotes = () => {
    api
      .get("/api/notes")
      .then((res) => res.data)
      .then((data) => {
        setNotes(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const deleteNote = (id) => {
    api
      .delete(`/api/notes/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) {
          alert("Note was deleted");
          getNotes();
        } else {
          alert("Failed to delete");
        }
      })
      .catch((error) => alert(error));
  };
  return (
    <div>
      {notes.length ? (
        <ul className="mynotes">
          {notes.map((note) => (
            <li key={note.id}>
              <h4>{note.title}</h4>
              <p>{note.content}</p>
              <button onClick={() => deleteNote(note.id)}>Delete Note</button>
            </li>
          ))}
          <p style={{fontSize:'1.5rem'}}><Link to='/createNote'>Create More Posts <IoIosAddCircleOutline style={{verticalAlign:'middle'}}/></Link></p>
        </ul>
        
      ) : (
        <p>
          No Notes Found. click <Link to="/createNote"> here</Link> and Create
          your notes📰😊
        </p>
      )}
    </div>
  );
}
