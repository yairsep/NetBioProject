import React from 'react'
const FAQ_list = require('./FAQ_List.json')

function FAQ() {

    return (
        <div>
            <h1>FAQ</h1>
            <div>
                {FAQ_list.map((item, i) => (
                    <div>
                        <div>{item.Question}</div>
                        <div>{item.Answer}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default FAQ
