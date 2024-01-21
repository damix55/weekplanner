import React from 'react'



function Day({day, dayTasks, onEdit}) {

    const show_tasks = (tasks) => {
        try{
            return tasks.map((task, index) => (
                <div    className="event bg-primary" 
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
        <ol className="days list-unstyled">
            {show_tasks(dayTasks)}
        </ol>


        
        
    )
}

export default Day
