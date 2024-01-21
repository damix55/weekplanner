import React from 'react'


const Button = ({color, text, onClick, id}) => {
    return(
        <button id={id} onClick={onClick}  className= {'btn '+ color}>
            {text}
        </button>
    )

    
}

export default Button
