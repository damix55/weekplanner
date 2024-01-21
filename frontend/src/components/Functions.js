import moment from 'moment';

export let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
export let inboxCol = ['Inbox List'];

export function currentDate(item) {
    var currentDate = new Date();
    var cDay = currentDate.getDate()
    var cMonth = currentDate.getMonth() + 1
    var cYear = currentDate.getFullYear()

    if(item === 'day')
        return cMonth
    if(item === 'month')
        return cMonth
    if(item === 'year')
        return cYear
    else if(item == null)
        return cYear + '-' + cMonth + '-' + cDay
} 


export function dayByDate(date){
    //return day name by date; e.g. 2020-9-12 -> Tuesday 
    var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var d = new Date(date);
    var dayName = days[d.getDay()];

    return dayName
}


export function get_date_current_week (day, onlyDay){
    var momentDay = moment().isoWeekday(day).get('date');
    var sunday_date = moment().isoWeekday('Sunday').get('date');

    if (onlyDay){
        if(momentDay === sunday_date){
        //return last sunday (first day of calendar)
            return moment().day('Sunday').get('date');
        }
        return momentDay;    
    }
    else {
        if(momentDay === sunday_date){
            //return last sunday (first day of calendar)
                return moment().day('Sunday');
        }
        return moment().isoWeekday(day);    
    }
    
}


