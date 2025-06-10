import { Link } from "react-router-dom"
import { Navigate } from "react-router-dom";
import { IoIosMailUnread,IoIosCreate } from "react-icons/io";
import { CgLogOut } from "react-icons/cg";



export const Logout=() =>{
  localStorage.clear();
  return <Navigate to="/login" />;
}
export default function PostNav(){
  
    return (
        <div>
        <p style={{fontSize:'2rem'}}>Welcome🙋‍♂️</p>
        <nav className="Post-nav">
             
          
        <p><Link to ='/notes' className ='link'>My Notes <IoIosMailUnread style={{verticalAlign:'middle'}} /></Link></p>
        <p><Link to ='/createNote' className ='link'>Create Note <IoIosCreate style={{verticalAlign:'middle'}}/></Link></p>
        <p><Link to ='/logout' className ='link'>Logout <CgLogOut style={{verticalAlign:'middle'}} /></Link></p>
       
        </nav>
        </div>
    )
}