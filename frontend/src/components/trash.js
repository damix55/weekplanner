import React, { Component } from 'react';

import axiosInstance from '../axios';
import jwt_decode from "jwt-decode";

import HeaderBar from './HeaderBar'
import Header from './Header'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faTrash } from '@fortawesome/free-solid-svg-icons'

export default class Trash extends Component{

    constructor(props){
        super(props);
        this.state = {
            items : []
        }
    };

    componentDidMount() {
        this.refreshList();
    }

    refreshList = () => {
        const token = localStorage.getItem('access_token');
        if (token){
            axiosInstance
              .get(`${jwt_decode(token).user_id}/trash/`)
              .then((res) => {
                this.setState({ items : res.data});
              })
        }
    }

    handleDelete = (item) => {
        const user_id = jwt_decode(localStorage.getItem('access_token')).user_id
        axiosInstance
            .delete(`${user_id}/trash/${item.id}/`)
            .then(() => {
                this.refreshList();
            }) 
    }

    handleRestore = (item) => {
        const user_id = jwt_decode(localStorage.getItem('access_token')).user_id
        axiosInstance
        .delete(`${user_id}/trash/${item.id}/`);

        axiosInstance
        .post(`${user_id}/inbox/`, item)
        .then((res) => {
            this.refreshList();
        }); 
    }

    render(){
        return(
            <div>
			    <HeaderBar />
                <div className="container py-5">
                    <div className="calendar shadow bg-white mx-auto w-75 p-5">
                        <Header title={<div><span>Trash</span> <FontAwesomeIcon icon={faTrash}/></div>}/>
                        {this.state.items.length === 0 
                        ?
                        <p class="font-italic text-muted mb-5">No tasks to show</p>
                        :
                        <ul class="list-group list-group-flush pt-5">
                            {this.state.items.map((task, index) => 
                                <li key={index} class="list-group-item d-flex justify-content-between align-items-center">
                                    <span id={"task-" + task.id}>
                                        {task.title}
                                    </span>
                                    <div>
                                        <button type="button" class="btn btn-warning" id={"restore-task-" + task.id} onClick={() => this.handleRestore(task)}>Restore</button>
                                        <button type="button" class="btn btn-danger" id={"delete-task-" + task.id} onClick={() => this.handleDelete(task)}>Delete</button>
                                    </div>
                                </li>
                            )}
                        </ul>
                        }   
                    </div>
                </div>
            </div>
        )
    }
}