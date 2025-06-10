import { Link, Outlet } from "react-router-dom";
import { FaHome } from "react-icons/fa";
import { LiaRegisteredSolid } from "react-icons/lia";
import { TbLogin2 } from "react-icons/tb";

export default function HomeNavbar() {
  return (
    <div>
      <div className="homenav">
        <p><Link className="link" to="/">Home <FaHome style={{verticalAlign:'middle'}}/></Link></p>
        <p><Link className="link" to="/register">Register<LiaRegisteredSolid style={{verticalAlign:'middle'}}/> </Link></p>
        <p><Link className="link" to="/login">Login<TbLogin2 style={{verticalAlign:'middle'}}/> </Link></p>
      </div>
      
      <Outlet /> {/* This renders the nested route components */}
    </div>
  );
}
