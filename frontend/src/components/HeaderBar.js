import React, { Component } from 'react';
import {
	Navbar,
	NavbarBrand,
	Nav,
	NavItem,
	NavLink,
  } from 'reactstrap';
import jwt_decode from "jwt-decode";

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTrash } from '@fortawesome/free-solid-svg-icons'

export default class HeaderBar extends Component {
	
	constructor(props){
        super(props);
        this.state = {
            loggedIn : localStorage.getItem('access_token')
			? true
			: false
        }
    };

	componentDidMount(){
		const refresh_token = localStorage.getItem('refresh_token');

		if (!refresh_token){
			this.setState({loggedIn: false})
		} else {
			const tokenParts = jwt_decode(refresh_token);
			const now = Math.ceil(Date.now() / 1000);
			if (tokenParts.exp < now) {	
				this.setState({loggedIn: false})
			}
		}
	}

	render(){
		return(
			<div>
			<Navbar color="light" light expand="md">
				<NavbarBrand href="/">WeekPlanner</NavbarBrand>
				<Nav className="ml-auto" navbar>
					{
						this.state.loggedIn
						? ''
						: <NavItem>
							<NavLink href="/register" id="register">Sign Up</NavLink>
						</NavItem>
					}
					{
						this.state.loggedIn
						? ''
						: <NavItem>
							<NavLink href="/login" id="login">Login</NavLink>
						</NavItem>
					}
					{
						this.state.loggedIn
						? <NavItem className="mr-1">
							<NavLink className="font-weight-bold" href="/trash" id="trash">
								<FontAwesomeIcon icon={faTrash} size="lg"/>
							</NavLink>
						  </NavItem>
						: ''
					}
					{
						this.state.loggedIn
						? <NavItem>
							<NavLink href="/logout" id="logout">Logout</NavLink>
						  </NavItem>
						: ''
					}
				</Nav>
			</Navbar>
		</div>
		)
	}
}
