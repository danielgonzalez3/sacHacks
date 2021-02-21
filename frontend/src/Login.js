import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./login.css";
import { LoginButton } from "./loginButton";

export default function Login() {
    {/* 
        const [email, setEmail] = useState("");
        const [password, setPassword] = useState("");

        function validateForm() {
            return email.length > 0 && password.length > 0;
        }

        function handleSubmit(event) {
            event.preventDefault();
        }
    */}
    

    return(
        <div className = "topImageContainer" >
            <div className = "imageFilter"> 
                <h1 className = "bigText"> Project Jensen </h1>
                <h1 className = "bigText"> the Future of teaching software </h1>
            </div>
            {/*
            <div className="Login">
                <div className="centerLogin">
                    <div className="box">
 
                    <Form onSubmit={handleSubmit}>
                        <Form.Group size="lg" controlId="email">
                            <Form.Label>Email</Form.Label>
                            <Form.Control
                                autoFocus
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />
                        </Form.Group>
                        <Form.Group size="lg" controlId="password">
                            <Form.Label>Password</Form.Label>
                            <Form.Control
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />
                        </Form.Group>
                    </Form>
                    </div>
                </div>
            </div>
            */}
        </div>
    )
}