
//components import
import React from 'react'
import { useEffect, useState } from 'react'

import Modal from './components/Modal'

import axiosInstance from './axios';
import jwt_decode from "jwt-decode";
import Header from './components/Header'
import HeaderBar from './components/HeaderBar'
import Button from './components/Button'
import CalDays from './components/CalDays'
import Calendar from './components/Calendar'
import Inbox from './components/Inbox'


const App = () => {
  const [state, setState] = useState(
    {viewCompleted: false,
      taskList: [],
      modal: false,
      activeItem: {
        title: '',
        description: '',
        completed: false,
        priority: '0',
        date: undefined,
      },
      repeat: false,
      repeatItem: {
        until: undefined,
        every: 1,
      }
    },
  );
  
  useEffect(() => {
    // make fetch request once when page loaded
    refreshList();
  }, []);
  
  const refreshList = () => {
    const token = localStorage.getItem('access_token');
    //download tasks in the state
    if (token){
      axiosInstance
        .get(`${jwt_decode(token).user_id}/calendar/`)
        .then((res) => setState( prevState => {
          return {...prevState, taskList: res.data }
        }))
        .catch((err) => console.log(err));
    }

    if (token){
      axiosInstance
        .get(`${jwt_decode(token).user_id}/inbox/`)
        .then((res) => setState( prevState => {
          return {...prevState, inboxList: res.data }
        }))
        .catch((err) => console.log(err));
    }
    
  };

  const toggle = () => {
    setState( prevState => {
      return {...prevState, modal: !state.modal, errors: {}, repeat: false,  repeatItem: {until: undefined, every: 1}}
    })
    refreshList()
    //setState({ modal: !state.modal });
  };


  const handleSubmitRepeat = (repeatItem, user_id, task_id) => {
    repeatItem.task_id = task_id
    axiosInstance
    .post(`/${user_id}/repeat`, repeatItem)
    .then((res) => {
      if(res.status === 201) {
        toggle();
      }
    })
    .catch((error) => {
      if (error.response) {
        console.log(error.response)
        setState( prevState => {
          return {...prevState, errors : error.response.data}
        })
      }
    });
  }


  const handleSubmit = (item, repeatItem) => {
    setState( prevState => {
      return {...prevState, errors: {} }
    })

    //const { toggle, refreshList } = props;
    const user_id = jwt_decode(localStorage.getItem('access_token')).user_id

    let type = 'inbox';

    if (typeof item.date !== 'undefined') {
      type = 'calendar';
    }

    if (item.id && type === state.currentType) {
      axiosInstance
        .put(`/${user_id}/${type}/${item.id}/`, item)
        .then((res) => {
          if(res.status === 200) {
            if(state.repeat && state.activeItem.date) {
              handleSubmitRepeat(repeatItem, user_id, res.data.id)
            } else {
              toggle();
            }
          }
        })
        .catch((error) => {
          if (error.response) {
            console.log(error.response)
            setState( prevState => {
              return {...prevState, errors : error.response.data}
            })
          }
        });
    }

    else {
      if (item.id) {
        axiosInstance.delete(`/${user_id}/${state.currentType}/${item.id}/`);
      }
      axiosInstance
        .post(`/${user_id}/${type}/`, item)
        .then((res) => {
          if(res.status === 201) {
            if(state.repeat && state.activeItem.date) {
              handleSubmitRepeat(repeatItem, user_id, res.data.id)
              item.id=res.data.id
            } else {
              toggle();
            }
          }
        })
        .catch((error) => {
          if (error.response) {
            setState( prevState => {
              return {...prevState, errors : error.response.data }
            })
          }
        });
    }
  };

  const handleDelete = (item) => {
    //const { toggle, refreshList } = props;
    const user_id = jwt_decode(localStorage.getItem('access_token')).user_id

    item.deletion_date = new Date().toISOString().split('T')[0]

    axiosInstance.delete(`${user_id}/${state.currentType}/${item.id}/`);
    axiosInstance
      .post(`${user_id}/trash/`, item)
      .then((res) => {
        toggle();
      })  
  };

  
  const handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...state.activeItem, [name]: value };

    //this.setState({ activeItem });
    setState( prevState => {
      return {...prevState, activeItem }
    })
  };

  const handleRepeat = (e) => {
    let value = e.target.checked;

    setState( prevState => {
      return {...prevState, repeat: value }
    })
  };


  const handleEvery = (e) => {
    let { name, value } = e.target;

    const repeatItem = { ...state.repeatItem, [name]: value };

    setState( prevState => {
      return {...prevState, repeatItem }
    })
  };


  const convertDate = (day) => {
    if (typeof day !== 'undefined') {
      day = day.toISOString().split('T')[0];
    }
    return day
  }

  
  const handleDayChange = (day) => {
    day = convertDate(day)
    let activeItem = state.activeItem;
    activeItem.date = day;
    setState( prevState => {
      return {...prevState, activeItem: activeItem }
    })
  }

  const handleUntilChange = (day) => {
    day = convertDate(day)
    let repeatItem = state.repeatItem;
    repeatItem.until = day;
    setState( prevState => {
      return {...prevState, repeatItem: repeatItem }
    })
  }

  const editItem = (item) => {
    let currentType = 'calendar';
    if (typeof item.date === 'undefined') {
      currentType = 'inbox';
    }
    setState( prevState => {
      return {...prevState, activeItem: item, modal: !state.modal, currentType: currentType }
    })
  };


  const createItem = () => {
    const item = { title: '', description: '', priority: '0', completed: false, date: undefined };

    setState( prevState => {
      return {...prevState, activeItem: item, modal: !state.modal }
    });
  };


  const token = localStorage.getItem('access_token');
  //download tasks in the state
  if (!token) {
    window.location.replace('/login')
  }
  else {

    return (
      <div>
      <HeaderBar />
      <div className="container-fluid">
        <div className="row">
        <div className="col-md-9">
          <div className="calendar shadow bg-white p-5">
            <Header title="Week Planner"/>
            <p className="font-italic text-muted mb-5"> 
            Plan your week
            {/* No events for this day. */}
            </p> 
            <CalDays />
            <Calendar taskList = {state.taskList} onEdit = {editItem} />

            <Button id = 'add-button' color = 'btn-success' text='Add task' onClick={ createItem } />
            <Button color = 'btn-dark' text='<' onClick={ null } />
            <Button color = 'btn-dark' text='>' onClick={ null } />
          </div>
        </div>
        <div className="col-md-3">
            <div className="calendar shadow bg-white p-5">
              <div className="mb-6">
              <div className="d-flex align-items-center"> 
                  <h2 className="font-weight-bold text-center">Inbox</h2>
              </div>
              </div>
              
              <Inbox taskList = {state.inboxList} 
                // viewCompleted={state.viewCompleted} 
                onEdit = {editItem} 
                // onTabClick={onTabClick} 
              />
             
            </div>
        </div>
        {state.modal ? (
          <Modal
            activeItem={state.activeItem}
            repeatItem={state.repeatItem}
            toggle={toggle}
            handleSubmit={handleSubmit}
            handleChange = {handleChange}
            handleDayChange = {handleDayChange}
            errors = {state.errors}
            handleDelete = {handleDelete}
            repeat = {state.repeat}
            handleRepeat = {handleRepeat}
            handleUntilChange = {handleUntilChange}
            handleEvery = {handleEvery}
          />
        ) : null}
        
        </div>
      </div>
      </div>
    );
  }
}

export default App;
