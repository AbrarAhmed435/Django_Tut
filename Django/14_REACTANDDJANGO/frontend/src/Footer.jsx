import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>📝 MyNotes App &copy; {new Date().getFullYear()}</p>
      </div>
    </footer>
  );
}
