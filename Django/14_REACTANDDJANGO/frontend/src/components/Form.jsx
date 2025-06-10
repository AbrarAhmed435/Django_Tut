import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constant";
import '../styles/Form.css'
import { Link } from "react-router-dom";
import { CiLogin } from "react-icons/ci";
import { FaRegRegistered } from "react-icons/fa";

function Form({ route, method }) {
  const [username, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [IsLoading, setIsLoading] = useState(false);

  const name = method == "login" ? "Login" : "Register";
  const navigate = useNavigate();

  const handleSubmit= async (e)=>{
    e.preventDefault();
    setIsLoading(true);
    if(!username.trim()||!password.trim()) return ;
    try{
        const res=await api.post(route,{username,password})
        if(method==='login'){
            localStorage.setItem(ACCESS_TOKEN,res.data.access) 
            localStorage.setItem(REFRESH_TOKEN,res.data.refresh)
            navigate('/')
        }else{
            navigate('/login')
        }
    }catch(err){
        alert(err)
    }finally{
        setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>{name}</h1>
      <input
        type="text"
        className="form-input"
        value={username}
        onChange={(e) => setUserName(e.target.value)}
        placeholder="User name"
      />
      <input
        type="password"
        className="form-input"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="User Password"
      />
      <button className="form-button">{name}</button>
      {method=='login'? <p><Link  to ='/register'>Register <FaRegRegistered style={{verticalAlign:'middle'}} /></Link></p>:
      <Link to ='/login'>Login<CiLogin style={{verticalAlign:'middle'}} /></Link>
      }
    </form>
  );
}


export default Form;