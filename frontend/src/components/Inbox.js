import React from 'react'
import {inboxCol} from './Functions';
import InboxList from './InboxList';

function listInbox(taskList) {

        try{
            //show item list completed or not based on viewCompleted
            var jsonStr = JSON.stringify(taskList);
            var json = JSON.parse(jsonStr);
            // });

            var item_list = json.sort( function (a,b){
                return b.priority - a.priority
            });

            return item_list
        }
        catch(e){
            //to fix undefined
            return {}
        }
}

//card of each day = Number in top row + tasklist of each day
function Inbox({taskList, onEdit}) {
    return (
            <li className="listInbox list-unstyled">
                {inboxCol.map( (item, index) => (
                    <li key = {index}>         
                        <InboxList 
                        inboxTasks = {listInbox(taskList)} 
                        onEdit = {onEdit} 
                        /> 
                    </li>
                ))}
            </li>
    )
}

export default Inbox

