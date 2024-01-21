import React from 'react'
import Day from './Day';
import {days} from './Functions';
import moment from 'moment';
import {get_date_current_week} from './Functions';


function dayFilteredList(taskList, day){
    var momentInputDay = get_date_current_week(day, false);
    var inputDayString = momentInputDay.toISOString().substr(0,10);

    //return tasks belonging to current day
    try{
        var jsonStr = JSON.stringify(taskList);
        var json = JSON.parse(jsonStr);

        var filteredTaskList = json.filter(function (task) {
            var momentTaskDate = moment(task.date).add(1, 'day');
            var taskDayString = momentTaskDate.toISOString().substr(0,10);

            return inputDayString === taskDayString; 
        });

        //order filtered dayList by priority (greater -> higher)
        filteredTaskList.sort( function (a,b){
            return b.priority - a.priority
        });

        return filteredTaskList; 
    }
    catch(e){
        //to fix undefined
        return {}
    }
} 


//card of each day = Number in top row + tasklist of each day
function Calendar({taskList, onEdit, setTodayTasks}) {
    return (
            <ol className="days list-unstyled">
                {days.map( (item, index) => (
                    <li key = {index}>         
                        <Day 
                        // day = {item} 

                        dayTasks = {dayFilteredList(taskList, days[index])} 
                        onEdit = {onEdit} 
                        /> 
                    </li>
                ))}
            </ol>
    )
}

export default Calendar


