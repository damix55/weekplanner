import React from 'react'
import {days} from './Functions'
import {currentDate} from './Functions';
import {dayByDate} from './Functions';
import {get_date_current_week} from './Functions';

function currentDayColor(day) {
    var cdate = currentDate();
    var cday = dayByDate(cdate);

    if(cday === day)
        return {color : 'red'};
    else
        return {color : 'black'}
}



//days in top row  (sun, mon, )
function CalDays() {
    return ( 
        <ol className="day-names list-unstyled">
            {days.map( (item, index) => (
                <li className="font-weight-bold text-uppercase" style={currentDayColor(item)} key = {index} > 
                    
                    {item.substring(0,3)}
                    <div className="date font-weight-lighter">{get_date_current_week(item, true)} </div>
                    
                </li>
            ))}
        </ol>
    )
}
export default CalDays






