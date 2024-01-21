import React from 'react'



function InboxList({inboxTasks, onEdit}) {

    const show_tasks = (tasks) => {
        try{
            return tasks.map((task, index) => (
                <div    className="event bg-0" 
                        id={'task-' + task.id} 
                        key = {index} 
                        onClick = {() => onEdit(task) }>
                    {task.title}  
                </div>
            ))
        }
        catch(e){
            return ''
        }
    }; 

    return(
        <li className="listInbox list-unstyled">
            {show_tasks(inboxTasks)}
        </li>


        
        
    )
}

export default InboxList