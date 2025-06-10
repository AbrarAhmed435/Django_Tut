import Form from "../components/Form"
import { Link } from "react-router-dom"

export default function Login(){
    return (
        <div>
        <Form route='api/token/' method='login' />
        </div>
        )
}