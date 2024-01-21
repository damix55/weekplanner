import React, { Component } from 'react';
import axiosInstance from '../axios';
import HeaderBar from './HeaderBar'

import {
	Form,
	FormGroup,
	Input,
	FormFeedback
} from 'reactstrap';

export default class Register extends Component {
    constructor(props){
        super(props);
        this.state = {
            email : '',
            username: '',
            password: '',
            errors: {}
        }
    };

    handleChange = (e) => {
        this.setState({ [e.target.name] : e.target.value.trim() })
    };

    handleSubmit = (e) => {
        e.preventDefault();

        axiosInstance
			.post('user/register/', {
				email: this.state.email,
				user_name: this.state.username,
				password: this.state.password,
			})
            .then(() => {
				axiosInstance
				.post('token/', {
					email: this.state.email,
					password: this.state.password,
				})
				.then((res) => {
					localStorage.setItem('access_token', res.data.access);
                	localStorage.setItem('refresh_token', res.data.refresh);
                	axiosInstance.defaults.headers['Authorization'] =
						'JWT ' + localStorage.getItem('access_token');
					this.props.history.push("/");
				})
			})
            .catch((error) => {
                if (error.response) {
                    this.setState({ errors : error.response.data});
                }
            })
    };

    render(){
        const { errors } = this.state;

        return(
			<div>
			<HeaderBar />
			<main className="container p-5">
				<div className="row">
					<div className="col-md-6 col-sm-10 mx-auto p-0">
						<div className="card p-3">
							<h4 className="card-title text-center mb-4 mt-1">Sign Up</h4>
            				<Form onSubmit={this.handleSubmit} noValidate>
								<FormGroup>
									<Input
                                		invalid={this.state.errors.email !== undefined}
										type="email"
										id="email"
										name="email"
										value={this.state.email}
										placeholder="email"
										onChange={this.handleChange}
									/>
									<FormFeedback id="email_error">
										{errors.email}
									</FormFeedback>
								</FormGroup>
								<FormGroup>
									<Input
										invalid={this.state.errors.user_name !== undefined}
										type="text"
										id="username"
										name="username"
										value={this.state.username}
										placeholder="username"
										onChange={this.handleChange}
									/>
                            		<FormFeedback id="username_error">
										{this.state.errors.user_name}
									</FormFeedback>
								</FormGroup>
								<FormGroup>
									<Input
										invalid={this.state.errors.password !== undefined}
										type="password"
										id="password"
										name="password"
										value={this.state.password}
										placeholder="password"
										onChange={this.handleChange}
									/>
                            		<FormFeedback id="password_error">
										{this.state.errors.password}
									</FormFeedback>
								</FormGroup>
								<button
									className="btn btn-primary btn-md btn-block"
									id="submit"
									type="submit"
								>
									Sign Up
								</button>
								<hr></hr>
								<p className="text-center">Already have an account? <a href="/login" className="link-primary">Login</a></p>
							</Form>
						</div>
					</div>
				</div>
			</main>
			</div>
		)
    }
}

