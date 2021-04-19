import React, { useState } from 'react';

const WordCloud = props => {
    const { keyword, maxPage, maxCandidate, rankMethod, subArea } =
        props.location.options

    const { result, setResult } = useState('')
    /* Activating axios */
    // const axios = require('axios').default;
    // function request() {
    //     axios.get('http://127.0.0.1:5000/visualization/wordCloud/')
    //     .then(function (response) {
    //         /* get request succeed */
    //         setResult(response.data)
    //     })
    //     .catch(function (error) {
    //         setResult('Error: get request failed.')
    //     })
    // }
    return (
        <div>
            <div style={{backgroundColor: "#F8F8FF"}}>
                <lable> keyword input: {keyword} </lable>
                <lable> maxPage input: {maxPage} </lable>
                <lable> maxCandidate input: {maxCandidate} </lable>
                <lable> rankMethod input: {rankMethod} </lable>
                <lable> subArea input: {subArea} </lable>
            </div>
            <div style={{backgroundColor: "#F8F8FF"}}>
                <textarea name="result"
                    value={result}/>
            </div>
        </div>

    );
};



export default WordCloud;