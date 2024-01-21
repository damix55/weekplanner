import React, { Component } from 'react';
import axiosInstance from '../axios';

export default class Logout extends Component {
	constructor(props){
        super(props);
        this.state = {
        }
    };

    componentDidMount() {
        axiosInstance.post('user/logout/blacklist/', {
            refresh_token: localStorage.getItem('refresh_token'),
        });
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        axiosInstance.defaults.headers['Authorization'] = null;
        this.props.history.push('/login');
    }

	render() {
        return(
            <div>
                Logout
            </div>
        )
    }
}