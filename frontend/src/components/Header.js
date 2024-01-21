import React, { Component } from 'react'


class Header extends Component {
    render(){
        return (
            <div className="d-flex align-items-center"> 
                <i className="fa fa-calendar fa-3x"></i>
                <h2 className="month font-weight-bold mb-0">{this.props.title}</h2>
            </div>
        )
    }
}

export default Header




